const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ headless: true,
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ locale: 'es-CL' })).newPage();
  const malas = [];
  p.on('response', r => { if (r.status() >= 400) malas.push(r.status() + ' ' + r.url().slice(0,120)); });
  await p.goto('https://foxnismone.github.io/hw-collector/', { waitUntil: 'load', timeout: 90000 });
  await p.waitForTimeout(5000);
  await p.evaluate(async () => {
    for (let i=0;i<14;i++){ window.scrollTo(0, window.scrollY+800); await new Promise(r=>setTimeout(r,250)); }
    window.scrollTo(0,0); await new Promise(r=>setTimeout(r,800));
  });
  await p.waitForTimeout(2000);

  const rotas = await p.evaluate(() => {
    const out = [];
    document.querySelectorAll('#grid .card').forEach(c => {
      const im = c.querySelector('img.thumb');
      const nm = c.querySelector('.nm')?.textContent?.trim();
      if (im && im.complete && im.naturalWidth === 0 && !im.classList.contains('imgerr')) {
        out.push({ nm: nm?.slice(0,40), src: im.src.slice(0,110), data: im.getAttribute('data-directo')?.slice(0,110) });
      }
    });
    return out;
  });
  console.log('=== IMAGENES ROTAS REALES (' + rotas.length + ') ===');
  rotas.slice(0,14).forEach(r => { console.log('  ' + r.nm); console.log('     src: ' + r.src); console.log('     dir: ' + (r.data||'(vacio)')); });

  const cls = await p.evaluate(() => ({ t: window.__cls, f: (window.__clsFuentes||[]).slice(0,8) }));
  console.log('\n=== CLS: ' + cls.t.toFixed(4) + ' ===');
  cls.f.forEach(f => console.log('  ' + f.nodo + ' ' + JSON.stringify(f.antes) + ' -> ' + JSON.stringify(f.despues) + ' (' + f.valor + ')'));

  console.log('\n=== 4xx de red (' + malas.length + ') ===');
  [...new Set(malas)].slice(0,10).forEach(m => console.log('  ' + m));
  await b.close();
})().catch(e => { console.error(e.message); process.exit(1); });
