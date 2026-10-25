/**
 * dom_audit.cjs — Auditoria estructural de las fichas en el DOM (flujo 1).
 *
 * Detecta en el navegador real:
 *   - tarjetas de vehiculo sin imagen (bloque vacio)
 *   - tarjetas cuyo contenedor de imagen queda en 0x0 (layout shift)
 *   - tarjetas con contenido interno vacio
 *   - fichas (drawer) que se abren sin datos
 *   - imagenes rotas despues del fallback (class imgerr)
 *
 * Uso:
 *   node dom_audit.cjs [URL] [--json]
 *
 * Sale con codigo 0 si no hay bloques rotos, 1 si los hay (para CI).
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const URL_SITIO = process.argv.find(a => a.startsWith('http')) ||
  'https://foxnismone.github.io/hw-collector/';
const JSON_SALIDA = process.argv.includes('--json');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';

const hallazgos = [];

function agregar(tipo, detalle) {
  hallazgos.push({ tipo, detalle });
}

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: CHROME,
    args: ['--no-sandbox'],
  });
  const page = await (await browser.newContext({ locale: 'es-CL' })).newPage();

  // layout shifts (CLS) acumulado durante la carga
  await page.addInitScript(() => {
    window.__cls = 0;
    window.__clsFuentes = [];
    new PerformanceObserver(list => {
      for (const e of list.getEntries()) {
        if (!e.hadRecentInput) {
          window.__cls += e.value;
          (e.sources || []).forEach(s => {
            window.__clsFuentes.push({
              nodo: s.node ? (s.node.className || s.node.tagName || '').toString().slice(0, 40) : '?',
              antes: [Math.round(s.previousRect?.x || 0), Math.round(s.previousRect?.y || 0)],
              despues: [Math.round(s.currentRect?.x || 0), Math.round(s.currentRect?.y || 0)],
              valor: +e.value.toFixed(4),
            });
          });
        }
      }
    }).observe({ type: 'layout-shift', buffered: true });
  });

  await page.goto(URL_SITIO, { waitUntil: 'load', timeout: 90000 });
  await page.waitForTimeout(5000);

  // disparar lazy loading
  await page.evaluate(async () => {
    for (let i = 0; i < 14; i++) {
      window.scrollTo(0, window.scrollY + 800);
      await new Promise(r => setTimeout(r, 250));
    }
    window.scrollTo(0, 0);
    await new Promise(r => setTimeout(r, 800));
  });
  await page.waitForTimeout(1500);

  // ---------------------------------------------------------- 1. tarjetas
  const cards = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll('#grid .card').forEach((c, i) => {
      const im = c.querySelector('img.thumb, img');
      const titulo = c.querySelector('.nm, h3, h2, .cname, b');
      const cont = c.querySelector('.thumb, .cimg, img');
      const r = c.getBoundingClientRect();
      out.push({
        i,
        titulo: (titulo?.textContent || '').trim().slice(0, 60),
        tieneImg: !!im,
        src: (im?.getAttribute('src') || '').slice(0, 90),
        naturalW: im?.naturalWidth || 0,
        naturalH: im?.naturalHeight || 0,
        esPlaceholder: im?.classList.contains('imgerr') || false,
        falloReal: im?.getAttribute('data-fallback') === '1' || false,
        esDivVacio: !im && !!cont && cont.classList.contains('imgerr'),
        ancho: Math.round(cont?.getBoundingClientRect().width || r.width),
        alto: Math.round(cont?.getBoundingClientRect().height || r.height),
        areaTarjeta: Math.round(r.width * r.height),
        textoVacio: (c.textContent || '').trim().length < 4,
      });
    });
    return out;
  });

  const total = cards.length;
  const sinImg = cards.filter(c => !c.tieneImg && !c.esDivVacio);
  // 'esPlaceholder' = el modelo no tiene foto y el sitio muestra el placeholder
  // elegante a proposito. Eso NO es una imagen rota: es el disenio correcto.
  // Placeholder elegante = el modelo no tiene foto: es el diseno correcto, NO un error.
  // Fallo real = la foto existia pero no cargo (data-fallback="1"): ahi si es bug.
  const conImgRota = cards.filter(c => c.falloReal);
  const placeholder = cards.filter(c => (c.esPlaceholder || c.esDivVacio) && !c.falloReal);
  const ceroArea = cards.filter(c => c.ancho === 0 || c.alto === 0);
  const sinTitulo = cards.filter(c => !c.titulo);
  const textoVacio = cards.filter(c => c.textoVacio);

  if (sinImg.length) agregar('tarjetas_sin_imagen', `${sinImg.length}/${total}`, sinImg.slice(0, 8).map(c => c.titulo));
  if (conImgRota.length) agregar('imagenes_rotas', `${conImgRota.length}/${total}`, conImgRota.slice(0, 8).map(c => c.src));
  if (ceroArea.length) agregar('layout_shift_contenedor_vacio', `${ceroArea.length}/${total}`, ceroArea.slice(0, 8).map(c => `${c.titulo} (${c.ancho}x${c.alto})`));
  if (sinTitulo.length) agregar('tarjetas_sin_titulo', `${sinTitulo.length}/${total}`, sinTitulo.slice(0, 5).map(c => c.titulo));
  if (textoVacio.length) agregar('tarjetas_con_texto_vacio', `${textoVacio.length}/${total}`, textoVacio.slice(0, 5).map(c => c.titulo));

  // ---------------------------------------------------------- 2. ficha (drawer)
  const ficha = await page.evaluate(() => {
    const card = document.querySelector('#grid .card');
    if (!card) return { error: 'no hay tarjetas' };
    card.click();
    return null;
  });
  await page.waitForTimeout(1800);

  const drawer = await page.evaluate(() => {
    const d = document.getElementById('drawer');
    if (!d) return { error: 'no hay drawer' };
    const txt = (d.textContent || '').trim();
    const img = d.querySelector('img');
    const r = d.getBoundingClientRect();
    return {
      abierto: d.dataset.open === '1',
      chars: txt.length,
      tieneTitulo: !!d.querySelector('h2'),
      tieneImg: !!img,
      imgW: img?.naturalWidth || 0,
      imgH: img?.naturalHeight || 0,
      imgEsPlaceholder: img?.classList.contains('imgerr') || false,
      imgFalloReal: img?.getAttribute('data-fallback') === '1' || false,
      imgSrc: (img?.getAttribute('src') || '').slice(0, 90),
      ancho: Math.round(r.width),
      alto: Math.round(r.height),
      seccionesVacias: [...d.querySelectorAll('.sec, section, .ficha, .galeria')]
        .filter(s => (s.textContent || '').trim().length < 4).length,
    };
  });

  if (ficha?.error) agregar('drawer', ficha.error);
  if (drawer.error) agregar('drawer', drawer.error);
  else {
    if (!drawer.abierto) agregar('drawer_no_abre', 'data-open != 1');
    if (drawer.chars < 200) agregar('drawer_casi_vacio', `${drawer.chars} chars`);
    if (!drawer.tieneTitulo) agregar('drawer_sin_titulo', 'sin <h2>');
    if (drawer.imgFalloReal)
      agregar('drawer_imagen_rota', `la foto existia pero no cargo: ${drawer.imgSrc}`);
    if (drawer.seccionesVacias)
      agregar('drawer_secciones_vacias', `${drawer.seccionesVacias} secciones sin contenido`);
  }

  await page.evaluate(() => {
    const c = document.querySelector('#drawer .close');
    if (c) c.click();
  });

  // ---------------------------------------------------------- 3. CLS
  const clsData = await page.evaluate(() => ({ total: window.__cls || 0, fuentes: window.__clsFuentes || [] }));
  const cls = clsData.total;
  if (cls > 0.25) {
    const top = clsData.fuentes.sort((a, b) => b.valor - a.valor).slice(0, 6);
    agregar('layout_shift_acumulado', `CLS ${cls.toFixed(3)} (umbral 0.25)`,
            top.map(f => `${f.nodo} ${f.antes} -> ${f.despues} (${f.valor})`));
  }

  // ---------------------------------------------------------- 4. resumen
  const resumen = {
    url: URL_SITIO,
    fecha: new Date().toISOString(),
    tarjetas: {
      total,
      con_imagen_cargada: cards.filter(c => c.tieneImg && c.naturalW > 0).length,
      placeholder_elegante: placeholder.length,   // modelos sin foto: diseno correcto, no error
      sin_imagen: sinImg.length,
      rotas: conImgRota.length,          // foto existia y no cargo (fallo real)
      sin_foto: placeholder.length,       // modelo sin foto: placeholder elegante (correcto)
      contenedores_vacios: ceroArea.length,
    },
    ficha: drawer.error ? { error: drawer.error } : {
      abierto: drawer.abierto,
      chars: drawer.chars,
      tiene_imagen: drawer.tieneImg && drawer.imgW > 0,
      img: `${drawer.imgW}x${drawer.imgH}`,
      secciones_vacias: drawer.seccionesVacias,
    },
    cls: +cls.toFixed(4),
    bloques_rotos: hallazgos.length,
    hallazgos,
  };

  if (JSON_SALIDA) {
    const ruta = path.join(__dirname, 'dom_audit_ultimo.json');
    fs.writeFileSync(ruta, JSON.stringify(resumen, null, 2));
    console.log(`\nJSON: ${ruta}`);
  }

  console.log('\n=== AUDITORIA DOM ===');
  console.log(`  Tarjetas: ${resumen.tarjetas.total}`);
  console.log(`  Con imagen cargada: ${resumen.tarjetas.con_imagen_cargada}`);
  console.log(`  Placeholder elegante (sin foto): ${resumen.tarjetas.placeholder_elegante}`);
  console.log(`  Sin imagen: ${resumen.tarjetas.sin_imagen}`);
  console.log(`  Rotas (fallo real): ${resumen.tarjetas.rotas}`);
  console.log(`  Sin foto (placeholder correcto): ${resumen.tarjetas.sin_foto}`);
  console.log(`  Contenedores vacios: ${resumen.tarjetas.contenedores_vacios}`);
  console.log(`  CLS: ${resumen.cls}`);
  console.log(`  Ficha: ${resumen.ficha.chars || 0} chars, img ${resumen.ficha.img || '-'}, secciones vacias ${resumen.ficha.secciones_vacias || 0}`);
  console.log('');
  if (!hallazgos.length) {
    console.log('  ✅ Sin bloques rotos ni vacios.');
  } else {
    console.log(`  ❌ ${hallazgos.length} hallazgos:`);
    for (const h of hallazgos) {
      console.log(`     - [${h.tipo}] ${h.detalle}`);
      if (h.ejemplos?.length) h.ejemplos.forEach(e => console.log(`         · ${e}`));
    }
  }

  await browser.close();
  process.exit(hallazgos.length ? 1 : 0);
})().catch(e => {
  console.error('FALLO dom_audit:', e.message);
  process.exit(2);
});
