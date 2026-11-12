h = open('index.html', encoding='utf-8').read()
i = h.find('function cardHTML(c){')
if i == -1:
    i = h.find('function cardHTML')
print(h[i:i+1700])
