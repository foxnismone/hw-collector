import urllib.request, re

req = urllib.request.Request('https://foxnismone.github.io/hw-collector/?vf3=1')
req.add_header('User-Agent','Mozilla/5.0')
html = urllib.request.urlopen(req, timeout=120).read().decode('utf-8','ignore')
print("HTML:", len(html))
print("JS defensivo (c.c||''):", "SI" if 'String(a.c||"")' in html else "NO")
print("JS defensivo (c.v||0):", "SI" if '(c.v||0).toFixed' in html else "NO")
print("drawer abre:", "SI" if 'd.dataset.open="1"' in html else "NO")
print("catLogoSVG:", "SI" if 'catLogoSVG' in html else "NO")

req2 = urllib.request.Request('https://foxnismone.github.io/hw-collector/data/cat.js')
req2.add_header('User-Agent','Mozilla/5.0')
cat = urllib.request.urlopen(req2, timeout=180).read().decode('utf-8','ignore')
print("\ncat.js:", len(cat))
print("  '\"v\":null':", cat.count('"v":null'))
print("  '\"y\":null':", cat.count('"y":null'))
print("  '\"c\":null':", cat.count('"c":null'))
print("  '\"x\":null':", cat.count('"x":null'))

req3 = urllib.request.Request('https://foxnismone.github.io/hw-collector/sw.js')
req3.add_header('User-Agent','Mozilla/5.0')
sw = urllib.request.urlopen(req3, timeout=60).read().decode('utf-8','ignore')
print("\nSW:", re.search(r'hwcollector-v\d+', sw).group(0))
