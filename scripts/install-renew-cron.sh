#!/bin/sh
# Installs a cron job that auto-renews the Let's Encrypt certs.
# nginx picks up the renewed cert by itself (the web container watches for changes),
# so the cron only needs to run `certbot renew`.
#
# Usage (on the server, from anywhere):  ./scripts/install-renew-cron.sh
set -e

PROJECT_DIR=$(cd "$(dirname "$0")/.." && pwd)
MARKER="certbot renew --webroot"
LINE="0 3 * * * cd $PROJECT_DIR && docker compose run --rm --entrypoint certbot certbot renew --webroot -w /var/www/certbot --quiet"

# Replace any previous entry, then add the current one.
( crontab -l 2>/dev/null | grep -vF "$MARKER"; echo "$LINE" ) | crontab -

echo "Installed cron job (daily 03:00, renews only when <30 days remain):"
echo "  $LINE"
echo
echo "nginx reloads the renewed cert automatically — no extra step needed."
