#!/bin/sh
set -e

echo "→ Migrations..."
python manage.py migrate --noinput

echo "→ Collecting static..."
python manage.py collectstatic --noinput

# Optional demo data seed (SEED_DEMO=1).
if [ "$SEED_DEMO" = "1" ]; then
  echo "→ Seeding demo data..."
  python manage.py seed_demo || true
fi

# Optional superuser creation from env (once).
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "→ Creating superuser (if missing)..."
  python manage.py createsuperuser --noinput || true
fi

exec "$@"
