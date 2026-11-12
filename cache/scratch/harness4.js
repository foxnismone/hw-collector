const fs = require('fs');
const vm = require('vm');
const BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/';

// Parsear los archivos de datos (formato: PREFIJO=json;)
function cargarDatos(archivo, nombre){
  const txt = fs.readFileSync(archivo,'utf8');
  const i = txt.indexOf('=');
  let s = txt.slice(i+1).trim();
  if (s.endsWith(';')) s = s.slice(0,-1);
  return JSON.parse(s);
}

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
const location = { protocol:'https:', href:'https://x/', origin:'https://x', pathname:'/' };

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
ctx.window = ctx; ctx.globalThis = ctx;
vm.createContext(ctx);

// asignar datos (como haria el navegador con const globales)
ctx.CAT = cargarDatos(BASE+'data/cat.js');
ctx.DISENADORES = cargarDatos(BASE+'data/disenadores.js');
ctx.WHEELTYPES = cargarDatos(BASE+'data/ruedas.js');
ctx.SERIES = cargarDatos(BASE+'data/series.js');

const html = fs.readFileSync(BASE+'index.html','utf8');
const m = html.match(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/);
try { vm.runInContext(m[1], ctx, {filename:'inline'}); console.log('script inline: OK'); }
catch(e){ console.log('script inline ERROR:', e.message); }

console.log('\n=== PRUEBAS ===');
console.log('CAT:', Array.isArray(ctx.CAT) ? ctx.CAT.length : 'NO');
console.log('galeriaHTML:', typeof ctx.galeriaHTML);
console.log('drawer:', typeof ctx.drawer);
try { ctx.render(true); console.log('render(true): OK, grid html='+ctx.document.getElementById('grid').innerHTML.length); }
catch(e){ console.log('render ERROR:', e.message); }

for (const id of ['2026-JJJ02','2024-HRY51']) {
  try { ctx.drawer(id); console.log(`drawer(${id}): OK, html=${ctx.document.getElementById('drawer').innerHTML.length} chars`); }
  catch(e){ console.log(`drawer(${id}) ERROR:`, e.message); }
}
process.exit(0);
