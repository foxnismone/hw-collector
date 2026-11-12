import re
h = open('index.html', encoding='utf-8').read()
i = h.find('const noPhotoSVG=(w=178,h=178)=>{')
end = h.find('return \'data:image/svg+xml,\'', i)
end = h.find('};', h.find("encodeURIComponent(sv)", end))
block = h[i:end+2]
print("FUNCION ACTUAL:")
print(repr(block))
