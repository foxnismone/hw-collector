const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true,
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', args: ['--no-sandbox'] });
  const page = await (await browser.newContext({ locale: 'es-CL' })).newPage();
  const errs = [];
  page.on('console', m => { if (m.type()==='error') errs.push(m.text().slice(0,250)); });
  page.on('pageerror', e => errs.push('PAGEERROR: ' + String(e).slice(0,250)));
  await page.goto('https://foxnismone.github.io/hw-collector/', { waitUntil:'load', timeout:90000 });
  await page.waitForTimeout(6000);
  console.log('ERRORES CONSOLA (' + errs.length + '):');
  [...new Set(errs)].slice(0,12).forEach(e => console.log('  -', e));
  await browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
