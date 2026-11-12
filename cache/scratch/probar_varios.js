const fs = require('fs');
const vm = require('vm');
const BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/';
function cargarDatos(a){ let s=fs.readFileSync(a,'utf8'); s=s.slice(s.indexOf('=')+1).trim(); if(s.endsWith(';'))s=s.slice(0,-1); return JSON.parse(s); }
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
vm.runInContext(html.match(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/)[1], ctx, {filename:'inline'});

// probar 20 modelos al azar
const cat = ctx.CAT;
let ok=0, err=0;
const fallos = [];
for (let i=0;i<20;i++){
  const c = cat[Math.floor(Math.random()*cat.length)];
  try { ctx.drawer(c.i); ok++; }
  catch(e){ err++; fallos.push([c.i, c.m, e.message]); }
}
console.log(`drawer: ok=${ok} err=${err}`);
if (fallos.length) fallos.forEach(f=>console.log('  FALLO:', f[0], f[1], '->', f[2]));

// probar todos los cardHTML
let okc=0, errc=0; const fallosc=[];
for (const c of cat){
  try { ctx.cardHTML(c); okc++; } catch(e){ errc++; if(fallosc.length<5) fallosc.push([c.i,c.m,e.message]); }
}
console.log(`cardHTML: ok=${okc} err=${errc}`);
if (fallosc.length) fallosc.forEach(f=>console.log('  FALLO:', f[0], f[1], '->', f[2]));

// un modelo con galeria y ficha
const conTodo = cat.find(m=>m.galeria && m.galeria.length && m.ficha && m.ficha.es && m.ficha.es.descripcion);
if (conTodo){
  ctx.drawer(conTodo.i);
  const dh = ctx.document.getElementById('drawer').innerHTML;
  console.log(`\nModelo con todo: ${conTodo.m}`);
  console.log('  ficha:', dh.includes('Ficha del modelo'));
  console.log('  galeria:', dh.includes('Galería'));
  console.log('  disenador:', dh.includes('Diseñador'));
  console.log('  html:', dh.length);
}
process.exit(0);
