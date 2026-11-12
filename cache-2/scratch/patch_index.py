import sys
h = open('index.html', encoding='utf-8').read()
orig = h

# ---------- 1) INSERTAR noPhotoSVG() antes del comentario del IMGFALLBACK ----------
anchor_comment = '// Fallback de imagen: reintenta directo y, si tambien falla, deja el placeholder'
assert h.count(anchor_comment) == 1, "anchor comment count"

noPhotoFunc = '''// Placeholder profesional para modelos sin foto o fotos rotas.
// Silueta estilizada de auto Hot Wheels + texto, con vars CSS del tema.
// Regla: NUNCA dejar un bloque vacio ni un círculo rojo/🚫.
const noPhotoSVG=(w=178,h=178)=>{
  if(!noPhotoSVG._c){
    const s=getComputedStyle(document.documentElement);
    noPhotoSVG._c={
      bg:s.getPropertyValue('--surface').trim()||'#15181e',
      ev:s.getPropertyValue('--elev').trim()||'#1d2128',
      ln:s.getPropertyValue('--line').trim()||'#2a2f38',
      mu:s.getPropertyValue('--muted-foreground').trim()||'#98a1ad',
      ac:s.getPropertyValue('--accent').trim()||'#ff4d00',
      br:s.getPropertyValue('--brand').trim()||'#ff4d00'
    };
  }
  const c=noPhotoSVG._c, m=w*0.106;
  const cx=w/2, fy=h*0.74, r=w*0.073, wl=cx-w*0.25, wr=cx+w*0.25;
  const innerH=w-2*m-24, rx=w*0.034;
  const sv='<svg xmlns="http://www.w3.org/2000/svg" width="'+w+'" height="'+h+'" viewBox="0 0 '+w+' '+h+'">'+
      '<rect width="'+w+'" height="'+h+'" rx="'+(w*0.042)+'" fill="'+c.bg+'">'+
      '<rect x="'+m+'" y="'+m+'" width="'+(w-2*m)+'" height="'+innerH+'" rx="'+rx+'" fill="'+c.ev+'" stroke="'+c.ln+'" stroke-width="1">'+
      '<ellipse cx="'+cx+'" cy="'+fy+'" rx="'+((wr-wl)/2+12)+'" ry="'+r*0.42+'" fill="'+c.ac+'" opacity=".55">'+
      '<circle cx="'+wl+'" cy="'+fy+'" r="'+r+'" fill="'+c.br+'" opacity=".45">'+
      '<circle cx="'+wr+'" cy="'+fy+'" r="'+r+'" fill="'+c.br+'" opacity=".45">'+
      '<circle cx="'+wl+'" cy="'+fy+'" r="'+r*0.4+'" fill="'+c.bg+'">'+
      '<circle cx="'+wr+'" cy="'+fy+'" r="'+r*0.4+'" fill="'+c.bg+'">'+
      '<path d="M'+(cx-13)+' '+(fy-r*1.6)+' L'+cx+' '+(fy-r*2.4)+' L'+(cx+14)+' '+(fy-r*1.6)+' Z" fill="#ffffff" opacity=".75">'+
      '<text x="'+cx+'" y="'+ (h-8)+'" font-size="11" fill="'+c.mu+'" text-anchor="middle" font-family="system-ui,monospace">Imagen próximamente</text>'+
    '</svg>';
  return 'data:image/svg+xml,'+encodeURIComponent(sv);
};
'''
h = h.replace(anchor_comment, noPhotoFunc + anchor_comment, 1)

