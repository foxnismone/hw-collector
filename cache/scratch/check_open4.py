html = open('index.html', encoding='utf-8').read()
i = html.find('function drawer(')
seg = html[i:i+15000]
print("=== 8300-9200 ===")
print(seg[8300:9200])
