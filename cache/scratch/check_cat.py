import json
from collections import Counter
cat = json.load(open('data/catalog_web.json', encoding='utf-8'))
c = Counter(m.get('k','') for m in cat)
print("Categorias (top 25):")
for k,v in c.most_common(25):
    print(f"  {v:5d}  {k}")
