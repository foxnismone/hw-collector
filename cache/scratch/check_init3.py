html = open('index.html', encoding='utf-8').read()
i = html.find('function initPage()')
seg = html[i:i+20000]
# buscar el final: proxima 'function ' a nivel 0
j = seg.find('\nfunction ', 10)
print("=== FINAL de initPage ===")
print(seg[j-1200:j+200])
