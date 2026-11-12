html = open('index.html', encoding='utf-8').read()
i = html.find('function drawer(')
print("drawer() en:", i)
seg = html[i:i+12000]
# buscar 'data-open'
k = seg.find('data-open')
print("data-open en drawer():", k)
if k>=0:
    print(seg[max(0,k-400):k+300])
else:
    # buscar el final
    print("--- ultimos 800 chars de drawer ---")
    print(seg[-800:])
