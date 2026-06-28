"""Seeds the DB with demo data: settings, CEFR levels, test questions,
plans, reviews and teachers (with generated avatars).

Run:  python manage.py seed_demo
Idempotent — re-running updates rather than duplicates.
"""
import io

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw

from apps.englishtest.models import Answer, Level, Question
from apps.pricing.models import Plan
from apps.reviews.models import Review
from apps.siteconfig.models import SiteSettings
from apps.teachers.models import Teacher

PALETTE = ["#f24b4b", "#252422", "#3b7a57", "#2b6cb0", "#b7791f"]

CEFR = [
    ("A1", "Beginner", "Початковий рівень — базові слова та фрази.",
     "Beginner level — basic words and phrases.", 0, 3),
    ("A2", "Elementary", "Елементарний — прості повсякденні розмови.",
     "Elementary — simple everyday conversations.", 4, 6),
    ("B1", "Intermediate", "Середній — впевнене спілкування на знайомі теми.",
     "Intermediate — confident on familiar topics.", 7, 9),
    ("B2", "Upper-Intermediate", "Вище середнього — вільне спілкування.",
     "Upper-Intermediate — fluent communication.", 10, 12),
    ("C1", "Advanced", "Просунутий — гнучка та точна мова.",
     "Advanced — flexible and precise language.", 13, 14),
    ("C2", "Proficiency", "Досконалий — рівень, близький до носія.",
     "Proficiency — near-native command.", 15, 99),
]

# (question, [options], correct index, points)
QUESTIONS = [
    ("She ___ to school every day.", ["go", "goes", "going", "gone"], 1, 1),
    ("There ___ any milk in the fridge.", ["isn't", "aren't", "not", "no"], 0, 1),
    ("I have lived here ___ 2010.", ["for", "since", "from", "during"], 1, 1),
    ("If it rains, we ___ at home.", ["stay", "stayed", "will stay", "would stay"], 2, 1),
    ("This is the ___ film I have ever seen.", ["good", "better", "best", "well"], 2, 1),
    ("He asked me where I ___ from.", ["come", "came", "am coming", "comes"], 1, 1),
    ("By next year she ___ her degree.", ["finishes", "will have finished",
     "finished", "is finishing"], 1, 1),
    ("I'm not used to ___ early.", ["wake up", "waking up", "woke up", "wakes up"], 1, 1),
    ("The report ___ by the team yesterday.", ["wrote", "was written",
     "is written", "writes"], 1, 1),
    ("Hardly ___ when the phone rang.", ["I had sat", "had I sat",
     "I sat", "did I sit"], 1, 1),
    ("Choose the synonym of 'meticulous'.", ["careless", "thorough",
     "quick", "loud"], 1, 1),
    ("I'd rather you ___ smoke here.", ["don't", "didn't", "won't", "not"], 1, 1),
    ("She ___ have told him; now he knows.", ["mustn't", "shouldn't",
     "needn't", "can't"], 1, 1),
    ("The committee ___ divided on the issue.", ["is", "are", "was being",
     "be"], 1, 1),
    ("'Ubiquitous' most nearly means:", ["rare", "everywhere",
     "hidden", "ancient"], 1, 1),
]

PLANS = [
    dict(title_uk="5 занять", title_en="5 lessons", lessons_count=5,
         price_per_lesson=300, total_price=1500, order=1),
    dict(title_uk="15 занять", title_en="15 lessons", lessons_count=15,
         price_per_lesson=280, total_price=4200, order=2, is_highlighted=True),
    dict(title_uk="30 занять", title_en="30 lessons", lessons_count=30,
         price_per_lesson=260, total_price=7800, order=3),
    dict(title_uk="Speaking Club", title_en="Speaking Club", lessons_count=4,
         price_per_lesson=0, total_price=800, is_speaking_club=True, order=4,
         note_uk="Місячна підписка (включено донат для ЗСУ)",
         note_en="Monthly subscription (includes a donation to the army)",
         features_uk=[
             "Теми, які засядуть надовго",
             "Лексика для ЗНО/НМТ та IELTS",
             "Фрази для говоріння в різних ситуаціях",
             "Широкий спектр рівнів A2–B2",
             "Зустрічі щотижня",
         ]),
]

REVIEWS = [
    ("Олена", "Найкраща школа! За пів року з A2 до B1.",
     "Best school! From A2 to B1 in half a year.", 5),
    ("Андрій", "Викладачі топ, заняття не нудні взагалі.",
     "Great teachers, lessons are never boring.", 5),
    ("Марія", "Speaking club — це любов. Рекомендую всім.",
     "Speaking club is love. Highly recommend.", 5),
    ("Дмитро", "Зручний розклад, адекватні ціни, є результат.",
     "Convenient schedule, fair prices, real progress.", 4),
]

