html = open('index.html', encoding='utf-8').read()
import re
i = html.find('const VER')
if i < 0: i = html.find('VER=')
print("=== VER ===")
print(html[max(0,i-200):i+500])
