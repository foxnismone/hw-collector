import json, re
cat = json.load(open('data/catalog_web.json', encoding='utf-8'))

# donde estan
donde = {'im':0, 'galeria':0}
ej_im, ej_gal = [], []
for m in cat:
    if 'not_available' in str(m.get('im','')).lower():
        donde['im'] += 1
        if len(ej_im)<4: ej_im.append((m['m'], m['im']))
    for u in (m.get('galeria') or []):
        if 'not_available' in str(u).lower():
            donde['galeria'] += 1
            if len(ej_gal)<4: ej_gal.append((m['m'], u))
print(f"En 'im': {donde['im']} | En 'galeria': {donde['galeria']}")

print("\n=== en im ===")
for e in ej_im: print(f"  {e[0][:35]:37s} {e[1][:90]}")
print("\n=== en galeria ===")
for e in ej_gal: print(f"  {e[0][:35]:37s} {e[1][:90]}")

# verificar que cargan
import urllib.request
def chk(u):
    try:
        r=urllib.request.Request(u); r.add_header('User-Agent','Mozilla/5.0')
        with urllib.request.urlopen(r,timeout=20) as x: return x.status, len(x.read())
    except Exception as e: return 'ERR', str(e)[:30]
if ej_im:
    print("\nPrueba im:", chk(ej_im[0][1]))
if ej_gal:
    print("Prueba gal:", chk(ej_gal[0][1]))
