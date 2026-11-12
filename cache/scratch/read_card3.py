h = open('index.html', encoding='utf-8').read()
i = h.find('function cardHTML(c){')
print(h[i+1400:i+1400+1100])
