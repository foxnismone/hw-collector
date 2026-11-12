// Harness de prueba: simula DOM minimo y ejecuta el script principal para probar drawer()
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/';

// --- DOM falso ---
const elementos = {};
function makeEl(id) {
  return {
    id, innerHTML: '', textContent: '', value: '', dataset: {}, style: {},
    classList: { add(){}, remove(){}, toggle(){}, contains(){return false} },
    addEventListener(){}, setAttribute(){}, getAttribute(){return null},
    appendChild(){}, insertAdjacentHTML(){}, children: [], dataset_open: '0',
  };
}
const document = {
  documentElement: { lang: 'es' },
  getElementById(id) { if(!elementos[id]) elementos[id]=makeEl(id); return elementos[id]; },
  querySelectorAll() { return []; },
  querySelector() { return null; },
  createElement() { return makeEl('tmp'); },
  addEventListener(){},
  body: makeEl('body'),
};
const store = {};
const localStorage = {
  getItem(k){ return store[k]||null; },
  setItem(k,v){ store[k]=v; },
  removeItem(k){ delete store[k]; },
};
const navigator = { onLine: true, serviceWorker: undefined, userAgent: 'node' };
const location = { protocol: 'https:', href: 'https://foxnismone.github.io/hw-collector/', origin: 'https://foxnismone.github.io', pathname: '/' };
const window = { addEventListener(){}, innerWidth: 1400, innerHeight: 900 };
window.document = document;
window.localStorage = localStorage;
window.navigator = navigator;
window.location = location;
window.console = console;

const ctx = {
  document, window, localStorage, navigator, location, console,
  setTimeout, setInterval, clearTimeout, clearInterval,
  fetch: () => Promise.resolve({ ok: true, json: () => Promise.resolve({}) }),
  IntersectionObserver: function(){ return { observe(){}, disconnect(){} }; },
  MutationObserver: function(){ return { observe(){}, disconnect(){} }; },
  speechSynthesis: undefined,
  URL, URLSearchParams, JSON, Math, Date, Object, Array, String, Number, Boolean,
  Promise, Map, Set, RegExp, Error, TypeError, parseInt, parseFloat, isNaN, encodeURIComponent, decodeURIComponent,
};
ctx.globalThis = ctx;
vm.createContext(ctx);

// --- cargar scripts ---
function cargar(archivo) {
  const codigo = fs.readFileSync(archivo, 'utf8');
  try { vm.runInContext(codigo, ctx, { filename: archivo }); return true; }
  catch(e) { console.log(`ERROR en ${path.basename(archivo)}: ${e.message}`); return false; }
}

// scripts externos
cargar(BASE + 'data/cat.js');
cargar(BASE + 'data/disenadores.js');
cargar(BASE + 'data/ruedas.js');
cargar(BASE + 'data/series.js');

// script principal del HTML
const html = fs.readFileSync(BASE + 'index.html', 'utf8');
const scripts = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
console.log(`Scripts inline: ${scripts.length}`);
for (let i=0; i<scripts.length; i++) {
  try { vm.runInContext(scripts[i], ctx, { filename: `inline-${i}` }); }
  catch(e) { console.log(`ERROR script inline #${i}: ${e.message}`); }
}

// --- probar ---
console.log('\n=== PRUEBAS ===');
const CAT = ctx.CAT;
console.log('CAT:', CAT ? CAT.length : 'undefined');

// render
try { ctx.render(true); console.log('render(true): OK'); }
catch(e) { console.log('render(true) ERROR:', e.message); }

// drawer con un modelo
const ids = ['2026-JJJ02', '2024-HRY51'];
for (const id of ids) {
  try { ctx.drawer(id); console.log(`drawer(${id}): OK, html=${ctx.document.getElementById('drawer').innerHTML.length} chars`); }
  catch(e) { console.log(`drawer(${id}) ERROR:`, e.message); }
}

// buscar un modelo con galeria
const conGal = CAT.find(m=>m.galeria && m.galeria.length);
if (conGal) {
  try { ctx.drawer(conGal.i); console.log(`drawer(${conGal.i}) con galeria: OK, html=${ctx.document.getElementById('drawer').innerHTML.length} chars`); }
  catch(e) { console.log(`drawer galeria ERROR:`, e.message); }
}

// cardHTML
try { const h = ctx.cardHTML(CAT[0]); console.log(`cardHTML: OK (${h.length} chars)`); }
catch(e) { console.log('cardHTML ERROR:', e.message); }
