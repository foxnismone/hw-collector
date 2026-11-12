html = open('index.html', encoding='utf-8').read()
i = html.find('function filtered(')
print(html[i:i+1200])
