h = open('index.html', encoding='utf-8').read()
import re
# IMGFALLBACK definition
m = re.search(r'IMGFALLBACK\s*=\s*function', h)
if not m: m = re.search(r'const\s+IMGFALLBACK\s*=', h)
if m:
    i = m.start()
    print("=== IMGFALLBACK ===")
    print(h[i:i+500])
    print()
# drawer big image: look for 'data-directo' / 'mirror' usage near 'dh' or large img
for kw in ['IMG_DIRECTA', 'function IMG(', 'const IMG=', 'width:480', 'width:320', 'class="big', 'class=\'big', 'thumb.big', 'galleryHTML']:
    i = h.find(kw)
    if i != -1:
        print(f"--- {kw} @ {i} ---")
        print("  ", h[max(0,i-60):i+200].replace('\n',' '))
        print()
PYEOF
python3 cache/scratch/read_drawer.py 2>&1 || echo "FAILED"