TEACHERS = [
    ("Анна", "Anna", "C2 Proficiency", "8 років досвіду", "8 years"),
    ("Олег", "Oleh", "C1 Advanced", "5 років досвіду", "5 years"),
    ("Катерина", "Kateryna", "C2 Proficiency", "10 років досвіду", "10 years"),
    ("Іван", "Ivan", "C1 Advanced", "4 роки досвіду", "4 years"),
]


def avatar(initial: str, color: str) -> ContentFile:
    img = Image.new("RGB", (400, 400), color)
    d = ImageDraw.Draw(img)
    d.ellipse((40, 40, 360, 360), fill="#f2f0d8")
    # Large letter centered.
    try:
        from PIL import ImageFont
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 200
        )
    except Exception:
        font = None
    bbox = d.textbbox((0, 0), initial, font=font) if font else (0, 0, 120, 200)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((400 - w) / 2 - bbox[0], (400 - h) / 2 - bbox[1]), initial,
           fill=color, font=font)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return ContentFile(buf.getvalue())


class Command(BaseCommand):
    help = "Seeds the DB with EGGCELLENT demo data."

    def handle(self, *args, **opts):
        self._site()
        self._levels()
        self._questions()
        self._plans()
        self._reviews()
        self._teachers()
        self.stdout.write(self.style.SUCCESS("Demo data seeded."))

    def _site(self):
        s = SiteSettings.load()
        s.hero_title_uk = "EGGCELLENT — англійська без яєчні в голові"
        s.hero_title_en = "EGGCELLENT — English that finally clicks"
        s.hero_subtitle_uk = "Онлайн-школа з живими викладачами та результатом"
        s.hero_subtitle_en = "Online school with real teachers and real results"
        s.instagram_url = "https://instagram.com/eggcellent"
        s.telegram_url = "https://t.me/eggcellent"
        s.facebook_url = "https://facebook.com/eggcellent"
        s.contact_phone = "+380000000000"
        s.contact_email = "hello@eggcellent.school"
        s.base_lesson_price = 400
        s.save()

    def _levels(self):
        for order, (code, title, d_uk, d_en, lo, hi) in enumerate(CEFR):
            lvl, _ = Level.objects.get_or_create(code=code)
            lvl.title_uk = f"{code} — {title}"
            lvl.title_en = f"{code} — {title}"
            lvl.description_uk = d_uk
            lvl.description_en = d_en
            lvl.min_score = lo
            lvl.max_score = hi
            lvl.order = order
            lvl.save()

    def _questions(self):
        # Re-seed from scratch to avoid duplicate answer options.
        Question.objects.all().delete()
        for order, (text, opts, correct, pts) in enumerate(QUESTIONS):
            q = Question.objects.create(points=pts, order=order, is_active=True)
            q.text_uk = text
            q.text_en = text
            q.save()
            for i, opt in enumerate(opts):
                a = Answer.objects.create(
                    question=q, is_correct=(i == correct), order=i
                )
                a.text_uk = opt
                a.text_en = opt
                a.save()

    def _plans(self):
        Plan.objects.all().delete()
        for p in PLANS:
            obj = Plan.objects.create(
                lessons_count=p["lessons_count"],
                price_per_lesson=p["price_per_lesson"],
                total_price=p["total_price"],
                is_speaking_club=p.get("is_speaking_club", False),
                is_highlighted=p.get("is_highlighted", False),
                order=p["order"],
                features=p.get("features_uk", []),
            )
            obj.title_uk = p["title_uk"]
            obj.title_en = p["title_en"]
            obj.note_uk = p.get("note_uk", "")
            obj.note_en = p.get("note_en", "")
            obj.save()

    def _reviews(self):
        Review.objects.all().delete()
        for order, (name, uk, en, rating) in enumerate(REVIEWS):
            r = Review.objects.create(author_name=name, rating=rating, order=order)
            r.text_uk = uk
            r.text_en = en
            r.save()

    def _teachers(self):
        Teacher.objects.all().delete()
        for order, (uk, en, level, exp_uk, exp_en) in enumerate(TEACHERS):
            t = Teacher(english_level=level, order=order, is_active=True)
            t.name_uk = uk
            t.name_en = en
            t.experience_uk = exp_uk
            t.experience_en = exp_en
            t.save()
            color = PALETTE[order % len(PALETTE)]
            t.photo.save(f"teacher_{order}.png", avatar(en[0], color), save=True)
