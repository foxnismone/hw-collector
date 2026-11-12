import re
h = open('index.html', encoding='utf-8').read()
print("=== imgerr ===")
for m in list(re.finditer(r'imgerr', h))[:6]:
    print(" ", h[max(0,m.start()-160):m.start()+120].replace('\n',' '))
    print()
print("=== class=\"thumb\" / thumb ===")
for m in list(re.finditer(r'thumb', h))[:6]:
    print(" ", h[max(0,m.start()-140):m.start()+140].replace('\n',' '))
    print()
