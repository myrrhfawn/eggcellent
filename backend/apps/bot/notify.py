"""Notifications to Telegram admins about new leads.

We send a short message (WITHOUT personal data) — only the fact of a new lead
and its channel (bot/site). Sending happens in a background thread so as not to
block the request.
"""
import json
import threading
import urllib.request

from django.conf import settings

_TG_SEND = "https://api.telegram.org/bot{token}/sendMessage"


def _send(token: str, chat_id: int, text: str) -> None:
    payload = json.dumps(
        {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    ).encode()
    req = urllib.request.Request(
        _TG_SEND.format(token=token),
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        # Best-effort notification — do not fail lead creation because of a TG error.
        pass


def notify_new_lead(channel: str) -> None:
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        return

    # Import inside the function — to avoid problems during startup/migrations.
    from .models import TelegramAdmin

    src = "бота 🤖" if channel == "bot" else "сайту 🌐"
    text = (
        "🔔 <b>Нова заявка!</b>\n"
        f"Джерело: <b>{src}</b>\n"
        "Деталі — у боті: /admin → 📋 Заявки"
    )

    try:
        chat_ids = list(
            TelegramAdmin.objects.filter(is_active=True).values_list(
                "chat_id", flat=True
            )
        )
    except Exception:
        return

    if not chat_ids:
        return

    def _worker():
        for cid in chat_ids:
            _send(token, cid, text)

    threading.Thread(target=_worker, daemon=True).start()
