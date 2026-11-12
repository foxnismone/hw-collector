html = open('index.html', encoding='utf-8').read()
i = html.find('function drawer(')
# encontrar el final: proxima 'function ' a nivel 0 (buscar '}\nfunction ')
j = i
depth = 0
ini = html.find('{', i)
for k in range(ini, len(html)):
    if html[k] == '{': depth += 1
    elif html[k] == '}':
        depth -= 1
        if depth == 0:
            j = k+1
            break
print(f"drawer(): {i} -> {j} ({j-i} chars)")
print(html[i:j])
