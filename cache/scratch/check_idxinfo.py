html = open('index.html', encoding='utf-8').read()
import re
i = html.find('IDXINFO')
print("=== IDXINFO referencias ===")
for m in list(re.finditer(r'IDXINFO', html))[:8]:
    print("  ", html[max(0,m.start()-100):m.start()+80].replace('\n',' ')[:190])
    print()
