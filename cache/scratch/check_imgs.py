import json, urllib.request, random
from concurrent.futures import ThreadPoolExecutor

cat = json.load(open('data/catalog_web.json', encoding='utf-8'))

def check(url):
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent','Mozilla/5.0')
        with urllib.request.urlopen(req, timeout=25) as r:
            return (url, r.status, len(r.read()))
    except Exception as e:
        return (url, 'ERR', str(e)[:40])

# 1. URLs weserv (modelos del arbol)
weserv = [m['im'] for m in cat if 'images.weserv.nl' in str(m.get('im',''))][:6]
print("=== Imagenes ya proxeadas (weserv) ===")
for u, st, sz in map(check, weserv):
    print(f"  {st} {sz}  {u[:70]}")

# 2. URLs Fandom -> el navegador las proxeara
fandom = [m['im'] for m in cat if 'static.wikia.nocookie.net' in str(m.get('im',''))][:6]
print("\n=== URLs Fandom (proxeadas por IMG) ===")
for u in fandom:
    proxy = 'https://images.weserv.nl/?url=' + u.replace('https://','')
    u2, st, sz = check(proxy)
    print(f"  {st} {sz}  {u[:70]}")

# 3. imagenes locales
locales = [m['im'] for m in cat if str(m.get('im','')).startswith('packs_culture/')][:3]
print("\n=== Locales ===")
for u in locales:
    u2, st, sz = check('https://foxnismone.github.io/hw-collector/img/' + u)
    print(f"  {st} {sz}  {u[:60]}")
