h = open('index.html', encoding='utf-8').read()
# comment block + IMGFALLBACK
c = h.find('// Fallback de imagen: reintenta directo y, si tambien falla')
e = h.find('};', h.find('fallar();', c))
print(repr(h[c:e+2]))
