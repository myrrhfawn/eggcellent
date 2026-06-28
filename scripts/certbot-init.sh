#!/bin/sh
# Auto-issues a Let's Encrypt cert on `docker compose up` when ENABLE_HTTPS=1 and
# no cert exists yet. Uses the webroot challenge (nginx serves /.well-known/...),
# writes into /etc/letsencrypt (mounted to CERTS_DIR, e.g. /data/certs). One-shot.
set -e

if [ "$ENABLE_HTTPS" != "1" ]; then
    echo "[certbot-init] ENABLE_HTTPS!=1 — nothing to do"
    exit 0
fi

primary=$(echo "$SERVER_NAME" | awk '{print $1}')
if [ -z "$primary" ] || [ "$primary" = "_" ]; then
    echo "[certbot-init] SERVER_NAME not set — skipping"
    exit 0
fi

if [ -f "/etc/letsencrypt/live/$primary/fullchain.pem" ]; then
    echo "[certbot-init] cert for $primary already exists — skipping issuance"
    exit 0
fi

domains=""
for d in $SERVER_NAME; do
    domains="$domains -d $d"
done

echo "[certbot-init] issuing cert for:$domains"
sleep 5  # let nginx come up to answer the ACME challenge
certbot certonly --webroot -w /var/www/certbot $domains \
    --email "$LETSENCRYPT_EMAIL" --agree-tos --no-eff-email --non-interactive \
    && echo "[certbot-init] done — nginx will switch to HTTPS automatically" \
    || echo "[certbot-init] issuance FAILED (check DNS / ports 80,443) — staying on HTTP"
