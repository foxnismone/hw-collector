import json
cat = json.load(open('data/catalog_web.json', encoding='utf-8'))

# Campos que usa cardHTML y drawer
campos = ['m','y','c','t','s','n','k','x','im','v','V','ficha']
faltan = {c:0 for c in campos}
for m in cat:
    for c in campos:
        if m.get(c) is None: faltan[c]+=1
print("Modelos con campos faltantes (None):")
for c,n in faltan.items():
    if n: print(f"  {c}: {n}")

# verificar ficha.es
sin_es = sum(1 for m in cat if isinstance(m.get('ficha'),dict) and not m['ficha'].get('es'))
print(f"\nFichas sin 'es': {sin_es}")

# verificar im
sin_im = sum(1 for m in cat if not m.get('im'))
print(f"Sin im: {sin_im}")

# tipos de dato de v/V
tipos = set(type(m.get('v')).__name__ for m in cat)
print(f"Tipos de v: {tipos}")

# ejemplo de modelo nuevo
nuevos = [m for m in cat if isinstance(m.get('i'),str) and m['i'].startswith('c-')]
print(f"\nModelos con i='c-...': {len(nuevos)}")
if nuevos:
    print(json.dumps(nuevos[0], ensure_ascii=False, indent=2)[:600])
