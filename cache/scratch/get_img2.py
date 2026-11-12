h = open('index.html', encoding='utf-8').read()
i = h.find('const IMG=f=>')
print(h[i:i+900])
