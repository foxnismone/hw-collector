import re
h = open('index.html', encoding='utf-8').read()
# que archivos JS carga?
for m in re.findall(r'src="([^"]+\.js)"', h):
    print("SRC:", m)
for m in re.findall(r"src='([^']+\.js)'", h):
    print("SRC':", m)
print("--- cat.js path ---")
for m in re.finditer(r'cat\.js', h):
    print("  ", h[max(0,m.start()-40):m.start()+20].replace('\n',' '))
# FLIP definition
m = re.search(r'FLIP\s*=', h)
if m:
    i=m.start(); end=h.find(';',i)+1
    print("\n=== FLIP ===")
    print(h[i:end])
