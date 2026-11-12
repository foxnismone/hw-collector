import re
html = open('index.html', encoding='utf-8').read()
# imgs sin alt
imgs = re.findall(r'<img[^>]*>', html)
sin = [i for i in imgs if 'alt=' not in i]
print(f"imgs totales (estaticas): {len(imgs)} | sin alt: {len(sin)}")
for i in sin[:5]: print("  ", i[:100])
# imgs con doble alt
doble = [i for i in imgs if i.count('alt=')>1]
print(f"imgs con doble alt: {len(doble)}")
for i in doble[:3]: print("  ", i[:120])
