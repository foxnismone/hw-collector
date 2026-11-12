import re, os, urllib.request
h = open('index.html', encoding='utf-8').read()
print("=== CSS de .imgerr (lo que ve el usuario) ===")
for m in re.finditer(r'\.thumb\.imgerr[^}]*\}', h):
    print(" ", m.group(0)[:220])
print()
print("=== placeholder local en img/ ? ===")
for f in os.listdir('img'):
    if 'not' in f.lower() or 'avail' in f.lower() or 'placeholder' in f.lower() or 'sin' in f.lower():
        print("  ", f)
print("  (ninguno)" if not any('not' in f.lower() or 'avail' in f.lower() for f in os.listdir('img')) else "")
print()
print("=== el placeholder de Fandom es accesible? ===")
u = 'https://images.weserv.nl/?url=static.wikia.nocookie.net/hotwheels/images/b/b5/Image_Not_Available.jpg'
try:
    req = urllib.request.Request(u); req.add_header('User-Agent','Mozilla/5.0')
    with urllib.request.urlopen(req, timeout=25) as r:
        print(f"  weserv: {r.status} | {len(r.read())} bytes")
except Exception as e:
    print("  weserv ERR:", str(e)[:60])
