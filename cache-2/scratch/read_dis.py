h = open('index.html', encoding='utf-8').read()
i = h.find('disHTML')
print(h[i-120:i+60])
# find the const definition / return
j = h.find('=', i)
k = h.find('`', j)
print("=== disHTML template start @", k)
print(h[k:k+900])
