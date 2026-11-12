html = open('index.html', encoding='utf-8').read()
import re
print("=== data-open ocurrencias ===")
for m in list(re.finditer(r'data-open', html))[:10]:
    print("  ", html[max(0,m.start()-150):m.start()+120].replace('\n',' '))
print("\n=== .drawer CSS ===")
i = html.find('.drawer')
print(html[i:i+400].replace('\n',' '))
