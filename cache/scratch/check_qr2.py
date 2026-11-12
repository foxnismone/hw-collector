import re
html = open('index.html', encoding='utf-8').read()
print("=== 'qr' (case-insensitive) ===")
for m in list(re.finditer(r'[Qq][Rr]', html))[:20]:
    seg = html[max(0,m.start()-60):m.start()+80].replace('\n',' ')
    print(f"  {m.start():>7}  ...{seg}...")
    print()
