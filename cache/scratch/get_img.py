import re
h = open('index.html', encoding='utf-8').read()
i = h.find('IMG=f=>')
print(h[i-200:i+400])
