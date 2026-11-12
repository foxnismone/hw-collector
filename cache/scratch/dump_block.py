html = open('index.html', encoding='utf-8').read()
print("=== BLOQUE 112928-115367 (contenido ignorado) ===")
bloque = html[112928:115367]
print(f"longitud: {len(bloque)}")
print(bloque[:2500])
