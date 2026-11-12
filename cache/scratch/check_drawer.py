html = open('index.html', encoding='utf-8').read()

i = html.find('function drawer(')
# buscar el final de la funcion: proximo 'function ' despues de i
j = html.find('\nfunction ', i+10)
if j < 0: j = i + 9000
print("=== FINAL de drawer() ===")
print(html[i+8000:j][:1800])
