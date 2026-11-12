import re
h = open('index.html', encoding='utf-8').read()

# catLogoSVG: el logo de categoria
m = re.search(r'function catLogoSVG\([^)]*\)\s*\{[^}]*\}', h)
if m:
    print("=== catLogoSVG ===")
    print(m.group(0)[:900])
print()

# donde se renderiza la linea/serie en el drawer (dh: div con img + h2)
i = h.find('d.dataset.open="1"')
j = h.find('drawer(id)')
print("=== drawer / linea del catalogo (dh) ===")
# buscar el template del drawer
for key in ['fichaHTML', 'linea', 'Series', 'c.s', 'c.k', 'catLogoSVG(c.k)']:
    for mm in list(re.finditer(re.escape(key), h))[:3]:
        print(f"  [{key}] ...{h[max(0,mm.start()-90):mm.start()+130].replace(chr(10),' ')}...")
    print()
