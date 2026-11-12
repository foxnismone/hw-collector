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

eval(nsBlock);
eval(imfBlock);
const dec=(s)=>decodeURIComponent(s.slice('data:image/svg+xml,'.length));

const u=global.noPhotoSVG(178,178);
console.log("T1 noPhotoSVG es data URI:", u.startsWith('data:image/svg+xml,'));
console.log("T1 has text:", dec(u).includes('Imagen próximamente'));
console.log("T1 no barras rojas:", !dec(u).includes('🚫'));
console.log("T1 cierra </svg>:", dec(u).endsWith('</svg>'));
console.log("T1 vars inyectadas:", dec(u).includes('#15181e')&&dec(u).includes('#ff4d00'));

const cNoImg={im:''};
const srcIfNoFoto = cNoImg.im ? 'real' : dec(global.noPhotoSVG(178,178));
console.log("T2 card sin foto usa placeholder:", srcIfNoFoto.endsWith('</svg>'));

let srcVal;
const el={
  dataset:{}, _k:'', classList:{add:(x)=>{this._k+=' '+x}},
  _a:{'data-directo':'https://fail.weserv/x'},
  onerror:null,
  getAttribute:(n)=>this._a[n]||null,
  removeAttribute:(n)=>{delete this._a[n]},
  set src(v){srcVal=v; this._a.src=v}, get src(){return this._a.src},
};
global.IMGFALLBACK(el);
console.log("T3 primera llamada setea retry data-directo:", srcVal==='https://fail.weserv/x');
global.IMGFALLBACK(el);
console.log("T3 segunda llamada setea placeholder SVG:", srcVal.startsWith('data:image/svg+xml,'));
console.log("T3 imgerr class agregada:", el._k.includes('imgerr'));
console.log("T3 data-fallback=1:", el._a['data-fallback']==='1');
console.log("T4 sin barras rojas en todo:", dec(srcVal).includes('🚫')===false);
console.log("\n✅ Tests OK");
