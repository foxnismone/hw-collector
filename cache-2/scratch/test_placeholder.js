// Placeholder profesional para autos sin foto / fotos rotas.
// Silueta estilizada de auto Hot Wheels + texto, con vars CSS del tema.
// Regla: NUNCA dejar un bloque vacio ni un 🚫.
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
  const e=(n,v)=>encodeURIComponent(n)+'='+encodeURIComponent(v),
        A=encodeURIComponent, join=(arr,sep)=>arr.join(sep);
  let d=[];
  d.push('data:image/svg+xml,'+A(
    '<svg xmlns="http://www.w3.org/2000/svg" width="'+w+'" height="'+h+'" viewBox="0 0 '+w+' '+h+'">'+
      '<rect width="'+w+'" height="'+h+'" rx="'+(w*0.042)+'" fill="'+c.bg+'">'+
      '<rect x="'+m+'" y="'+m+'" width="'+(w-2*m)+'" height="'+innerH+'" rx="'+rx+'" fill="'+c.ev+'" stroke="'+c.ln+'" stroke-width="1">'+
      // chasis + llantas (silueta auto)
      '<ellipse cx="'+cx+'" cy="'+fy+'" rx="'+((wr-wl)/2+12)+'" ry="'+r*0.42+'" fill="'+c.ac+'" opacity=".55">'+
      '<circle cx="'+wl+'" cy="'+fy+'" r="'+r+'" fill="'+c.br+'" opacity=".45">'+
      '<circle cx="'+wr+'" cy="'+fy+'" r="'+r+'" fill="'+c.br+'" opacity=".45">'+
      '<circle cx="'+wl+'" cy="'+fy+'" r="'+r*0.4+'" fill="'+c.bg+'">'+
      '<circle cx="'+wr+'" cy="'+fy+'" r="'+r*0.4+'" fill="'+c.bg+'">'+
      // parabrisas
      '<path d="M'+(cx-13)+' '+(fy-r*1.6)+' L'+cx+' '+(fy-r*2.4)+' L'+(cx+14)+' '+(fy-r*1.6)+' Z" fill="#ffffff" opacity=".75">'+
      '<text x="'+cx+'" y="'+(h-8)+'" font-size="11" fill="'+c.mu+'" text-anchor="middle" font-family="system-ui,monospace">Imagen próximamente</text>'+
    '</svg>'
  ));
  return d.join('');
};
// ---- mock DOM para test ----
if(!global.document){
  let stored='--surface=#15181e;--elev=#1d2128;--line=#2a2f38;--muted-foreground=#98a1ad;--accent=#ff4d00;--brand=#ff4d00;';
  global.document={documentElement:{}};
  global.getComputedStyle=(_)=>({
    getPropertyValue:(n)=>n in {_:'x'}?'':'',
    // parse from stored
  });
  // real parser
  global.getComputedStyle=(_)=>(({p:stored})=>{
    return {getPropertyValue:(n)=>{const m=stored.match(n.replace(/[-:]/g,ch=>'\\'+ch)+'\\s*:\\s*([^;]+)');return m?m[1].trim():''}
    };
  })(stored));
}
const u178=noPhotoSVG(178,178);
const u120=noPhotoSVG(120,120);
const u64=noPhotoSVG(64,64);
console.log("178 len:",u178.length);
// decode and sanity check
const dec=(u)=>decodeURIComponent(u.slice('data:image/svg+xml,'.length));
const svg178=dec(u178);
console.log("178 contains svg:", svg178.startsWith('<svg'));
console.log("178 contains text:", svg178.includes('Imagen próximamente'));
console.log("178 contains placeholder-avoid 🚫:", !svg178.includes('🚫'));
console.log("178 ends </svg>:", svg178.endsWith('</svg>'));
console.log("120 ends </svg>:", dec(u120).endsWith('</svg>'));
console.log("64 ends </svg>:", dec(u64).endsWith('</svg>'));
console.log("vars injected surface=", svg178.includes('#15181e')," accent=", svg178.includes('#ff4d00'));
console.log("\nSVG 178:\n"+svg178);
