const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ headless: true,
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ locale: 'es-CL' })).newPage();
  await p.goto('https://foxnismone.github.io/hw-collector/', { waitUntil: 'load', timeout: 90000 });
  await p.waitForTimeout(4000);
  await p.evaluate(async () => { for (let i=0;i<14;i++){ window.scrollTo(0, window.scrollY+700); await new Promise(r=>setTimeout(r,240)); } window.scrollTo(0,0); });
  await p.waitForTimeout(2000);
  const r = await p.evaluate(() => {
    const vacios = [];
    document.querySelectorAll('#grid .card').forEach(c => {
      const t = c.querySelector('.thumb');
      const im = c.querySelector('img');
      const esPlaceholderDiv = t && t.tagName === 'DIV';
      const imgErr = im && im.classList.contains('imgerr');
      if (esPlaceholderDiv || imgErr) {
        const h2 = c.querySelector('h2')?.textContent || '';
        vacios.push({
          nombre: h2.trim().slice(0,50),
          tipo: esPlaceholderDiv ? 'div-placeholder' : 'img-error',
          src: im ? (im.getAttribute('src')||'').slice(0,100) : '',
          directo: im ? (im.getAttribute('data-directo')||'').slice(0,100) : '',
          natural: im ? im.naturalWidth : 0,
        });
      }
    });
    return { n: vacios.length, muestra: vacios.slice(0,12) };
  });
  console.log('vacios:', r.n);
  r.muestra.forEach((v,i) => console.log(`  [${i}] ${v.tipo} | ${v.nombre} | nat=${v.natural}\n      src=${v.src}\n      dir=${v.directo}`));
  await b.close();
})().catch(e => { console.error(e.message); process.exit(1); });
