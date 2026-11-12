const { Resvg } = require('@resvg/resvg-js');
const fs = require('fs');
const path = process.argv[2];
const out = process.argv[3];
const w = parseInt(process.argv[4] || '0', 10);
const bg = process.argv[5] || null;

const svg = fs.readFileSync(path, 'utf8');
const opts = {
  fitTo: w ? { mode: 'width', value: w } : { mode: 'original' },
  font: {
    loadSystemFonts: true,
    defaultFontFamily: 'Arial Black',
  },
};
if (bg) opts.background = bg;
const r = new Resvg(svg, opts);
const png = r.render().asPng();
fs.writeFileSync(out, png);
console.log('OK', out, png.length, 'bytes');
