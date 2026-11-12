html = open('index.html', encoding='utf-8').read()
i = html.find('function initPage()')
j = html.find('\nfunction ', i+10)
if j < 0: j = i+4000
print(html[i:i+3500])
