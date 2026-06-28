#!/bin/sh
# nginx launcher with automatic HTTP↔HTTPS handling.
#
#   ENABLE_HTTPS != 1            → serve HTTP.
#   ENABLE_HTTPS == 1 + certs    → serve HTTPS.
#   ENABLE_HTTPS == 1 + no certs → serve HTTP (bootstrap) so certbot can pass the
#                                  ACME challenge; auto-switch to HTTPS once the
#                                  cert appears.
#
# A background watcher re-renders the config every 60s and reloads nginx when it
# changes (HTTP→HTTPS switch) or when the cert is renewed (mtime change).
set -e

CONF=/etc/nginx/conf.d/default.conf

render() {  # prints the desired config to stdout
    if [ "$ENABLE_HTTPS" = "1" ] && [ -f "$SSL_CERT" ] && [ -f "$SSL_KEY" ]; then
        envsubst '${SERVER_NAME} ${SSL_CERT} ${SSL_KEY}' \
            < /etc/nginx/eggcellent/https.conf.template
    else
        cat /etc/nginx/eggcellent/http.conf
    fi
}

render > "$CONF"
if [ "$ENABLE_HTTPS" = "1" ] && { [ ! -f "$SSL_CERT" ] || [ ! -f "$SSL_KEY" ]; }; then
    echo "[eggcellent] ENABLE_HTTPS=1 but cert missing → HTTP bootstrap (waiting for certbot)"
else
    [ "$ENABLE_HTTPS" = "1" ] && echo "[eggcellent] HTTPS enabled" || echo "[eggcellent] HTTP only"
fi

# Background watcher — auto-upgrade to HTTPS and pick up renewals without restart.
(
    set +e
    last_cert=""
    while :; do
        sleep 60
        render > /tmp/desired.conf
        changed=0
        if ! cmp -s /tmp/desired.conf "$CONF"; then
            cp /tmp/desired.conf "$CONF"
            changed=1
        fi
        if [ "$ENABLE_HTTPS" = "1" ] && [ -f "$SSL_CERT" ]; then
            cur=$(stat -c %Y "$SSL_CERT" 2>/dev/null || echo 0)
            if [ "$cur" != "$last_cert" ]; then
                last_cert="$cur"
                changed=1
            fi
        fi
        if [ "$changed" = "1" ]; then
            echo "[eggcellent] config/cert changed → reloading nginx"
            nginx -s reload 2>/dev/null || true
        fi
    done
) &

exec nginx -g 'daemon off;'
