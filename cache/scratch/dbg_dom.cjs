const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ headless: true,
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ locale: 'es-CL' })).newPage();
  await p.goto('https://foxnismone.github.io/hw-collector/', { waitUntil: 'load', timeout: 90000 });
  await p.waitForTimeout(5000);

  // 1. que selector de titulo existe realmente
  const sel = await p.evaluate(() => {
    const c = document.querySelector('#grid .card');
    return {
      html: c ? c.innerHTML.slice(0, 400) : 'sin tarjeta',
      tags: c ? [...c.querySelectorAll('*')].map(e => e.tagName + '.' + e.className).slice(0, 20) : [],
    };
  });
  console.log('=== PRIMERA TARJETA ===');
  console.log(sel.html.replace(/\s+/g,' '));
  console.log('\ntags:', sel.tags.join(' | '));

  // 2. drawer
  await p.evaluate(() => document.querySelector('#grid .card')?.click());
  await p.waitForTimeout(2000);
  const d = await p.evaluate(() => {
    const dr = document.getElementById('drawer');
    const im = dr.querySelector('img');
    return {
      chars: (dr.textContent||'').trim().length,
      imgSrc: im?.getAttribute('src')?.slice(0,110),
      imgW: im?.naturalWidth, imgH: im?.naturalHeight,
      dataDirecto: im?.getAttribute('data-directo')?.slice(0,110),
      imgClass: im?.className,
      titulo: dr.querySelector('h2')?.textContent?.slice(0,50),
    };
  });
  console.log('\n=== DRAWER ===');
  console.log(JSON.stringify(d, null, 2));
  await b.close();
})().catch(e => { console.error(e.message); process.exit(1); });
