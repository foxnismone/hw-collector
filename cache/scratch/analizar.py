html = open('index.html', encoding='utf-8').read()
import re

# Funciones que usa drawer y cardHTML
funcs = ['IMG','FLIP','catLogoSVG','galeriaHTML','_hist','donut','bar','fmt','conv','valorRef','bestChannels','clsDe','slugCat','nivelColor','CASEBY']
print("=== Funciones definidas ===")
for f in funcs:
    ok = ('function '+f) in html or (f+'=') in html or (f+' =') in html
    print(f"  {f}: {'OK' if ok else 'FALTA'}")

print("\n=== .toFixed( sobre campos (peligro si null) ===")
for m in list(re.finditer(r'\.toFixed\(', html))[:12]:
    print("  ", html[max(0,m.start()-60):m.start()+20].replace('\n',' '))

print("\n=== .map( sobre campos potencialmente undefined ===")
for m in list(re.finditer(r'(c\.f|\.f)\.map\(', html))[:6]:
    print("  ", html[max(0,m.start()-80):m.start()+60].replace('\n',' '))
