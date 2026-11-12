import json
from collections import Counter
cat = json.load(open('data/catalog_web.json', encoding='utf-8'))
c = Counter(m.get('k','') for m in cat)
print("Categorias:", len(c))
for k,v in c.most_common(25):
    print(f"  {v:6d}  {k}")
# verificar CLS cubre todas
html = open('index.html', encoding='utf-8').read()
import re
i = html.find('const CLS=')
j = html.find('};', i)
claves = re.findall(r"'([^']+)':\{t:", html[i:j])
faltan = [k for k in c if k not in claves]
print(f"\nCLS cubre: {len(claves)} | faltan en CLS: {faltan}")
