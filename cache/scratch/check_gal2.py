html = open('index.html', encoding='utf-8').read()
print("=== alrededor de 220089 (galeriaHTML) ===")
print(repr(html[220050:220200]))
print("\n=== alrededor de 114698 ===")
print(repr(html[114600:114800]))
# buscar definicion exacta
import re
for m in re.finditer(r'.{40}galeriaHTML.{40}', html):
    print("\n  ", repr(m.group(0)))
