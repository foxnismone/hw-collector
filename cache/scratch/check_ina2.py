import json
cat = json.load(open('data/catalog_web.json', encoding='utf-8'))

# buscar en galeria
n_gal = 0
ej = []
for m in cat:
    for u in (m.get('galeria') or []):
        if 'not available' in u.lower() or 'notavailable' in u.lower().replace(' ',''):
            n_gal += 1
            if len(ej)<5: ej.append((m['m'], u))
print(f"URLs 'not available' en galeria: {n_gal}")
for e in ej: print(f"  {e[0][:35]:37s} {e[1][:80]}")

# buscar en ficha / textos
n_f = 0
for m in cat:
    f = m.get('ficha') or {}
    for k,v in f.items():
        if isinstance(v,str) and 'not available' in v.lower():
            n_f += 1
print(f"\n'not available' en fichas: {n_f}")

# Cuantos modelos tienen galeria con URL de Fandom (no weserv)
import collections
c = collections.Counter()
for m in cat:
    for u in (m.get('galeria') or []):
        if 'weserv' in u: c['weserv'] += 1
        elif 'static.wikia' in u or 'hotwheels.fandom' in u: c['fandom'] += 1
        else: c['otro'] += 1
print(f"\nGaleria URL tipos: {dict(c)}")

# Cuantos tienen galeria vacia
sin_gal = sum(1 for m in cat if not m.get('galeria'))
print(f"Sin galeria: {sin_gal}")
