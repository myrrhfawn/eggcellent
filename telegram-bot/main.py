"""EGGCELLENT Telegram bot.

Features:
  • /start — menu (take the test / leave a request)
  • English level test — questions are pulled from the backend (REST API),
    the score is computed on the backend (/api/test/submit/)
  • Leave a request — the user shares a contact → a request is created immediately
  • /admin (hidden command) — asks for a password; on a correct one grants access
    to the request list. New requests are sent to admins as a notification (no data,
    only the fact + channel) — handled by the backend.

All communication with the backend goes through the REST API (the same as the site).
"""
import asyncio
import logging
import os

import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    BotCommand,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("eggbot")

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
API_BASE = os.environ.get("API_BASE_URL", "http://app:8000/api").rstrip("/")
BOT_SECRET = os.environ.get("BOT_API_SECRET", "")
LANG = os.environ.get("BOT_LANG", "uk")

SECRET_HEADERS = {"X-Bot-Secret": BOT_SECRET}

dp = Dispatcher(storage=MemoryStorage())


class Flow(StatesGroup):
    testing = State()
    admin_password = State()


# ---------- HTTP ----------
async def api_get(path, params=None, secret=False):
    headers = SECRET_HEADERS if secret else {}
    async with aiohttp.ClientSession() as s:
        async with s.get(f"{API_BASE}{path}", params=params, headers=headers) as r:
            return r.status, await r.json(content_type=None)


async def api_post(path, json_body, secret=False):
    headers = SECRET_HEADERS if secret else {}
    async with aiohttp.ClientSession() as s:
        async with s.post(f"{API_BASE}{path}", json=json_body, headers=headers) as r:
            try:
                data = await r.json(content_type=None)
            except Exception:
                data = {}
            return r.status, data


# ---------- Keyboards ----------
def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Пройти тест", callback_data="menu:test")],
            [
                InlineKeyboardButton(
                    text="📞 Залишити заявку", callback_data="menu:apply"
                )
            ],
        ]
    )


def contact_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Поділитися номером", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def render_test(data):
    """Builds (text, keyboard) for the current question: highlights the selected
    answer, shows "Back" and "Next/Finish"."""
    questions = data["questions"]
    idx = data["idx"]
    answers = data["answers"]
    q = questions[idx]
    selected = answers.get(str(q["id"]))

    text = (
        "🎓 <b>Тест на рівень CEFR</b>\n"
        f"Питання {idx + 1}/{len(questions)}\n\n"
        f"{q['text']}"
    )

    rows = []
    for a in q["answers"]:
        mark = "✅ " if selected == a["id"] else "▫️ "
        rows.append(
            [InlineKeyboardButton(text=mark + a["text"], callback_data=f"a:{a['id']}")]
        )

    nav = []
    if idx > 0:
        nav.append(InlineKeyboardButton(text="⬅️ Назад", callback_data="nav:back"))
    if selected is not None:
        label = "Завершити ✅" if idx == len(questions) - 1 else "Далі ➡️"
        nav.append(InlineKeyboardButton(text=label, callback_data="nav:next"))
    if nav:
        rows.append(nav)

    return text, InlineKeyboardMarkup(inline_keyboard=rows)


async def show_test(message, state: FSMContext, edit: bool):
    text, kb = render_test(await state.get_data())
    if edit:
        try:
            await message.edit_text(text, reply_markup=kb)
        except Exception:
            pass
    else:
        await message.answer(text, reply_markup=kb)


async def begin_test(message, state: FSMContext):
    status, questions = await api_get("/test/questions/", params={"lang": LANG})
    if status != 200 or not questions:
        await message.answer("Не вдалося завантажити тест. Спробуй пізніше.")
        return
    await state.set_state(Flow.testing)
    await state.update_data(questions=questions, idx=0, answers={})
    await show_test(message, state, edit=False)


# ---------- /start ----------
@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🥚 <b>EGGCELLENT online school</b>\n\n"
        "Привіт! Я допоможу визначити твій рівень англійської та записатись на навчання.\n\n"
        "Обери, з чого почнемо:",
        reply_markup=main_menu(),
    )


# ---------- Test ----------
@dp.callback_query(F.data == "menu:test")
async def start_test(cb: CallbackQuery, state: FSMContext):
    await begin_test(cb.message, state)
    await cb.answer()


@dp.callback_query(Flow.testing, F.data.startswith("a:"))
async def select_answer(cb: CallbackQuery, state: FSMContext):
    answer_id = int(cb.data.split(":")[1])
    data = await state.get_data()
    q = data["questions"][data["idx"]]
    if data["answers"].get(str(q["id"])) == answer_id:
        await cb.answer()  # already selected — nothing changes
        return
    data["answers"][str(q["id"])] = answer_id
    await state.update_data(answers=data["answers"])
    await show_test(cb.message, state, edit=True)
    await cb.answer()


