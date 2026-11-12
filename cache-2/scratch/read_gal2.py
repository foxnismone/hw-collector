h = open('index.html', encoding='utf-8').read()
i = h.find('function galeriaHTML(c){')
print(h[i:i+1700])
