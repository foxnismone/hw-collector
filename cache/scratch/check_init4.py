html = open('index.html', encoding='utf-8').read()
i = html.find('function initPage()')
print("initPage en:", i)
# imprimir los ultimos 1500 chars antes de 'function render('
k = html.find('function render(', i)
print("render en:", k)
print("=== entre initPage y render ===")
print(html[k-1500:k])
