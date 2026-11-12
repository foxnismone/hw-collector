html = open('index.html', encoding='utf-8').read()
i = html.find('navigator.serviceWorker.register("sw.js")')
print(repr(html[i:i+400]))
