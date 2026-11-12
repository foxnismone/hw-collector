import json, collections
cat = json.load(open('data/catalog_web.json', encoding='utf-8'))

fandom = []
for m in cat:
    for u in (m.get('galeria') or []):
        if 'weserv' not in u:
            fandom.append(u)

print(f"URLs no-weserv en galeria: {len(fandom)}")
print("\n=== ejemplos ===")
for u in fandom[:10]: print(f"  {u[:100]}")

# patrones
pats = collections.Counter()
for u in fandom:
    if u.startswith('http'): pats['http absoluto'] += 1
    elif '/' in u: pats['con barra (ruta parcial)'] += 1
    else: pats['solo nombre de archivo'] += 1
print(f"\nPatrones: {dict(pats)}")
