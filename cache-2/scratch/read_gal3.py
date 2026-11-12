h = open('index.html', encoding='utf-8').read()
i = h.find('galeriaHTML(c){')
if i == -1:
    i = h.lower().find('galeriahtml')
print("pos:", i)
print(repr(h[i-60:i+30]))
# find next function after galeriaHTML
j = h.find('function', i+10)
print(h[i:j][:1800])
