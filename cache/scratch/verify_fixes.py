import urllib.request, re

req = urllib.request.Request('https://foxnismone.github.io/hw-collector/?vf=1')
req.add_header('User-Agent','Mozilla/5.0')
html = urllib.request.urlopen(req, timeout=120).read().decode('utf-8','ignore')
print("HTML en vivo:", len(html))

# 1. drawer abre
print("1. drawer abre (d.dataset.open='1'):", "SI" if "d.dataset.open=\"1\"" in html else "NO")
# 2. bandera
print("2. bandera de origen:", "SI" if "bandera=" in html else "NO")
# 3. logo de categoria
print("3. catLogoSVG:", "SI" if "catLogoSVG" in html else "NO")
# 4. barras naranjas
print("4. nivelColor naranja:", "SI" if '#ff4d00":(v>=44' in html else "NO")
print("   idxHTML usa bar():", "SI" if "Object.keys(det).map" in html else "NO")
print("   CSS .catlogo:", "SI" if ".catlogo{" in html else "NO")

# Verificar cat.js tiene pais e indice_detalle
req2 = urllib.request.Request('https://foxnismone.github.io/hw-collector/data/cat.js')
req2.add_header('User-Agent','Mozilla/5.0')
cat = urllib.request.urlopen(req2, timeout=180).read().decode('utf-8','ignore')
print("\ncat.js en vivo:", len(cat))
print("   con 'pais':", "SI" if '"pais":' in cat else "NO")
print("   con 'indice_detalle':", "SI" if '"indice_detalle":' in cat else "NO")
