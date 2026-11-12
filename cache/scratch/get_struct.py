import re
html = open('index.html', encoding='utf-8').read()
# header
m = re.search(r'<header[^>]*>', html)
print("header:", m.group(0) if m else "NO")
m = re.search(r'<nav[^>]*>', html)
print("nav:", m.group(0) if m else "NO")
m = re.search(r'<main[^>]*>', html)
print("main:", m.group(0) if m else "NO")
m = re.search(r'<aside[^>]*>', html)
print("aside:", m.group(0) if m else "NO")
m = re.search(r'<footer[^>]*>', html)
print("footer:", m.group(0) if m else "NO")
# modales / dialogos
print("\n=== candidatos a dialogo ===")
for m in list(re.finditer(r'<div[^>]*id="(wheelModal|cuentamodal|drawer)"[^>]*>', html))[:5]:
    print("  ", m.group(0)[:150])
