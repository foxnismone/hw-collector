const fs = require('fs');
const vm = require('vm');
const BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/';

const elementos = {};
function makeEl(id) {
  return { id, innerHTML:'', textContent:'', value:'', dataset:{}, style:{},
    classList:{add(){},remove(){},toggle(){},contains(){return false}},
    addEventListener(){}, setAttribute(){}, getAttribute(){return null},
    appendChild(){}, insertAdjacentHTML(){}, children:[], outerHTML:'' };
}
const document = {
  documentElement:{lang:'es'},
  getElementById(id){ if(!elementos[id]) elementos[id]=makeEl(id); return elementos[id]; },
  querySelectorAll(){return[];}, querySelector(){return null;},
  createElement(){return makeEl('tmp');}, addEventListener(){}, body:makeEl('body'),
};
const store = {};
const localStorage = { getItem(k){return store[k]||null;}, setItem(k,v){store[k]=v;}, removeItem(k){delete store[k];} };
const navigator = { onLine:true, userAgent:'node' };
const location = { protocol:'https:', href:'https://foxnismone.github.io/hw-collector/', origin:'https://foxnismone.github.io', pathname:'/' };

const ctx = {
  document, localStorage, navigator, location, console,
  setTimeout, setInterval, clearTimeout, clearInterval,
  addEventListener(){}, removeEventListener(){},
  fetch:()=>Promise.resolve({ok:true,json:()=>Promise.resolve({})}),
  IntersectionObserver:function(){return{observe(){},disconnect(){}};},
  URL, URLSearchParams, JSON, Math, Date, Object, Array, String, Number, Boolean,
  Promise, Map, Set, RegExp, Error, TypeError, parseInt, parseFloat, isNaN,
  encodeURIComponent, decodeURIComponent,
};
ctx.window = ctx;
ctx.globalThis = ctx;
vm.createContext(ctx);

function cargar(archivo){
  try { vm.runInContext(fs.readFileSync(archivo,'utf8'), ctx, {filename:archivo}); return true; }
  catch(e){ console.log(`ERROR cargando ${archivo}: ${e.message}`); return false; }
}
cargar(BASE+'data/cat.js');
cargar(BASE+'data/disenadores.js');
cargar(BASE+'data/ruedas.js');
cargar(BASE+'data/series.js');

const html = fs.readFileSync(BASE+'index.html','utf8');
const m = html.match(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/);
try { vm.runInContext(m[1], ctx, {filename:'inline'}); console.log('script inline: OK'); }
catch(e){ console.log('script inline ERROR:', e.message, '\n  stack:', (e.stack||'').split('\n').slice(0,4).join('\n')); }

console.log('\n=== PRUEBAS ===');
console.log('CAT:', ctx.CAT ? ctx.CAT.length : 'undefined');
console.log('galeriaHTML:', typeof ctx.galeriaHTML);
console.log('drawer:', typeof ctx.drawer);
try { ctx.render(true); console.log('render(true): OK, grid html='+ctx.document.getElementById('grid').innerHTML.length); }
catch(e){ console.log('render ERROR:', e.message); }

for (const id of ['2026-JJJ02','2024-HRY51']) {
  try { ctx.drawer(id); console.log(`drawer(${id}): OK, html=${ctx.document.getElementById('drawer').innerHTML.length} chars`); }
  catch(e){ console.log(`drawer(${id}) ERROR:`, e.message); }
}
