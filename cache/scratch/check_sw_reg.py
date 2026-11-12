html = open('index.html', encoding='utf-8').read()
import re
for m in list(re.finditer(r'serviceWorker', html))[:5]:
    print("  ", html[max(0,m.start()-150):m.start()+200].replace('\n',' ')[:340])
    print()
