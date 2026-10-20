#!/usr/bin/env python3
"""After Railway deploy: generate FlClash (mihomo) yaml, vless link and QR.
Usage: python3 make_flclash.py --host <your>.up.railway.app [--name Railway]
Reads params.env (UUID, WS_PATH). QR encodes the vless:// link for import.
"""
import argparse, pathlib, urllib.parse
HERE = pathlib.Path(__file__).parent
def load_env():
    env={}
    for line in (HERE/"params.env").read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k,v=line.split("=",1); env[k.strip()]=v.strip()
    return env
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--host",required=True); ap.add_argument("--name",default="Railway")
    a=ap.parse_args(); env=load_env(); uuid=env["UUID"]; path=env["WS_PATH"]
    q={"encryption":"none","security":"tls","sni":a.host,"fp":"chrome","type":"ws","host":a.host,"path":path}
    link=f"vless://{uuid}@{a.host}:443?"+urllib.parse.urlencode(q)+"#"+urllib.parse.quote(a.name)
    yaml=f"""mixed-port: 7890
allow-lan: false
mode: rule
log-level: info
proxies:
  - name: "{a.name}"
    type: vless
    server: {a.host}
    port: 443
    uuid: {uuid}
    network: ws
    tls: true
    udp: true
    servername: {a.host}
    ws-opts:
      path: "{path}"
      headers:
        Host: {a.host}
    client-fingerprint: chrome
proxy-groups:
  - name: PROXY
    type: select
    proxies: ["{a.name}", DIRECT]
rules:
  - GEOIP,CN,DIRECT
  - MATCH,PROXY
"""
    (HERE/"flclash.yaml").write_text(yaml)
    (HERE/"flclash-link.txt").write_text(link+"\n")
    import qrcode
    qr=qrcode.QRCode(border=2,box_size=10); qr.add_data(link); qr.make(fit=True); qr.make_image().save(HERE/"flclash-qr.png")
    print("wrote flclash.yaml, flclash-link.txt, flclash-qr.png for",a.host)
if __name__=="__main__": main()
