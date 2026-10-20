#!/bin/sh
set -eu
# Railway assigns $PORT and terminates TLS at its edge (*.up.railway.app).
# Inside the container Xray serves plain WS on $PORT; externally it is wss://.
: "${UUID:?Set UUID variable in Railway}"
: "${WS_PATH:?Set WS_PATH variable in Railway (e.g. /abc123)}"
PORT="${PORT:-8080}"
sed -e "s|__UUID__|${UUID}|g" -e "s|__WS_PATH__|${WS_PATH}|g" -e "s|__PORT__|${PORT}|g" \
  /usr/local/etc/xray/config.json.template > /usr/local/etc/xray/config.json
exec /usr/local/bin/xray run -config /usr/local/etc/xray/config.json
