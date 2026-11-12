html = open('index.html', encoding='utf-8').read()
i = html.find('function cardHTML(c)')
j = html.find('function render(', i)
print(html[i:j])
