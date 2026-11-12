import re
h = open('index.html', encoding='utf-8').read()
print("IMGFALLBACK definida:", "const IMGFALLBACK=" in h)
print("IMG_DIRECTA definida:", "const IMG_DIRECTA=" in h)
print("bypass %25:", "f.includes('%25')" in h)
print()
# los onerror existentes
pat = re.compile(r'onerror=\\"[^"]*imgerr[^"]*\\"')
ms = pat.findall(h)
print(f"onerror con imgerr: {len(ms)}")
for m in set(ms):
    print("  ", m[:160])