@dp.callback_query(Flow.testing, F.data == "nav:back")
async def nav_back(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data["idx"] > 0:
        await state.update_data(idx=data["idx"] - 1)
        await show_test(cb.message, state, edit=True)
    await cb.answer()


@dp.callback_query(Flow.testing, F.data == "nav:next")
async def nav_next(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    idx, questions, answers = data["idx"], data["questions"], data["answers"]
    q = questions[idx]
    if str(q["id"]) not in answers:
        await cb.answer("Спершу оберіть відповідь")
        return

    if idx < len(questions) - 1:
        await state.update_data(idx=idx + 1)
        await show_test(cb.message, state, edit=True)
        await cb.answer()
        return

    # last question — compute the level on the backend
    status, result = await api_post("/test/submit/", {"answers": answers})
    await cb.answer()
    if status != 200:
        await cb.message.edit_text("Помилка обрахунку. Спробуй ще раз.")
        await state.clear()
        return

    level = result.get("level") or {}
    await state.clear()
    await state.update_data(submission_id=result.get("id"))
    try:
        await cb.message.edit_text(
            f"✅ <b>Готово!</b>\n\nТвій рівень: <b>{level.get('code', '—')}</b> "
            f"({level.get('title', '')})\n{level.get('description', '')}\n\n"
            f"Балів: {result.get('score')}/{result.get('max_score')}",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="📞 Залишити заявку", callback_data="menu:apply"
                        )
                    ]
                ]
            ),
        )
    except Exception:
        pass


# ---------- Request ----------
@dp.callback_query(F.data == "menu:apply")
async def ask_contact(cb: CallbackQuery):
    await cb.message.answer(
        "Щоб залишити заявку, поділись номером телефону 👇\n"
        "Ми зателефонуємо й підберемо формат навчання.",
        reply_markup=contact_kb(),
    )
    await cb.answer()


@dp.message(F.contact)
async def got_contact(message: Message, state: FSMContext):
    contact = message.contact
    name = " ".join(filter(None, [contact.first_name, contact.last_name])) or "—"
    data = await state.get_data()
    payload = {"name": name, "phone": contact.phone_number}
    if data.get("submission_id"):
        payload["submission_id"] = data["submission_id"]

    status, resp = await api_post("/bot/leads/", payload, secret=True)
    await state.clear()
    if status == 200 and resp.get("ok"):
        lvl = resp.get("level")
        extra = f"\nТвій рівень: <b>{lvl}</b>" if lvl else ""
        await message.answer(
            f"✅ Дякуємо, <b>{name}</b>! Заявку прийнято.{extra}\n"
            "Ми скоро зателефонуємо 🥚",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.answer(
            "Не вдалося зберегти заявку 😔 Спробуй пізніше.",
            reply_markup=ReplyKeyboardRemove(),
        )


# ---------- Admin (hidden) ----------
@dp.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext):
    await state.set_state(Flow.admin_password)
    await message.answer("🔐 Введи пароль адміністратора:")


@dp.message(Flow.admin_password, F.text)
async def check_password(message: Message, state: FSMContext):
    password = message.text.strip()
    # immediately remove the message containing the password
    try:
        await message.delete()
    except Exception:
        pass
    status, resp = await api_post(
        "/bot/auth/",
        {
            "password": password,
            "chat_id": message.chat.id,
            "username": message.from_user.username or "",
        },
        secret=True,
    )
    await state.clear()
    if status == 200 and resp.get("ok"):
        await message.answer(
            "✅ Доступ надано. Тепер ти отримуватимеш сповіщення про нові заявки.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="📋 Заявки", callback_data="admin:leads"
                        )
                    ]
                ]
            ),
        )
    else:
        await message.answer("❌ Невірний пароль.")


@dp.callback_query(F.data == "admin:leads")
async def admin_leads(cb: CallbackQuery):
    status, leads = await api_get(
        "/bot/leads/list/", params={"chat_id": cb.message.chat.id}, secret=True
    )
    await cb.answer()
    if status != 200 or not isinstance(leads, list) or not leads:
        await cb.message.answer("Заявок поки немає (або немає доступу).")
        return

    lines = ["📋 <b>Останні заявки:</b>\n"]
    for ld in leads:
        ch = "🤖 бот" if ld.get("channel") == "bot" else "🌐 сайт"
        lvl = f" · {ld['level']}" if ld.get("level") else ""
        done = "✅" if ld.get("is_processed") else "🆕"
        created = (ld.get("created_at") or "")[:16].replace("T", " ")
        lines.append(
            f"{done} <b>{ld.get('name')}</b> — {ld.get('phone')}{lvl}\n"
            f"   {ch} · {created}"
        )
    await cb.message.answer("\n".join(lines))


# ---------- startup ----------
async def on_startup(bot: Bot):
    # Menu commands — WITHOUT /admin (hidden)
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Головне меню"),
            BotCommand(command="test", description="Пройти тест на рівень"),
            BotCommand(command="apply", description="Залишити заявку"),
        ]
    )
    log.info("Bot commands set. Polling...")


# convenient command aliases
@dp.message(Command("test"))
async def cmd_test(message: Message, state: FSMContext):
    await begin_test(message, state)


@dp.message(Command("apply"))
async def cmd_apply(message: Message):
    await message.answer(
        "Щоб залишити заявку, поділись номером телефону 👇",
        reply_markup=contact_kb(),
    )


async def main():
    if not TOKEN:
        raise SystemExit("TELEGRAM_BOT_TOKEN is not set")
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await on_startup(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
