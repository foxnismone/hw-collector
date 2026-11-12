html = open('index.html', encoding='utf-8').read()
i = html.find('function esc(s)')
print(repr(html[i:i+180]))
