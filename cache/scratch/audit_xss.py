import re
html = open('index.html', encoding='utf-8').read()

# 1. Funcion esc()
i = html.find('function esc(')
print("=== esc() ===")
print(html[i:i+220])

# 2. Interpolaciones en innerHTML / template literals con datos de catalogo
print("\n=== ${c.*} SIN esc() en templates de HTML ===")
# buscar lines con ${c. que no tengan esc( antes
patron = re.compile(r'\$\{[^}]*\bc\.[\w.]+\}')
matches = []
for m in re.finditer(r'\$\{[^}]+\}', html):
    expr = m.group(0)
    # interpolaciones que usan c. o disenador. o ficha sin esc()
    if re.search(r'\b(c\.|disenador\.|fSel\.|vm\.|_hist\.|d\.|w\.)', expr):
        ctx = html[max(0,m.start()-40):m.start()]
        if 'esc(' not in expr and 'esc(' not in ctx[-25:]:
            matches.append((m.start(), expr[:80]))
print(f"total: {len(matches)}")
for p, e in matches[:40]:
    print(f"  {p:>7}  {e}")
