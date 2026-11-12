const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ headless: true,
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', args: ['--no-sandbox'] });
  const p = await (await b.newContext({ locale: 'es-CL' })).newPage();
  const urls = {
    'directa %25': 'https://static.wikia.nocookie.net/hotwheels/images/c/c9/Bat_-_1989_-_03_100%25.jpg',
    'weserv  %25': 'https://images.weserv.nl/?url=static.wikia.nocookie.net/hotwheels/images/c/c9/Bat_-_1989_-_03_100%25.jpg',
    'directa normal': 'https://static.wikia.nocookie.net/hotwheels/images/e/e6/Bat_-_1966_-_ComicCon.jpg',
  };
  for (const [k, u] of Object.entries(urls)) {
    const r = await p.evaluate(async (u) => {
      return await new Promise(res => {
        const im = new Image();
        im.onload = () => res(`OK ${im.naturalWidth}x${im.naturalHeight}`);
        im.onerror = () => res('ERROR');
        setTimeout(() => res('TIMEOUT'), 12000);
        im.src = u;
      });
    }, u);
    console.log(`  ${k.padEnd(16)} ${r}`);
  }
  await b.close();
})().catch(e => { console.error(e.message); process.exit(1); });
