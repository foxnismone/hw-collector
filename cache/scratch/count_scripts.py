import re
html = open('index.html', encoding='utf-8').read()
# scripts con src
src = re.findall(r'<script[^>]*src="([^"]+)"', html)
print(f"Scripts con src: {len(src)}")
for s in src: print(f"  {s}")
# scripts inline
inline = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', html, re.DOTALL)
print(f"\nScripts inline: {len(inline)}")
for i, s in enumerate(inline):
    prim = s.strip()[:80].replace('\n',' ')
    print(f"  #{i}: {len(s)} chars | {prim}")

# donde esta galeriaHTML y drawer
print("\ngaleriaHTML en:", [m.start() for m in re.finditer(r'galeriaHTML', html)])
print("drawer en:", html.find('function drawer('))
