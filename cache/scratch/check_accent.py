import re
html = open('index.html', encoding='utf-8').read()

# Variables CSS
for var in ['--accent', '--brand', '--ink', '--muted']:
    for m in list(re.finditer(re.escape(var)+r'\s*:\s*([^;]+);', html))[:2]:
        print(f"  {var}: {m.group(1).strip()}")

# ¿donde se usa .idx en cardHTML?
i = html.find('class=\\"idx\\"')
print("\n.idx en cardHTML:", html[i-100:i+150] if i>=0 else "NO")

# bar() uso
print("\nbar( usos:", len(re.findall(r'bar\(', html)))
for m in list(re.finditer(r'bar\([^)]{0,30}\)', html))[:5]:
    print("  ", m.group(0))
