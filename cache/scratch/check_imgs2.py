import json
cat = json.load(open('data/catalog_web.json', encoding='utf-8'))

# imagenes "otro"
otros = [m for m in cat if str(m.get('im','')) and not str(m['im']).startswith(('packs_culture/','http'))]
print(f"Imagenes 'otro': {len(otros)}")
for m in otros[:6]:
    print(f"  {m['im'][:60]}")

# ids duplicados
from collections import Counter
ids = Counter(str(m.get('i')) for m in cat)
dup = {k:v for k,v in ids.items() if v>1}
print(f"\nIDs duplicados: {len(dup)}")
for k,v in list(dup.items())[:8]:
    ej = [m for m in cat if str(m.get('i'))==k]
    print(f"  {k} ({v}): {[e['m'][:25] for e in ej]}")

# modelo sin nombre
sin = [m for m in cat if not m.get('m')]
print(f"\nSin nombre: {len(sin)}")
for m in sin: print(f"  i={m['i']} y={m['y']} s={m.get('s')}")

# sin imagen
sinim = [m for m in cat if not m.get('im')]
print(f"\nSin imagen: {len(sinim)}")
for m in sinim[:5]: print(f"  {m['m'][:30]} ({m['y']})")
