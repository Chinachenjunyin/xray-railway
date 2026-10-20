FROM ghcr.io/xtls/xray-core:latest
COPY config.json.template /usr/local/etc/xray/config.json.template
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
