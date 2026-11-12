import re
html = open('index.html', encoding='utf-8').read()

print("=== ETIQUETAS SEMANTICAS HTML5 ===")
for t in ['<main','<header','<footer','<nav','<article','<aside','<section','<figure','<figcaption','<time']:
    print(f"  {t}: {len(re.findall(re.escape(t)+r'[ >]', html))}")

print("\n=== <div> ===")
print(f"  <div: {len(re.findall(r'<div[ >]', html))}")

print("\n=== Atributos obsoletos (HTML4/XHTML) ===")
obso = ['<center','<font','<big','<strike','<tt','<marquee','<applet','<dir',
        'align="','valign="','bgcolor=','cellpadding','cellspacing','hspace','vspace',
        'border="0"','name="description"','http-equiv="refresh"','<frameset','<noframes',
        'language="JavaScript"','type="text/css"','scrolling="','frameborder',
        'allowtransparency','hspace','compact="','noshade']
tot = 0
for o in obso:
    n = len(re.findall(re.escape(o), html))
    if n:
        print(f"  {o}: {n}")
        tot += n
print(f"  TOTAL obsoletos: {tot}")

print("\n=== Tablas para diseno ===")
print(f"  <table: {len(re.findall(r'<table', html))}")
for m in list(re.finditer(r'<table[^>]*>', html))[:5]:
    print("   ", m.group(0)[:110])

print("\n=== iframes ===")
print(f"  <iframe: {len(re.findall(r'<iframe', html))}")

print("\n=== CSP actual ===")
m = re.search(r'http-equiv="Content-Security-Policy" content="([^"]+)"', html)
print("  ", m.group(1) if m else "NO")

print("\n=== ARIA ===")
print(f"  role=: {len(re.findall(r'role=', html))} | aria-: {len(re.findall(r'aria-[a-z]+=', html))}")
