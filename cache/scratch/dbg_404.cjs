const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true,
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', args: ['--no-sandbox'] });
  const page = await (await browser.newContext({ locale: 'es-CL' })).newPage();
  const bad = [];
  page.on('response', r => { if (r.status() >= 400) bad.push(r.status() + ' ' + r.url()); });
  page.on('requestfailed', r => bad.push('FAILED ' + r.url() + ' ' + (r.failure()?.errorText||'')));
  await page.goto('https://foxnismone.github.io/hw-collector/', { waitUntil:'load', timeout:90000 });
  await page.waitForTimeout(8000);
  console.log('RESPUESTAS FALLIDAS (' + bad.length + '):');
  [...new Set(bad)].slice(0,15).forEach(e => console.log('  -', e.slice(0,160)));
  await browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
