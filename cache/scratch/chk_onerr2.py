import re
h = open('index.html', encoding='utf-8').read()
print("=== ocurrencias de onerror ===")
for m in re.finditer(r'onerror', h):
    print(" ", h[m.start():m.start()+150].replace('\n',' '))
print()
print("=== class=\"thumb ===")
for m in list(re.finditer(r'class="thumb', h))[:4]:
    print(" ", h[max(0,m.start()-60):m.start()+220].replace('\n',' '))
    print()
