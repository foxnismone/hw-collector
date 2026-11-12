import re
html = open('index.html', encoding='utf-8').read()
i = html.find('QRCode')
print("=== usos de QRCode ===")
for m in list(re.finditer(r'QRCode', html))[:12]:
    print(f"  {m.start():>7}  {html[max(0,m.start()-100):m.start()+130]}")
    print()
