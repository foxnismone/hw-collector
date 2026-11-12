html = open('index.html', encoding='utf-8').read()
i = html.find('fuenteFactor')
print("=== fuenteFactor ===")
print(html[i-20:i+600] if i>=0 else "*** NO EXISTE ***")
