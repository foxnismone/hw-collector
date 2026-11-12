const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ headless: true,
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ locale: 'es-CL' })).newPage();
  await p.goto('https://foxnismone.github.io/hw-collector/', { waitUntil: 'load', timeout: 90000 });
  await p.waitForTimeout(5000);
  const r = await p.evaluate(async () => {
    const urls = {
      'directa %25': 'https://static.wikia.nocookie.net/hotwheels/images/c/c9/Bat_-_1989_-_03_100%25.jpg',
      'weserv  %25': 'https://images.weserv.nl/?url=static.wikia.nocookie.net/hotwheels/images/c/c9/Bat_-_1989_-_03_100%25.jpg',
      'directa normal': 'https://static.wikia.nocookie.net/hotwheels/images/e/e6/Bat_-_1966_-_ComicCon.jpg',
    };
    const out = {};
    for (const [k, u] of Object.entries(urls)) {
      out[k] = await new Promise(res => {
        const im = new Image();
        im.onload = () => res(`OK ${im.naturalWidth}x${im.naturalHeight}`);
        im.onerror = () => res('ERROR');
        setTimeout(() => res('TIMEOUT'), 12000);
        im.src = u;
      });
    }
    return out;
  });
  console.log(JSON.stringify(r, null, 2));
  await b.close();
})().catch(e => { console.error(e.message); process.exit(1); });
