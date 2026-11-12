html = open('index.html', encoding='utf-8').read()
import re
i = html.find('data-clase="Mainline"')
print("=== chips HTML ===")
print(html[max(0,i-500):i+600])
