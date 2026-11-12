html = open('index.html', encoding='utf-8').read()

# ¿Como se pobla el filtro de categorias?
import re
i = html.find('fcat')
print("=== fcat (filtro categorias) ===")
for m in list(re.finditer(r'fcat', html))[:6]:
    print("  ", html[max(0,m.start()-200):m.start()+250].replace('\n',' ')[:400])
    print()
