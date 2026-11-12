const fs=require('fs');
const V={'--surface':'#15181e','--elev':'#1d2128','--line':'#2a2f38','--muted-foreground':'#98a1ad','--accent':'#ff4d00','--brand':'#ff4d00'};
global.document={documentElement:{}};
global.getComputedStyle=(_=>({getPropertyValue:(n)=>V[n]||''}));
global.window={};

const src=fs.readFileSync('cache-2/scratch/inline.js','utf8');
const ns=src.indexOf('const noPhotoSVG=');
const reReturn=src.indexOf("return 'data:image/svg+xml,'", ns);
const nsEnd=reReturn+src.slice(reReturn).indexOf('};')+2;
const nsBlock=src.slice(ns, nsEnd).replace('const noPhotoSVG=','global.noPhotoSVG=');
const imf=src.indexOf('const IMGFALLBACK=', nsEnd);
const imfRe=src.indexOf("el.src=noPhotoSVG(w,w);", imf);
const imfEnd=imfRe+src.slice(imfRe).indexOf('};')+2;
const imfBlock=src.slice(imf, imfEnd).replace('const IMGFALLBACK=','global.IMGFALLBACK=');
eval(nsBlock); eval(imfBlock);
const dec=(s)=>decodeURIComponent(s.slice('data:image/svg+xml,'.length));

const u=global.noPhotoSVG(178,178);
console.log("T1 noPhotoSVG es data URI:", u.startsWith('data:image/svg+xml,'));
console.log("T1 has text:", dec(u).includes('Imagen próximamente'));
console.log("T1 no barras rojas:", !dec(u).includes('🚫'));
console.log("T1 cierra </svg>:", dec(u).endsWith('</svg>'));
console.log("T1 vars inyectadas:", dec(u).includes('#15181e')&&dec(u).includes('#ff4d00'));

let srcVal;
const el={
  dataset:{}, _k:'', classList:{add(x){this._k+=' '+x}},
  _a:{'data-directo':'https://fail.weserv/x'},
  onerror:null,
  getAttribute(n){return this._a[n]||null},
  removeAttribute(n){delete this._a[n]}, setAttribute(n,v){this._a[n]=v},
  set src(v){srcVal=v; this._a.src=v}, get src(){return this._a.src},
};
global.IMGFALLBACK(el);
console.log("T2 fallback: data-directo -> retry:", el._a.src==='https://fail.weserv/x');
delete el._a['data-directo'];
global.IMGFALLBACK(el);
console.log("T2 fallback: segunda llamada -> placeholder SVG:", srcVal.startsWith('data:image/svg+xml,'));
console.log("T2 imgerr class:", el._k.includes('imgerr'), "| data-fallback=1:", el._a['data-fallback']==='1');
console.log("T3 sin barras rojas en placeholder final:", dec(srcVal).includes('🚫')===false);
console.log("\n✅ Tests OK");
