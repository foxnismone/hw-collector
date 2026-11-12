import urllib.request, re

req = urllib.request.Request('https://foxnismone.github.io/hw-collector/?livecheck=1')
req.add_header('User-Agent','Mozilla/5.0')
html = urllib.request.urlopen(req, timeout=120).read().decode('utf-8','ignore')
print("HTML en vivo: {:,} chars".format(len(html)))

CARD = 'closest(".card")'
print("listener .card:", "SI" if CARD in html else "NO")
print("cardHTML:", "SI" if 'function cardHTML' in html else "NO")
print("drawer():", "SI" if 'function drawer(' in html else "NO")
print("bandera pais:", "SI" if 'bandera=' in html else "NO")
print("thLogo:", "SI" if 'thLogo' in html else "NO")
print("fbar:", "SI" if 'fbar' in html else "NO")
print("nivelColor:", "SI" if 'nivelColor' in html else "NO")
print("data/cat.js script:", "SI" if 'data/cat.js' in html else "NO")

m = re.search(r'addEventListener\("click",e=>\{[^}]{0,200}closest\("\.card"\)', html)
print("listener exacto:", "SI" if m else "NO")
if m: print("  ", m.group(0)[:200])

print("drawer div:", "SI" if 'id="drawer"' in html else "NO")
print("closeDrawer:", "SI" if 'function closeDrawer' in html else "NO")
print("IDX:", "SI" if 'const IDX=' in html else "NO")
print("CAT ref:", "SI" if 'CAT.forEach' in html else "NO")
