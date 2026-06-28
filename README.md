# EGGCELLENT — online English school 🥚

Website for the **EGGCELLENT online school**: a landing page with teachers,
reviews, pricing and a CEFR level test, plus a fully configurable Django admin.

## Stack

- **Backend:** Python + Django 5 + Django REST Framework, SQLite (default DB),
  `django-modeltranslation` (i18n uk/en), Pillow, gunicorn, whitenoise.
- **Frontend:** TypeScript + React 18 + Vite + TailwindCSS + Framer Motion
  (animations/parallax) + Embla (carousels) + react-query + react-i18next.
- **Deploy:** two containers — `app` (Django) and `web` (nginx serving the
  frontend and proxying to the backend). Plus a `bot` container for the Telegram bot.

## Structure

```
backend/        Django + DRF (apps: siteconfig, teachers, reviews, pricing, englishtest, leads, bot)
frontend/       React + TS (Vite), brand SVG assets and fonts
telegram-bot/   Telegram bot (aiogram)
nginx/          nginx config for the web container
scripts/        png_to_svg.py — logo/mascot to SVG converter
designs/        Reference designs (PNG) — not part of the build
fonts/          Brand fonts (League Spartan, Aka-AcidGR, Montserrat, Onest) — source
```

## Run with Docker (recommended)

```bash
cp .env.example .env          # edit SECRET_KEY, passwords, etc. as needed
docker compose up --build     # site at http://localhost
```

- Site: <http://localhost>
- Admin: <http://localhost/admin/> (login/password from `.env`,
  default `admin` / `admin12345`)
- API: <http://localhost/api/>

On first start (`SEED_DEMO=1`) the DB is filled with demo data: teachers,
reviews, plans, CEFR levels and test questions. The bot starts together with the
stack.

## Local development

**Backend:**

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo            # demo data
python manage.py createsuperuser      # admin access
python manage.py runserver            # http://localhost:8000
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev                           # http://localhost:5173 (proxies /api → :8000)
```

## PNG → SVG conversion

The logo and mascot are vectorized from `designs/` into `frontend/src/assets/`:

```bash
pip install vtracer
python scripts/png_to_svg.py
```

> `logo.svg` contains live text using the brand fonts (League Spartan +
> Aka-AcidGR-FatItalic from `fonts/`), so it is inlined into the DOM rather than
> used via `<img>`.

## Telegram bot

The bot (`telegram-bot/`, aiogram) runs in a separate container and talks to the
**same REST API** as the site. Features:

- **/start** — menu: take the test or leave a request.
- **Test** — questions are pulled from the backend, scored on the server (`/api/test/submit/`).
- **Request** — the user shares a contact → a lead is created immediately (channel `bot`).
- **/admin** — hidden command (not in the command menu). Asks for a password
  (`BOT_ADMIN_PASSWORD`); on success it registers the admin and grants access to the lead list.
- **Notifications** — whenever a new lead appears (from the site or the bot), all
  registered admins get a message **without personal data** — only the fact of a
  new lead and its source (bot/site). Details are available in the bot via `/admin → Leads`.

Bot endpoints (`/api/bot/*`) are protected by a shared secret `BOT_API_SECRET`
(header `X-Bot-Secret`). Required env: `TELEGRAM_BOT_TOKEN`, `BOT_API_SECRET`,
`BOT_ADMIN_PASSWORD` (see `.env.example`). The bot starts together with the stack
(`docker compose up`).

## What is configurable from the admin

Everything important: site settings and social links, teachers (carousel), reviews,
plans (with discounts) + speaking club, CEFR levels with score thresholds, test
questions and answers, and all leads.
