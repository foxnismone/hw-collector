import json
h = open('index.html', encoding='utf-8').read()

# 1) bloque comment+IMGFALLBACK
a = h.find('// Fallback de imagen: reintenta directo y, si tambien falla')
b = h.find('};', h.find('fallar();', a)) + 2
bloco1 = h[a:b]
print("BLOQUE1 (IMGFALLBACK) único:", h.count(bloco1) == 1, "| len", len(bloco1))

# 2) cardHTML img else-branch
c2 = "`<div class=\"thumb imgerr\"></div>`;"
print("C2 (card div imgerr) único:", h.count(c2) == 1, "| count", h.count(c2))

# 3) drawer .dh img
c3 = '<img class="${FLIP(c)?\'mirror\':\'\'}" src="${escA(IMG(c.im))}" alt="" onerror="IMGFALLBACK(this)" data-directo="${escA(IMG_DIRECTA(c.im))}">'
print("C3 (drawer img) único:", h.count(c3) == 1, "| count", h.count(c3))

# 4) CSS .thumb.imgerr::after
c4 = '.thumb.imgerr::after{content:\"🚫\";font-size:20px;opacity:.3}'
print("C4 (CSS 🚫) único:", h.count(c4) == 1, "| count", h.count(c4))

# 5) CSS .thumb.imgerr
c5 = '.thumb.imgerr{background:var(--elev);display:flex;align-items:center;justify-content:center}'
print("C5 (CSS thumb imgerr bg) único:", h.count(c5) == 1, "| count", h.count(c5))

# show exact c3 for reference
print("\nC3 raw repr:", repr(c3[:90]))
