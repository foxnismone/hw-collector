html = open('index.html', encoding='utf-8').read()
import re
print("=== state.cat / fcat en el filtro ===")
for m in list(re.finditer(r'state\.cat|fcat', html))[:8]:
    print("  ", html[max(0,m.start()-160):m.start()+160].replace('\n',' ')[:300])
    print()
