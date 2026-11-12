h = open('index.html', encoding='utf-8').read()
import re
m = re.search(r'const\s+IMGFALLBACK\s*=', h)
if not m:
    m = re.search(r'IMGFALLBACK\s*=\s*function', h)
if m:
    i = m.start()
    print("=== IMGFALLBACK ===")
    print(h[i:i+500])
    print()
for kw in ['IMG_DIRECTA', 'function IMG(', 'const IMG=', 'width:480', 'width:320', 'class="big', 'galleryHTML']:
    i = h.find(kw)
    if i != -1:
        print("--- " + kw + " @ " + str(i) + " ---")
        print("  " + h[max(0,i-60):i+200].replace("\n"," "))
        print()
