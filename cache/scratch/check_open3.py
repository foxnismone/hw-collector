html = open('index.html', encoding='utf-8').read()
i = html.find('function drawer(')
seg = html[i:i+15000]
# encontrar d.innerHTML
k = seg.find('d.innerHTML')
print("d.innerHTML en drawer:", k)
print("=== 700 chars despues de d.innerHTML ===")
print(seg[k:k+700])
print("\n=== buscar setAttribute/classList en drawer ===")
for pat in ['setAttribute', 'classList.add', 'data-open', 'd.style']:
    p = seg.find(pat)
    print(f"  {pat}: {p}")
