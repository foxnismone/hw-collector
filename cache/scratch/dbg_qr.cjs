const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true,
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', args: ['--no-sandbox'] });
  const page = await (await browser.newContext({ locale: 'es-CL' })).newPage();
  await page.goto('https://foxnismone.github.io/hw-collector/', { waitUntil:'load', timeout:90000 });
  await page.waitForTimeout(6000);
  const r = await page.evaluate(() => ({
    QRCode: typeof QRCode,
    ZXing: typeof ZXing,
    Tesseract: typeof Tesseract,
    supabase: typeof supabase,
  }));
  console.log('Librerias globales:', JSON.stringify(r, null, 2));
  // probar generar un QR
  const qr = await page.evaluate(async () => {
    if (typeof QRCode === 'undefined') return 'QRCode no definido';
    try {
      const c = document.createElement('canvas');
      await QRCode.toCanvas(c, 'TEST123', { width: 64 });
      return 'OK canvas ' + c.width + 'x' + c.height + ' data=' + c.toDataURL().length;
    } catch(e) { return 'ERROR: ' + e.message; }
  });
  console.log('Generar QR:', qr);
  await browser.close();
})().catch(e => { console.error(e.message); process.exit(1); });
