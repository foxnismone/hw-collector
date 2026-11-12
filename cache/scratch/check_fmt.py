html = open('index.html', encoding='utf-8').read()
import re
for pat in ['function fmt', 'const fmt=', 'fmt=']:
    i = html.find(pat)
    if i >= 0:
        print(f"=== {pat} ===")
        print(html[i:i+250])
        break
# tambien conv
i = html.find('function conv')
print("\n=== conv ===")
print(html[i:i+200] if i>=0 else "no")
