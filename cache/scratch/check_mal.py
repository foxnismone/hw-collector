import json, re
cat = json.load(open('data/catalog_web.json', encoding='utf-8'))

# URLs malformadas: weserv pero sin hash (falta /x/xy/)
mal = []
for m in cat:
    urls = []
    if m.get('im'): urls.append(('im', m['im']))
    for u in (m.get('galeria') or []): urls.append(('gal', u))
    for tipo, u in urls:
        if 'weserv' in u:
            # deberia tener /images/x/xy/
            if not re.search(r'/images/[a-z0-9]/[a-z0-9]{2}/', u):
                mal.append((m['m'][:30], tipo, u))

print(f"URLs malformadas (sin hash): {len(mal)}")
for x in mal[:8]: print(f"  {x[0]:32s} {x[1]}  {x[2][:95]}")
