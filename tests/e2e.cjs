// suite E2E real con Playwright sobre el sitio en vivo
// Uso: NODE_PATH=<hermes>/node_modules node tests/e2e.cjs [URL]
const { chromium } = require('playwright');

const URL = process.argv[2] || 'https://foxnismone.github.io/hw-collector/';
const HEADLESS = true;

let passed = 0, failed = 0;
const fallos = [];
function ok(nombre, cond, extra = '') {
  if (cond) { passed++; console.log(`  \u2705 ${nombre}${extra ? ' — ' + extra : ''}`); }
  else { failed++; fallos.push(nombre); console.log(`  \u274c ${nombre}${extra ? ' — ' + extra : ''}`); }
}

(async () => {
  console.log(`\n=== E2E: ${URL} ===\n`);
  const browser = await chromium.launch({
    headless: HEADLESS,
    executablePath: process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  });
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, locale: 'es-CL' });
  const page = await ctx.newPage();

  const erroresConsola = [];
  const erroresPagina = [];
  const AVISOS_BENIGNOS = [
    "frame-ancestors' is ignored when delivered via a <meta>",
    'X-Frame-Options may only be set via an HTTP header',
    'Refused to execute inline script',
    'Progressive Web App',
  ];
  page.on('console', m => {
    if (m.type() !== 'error') return;
    const txt = m.text();
    if (AVISOS_BENIGNOS.some(a => txt.includes(a))) return;   // limitacion de GitHub Pages (sin headers HTTP)
    erroresConsola.push(txt.slice(0, 200));
  });
  page.on('pageerror', e => erroresPagina.push(String(e).slice(0, 300)));
  const respuestasFallidas = [];
  page.on('response', r => { if (r.status() >= 400) respuestasFallidas.push(`${r.status()} ${r.url().slice(0,110)}`); });

  console.log('--- 1. CARGA ---');
  await page.goto(URL, { waitUntil: 'load', timeout: 90000 });
  await page.waitForTimeout(4000);

  ok('sin errores JS en carga', erroresPagina.length === 0, erroresPagina.slice(0,2).join(' | '));
  ok('sin errores de consola en carga', erroresConsola.length === 0, erroresConsola.slice(0,2).join(' | '));
  ok('doctype HTML5', (await page.evaluate(() => document.doctype?.name)) === 'html');
  ok('lang="es"', (await page.evaluate(() => document.documentElement.lang)) === 'es');
  ok('charset utf-8', (await page.content()).includes('charset="utf-8"') || (await page.content()).includes('charset=utf-8'));
  ok('viewport presente', (await page.content()).includes('name="viewport"'));

  console.log('\n--- 2. DATOS ---');
  const nCat = await page.evaluate(() => (typeof CAT !== 'undefined' && CAT) ? CAT.length : -1);
  ok('CAT definido', nCat > 0, `${nCat} modelos`);
  ok('CAT >= 12000 modelos', nCat >= 12000, `${nCat}`);

  console.log('\n--- 3. GRID / TARJETAS ---');
  await page.waitForTimeout(2500);
  const nCards = await page.evaluate(() => document.querySelectorAll('#grid .card').length);
  ok('grid renderiza tarjetas', nCards > 0, `${nCards} tarjetas`);

  const datosTarjeta = await page.evaluate(() => {
    const c = document.querySelector('#grid .card');
    if (!c) return null;
    return {
      nombre: c.querySelector('.nm')?.textContent || '',
      categoria: c.querySelector('.chipc')?.textContent || '',
      indice: c.querySelector('.idxrow span')?.textContent || '',
      dataId: c.getAttribute('data-id') || '',
      imgs: c.querySelectorAll('img').length,
    };
  });
  ok('tarjeta tiene nombre', !!datosTarjeta?.nombre, datosTarjeta?.nombre?.slice(0,40));
  ok('tarjeta tiene categoria en MAYUSCULA', datosTarjeta?.categoria === datosTarjeta?.categoria?.toUpperCase(), datosTarjeta?.categoria);
  ok('tarjeta tiene indice numerico', /Índice [\d.]+/.test(datosTarjeta?.indice || ''), datosTarjeta?.indice);
  ok('tarjeta tiene imagen', datosTarjeta?.imgs > 0, `${datosTarjeta?.imgs} img`);

  // imagenes realmente cargadas (naturalWidth > 0)
  const imgsRotas = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll('#grid img.thumb').forEach(im => {
      if (im.src && !im.src.startsWith('data:') && im.naturalWidth === 0 && !im.classList.contains('imgerr')) {
        out.push(im.src.slice(0, 100));
      }
    });
    return out;
  });
  ok('imagenes del grid cargan', imgsRotas.length === 0, imgsRotas.length ? `${imgsRotas.length} rotas: ${imgsRotas[0]}` : 'todas OK');

  console.log('\n--- 4. CLIC -> DRAWER ---');
  const idPrimero = datosTarjeta?.dataId;
  if (idPrimero) {
    await page.evaluate(id => {
      const el = document.querySelector(`#grid .card[data-id="${id}"]`);
      if (el) el.click();
    }, idPrimero);
    await page.waitForTimeout(1800);

    const drawer = await page.evaluate(() => {
      const d = document.getElementById('drawer');
      return {
        open: d?.dataset?.open,
        html: (d?.innerHTML || '').length,
        h2: d?.querySelector('h2')?.textContent || '',
        tieneFicha: !!(d?.querySelector('h3')?.textContent || '').includes('Ficha'),
        tieneIndice: !!(d?.textContent || '').includes('Índice de coleccionabilidad'),
        tieneBarras: d ? d.querySelectorAll('.fbar, .fbar2').length : 0,
        tieneImg: d ? d.querySelectorAll('img').length : 0,
      };
    });
    ok('drawer se abre (data-open=1)', drawer.open === '1', `open=${drawer.open}`);
    ok('drawer tiene contenido', drawer.html > 2000, `${drawer.html} chars`);
    ok('drawer tiene titulo', !!drawer.h2, drawer.h2.slice(0,45));
    ok('drawer tiene ficha', drawer.tieneFicha);
    ok('drawer tiene indice', drawer.tieneIndice);
    ok('drawer tiene barras de indice', drawer.tieneBarras > 0, `${drawer.tieneBarras} barras`);
    ok('drawer tiene imagen', drawer.tieneImg > 0, `${drawer.tieneImg} img`);
  }

  console.log('\n--- 5. XSS / ESCAPE ---');
  const xss = await page.evaluate(() => {
    // inyectar un modelo con HTML malicioso en el DOM y verificar que se escapa
    const mal = '<img src=x onerror=window.__xss=1>';
    // probar que escT escapa
    const res = (typeof escT === 'function') ? escT(mal) : null;
    // buscar inyeccion real en el grid
    const scripts = document.querySelectorAll('#grid script').length;
    const onerror = [...document.querySelectorAll('#grid img')].filter(i => (i.getAttribute('onerror')||'').includes('window.__xss')).length;
    return { res, scripts, onerror, mal };
  });
  ok('escT definido y escapa HTML', xss.res === '&lt;img src=x onerror=window.__xss=1&gt;', JSON.stringify(xss.res));
  ok('no hay <script> inyectados en el grid', xss.scripts === 0, `${xss.scripts}`);

  console.log('\n--- 6. FILTROS ---');
  // filtro por categoria (se compara el contador de resultados: el grid pagina de a 60)
  const leerCount = () => page.evaluate(() => parseInt((document.getElementById('rescount')?.textContent || '0').replace(/[.]/g, ''), 10));
  const total = await leerCount();
  const catSel = await page.evaluate(() => {
    const s = document.getElementById('fcat');
    if (!s) return null;
    const opt = [...s.options].find(o => o.value && o.value !== 'MAINLINE');
    return opt ? opt.value : null;
  });
  if (catSel) {
    await page.selectOption('#fcat', catSel).catch(() => {});
    await page.waitForTimeout(1400);
    const filtrado = await leerCount();
    ok('filtro por categoria reduce resultados', filtrado > 0 && filtrado < total, `${total} -> ${filtrado} (${catSel})`);
    await page.selectOption('#fcat', '').catch(() => {});
    await page.waitForTimeout(900);
    const restaurado = await leerCount();
    ok('al quitar el filtro vuelve el total', restaurado === total, `${restaurado} vs ${total}`);
  } else {
    ok('filtro por categoria reduce resultados', false, 'no hay opciones');
  }

  // busqueda
  await page.fill('#q', 'Shelby').catch(() => {});
  await page.waitForTimeout(1200);
  const nBusq = await page.evaluate(() => document.querySelectorAll('#grid .card').length);
  const textoBusq = await page.evaluate(() => document.querySelector('#grid')?.textContent || '');
  ok('busqueda filtra', nBusq > 0 && /Shelby/i.test(textoBusq), `${nBusq} resultados`);
  await page.fill('#q', '').catch(() => {});
  await page.waitForTimeout(600);

  console.log('\n--- 7. SEGURIDAD ---');
  const seg = await page.evaluate(() => ({
    csp: document.querySelector('meta[http-equiv="Content-Security-Policy"]')?.content || '',
    noopener: document.querySelectorAll('a[target="_blank"]:not([rel*="noopener"])').length,
    iframes: document.querySelectorAll('iframe').length,
    imgsSinAlt: [...document.querySelectorAll('img')].filter(i => !i.hasAttribute('alt')).length,
  }));
  ok('CSP presente', seg.csp.includes('default-src'), seg.csp.slice(0, 60));
  ok("CSP object-src 'none'", seg.csp.includes("object-src 'none'"));
  ok("CSP frame-src 'none'", seg.csp.includes("frame-src 'none'"));
  ok('enlaces externos con noopener', seg.noopener === 0, `${seg.noopener} sin rel`);
  ok('sin iframes', seg.iframes === 0, `${seg.iframes}`);
  ok('todas las img tienen alt', seg.imgsSinAlt === 0, `${seg.imgsSinAlt} sin alt`);

  console.log('\n--- 8. ERRORES DE RED ---');
  const NO_APLICAN_EN_ESTATICO = /tts-voices|agent\/status|trends|agent\/|sync\//;
  const errs = respuestasFallidas.filter(r => !/favicon|qrserver/.test(r) && !NO_APLICAN_EN_ESTATICO.test(r));
  ok('sin respuestas 4xx/5xx criticas', errs.length === 0, errs.slice(0,3).join(' | ') || 'ninguna');

  await browser.close();

  console.log(`\n=== RESULTADO: ${passed} OK / ${failed} FALLIDOS ===`);
  if (fallos.length) console.log('Fallidos:\n' + fallos.map(f => '  - ' + f).join('\n'));
  process.exit(failed > 0 ? 1 : 0);
})().catch(e => { console.error('ERROR FATAL E2E:', e.message); process.exit(2); });
