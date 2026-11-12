html = open('index.html', encoding='utf-8').read()
i = html.find('galeriaHTML')
# buscar la definicion
j = html.find('function galeriaHTML')
if j < 0: j = html.find('galeriaHTML=')
print("=== galeriaHTML definicion ===")
print(html[j:j+900])
