import urllib.request, re
req = urllib.request.Request('https://foxnismone.github.io/hw-collector/?vf4=1')
req.add_header('User-Agent','Mozilla/5.0')
html = urllib.request.urlopen(req, timeout=120).read().decode('utf-8','ignore')
print("HTML:", len(html))
for nombre, patron in [
    ("drawer abre", 'd.dataset.open="1"'),
    ("JS defensivo c.c", 'String(a.c||"")'),
    ("JS defensivo c.v", '(c.v||0).toFixed'),
    ("clsDe fallback", 'const clsDe='),
    ("catLogoSVG", 'catLogoSVG'),
    ("barras R/D/C/A/M", 'Object.keys(det).map'),
    ("filtro por c.k", 'if(state.cat&&c.k!==state.cat)'),
    ("slugCat", 'const slugCat='),
    ("categorias MAYUS", 'toUpperCase()'),
]:
    print(f"  {nombre}: {'SI' if patron in html else 'NO'}")

req2 = urllib.request.Request('https://foxnismone.github.io/hw-collector/data/cat.js')
req2.add_header('User-Agent','Mozilla/5.0')
cat = urllib.request.urlopen(req2, timeout=180).read().decode('utf-8','ignore')
print("\ncat.js:", len(cat))
print("  nulls v/y/c/x:", cat.count('"v":null'), cat.count('"y":null'), cat.count('"c":null'), cat.count('"x":null'))
print("  fichas es:", cat.count('"es":{"descripcion"'))
print("  galeria:", cat.count('"galeria":['))
print("  disenador:", cat.count('"disenador":"'))
print("  indice_detalle:", cat.count('"indice_detalle":{"R"'))
print("  pais:", cat.count('"pais":"'))

req3 = urllib.request.Request('https://foxnismone.github.io/hw-collector/sw.js')
req3.add_header('User-Agent','Mozilla/5.0')
sw = urllib.request.urlopen(req3, timeout=60).read().decode('utf-8','ignore')
print("\nSW:", re.search(r'hwcollector-v\d+', sw).group(0))
