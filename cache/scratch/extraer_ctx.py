html = open('index.html', encoding='utf-8').read()
import re
# Lineas exactas con interpolaciones peligrosas (texto plano)
targets = [
    ('c.m', r'<div class="nm">\$\{c\.m\}</div>'),
    ('ficha descripcion', r'\$\{fSel\.descripcion\}\'</div>\''),
]
# Buscar las lineas exactas que contienen interpolaciones de ficha
for pat in [r"\$\{fSel\.descripcion\}'", r"\$\{fSel\.historia\}'", r"\$\{fSel\.curiosidades\}'", r"\$\{fSel\.dato_clave\}'", r"\$\{c\.m\}", r"\$\{c\.s\}", r"\$\{c\.t\}", r"\$\{c\.c\}", r"\$\{c\.pais\}"]:
    for m in list(re.finditer(pat, html))[:3]:
        print(f"{m.start():>7}  {html[max(0,m.start()-90):m.start()+60]}")
    print()
