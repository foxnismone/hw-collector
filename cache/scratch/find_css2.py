import re
h = open('index.html', encoding='utf-8').read()
# buscar la regla .dh{ completa
for pat in [r'\.dh\{[^}]*\}', r'\.dh\s*\{[^}]*\}', r'dh\{[^}]*\}']:
    m = re.search(pat, h)
    if m:
        print("=== ", m.group(0))
print()
# el grid de tarjetas y la cabecera del drawer
for frag in ['grid{display', '.grid{', '#grid{', 'header.top', 'header .bar', 'brandlogo']:
    i = h.find(frag)
    if i != -1:
        end = h.find('}', i)
        print(f"--- '{frag}' (pos {i}) ---")
        print("  ", h[i:end+1][:280].replace('\n',' '))
        print()
