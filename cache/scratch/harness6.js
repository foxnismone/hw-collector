const fs = require('fs');
const vm = require('vm');
const BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/';
function cargarDatos(archivo){
  const txt = fs.readFileSync(archivo,'utf8');
  let s = txt.slice(txt.indexOf('=')+1).trim();
  if (s.endsWith(';')) s = s.slice(0,-1);
  return JSON.parse(s);
}
const elementos = {};
function makeEl(id){ return { id, innerHTML:'', textContent:'', value:'', dataset:{}, style:{},
  classList:{add(){},remove(){},toggle(){},contains(){return false}},
  addEventListener(){}, setAttribute(){}, getAttribute(){return null},
  appendChild(){}, insertAdjacentHTML(){}, children:[], outerHTML:'' }; }
const document = { documentElement:{lang:'es'},
  getElementById(id){ if(!elementos[id]) elementos[id]=makeEl(id); return elementos[id]; },
  querySelectorAll(){return[];}, querySelector(){return null;},
  createElement(){return makeEl('tmp');}, addEventListener(){}, body:makeEl('body') };
const store = {};
const localStorage = { getItem(k){return store[k]||null;}, setItem(k,v){store[k]=v;}, removeItem(k){delete store[k];} };
const navigator = { onLine:true, userAgent:'node' };
const location = { protocol:'https:', href:'https://x/', origin:'https://x', pathname:'/' };
const ctx = { document, localStorage, navigator, location, console,
  setTimeout, setInterval, clearTimeout, clearInterval, addEventListener(){}, removeEventListener(){},
  fetch:()=>Promise.resolve({ok:true,json:()=>Promise.resolve({})}),
  IntersectionObserver:function(){return{observe(){},disconnect(){}};},
  URL, URLSearchParams, JSON, Math, Date, Object, Array, String, Number, Boolean,
  Promise, Map, Set, RegExp, Error, TypeError, parseInt, parseFloat, isNaN,
  encodeURIComponent, decodeURIComponent };
ctx.window = ctx; ctx.globalThis = ctx;
vm.createContext(ctx);
ctx.CAT = cargarDatos(BASE+'data/cat.js');
ctx.DISENADORES = cargarDatos(BASE+'data/disenadores.js');
ctx.WHEELTYPES = cargarDatos(BASE+'data/ruedas.js');
ctx.SERIES = cargarDatos(BASE+'data/series.js');

const html = fs.readFileSync(BASE+'index.html','utf8');
const scripts = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
console.log('Scripts inline encontrados:', scripts.length);
for (let i=0;i<scripts.length;i++){
  try { vm.runInContext(scripts[i], ctx, {filename:'inline'+i}); console.log(`  #${i} (${scripts[i].length} chars): OK`); }
  catch(e){ console.log(`  #${i} ERROR: ${e.message}`); }
}
console.log('\n=== PRUEBAS ===');
console.log('CAT:', Array.isArray(ctx.CAT)?ctx.CAT.length:'NO');
console.log('galeriaHTML:', typeof ctx.galeriaHTML);
console.log('abrirGaleria:', typeof ctx.abrirGaleria);
console.log('drawer:', typeof ctx.drawer);
for (const id of ['2026-JJJ02','2024-HRY51']) {
  try { ctx.drawer(id); console.log(`drawer(${id}): OK`); }
  catch(e){ console.log(`drawer(${id}) ERROR:`, e.message); }
}
process.exit(0);
