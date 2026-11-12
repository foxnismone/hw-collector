import re
h = open('index.html', encoding='utf-8').read()
print("=== 'brandlogo' / 'logo' ===")
for m in list(re.finditer(r'(brandlogo|logo|brand)', h, re.I))[:8]:
    print("  ", h[max(0,m.start()-80):m.start()+130].replace('\n',' '))
    print()
print("=== categoria/tag del modelo (k / catLogoSVG / categoria) ===")
for m in list(re.finditer(r'(catLogo|categoria|categor|tag.*categor|CAT\b)', h, re.I))[:10]:
    print("  ", h[max(0,m.start()-90):m.start()+120].replace('\n',' '))
    print()
print("=== linea del catalogo (series / serie / line) ===")
for m in list(re.finditer(r'(Series|series|Serie|Line\s|linea)', h, re.I))[:6]:
    print("  ", h[max(0,m.start()-60):m.start()+110].replace('\n',' '))
