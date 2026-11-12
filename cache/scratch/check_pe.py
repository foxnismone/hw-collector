html = open('index.html', encoding='utf-8').read()
import re
print("=== pointer-events ===")
for m in list(re.finditer(r'pointer-events', html))[:6]:
    print("  ", html[max(0,m.start()-80):m.start()+80].replace('\n',' '))

print("\n=== .thumb CSS ===")
i = html.find('.thumb{')
print(html[i:i+250].replace('\n',' ') if i>=0 else "NO")

print("\n=== .cardwrap CSS ===")
j = html.find('.cardwrap{')
print(html[j:j+200].replace('\n',' ') if j>=0 else "NO")
