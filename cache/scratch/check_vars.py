import re
html = open('index.html', encoding='utf-8').read()
# Buscar el bloque :root
i = html.find(':root')
print("=== :root en", i, "===")
print(html[i:i+1200] if i>=0 else "NO HAY :root")
print("\n=== variables usadas pero quizas no definidas ===")
usadas = set(re.findall(r'var\((--[a-z0-9-]+)\)', html))
definidas = set(re.findall(r'(--[a-z0-9-]+)\s*:', html))
faltan = usadas - definidas
print(f"usadas: {len(usadas)} | definidas: {len(definidas)}")
if faltan: print(f"*** FALTAN: {sorted(faltan)}")
else: print("todas definidas")
