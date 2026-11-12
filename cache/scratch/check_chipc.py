html = open('index.html', encoding='utf-8').read()
import re
print("=== .chipc CSS ===")
for m in list(re.finditer(r'\.chipc', html))[:8]:
    print("  ", html[max(0,m.start()-60):m.start()+180].replace('\n',' ')[:240])

print("\n=== chips de clase (data-clase) ===")
for m in list(re.finditer(r'data-clase="[^"]*"', html))[:10]:
    print("  ", m.group(0))

print("\n=== state.clase usos ===")
for m in list(re.finditer(r'state\.clase\s*=', html))[:6]:
    print("  ", html[max(0,m.start()-120):m.start()+80].replace('\n',' ')[:200])
