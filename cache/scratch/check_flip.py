html = open('index.html', encoding='utf-8').read()
import re
for pat in ['function FLIP', 'FLIP=', 'const FLIP']:
    i = html.find(pat)
    if i>=0:
        print(f"=== {pat} ===")
        print(html[i:i+600])
        break
# ORIENT / FLIPMAN
for pat in ['ORIENT', 'FLIPMAN=']:
    j = html.find(pat)
    if j>=0:
        print(f"\n=== {pat} ===")
        print(html[max(0,j-150):j+300])
