#!/usr/bin/env python3
"""After Railway deploy: generate Shadowrocket vless link, single-node
subscription (base64) and QR. Usage:
  python3 make_shadowrocket.py --host <your>.up.railway.app [--name Railway]
Reads params.env in this folder (UUID, WS_PATH). QR encodes the vless:// link,
which Shadowrocket imports directly by scanning.
"""
import argparse, base64, pathlib, urllib.parse
HERE = pathlib.Path(__file__).parent
def load_env():
    env={}
    for line in (HERE/"params.env").read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k,v=line.split("=",1); env[k.strip()]=v.strip()
    return env
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--host",required=True); ap.add_argument("--name",default="Railway")
    a=ap.parse_args(); env=load_env()
    q={"encryption":"none","security":"tls","sni":a.host,"fp":"chrome","type":"ws","host":a.host,"path":env["WS_PATH"]}
    link=f"vless://{env['UUID']}@{a.host}:443?"+urllib.parse.urlencode(q)+"#"+urllib.parse.quote(a.name)
    (HERE/"shadowrocket-link.txt").write_text(link+"\n")
    (HERE/"subscription.txt").write_text(base64.b64encode((link+"\n").encode()).decode()+"\n")
    import qrcode
    qr=qrcode.QRCode(border=2,box_size=10); qr.add_data(link); qr.make(fit=True); qr.make_image().save(HERE/"shadowrocket-qr.png")
    print("wrote shadowrocket-link.txt, subscription.txt, shadowrocket-qr.png for",a.host)
if __name__=="__main__": main()
