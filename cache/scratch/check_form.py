import re
html = open('index.html', encoding='utf-8').read()

print("=== <form> ===")
for m in list(re.finditer(r'<form', html))[:5]:
    print("  ", html[m.start():m.start()+200].replace('\n',' '))

print("\n=== id=grid ===")
i = html.find('id="grid"')
print(html[max(0,i-300):i+100].replace('\n',' '))

print("\n=== drawer HTML ===")
j = html.find('id="drawer"')
print(html[max(0,j-200):j+300].replace('\n',' '))

# ¿El grid está dentro de un form?
grid_pos = html.find('id="grid"')
for m in re.finditer(r'</form>', html):
    if m.start() > grid_pos:
        print(f"\n</form> en {m.start()} (grid en {grid_pos}) -> grid DENTRO de form: {grid_pos < m.start()}")
        break
