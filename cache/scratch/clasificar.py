import re
html = open('index.html', encoding='utf-8').read()

items = []
for m in re.finditer(r'\$\{([^}]+)\}', html):
    items.append({'pos': m.start(), 'expr': m.group(1), 'ctx': html[max(0,m.start()-45):m.start()]})

attr_js, attr_url, texto, otros = [], [], [], []
for it in items:
    ctx = it['ctx']; e = it['expr']
    if ctx.rstrip().endswith("'") or "onclick=" in ctx[-30:]:
        attr_js.append(it)
    elif ctx.rstrip().endswith('="') or 'href="' in ctx[-25:]:
        attr_url.append(it)
    elif 'esc(' in e:
        otros.append(it)
    else:
        texto.append(it)

print(f"TOTAL: {len(items)}")
print(f"  JS-string(onclick): {len(attr_js)}")
print(f"  URL/attr: {len(attr_url)}")
print(f"  texto: {len(texto)}")
print(f"  otros: {len(otros)}")

print("\n=== JS-STRING ===")
for it in attr_js: print(f"  {it['pos']:>7}  ...{it['ctx'][-22:]}{it['expr'][:45]}")

print("\n=== URL/attr ===")
for it in attr_url[:12]: print(f"  {it['pos']:>7}  ...{it['ctx'][-22:]}{it['expr'][:45]}")

campos = {}
for it in texto:
    for cm in re.finditer(r'\b(?:c\.[A-Za-z_]+|fSel\.[A-Za-z_]+|vm\.[A-Za-z_]+|d\.[A-Za-z_]+|w\.[A-Za-z_]+)', it['expr']):
        campos[cm.group(0)] = campos.get(cm.group(0),0)+1
print("\n=== CAMPOS en texto ===")
for k,v in sorted(campos.items(), key=lambda x:-x[1])[:25]:
    print(f"  {v:>3}  {k}")
