const fs = require('fs');
const vm = require('vm');
const BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/';
const html = fs.readFileSync(BASE+'index.html','utf8');
const m = html.match(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/);
const codigo = m[1];
console.log('longitud script inline:', codigo.length);
console.log('contiene window.galeriaHTML=:', codigo.includes('window.galeriaHTML='));
console.log('posicion:', codigo.indexOf('window.galeriaHTML='));
// los ultimos 200 chars
console.log('\n=== ULTIMOS 300 chars del script ===');
console.log(JSON.stringify(codigo.slice(-300)));
// buscar donde se asigna
const i = codigo.indexOf('window.galeriaHTML=');
console.log('\n=== contexto de window.galeriaHTML= ===');
console.log(JSON.stringify(codigo.slice(i-300, i+100)));
