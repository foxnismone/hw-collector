html = open('index.html', encoding='utf-8').read()
import re
print("=== render() sin args ===")
for m in list(re.finditer(r'render\(\)', html))[:6]:
    print("  ", html[max(0,m.start()-120):m.start()+40].replace('\n',' ')[:180])

print("\n=== 'render(true);' cerca del final del script ===")
pos = [m.start() for m in re.finditer(r'render\(true\)', html)]
print("total:", len(pos), "ultimos:", pos[-5:])
for p in pos[-3:]:
    print("  ", html[max(0,p-100):p+60].replace('\n',' ')[:170])
