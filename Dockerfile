# NOTE: ghcr.io/xtls/xray-core is a minimal image with no /bin/sh, so RUN steps
# and shell entrypoints fail there ("stat /bin/sh: no such file or directory",
# Railway build failure 2026-10-20). Build on Alpine instead and install the
# pinned official Xray release binary (static, runs fine on musl).
FROM alpine:3.20

ARG XRAY_VERSION=v26.3.27

RUN apk add --no-cache ca-certificates curl unzip tzdata \
 && curl -fsSL -o /tmp/xray.zip "https://github.com/XTLS/Xray-core/releases/download/${XRAY_VERSION}/Xray-linux-64.zip" \
 && mkdir -p /usr/local/bin /usr/local/share/xray /usr/local/etc/xray \
 && unzip -o /tmp/xray.zip -d /tmp/xray \
 && install -m 0755 /tmp/xray/xray /usr/local/bin/xray \
 && install -m 0644 /tmp/xray/geoip.dat /tmp/xray/geosite.dat /usr/local/share/xray/ \
 && cp /tmp/xray/geoip.dat /tmp/xray/geosite.dat /usr/local/bin/ \
 && rm -rf /tmp/xray /tmp/xray.zip \
 && /usr/local/bin/xray version

COPY config.json.template /usr/local/etc/xray/config.json.template
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
