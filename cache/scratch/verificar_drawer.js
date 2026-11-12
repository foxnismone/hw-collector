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
const m = html.match(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/);
vm.runInContext(m[1], ctx, {filename:'inline'});

const c = ctx.CAT[0];
ctx.drawer(c.i);
const dh = ctx.document.getElementById('drawer').innerHTML;
console.log('drawer HTML:', dh.length, 'chars');
console.log('data-open:', ctx.document.getElementById('drawer').dataset.open);
console.log('tiene h2:', dh.includes('<h2>'));
console.log('tiene ficha:', dh.includes('Ficha del modelo'));
console.log('tiene galeria:', dh.includes('Galería'));
console.log('tiene indice:', dh.includes('Índice de coleccionabilidad'));
console.log('tiene barras:', dh.includes('class="fbar"'));
console.log('tiene imagen:', dh.includes('<img'));
console.log('tiene catlogo:', dh.includes('catlogo'));
console.log('nombre:', c.m);
console.log('categoria:', c.k);
console.log('x:', c.x);
// verificar cardHTML
const ch = ctx.cardHTML(c);
console.log('\ncardHTML:', ch.length, 'chars');
console.log('  tiene img:', ch.includes('<img'));
console.log('  tiene badge:', ch.includes('chipc'));
process.exit(0);
