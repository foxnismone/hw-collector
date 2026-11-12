import re
h = open('index.html', encoding='utf-8').read()
print("=== todos los onerror ===")
for m in re.finditer(r'onerror="[^"]*"', h):
    print("  ", h[max(0,m.start()-90):m.end()].replace('\n',' ')[-150:])
print()
print("=== usos de IMG( ===")
for m in list(re.finditer(r'IMG\(', h))[:12]:
    print("  ", h[max(0,m.start()-60):m.start()+90].replace('\n',' '))
