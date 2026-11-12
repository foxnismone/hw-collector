html = open('index.html', encoding='utf-8').read()
i = html.find('const fichaHTML=')
print(html[i:i+700])