# ---------- 2) REESCRIBIR IMGFALLBACK ----------
old_ifb = '''const IMGFALLBACK=el=>{
  el.onerror=null;
  const fallar=()=>{ el.classList.add('imgerr'); el.setAttribute('data-fallback','1'); el.removeAttribute('src'); };
  if(el.dataset.fb){ fallar(); return; }
  el.dataset.fb='1';
  const d=el.getAttribute('data-directo');
  if(d){ el.removeAttribute('data-directo'); el.src=d; return; }
  fallar();
};'''
new_ifb = '''// Reintena directo (weserv->IMG_DIRECTA) y, si también falla, usa el placeholder
// profesional noPhotoSVG. NUNCA deja un <img> vacío ni queda un bloque roto.
// data-fallback="1" => foto existía pero no cargó (fallo real, auditoría).
const IMGFALLBACK=el=>{
  if(el.dataset.fallbackDone) return;
  const d=el.getAttribute('data-directo');
  if(d){ el.removeAttribute('data-directo'); el.src=d; return; }
  el.dataset.fallbackDone='1';
  el.onerror=null;
  el.classList.add('imgerr');
  el.setAttribute('data-fallback','1');
  const w=Math.max(parseInt(getComputedStyle(el).width)||178,120);
  el.src=noPhotoSVG(w,w);
};'''
assert h.count(old_ifb) == 1, "IFB count: "+str(h.count(old_ifb))
h = h.replace(old_ifb, new_ifb, 1)

# ---------- 3) CARD: rama sin foto ----------
old_card = '''`<div class="thumb imgerr"></div>`;'''
new_card = '''`<img alt="Sin foto: ${escA(c.m)}" class="thumb placeholder" loading="lazy" decoding="async" src="${noPhotoSVG(178,178)}" data-noimg="1">`;'''
assert h.count(old_card) == 1, "card count: "+str(h.count(old_card))
h = h.replace(old_card, new_card, 1)

# ---------- 4) DRAWER .dh img ----------
old_drawer = '<img class="${FLIP(c)?\'mirror\':\'\'}" src="${escA(IMG(c.im))}" alt="" onerror="IMGFALLBACK(this)" data-directo="${escA(IMG_DIRECTA(c.im))}">'
new_drawer = '<img class="${FLIP(c)?\'mirror\':\'\'}" src="${c.im?escA(IMG(c.im)):escA(noPhotoSVG(120,120))}" alt="${c.im?escT(c.m):\'Sin foto: '+escT(c.m).replace(/'/g,"\\\\'")+'\'}" onerror="IMGFALLBACK(this)" data-directo="${c.im?escA(IMG_DIRECTA(c.im)):escA(noPhotoSVG(120,120))}">'
# the drawer alt escaping is getting hairy; keep it simple and safe:
new_drawer = '<img class="${FLIP(c)?\'mirror\':\'\'}" src="${c.im?escA(IMG(c.im)):escA(noPhotoSVG(120,120))}" alt="${c.im?escA(c.m):\'Sin foto\'+escA(c.m).replace(/&/g,\"&amp;\").replace(/[\\"\\']/g,\\\\$&)}" onerror="IMGFALLBACK(this)" data-directo="${c.im?escA(IMG_DIRECTA(c.im)):escA(noPhotoSVG(120,120))}">'
assert h.count(old_drawer) == 1, "drawer count: "+str(h.count(old_drawer))
h = h.replace(old_drawer, new_drawer, 1)

# ---------- 5) CSS: eliminar el 🚫 ----------
old_css = '.thumb.imgerr::after{content:"🚫";font-size:20px;opacity:.3}'
new_css = '.thumb.imgerr{background:var(--elev);display:flex;align-items:center;justify-content:center;border:1px dashed var(--line)} .thumb.placeholder{border:1px dashed var(--line);}'
assert h.count(old_css) == 1, "css count: "+str(h.count(old_css))
h = h.replace(old_css, new_css, 1)

open('index.html','w',encoding='utf-8').write(h)
print("OK. len antes:", len(orig), "despues:", len(h))
print("noPhotoSVG count:", h.count('noPhotoSVG'))
print("IMGFALLBACK new (fallbackDone):", h.count('fallbackDone'))
print("placeholder count:", h.count('placeholder'))
print("still has barras rojas?", '🚫' in h)
