html = open('index.html', encoding='utf-8').read()
i = html.find('const CLS=')
print("=== CLS ===")
print(html[i:i+900])
print("\n=== usos de CLS ===")
import re
for m in list(re.finditer(r'CLS\[', html))[:8]:
    print("  ", html[max(0,m.start()-80):m.start()+120].replace('\n',' ')[:200])
