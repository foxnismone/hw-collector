const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    args: ['--no-sandbox'],
  });
  const page = await (await browser.newContext({ locale: 'es-CL' })).newPage();
  await page.goto('https://foxnismone.github.io/hw-collector/', { waitUntil: 'load', timeout: 90000 });
  await page.waitForTimeout(4000);

  const info = await page.evaluate(() => {
    const sel = document.getElementById('fcat');
    const opts = sel ? [...sel.options].map(o => ({ v: o.value, t: o.textContent })) : [];
    return {
      nOpts: opts.length,
      primeros: opts.slice(0, 8),
      estadoCat: typeof state !== 'undefined' ? state.cat : 'state no definido',
      nCards: document.querySelectorAll('#grid .card').length,
    };
  });
  console.log('Opciones fcat:', JSON.stringify(info, null, 2));

  // probar filtrar por MAINLINE
  const r = await page.evaluate(() => {
    const sel = document.getElementById('fcat');
    sel.value = 'MAINLINE';
    sel.dispatchEvent(new Event('change'));
    return new Promise(res => setTimeout(() => {
      res({
        stateCat: state.cat,
        nCards: document.querySelectorAll('#grid .card').length,
        rescount: document.getElementById('rescount')?.textContent,
      });
    }, 1500));
  });
  console.log('Tras filtrar MAINLINE:', JSON.stringify(r, null, 2));

  // probar una categoria rara
  const r2 = await page.evaluate(() => {
    const sel = document.getElementById('fcat');
    sel.value = 'CAR CULTURE';
    sel.dispatchEvent(new Event('change'));
    return new Promise(res => setTimeout(() => {
      res({
        stateCat: state.cat,
        nCards: document.querySelectorAll('#grid .card').length,
        rescount: document.getElementById('rescount')?.textContent,
      });
    }, 1500));
  });
  console.log('Tras filtrar CAR CULTURE:', JSON.stringify(r2, null, 2));

  await browser.close();
})().catch(e => { console.error('ERR:', e.message); process.exit(1); });
