
// Popular lista de recientes
(function(){
  var list = document.getElementById('recentList');
  if(!list || typeof CAT === 'undefined') return;
  var recientes = CAT.slice(0, 8);
  list.innerHTML = recientes.map(function(c){
    var img = c.im ? '<img src="'+IMG(c.im)+'" alt="" onerror="this.style.display=\'none\'">' : '<div style="width:40px;height:40px;background:var(--card-bg)"></div>';
    return '<div class="mini-card" onclick="drawer(\''+c.i+'\')">' + img + '<span class="nm">'+esc(c.m)+'</span><span class="tag">'+esc(c.y||'')+'</span></div>';
  }).join('');
})();


/* ===== Galería de la ficha + lightbox ===== */
window.abrirGaleria=function(urls,idx){
  if(!urls||!urls.length) return;
  idx=idx||0;
  let lb=document.createElement('div'); lb.className='lightbox';
  const pinta=()=>{
    lb.innerHTML='<button class="lb-x" onclick="this.parentElement.remove()">&times;</button>'
      +'<img src="'+VER(urls[idx])+'" alt="" onerror="this.style.opacity=.3">'
      +'<div class="lb-nav"><button onclick="event.stopPropagation();window._lbPrev()">&larr;</button>'
      +'<span class="lb-count">'+(idx+1)+' / '+urls.length+'</span>'
      +'<button onclick="event.stopPropagation();window._lbNext()">&rarr;</button></div>';
  };
  window._lbPrev=()=>{ idx=(idx-1+urls.length)%urls.length; pinta(); };
  window._lbNext=()=>{ idx=(idx+1)%urls.length; pinta(); };
  lb.onclick=e=>{ if(e.target===lb) lb.remove(); };
  document.addEventListener('keydown',function k(e){ if(!document.body.contains(lb)){document.removeEventListener('keydown',k);return;} if(e.key==='Escape')lb.remove(); if(e.key==='ArrowLeft')window._lbPrev(); if(e.key==='ArrowRight')window._lbNext(); });
  document.body.appendChild(lb); pinta();
};
window.galeriaHTML=function(c){
  const g=(c&&c.galeria)||[];
  if(!g.length) return '';
  const prim=g[0];
  const resto=g.slice(1);
  const thumbs=g.slice(0,8).map((u,i)=>'<img src="'+VER(u)+'" alt="" loading="lazy" onclick="abrirGaleria('+JSON.stringify(g).replace(/"/g,'&quot;')+','+i+')" onerror="this.style.visibility=\'hidden\'">').join('');
  return '<div class="sec" style="border:1px solid var(--line);padding:12px;margin-bottom:10px"><h3 style="margin:0 0 8px">Galería ('+g.length+')</h3><div class="galeria-grid">'+thumbs+'</div>'
    +((g.length>8)?'<div class="galeria-vacia">+ '+(g.length-8)+' imágenes más (hacé clic para recorrerlas)</div>':'')+'</div>';
};

