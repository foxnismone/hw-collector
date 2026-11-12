h = open('index.html', encoding='utf-8').read()
i = h.find('galeriaHTML')
print("=== galeriaHTML @", i, "===")
print(h[i:i+1200])
