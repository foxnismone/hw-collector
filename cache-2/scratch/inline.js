
/* ===== datos embebidos ===== */
function esc(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');}
/* === Defensa en profundidad XSS: escape por contexto ===
   escT -> texto plano dentro de HTML
   escA -> valor de atributo (comillas incluidas)
   escJ -> literal de string JS (para onclick="fn('${escJ(...)}')")
   Ninguna interpolacion de datos dinamicos debe quedar sin envolver. */
const escT=s=>String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const escA=s=>String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
const escJ=s=>String(s??'').replace(/\\/g,'\\\\').replace(/'/g,"\\'").replace(/"/g,'\\"').replace(/\n/g,'\\n').replace(/\r/g,'');
const escU=s=>String(s??'').replace(/"/g,'&quot;').replace(/'/g,'&#39;').replace(/[<>]/g,'');
;const PRE={"meta":{"generado":"2026-10-11","moneda":"USD","fuente_principal":"research/02_mercado_y_valores.md (cada fila lleva su URL y fecha)","advertencia":"Los rangos por CLASE son referenciales y NO sustituyen comparables de ventas reales del modelo exacto. Confianza: baja."},"rangos_por_clase":[{"clase":"Mainline","estado":"carded (en tarjeta)","min":1.0,"max":5.0,"fuente":"hobbyDB listings 2024-2025","fecha":"2025"},{"clase":"Mainline","estado":"loose (suelto)","min":0.5,"max":3.0,"fuente":"hobbyDB / allhotwheels","fecha":"2025"},{"clase":"Treasure Hunt","estado":"carded","min":5.0,"max":20.0,"fuente":"iCollectEverything","fecha":"2026"},{"clase":"Treasure Hunt","estado":"loose","min":2.0,"max":8.0,"fuente":"iCollectEverything","fecha":"2026"},{"clase":"Super Treasure Hunt","estado":"carded","min":85.0,"max":250.0,"fuente":"resellcalendar.com / autoevolution.com (STH 2024-2025)","fecha":"2025"},{"clase":"Premium / Car Culture (unidad)","estado":"carded","min":6.95,"max":12.5,"fuente":"eBay listings","fecha":"2024-2025"},{"clase":"Premium / Car Culture (set de 5)","estado":"carded","min":29.95,"max":64.99,"fuente":"eBay listings","fecha":"2023-2025"},{"clase":"RLC (Red Line Club)","estado":"carded","min":29.99,"max":84.99,"fuente":"99diecast.com / wheelcollectors.com / coloradodiecast.com","fecha":"2024-2025"},{"clase":"Convention Exclusive","estado":"carded","min":42.99,"max":140.0,"fuente":"hobbyDB Blog / wheelcollectors.com","fecha":"2022-2025"},{"clase":"Redline vintage (1968-1977)","estado":"played-with","min":50.0,"max":400.0,"fuente":"yonkerstimes.com / howmuchisitworth.app","fecha":"2026"},{"clase":"Redline vintage (1968-1977)","estado":"near mint","min":300.0,"max":3500.0,"fuente":"yonkerstimes.com / rarityfinder.com (PSA)","fecha":"2026"},{"clase":"Grail / prototipo","estado":"cualquiera","min":5000.0,"max":175000.0,"fuente":"icollecteverything.com / underpricedai.com","fecha":"2024-2026"}],"modelos_con_precio_verificado":[{"modelo":"Pink Rear-Loading Beach Bomb","anio":1969,"linea":"Prototipo Redline","min":100000,"max":175000,"fuente":"https://www.icollecteverything.com/2026/04/04/most-valuable-hot-wheels-cars/","fecha":"2024-2026"},{"modelo":"Pink Custom Volkswagen (sunroof)","anio":"1968-70","linea":"Redline","min":5000,"max":25000,"fuente":"https://underpricedai.com/blog/hot-wheels-value-guide","fecha":"2026"},{"modelo":"Pink Olds 442","anio":1969,"linea":"Redline","min":4000,"max":10000,"fuente":"https://underpricedai.com/blog/hot-wheels-value-guide","fecha":"2026"},{"modelo":"Pink Mighty Maverick","anio":1970,"linea":"Redline","min":3000,"max":8000,"fuente":"https://underpricedai.com/blog/hot-wheels-value-guide","fecha":"2026"},{"modelo":"Beach Bomb (side-loader, pink)","anio":1969,"linea":"Redline","min":5000,"max":10000,"fuente":"https://howmuchisitworth.app/hot-wheels-redline","fecha":"2026"},{"modelo":"Beach Bomb (side-loader, común)","anio":1969,"linea":"Redline","min":200,"max":3500,"fuente":"https://yonkerstimes.com/the-ultimate-redline-hot-wheels-price-guide-by-year-1968-to-1977/","fecha":"2026"},{"modelo":"Custom Camaro (rose/pink)","anio":1968,"linea":"Redline","min":400,"max":1500,"fuente":"https://howmuchisitworth.app/hot-wheels-redline","fecha":"2026"},{"modelo":"Custom Camaro (común, played-with)","anio":1968,"linea":"Redline","min":150,"max":400,"fuente":"https://yonkerstimes.com/...","fecha":"2026"},{"modelo":"Silhouette","anio":1968,"linea":"Redline","min":50,"max":800,"fuente":"https://yonkerstimes.com/...","fecha":"2026"},{"modelo":"Red Baron / Beatnik Bandit / Heavy Chevy / Olds 442","anio":"1968-69","linea":"Redline","min":55.86,"max":3575.19,"fuente":"https://www.rarityfinder.com/blog/hot-wheels-redline-checklist-1968-1977","fecha":"2026-05-15","nota":"$55.86 raw / $160 PSA 9 / $3,575.19 PSA 10"},{"modelo":"'83 Chevy Silverado STH","anio":2024,"linea":"Super Treasure Hunt","min":250,"max":250,"fuente":"https://www.autoevolution.com/news/hot-wheels-super-treasure-hunt-prices-2025-vs-2024-253713.html","fecha":"2024"},{"modelo":"Mazda 787B STH","anio":2024,"linea":"Super Treasure Hunt","min":200,"max":200,"fuente":"autoevolution.com","fecha":"2024"},{"modelo":"'89 Mercedes-Benz 560 SEC AMG STH","anio":2024,"linea":"Super Treasure Hunt","min":150,"max":150,"fuente":"autoevolution.com","fecha":"2024"},{"modelo":"Lamborghini Huracán Super Trofeo STH","anio":2024,"linea":"Super Treasure Hunt","min":150,"max":150,"fuente":"autoevolution.com","fecha":"2024"},{"modelo":"Porsche 911 STH","anio":2025,"linea":"Super Treasure Hunt","min":100,"max":150,"fuente":"https://resellcalendar.com/news/feed/2025-hot-wheels-super-treasure-hunt-reseller/","fecha":"2025"},{"modelo":"BMW 507 STH / '71 El Camino STH","anio":2025,"linea":"Super Treasure Hunt","min":85,"max":85,"fuente":"resellcalendar.com","fecha":"2025"},{"modelo":"'87 Audi Quattro STH","anio":2025,"linea":"Super Treasure Hunt","min":20,"max":252,"fuente":"autoevolution.com","fecha":"2025"},{"modelo":"Mitsubishi Pajero Evolution STH","anio":2024,"linea":"Super Treasure Hunt","min":19.5,"max":19.5,"fuente":"autoevolution.com","fecha":"2024"},{"modelo":"Set completo STH 2025 (15 autos)","anio":2025,"linea":"Super Treasure Hunt","min":396,"max":2751,"fuente":"autoevolution.com","fecha":"2025"},{"modelo":"Set completo STH 2024 (15 autos)","anio":2024,"linea":"Super Treasure Hunt","min":446,"max":2240,"fuente":"autoevolution.com","fecha":"2024"},{"modelo":"'99 Honda Civic Type R (EK9) STH","anio":2022,"linea":"Super Treasure Hunt","min":270,"max":270,"fuente":"https://blog.hobbydb.com/2023/01/05/top-15-most-valuable-hot-wheels-models-from-2022/","fecha":"2022"},{"modelo":"Porsche 935 - Toy Fair","anio":2022,"linea":"Exclusivo","min":690,"max":690,"fuente":"blog.hobbydb.com","fecha":"2022"},{"modelo":"Twin Mill - Mobil 1 Sweepstakes","anio":2022,"linea":"Exclusivo","min":620,"max":620,"fuente":"blog.hobbydb.com","fecha":"2022"},{"modelo":"Automobili Pininfarina Battista - Hot Wheels iD","anio":2022,"linea":"Exclusivo","min":340,"max":340,"fuente":"blog.hobbydb.com","fecha":"2022"},{"modelo":"'69 Chevy Camaro - 36th Annual Convention","anio":2022,"linea":"Convention","min":140,"max":140,"fuente":"blog.hobbydb.com","fecha":"2022"},{"modelo":"Porsche 959 RLC (Gulf)","anio":2025,"linea":"RLC","min":84.99,"max":85,"fuente":"https://www.ebay.com/shop/hot-wheels-rlc-porsche","fecha":"2025"},{"modelo":"Porsche 959 RLC (Blue)","anio":2024,"linea":"RLC","min":37,"max":55,"fuente":"eBay","fecha":"2024-2025"},{"modelo":"Nissan Skyline GT-R (BNR34) RLC","anio":2024,"linea":"RLC","min":59.99,"max":59.99,"fuente":"https://99diecast.com/collections/red-line-club","fecha":"2024"},{"modelo":"1982 Lamborghini Countach LP 500 S RLC","anio":2025,"linea":"RLC","min":69.99,"max":84.99,"fuente":"99diecast.com","fecha":"2025"},{"modelo":"Honda Motocompo","anio":2025,"linea":"Mainline","min":2.99,"max":3.99,"fuente":"https://www.hobbydb.com/marketplaces/t-hunted/collectibles/67322553","fecha":"2025"},{"modelo":"Honda Civic Custom (Red)","anio":2024,"linea":"Mainline","min":2.0,"max":2.0,"fuente":"https://www.hobbydb.com/home/hotwheels","fecha":"2025"},{"modelo":"'67 Pontiac Firebird 400 (Red 5SPGY)","anio":2024,"linea":"Mainline","min":4.0,"max":4.0,"fuente":"hobbydb.com","fecha":"2025"},{"modelo":"1985 Chevrolet K5 Blazer","anio":2024,"linea":"Mainline","min":3.38,"max":3.38,"fuente":"hobbydb.com (estimated)","fecha":"2025"},{"modelo":"Custom 2020 Honda E","anio":2024,"linea":"Mainline","min":3.88,"max":3.88,"fuente":"hobbydb.com (estimated)","fecha":"2025"}],"tiempo_de_venta":[{"rango":"$0.50 - $3","tiempo":"semanas a meses individual; días en lotes","canal":"Lotes en eBay o Facebook Marketplace","fuente":"reddit.com/r/HotWheels"},{"rango":"$3 - $15","tiempo":"1-4 semanas","canal":"eBay Buy It Now","fuente":"resellcalendar.com"},{"rango":"$15 - $50","tiempo":"1-2 semanas","canal":"eBay subasta o BIN","fuente":"autoevolution.com"},{"rango":"$50 - $200","tiempo":"1-4 semanas","canal":"eBay subasta","fuente":"blog.hobbydb.com"},{"rango":"$200 - $1,000","tiempo":"1-6 meses","canal":"eBay subasta / casas de subastas","fuente":"underpricedai.com"},{"rango":"$1,000+","tiempo":"meses a años","canal":"Casas de subastas especializadas","fuente":"icollecteverything.com"}],"comisiones":[{"canal":"eBay","vendedor":"13.25% + $0.40","neto_sobre_50":42.98,"fuente":"https://www.ebay.com/sellercenter/selling/seller-fees"},{"canal":"Mercari","vendedor":"10%","neto_sobre_50":45.0,"fuente":"https://www.mercari.com/us/help_center/article/169/"},{"canal":"Whatnot","vendedor":"8% + 2.9% + $0.30","neto_sobre_50":44.6,"fuente":"https://fluf.io/crosslisting/mercari-to-whatnot/"},{"canal":"Facebook Marketplace","vendedor":"0%","neto_sobre_50":50.0,"fuente":"https://www.facebook.com/marketplace"},{"canal":"Etsy","vendedor":"6.5% + fees de pago","neto_sobre_50":45.0,"fuente":"https://www.etsy.com"},{"canal":"hobbyDB","vendedor":"0%","neto_sobre_50":50.0,"fuente":"https://www.hobbydb.com/home/hotwheels"}],"descuento_por_lote":[{"tipo":"Pieza por pieza","descuento":"0%","fuente":"reddit.com/r/HotWheels"},{"tipo":"Lote pequeño (2-6)","descuento":"10-20%","fuente":"youtube.com"},{"tipo":"Lote mediano (20-50)","descuento":"30-50%","fuente":"reddit.com/r/HotWheels"},{"tipo":"Colección completa (100+)","descuento":"50-70%","fuente":"reddit.com/r/HotWheels"},{"tipo":"Venta a revendedor","descuento":"50-70%","fuente":"reddit.com/r/HotWheels"}]}, OWNED_DEMO={"meta":{"usuario":"(tu nombre)","moneda":"USD","actualizado":"2026-10-11","demo":true,"nota":"Este archivo es una PLANTILLA con datos de EJEMPLO. Reemplaza 'items' con tu colección real (o cárgala desde la app). 'catalog_id' debe coincidir con un id de data/catalog.json."},"items":[{"catalog_id":"2025-HYW18","cantidad":2,"condicion":"carded-nuevo","precio_compra":null,"ubicacion":"Caja A","notas":"EJEMPLO — reemplazar por tu colección real","foto_propia":null},{"catalog_id":"2025-HYW34","cantidad":1,"condicion":"carded-nuevo","precio_compra":null,"ubicacion":"Caja A","notas":"EJEMPLO — reemplazar por tu colección real","foto_propia":null},{"catalog_id":"2025-HYY72","cantidad":1,"condicion":"carded-nuevo","precio_compra":null,"ubicacion":"Caja A","notas":"EJEMPLO — reemplazar por tu colección real","foto_propia":null},{"catalog_id":"2024-HRY51","cantidad":1,"condicion":"carded-nuevo","precio_compra":null,"ubicacion":"Caja A","notas":"EJEMPLO — reemplazar por tu colección real","foto_propia":null},{"catalog_id":"2024-HTB08","cantidad":2,"condicion":"carded-nuevo","precio_compra":null,"ubicacion":"Caja A","notas":"EJEMPLO — reemplazar por tu colección real","foto_propia":null},{"catalog_id":"2025-HYW86","cantidad":1,"condicion":"carded-nuevo","precio_compra":null,"ubicacion":"Caja A","notas":"EJEMPLO — reemplazar por tu colección real","foto_propia":null},{"catalog_id":"2024-HTC73","cantidad":1,"condicion":"carded-nuevo","precio_compra":null,"ubicacion":"Caja A","notas":"EJEMPLO — reemplazar por tu colección real","foto_propia":null},{"catalog_id":"2026-JJJ14","cantidad":1,"condicion":"carded-nuevo","precio_compra":null,"ubicacion":"Caja A","notas":"EJEMPLO — reemplazar por tu colección real","foto_propia":null},{"catalog_id":"2025-HYW72","cantidad":1,"condicion":"carded-nuevo","precio_compra":null,"ubicacion":"Caja A","notas":"EJEMPLO — reemplazar por tu colección real","foto_propia":null}]}, MKT={"meta":{"generado":"2026-10-11","moneda_base":"USD","nota":"Todos los precios del catálogo están en USD y se convierten con estos tipos. El tipo EUR/USD y GBP/USD son tipos de cambio reales; EUR/CLP y GBP/CLP son TIPOS CRUZADOS calculados (no cotización directa).","advertencia":"Los tipos de cambio y las comisiones cambian. Refrescar antes de decidir una venta.","canales_nota":"pct = comisión sobre el precio de venta; fijo_usd = cargo fijo por orden convertido a USD con el tipo de cambio cargado; extra_pct = cargo adicional (p. ej. conversión de moneda)."},"monedas":{"USD":{"nombre":"Dólar estadounidense","simbolo":"US$","por_usd":1.0,"decimales":2,"sep_dec":".","sep_mil":",","fuente":"moneda base","fecha":"2026-10-11"},"CLP":{"nombre":"Peso chileno","simbolo":"$","por_usd":981.61,"decimales":0,"sep_dec":",","sep_mil":".","fuente":"mindicador.cl /api/dolar (dólar observado)","fecha":"2026-10-09"},"EUR":{"nombre":"Euro","simbolo":"€","por_usd":1.1344,"decimales":2,"sep_dec":",","sep_mil":".","fuente":"exchangerate-api.com EUR/USD 0,88152 — tipo cruzado para CLP","fecha":"2026-09-30"},"GBP":{"nombre":"Libra esterlina","simbolo":"£","por_usd":1.32282,"decimales":2,"sep_dec":".","sep_mil":",","fuente":"exchangerate-api.com GBP/USD 0,755961","fecha":"2026-09-30"}},"mercados":[{"id":"CL","nombre":"Chile","moneda":"CLP","bandera":"CL","retail":[{"item":"Auto básico (mainline)","precio_local":1990,"usd":2.03,"fuente":"littletoys.cl","fecha":"2026"},{"item":"Auto básico (mainline)","precio_local":2450,"usd":2.5,"fuente":"isatoyschile.cl","fecha":"2026"},{"item":"Pack 5 autos mainline","precio_local":9990,"usd":10.18,"fuente":"littletoys.cl / Lider.cl","fecha":"2026"},{"item":"Pack 5 autos (Rosso)","precio_local":10990,"usd":11.2,"fuente":"super.lider.cl","fecha":"2026"},{"item":"Car Culture / Auto Cultura Automotriz","precio_local":6290,"usd":6.41,"fuente":"super.lider.cl","fecha":"2026"},{"item":"Boulevard","precio_local":7990,"usd":8.14,"fuente":"super.lider.cl","fecha":"2026"},{"item":"Racing Club (colección)","precio_local":7990,"usd":8.14,"fuente":"isatoyschile.cl","fecha":"2026"},{"item":"Collector Fast & Furious (Datsun)","precio_local":10990,"usd":11.2,"fuente":"isatoyschile.cl","fecha":"2026"},{"item":"Premium Collector (Barbie GMC Panel Van)","precio_local":12990,"usd":13.23,"fuente":"isatoyschile.cl","fecha":"2026"},{"item":"Character Cars (Mario Kart)","precio_local":13990,"usd":14.25,"fuente":"autofact.cl / MercadoLibre","fecha":"2026"},{"item":"Character Cars (Minions)","precio_local":19800,"usd":20.17,"fuente":"autofact.cl / MercadoLibre","fecha":"2026"},{"item":"Collector Premium transportador","precio_local":19990,"usd":20.36,"fuente":"super.lider.cl","fecha":"2026"}],"canales":[{"canal":"MercadoLibre Chile — Clásica","comision":"8%–17% según categoría","fijo":"~$700 hasta $9.990 · ~$1.000 entre $9.990 y $19.990 (referencial)","envio":"$800–$1.000 (≤0,3 kg, reputación verde) · $3.050 desde $19.990","extra":"IVA 19% sobre la comisión · cuotas sin interés 3%–10% si las ofrecés · envío gratis obligatorio sobre $19.990","fuente":"mercadolibre.cl/ayuda/Costos-de-vender-un-producto_870 · profitar.app/cl · mercadoru.com","verificado":"parcial"},{"canal":"MercadoLibre Chile — Premium","comision":"11%–21% según categoría","fijo":"igual criterio","envio":"igual criterio","fuente":"mercadolibre.cl/ayuda","verificado":"si"},{"canal":"Facebook Marketplace / grupos de coleccionistas","comision":"0%","fijo":"—","envio":"a convenir (retiro en persona o courier)","fuente":"facebook.com/marketplace","verificado":"si"},{"canal":"Feria / persa presencial","comision":"0%","fijo":"—","envio":"—","fuente":"práctica local","verificado":"no"}],"importacion":{"regla":"Hasta US$500: SOLO IVA 19% (sin arancel). Sobre US$500: 6% de arancel + 19% de IVA sobre el valor CIF. Envíos entre personas naturales (C2C) de hasta US$500 son exentos de IVA y derechos si son ocasionales y no comerciales.","iva":0.19,"arancel_sobre":0.06,"umbral_arancel":500,"exencion_c2c":500,"fuente":"aduana.cl (Ley N°21.713, vigente 25-oct-2025) · sii.cl · FedEx regulatory alert","verificado":"si"}},{"id":"US","nombre":"Estados Unidos","moneda":"USD","bandera":"US","retail":[{"item":"Auto básico (mainline)","precio_local":1.25,"usd":1.25,"fuente":"eathealthy365 (precio histórico ~$1)","fecha":"2026"},{"item":"Premium / Car Culture (unidad)","precio_local":6.95,"usd":6.95,"fuente":"eBay listings","fecha":"2024-2025"},{"item":"Premium (set de 5)","precio_local":29.95,"usd":29.95,"fuente":"eBay listings","fecha":"2024"},{"item":"Super Treasure Hunt (reventa)","precio_local":85,"usd":85,"fuente":"resellcalendar / autoevolution","fecha":"2025"}],"canales":[{"canal":"eBay (vendedor particular/business)","comision":"13,25% + US$0,40","envio":"a cargo del vendedor o del comprador","fuente":"ebay.com/sellercenter/selling/seller-fees","verificado":"si"},{"canal":"Mercari","comision":"10%","fuente":"mercari.com help center","verificado":"si"},{"canal":"Whatnot (subasta en vivo)","comision":"8% + 2,9% + US$0,30","fuente":"fluf.io","verificado":"si"},{"canal":"Facebook Marketplace","comision":"0%","fuente":"facebook.com/marketplace","verificado":"si"},{"canal":"hobbyDB marketplace","comision":"0%","fuente":"hobbydb.com","verificado":"si"}],"importacion":{"regla":"De minimis histórico de US$800 para arancel; el sales tax estatal puede aplicar según el estado.","fuente":"no verificado en esta investigación","verificado":"no"}},{"id":"EU","nombre":"Europa (eBay DE/UK)","moneda":"EUR","bandera":"EU","retail":[{"item":"Auto básico (mainline)","precio_local":2.0,"usd":2.27,"fuente":"eathealthy365 (mainline ≈€2-3 en Europa)","fecha":"2026"},{"item":"Auto básico (mainline)","precio_local":3.0,"usd":3.4,"fuente":"eathealthy365","fecha":"2026"},{"item":"Convention Porsche 911 GT3 RS (listado)","precio_local":80.36,"usd":91.16,"fuente":"ebay.de","fecha":"2026"},{"item":"Listado colección (promedio de 96 avisos)","precio_local":42.57,"usd":48.29,"fuente":"for-sale.ie","fecha":"2026"}],"canales":[{"canal":"eBay DE/UE — vendedor business, categoría Collectables","comision":"10,9% + cargo por orden (€/£0,30–0,40)","fuente":"ebay.co.uk/help/selling (Fees for business sellers)","verificado":"si"},{"canal":"eBay UK — vendedor particular","comision":"0% desde oct-2024 (excepto Motors); conversión de moneda 2,5% (2,75% desde 1-dic-2026)","fuente":"ebay.co.uk/help/selling (Fees for private sellers)","verificado":"si"},{"canal":"eBay UK — vendedor business","comision":"12,8% + £0,30 (y £0,40 en órdenes > £10 desde 12-feb-2026) + Regulatory Operating Fee 0,35%","fuente":"ebay.co.uk/sellercentre/news/2026-january/rate-card-change","verificado":"si"}],"importacion":{"regla":"Desde el 1-jul-2026 se eliminó la exención de arancel de €150: se aplica un ARANCEL FIJO TEMPORAL DE €3 POR ÍTEM en envíos de hasta €150 (hasta el 1-jul-2028). El IVA de importación se aplica a TODOS los bienes sin importar el valor (desde 2021); con IOSS el IVA se cobra en la compra y la importación queda exenta de IVA. Tipos de IVA típicos: 19%–21%.","iva":"19%–21% según país","arancel_fijo":3,"umbral":150,"fuente":"taxation-customs.ec.europa.eu (Council Regulation (EU) 2026/382) · zoll.de","verificado":"si"}},{"id":"UK","nombre":"Reino Unido","moneda":"GBP","bandera":"UK","retail":[{"item":"Auto suelto (listados eBay UK)","precio_local":4.92,"usd":6.51,"fuente":"ebay.co.uk","fecha":"2026"},{"item":"Super Treasure Hunt 2026 Pontiac Firebird","precio_local":38.82,"usd":51.35,"fuente":"ebay.co.uk","fecha":"2026"},{"item":"Premium set de 5 (2026 Aero Style)","precio_local":31.58,"usd":41.77,"fuente":"ebay.co.uk","fecha":"2026"},{"item":"Lote 30 autos (joblot)","precio_local":35.7,"usd":47.22,"fuente":"ebay.co.uk","fecha":"2026","por_auto":1.57},{"item":"Lote 50 autos (clearance joblot)","precio_local":85.0,"usd":112.44,"fuente":"ebay.co.uk","fecha":"2026","por_auto":2.25},{"item":"Redline suelto común (compra → venta)","precio_local":10.0,"usd":13.23,"fuente":"listingmonster.ai (sourced £2-8, sold £10-40)","fecha":"2026"}],"canales":[{"canal":"eBay UK — particular","comision":"0% + conversión 2,5%","fuente":"ebay.co.uk/help/selling (private sellers)","verificado":"si"},{"canal":"eBay UK — business","comision":"12,8% + £0,30/£0,40","fuente":"ebay.co.uk","verificado":"si"}],"importacion":{"regla":"El IVA de importación (20%) aplica a bienes importados; el umbral de £135 rige para el tratamiento del IVA en ventas a distancia.","fuente":"no verificado en esta investigación","verificado":"no"}}],"comparacion_clase":[{"clase":"Mainline (auto suelto)","US":["US$1,25 retail","US$1–5 reventa carded"],"CL":["$1.990–$2.450 retail"],"EU":["€2–€3 retail"],"UK":["£4,92 listado típico"],"lectura":"Chile está ~1,6–2× sobre el precio de EE.UU.; Europa ~1,8–2,7×."},{"clase":"Premium / Car Culture","US":["US$6,95–12,50 unidad","US$29,95–64,99 set de 5"],"CL":["$6.290–$12.990 unidad"],"EU":["~€8–15 unidad"],"UK":["£31,58 set de 5 (≈US$41,8)"],"lectura":"El set de 5 europeo se paga cerca del techo del rango estadounidense."},{"clase":"Treasure Hunt","US":["US$5–20 carded"],"CL":["poco frecuente en retail local"],"EU":["aparece en eBay DE/UK"],"UK":["£38,82 un STH 2026 (≈US$51)"],"lectura":"El coleccionista europeo paga más por STH que el estadounidense medio."},{"clase":"Super Treasure Hunt","US":["US$85–250"],"CL":["importación o mercado secundario"],"EU":["€80–200 en eBay DE"],"UK":["£38,82–£85"],"lectura":"El mejor precio de venta para STH está en EE.UU.; Europa es el segundo mercado."},{"clase":"Lotes (joblot)","US":["US$0,50–3 por auto"],"CL":["$1.990 por auto nuevo"],"EU":["~€2–3 por auto"],"UK":["£1,19–£1,70 por auto (lotes de 30 y 50)"],"lectura":"En el Reino Unido los lotes se pagan mejor por unidad que en EE.UU.: es el mejor destino para vender volumen."}],"por_que_difieren":[{"factor":"Aranceles e impuestos","efecto":"El IVA (19% en Chile, 19–21% en la UE, 20% en el Reino Unido) se suma al precio final.","fuente":"aduana.cl / taxation-customs.ec.europa.eu"},{"factor":"Logística y envío","efecto":"El costo de mover el producto desde Asia hacia mercados lejanos encarece el precio.","fuente":"eathealthy365"},{"factor":"Tipo de cambio","efecto":"El precio local depende del dólar y de la paridad; hoy 1 USD = $981,61 CLP.","fuente":"mindicador.cl"},{"factor":"Margen del retail local","efecto":"Cada eslabón de la cadena agrega margen: un auto de US$1,25 se vende a $1.990–$2.450 en Chile.","fuente":"eathealthy365 + littletoys.cl"},{"factor":"Oferta y demanda local","efecto":"Lo que en EE.UU. es basura de estantería, en Chile puede no llegar nunca: la escasez local sube el precio.","fuente":"análisis propio a partir de los precios observados"}],"calculadora_canales":[{"mercado":"US","moneda":"USD","canal":"eBay EE.UU.","pct":0.1325,"fijo_usd":0.4,"tiempo_dias":[7,28],"fuente":"ebay.com/sellercenter/selling/seller-fees"},{"mercado":"US","moneda":"USD","canal":"Mercari","pct":0.1,"fijo_usd":0.0,"tiempo_dias":[7,21],"fuente":"mercari.com help center"},{"mercado":"US","moneda":"USD","canal":"Whatnot (en vivo)","pct":0.109,"fijo_usd":0.3,"tiempo_dias":[0,1],"fuente":"fluf.io"},{"mercado":"US","moneda":"USD","canal":"Facebook Marketplace","pct":0.0,"fijo_usd":0.0,"tiempo_dias":[7,21],"fuente":"facebook.com/marketplace"},{"mercado":"CL","moneda":"CLP","canal":"MercadoLibre Chile (Clásica ~12,5%)","pct":0.125,"fijo_usd":0.713,"tiempo_dias":[7,30],"fuente":"mercadolibre.cl/ayuda + profitar.app/cl"},{"mercado":"CL","moneda":"CLP","canal":"MercadoLibre Chile (Premium ~16%)","pct":0.16,"fijo_usd":0.713,"tiempo_dias":[7,30],"fuente":"mercadolibre.cl/ayuda"},{"mercado":"CL","moneda":"CLP","canal":"Facebook Marketplace Chile","pct":0.0,"fijo_usd":0.0,"tiempo_dias":[7,21],"fuente":"facebook.com/marketplace"},{"mercado":"CL","moneda":"CLP","canal":"Feria / persa (presencial)","pct":0.0,"fijo_usd":0.0,"tiempo_dias":[1,1],"fuente":"práctica local"},{"mercado":"UK","moneda":"GBP","canal":"eBay UK — particular","pct":0.0,"fijo_usd":0.0,"extra_pct":0.025,"tiempo_dias":[7,28],"fuente":"ebay.co.uk/help/selling (private sellers)"},{"mercado":"UK","moneda":"GBP","canal":"eBay UK — business (Collectables 10,9%)","pct":0.109,"fijo_usd":0.529,"tiempo_dias":[7,28],"fuente":"ebay.co.uk/help/selling (business sellers)"},{"mercado":"EU","moneda":"EUR","canal":"eBay DE — business (Collectables 10,9%)","pct":0.109,"fijo_usd":0.34,"tiempo_dias":[7,28],"fuente":"ebay.co.uk/help/selling (business sellers)"},{"mercado":"EU","moneda":"EUR","canal":"Catawiki / subasta especializada","pct":0.12,"fijo_usd":0.0,"tiempo_dias":[14,45],"fuente":"no verificado — comisión de referencia"}]}, SEG={"meta":{"actualizado":"2026-10-12","motor":"build/refresh_market.py","nota":"Estado de seguimiento por auto. Los valores son referenciales por clase hasta que el motor cargue comparables del modelo exacto. El historial crece en cada actualización.","frescura_dias":{"fresco":7,"aceptable":30}},"items":{"2025-HYW18":{"modelo":"Mazda MX-5 Miata","anio":2025,"clase":"Mainline","cantidad":2,"valor_actual_usd":3.0,"valor_anterior_usd":null,"fecha_actualizacion":"2026-10-11","fuente":"rango por clase (referencia)","confianza":"baja","frescura":"fresco","historial":[{"fecha":"2026-10-11","usd":3.0,"fuente":"rango por clase"}],"senales":{"demanda_coleccionistas_rank":null,"precio_chile_clp":null,"ebay_usd":null,"mercadolibre_clp":null},"alertas":{"precio_objetivo_usd":7.5,"cambio_pct":20,"canal_preferido":"MercadoLibre Chile"}},"2025-HYW34":{"modelo":"Ferrari SF90 Stradale","anio":2025,"clase":"Mainline","cantidad":1,"valor_actual_usd":3.0,"valor_anterior_usd":null,"fecha_actualizacion":"2026-10-11","fuente":"rango por clase (referencia)","confianza":"baja","frescura":"fresco","historial":[{"fecha":"2026-10-11","usd":3.0,"fuente":"rango por clase"}],"senales":{"demanda_coleccionistas_rank":1,"precio_chile_clp":null,"ebay_usd":null,"mercadolibre_clp":null},"alertas":{"precio_objetivo_usd":7.5,"cambio_pct":20,"canal_preferido":"MercadoLibre Chile"}},"2025-HYY72":{"modelo":"Nissan Skyline GT-R (BNR32)","anio":2025,"clase":"Mainline","cantidad":1,"valor_actual_usd":3.0,"valor_anterior_usd":null,"fecha_actualizacion":"2026-10-11","fuente":"rango por clase (referencia)","confianza":"baja","frescura":"fresco","historial":[{"fecha":"2026-10-11","usd":3.0,"fuente":"rango por clase"}],"senales":{"demanda_coleccionistas_rank":null,"precio_chile_clp":null,"ebay_usd":null,"mercadolibre_clp":null},"alertas":{"precio_objetivo_usd":7.5,"cambio_pct":20,"canal_preferido":"MercadoLibre Chile"}},"2024-HRY51":{"modelo":"Mazda Autozam","anio":2024,"clase":"Mainline","cantidad":1,"valor_actual_usd":3.0,"valor_anterior_usd":null,"fecha_actualizacion":"2026-10-11","fuente":"rango por clase (referencia)","confianza":"baja","frescura":"fresco","historial":[{"fecha":"2026-10-11","usd":3.0,"fuente":"rango por clase"}],"senales":{"demanda_coleccionistas_rank":null,"precio_chile_clp":null,"ebay_usd":null,"mercadolibre_clp":null},"alertas":{"precio_objetivo_usd":7.5,"cambio_pct":20,"canal_preferido":"MercadoLibre Chile"}},"2024-HTB08":{"modelo":"'96 Nissan 180SX Type X","anio":2024,"clase":"STH","cantidad":2,"valor_actual_usd":167.5,"valor_anterior_usd":null,"fecha_actualizacion":"2026-10-11","fuente":"rango por clase (referencia)","confianza":"baja","frescura":"fresco","historial":[{"fecha":"2026-10-11","usd":167.5,"fuente":"rango por clase"}],"senales":{"demanda_coleccionistas_rank":null,"precio_chile_clp":null,"ebay_usd":null,"mercadolibre_clp":null},"alertas":{"precio_objetivo_usd":375.0,"cambio_pct":20,"canal_preferido":"MercadoLibre Chile"}},"2025-HYW86":{"modelo":"Tesla Model S Plaid","anio":2025,"clase":"Mainline","cantidad":1,"valor_actual_usd":3.0,"valor_anterior_usd":null,"fecha_actualizacion":"2026-10-11","fuente":"rango por clase (referencia)","confianza":"baja","frescura":"fresco","historial":[{"fecha":"2026-10-11","usd":3.0,"fuente":"rango por clase"}],"senales":{"demanda_coleccionistas_rank":null,"precio_chile_clp":null,"ebay_usd":null,"mercadolibre_clp":null},"alertas":{"precio_objetivo_usd":7.5,"cambio_pct":20,"canal_preferido":"MercadoLibre Chile"}},"2024-HTC73":{"modelo":"'83 Chevy Silverado","anio":2024,"clase":"STH","cantidad":1,"valor_actual_usd":167.5,"valor_anterior_usd":null,"fecha_actualizacion":"2026-10-11","fuente":"rango por clase (referencia)","confianza":"baja","frescura":"fresco","historial":[{"fecha":"2026-10-11","usd":167.5,"fuente":"rango por clase"}],"senales":{"demanda_coleccionistas_rank":null,"precio_chile_clp":null,"ebay_usd":null,"mercadolibre_clp":null},"alertas":{"precio_objetivo_usd":375.0,"cambio_pct":20,"canal_preferido":"MercadoLibre Chile"}},"2026-JJJ14":{"modelo":"Ford Mustang GTD","anio":2026,"clase":"STH","cantidad":1,"valor_actual_usd":167.5,"valor_anterior_usd":null,"fecha_actualizacion":"2026-10-11","fuente":"rango por clase (referencia)","confianza":"baja","frescura":"fresco","historial":[{"fecha":"2026-10-11","usd":167.5,"fuente":"rango por clase"}],"senales":{"demanda_coleccionistas_rank":3,"precio_chile_clp":null,"ebay_usd":null,"mercadolibre_clp":null},"alertas":{"precio_objetivo_usd":375.0,"cambio_pct":20,"canal_preferido":"MercadoLibre Chile"}},"2025-HYW72":{"modelo":"'87 Audi quattro","anio":2025,"clase":"STH","cantidad":1,"valor_actual_usd":167.5,"valor_anterior_usd":null,"fecha_actualizacion":"2026-10-11","fuente":"rango por clase (referencia)","confianza":"baja","frescura":"fresco","historial":[{"fecha":"2026-10-11","usd":167.5,"fuente":"rango por clase"}],"senales":{"demanda_coleccionistas_rank":null,"precio_chile_clp":null,"ebay_usd":null,"mercadolibre_clp":null},"alertas":{"precio_objetivo_usd":375.0,"cambio_pct":20,"canal_preferido":"MercadoLibre Chile"}}}}, TEND={"meta":{"generado":"2026-10-11","moneda_base":"USD","tipo_cambio_clp":981.61,"nota":"Señales de demanda y precios observados en el mercado real. Cada fila lleva fuente y fecha. Los rankings de coleccionistas NO son precios de mercado secundario."},"demanda_coleccionistas":{"fuente":"HW Price Guide (hwpriceguide.com) — datos reales de tracking de coleccionistas","metodologia":"Cuenta cuántos coleccionistas agregaron cada casting a su colección durante el mes. NO refleja precio de mercado secundario.","url":"https://hwpriceguide.com/article/top-20-most-collected-2026-hot-wheels-mainlines-february-2026/","enero_2026":[{"rank":1,"modelo":"Ferrari SF90 Stradale","grupo":"2026 Mainline","categoria":"Mainline","coleccionistas":135,"catalogo_ids":["2025-HYW34","2025-HYY08","2026-JJJ12","2026-JJK89"]},{"rank":2,"modelo":"'87 Buick Regal GNX","grupo":"2026 Treasure Hunts","categoria":"Treasure Hunt","coleccionistas":107,"catalogo_ids":["2021-GTB43","2021-GTD44","2026-JJM00"]},{"rank":3,"modelo":"Ferrari F40 Competizione","grupo":"2026 Super Treasure Hunts","categoria":"Super Treasure Hunt","coleccionistas":57,"catalogo_ids":["2025-HYW59","2025-JBB92"]},{"rank":4,"modelo":"Ferrari 250 GTO & Fiat 642 RN2 Bartoletti Transporter","grupo":"2025 Car Culture Team Transport","categoria":"Car Culture Team Transport","coleccionistas":57,"catalogo_ids":[]},{"rank":5,"modelo":"1997 Toyota Supra","grupo":"2025 Red Line Club","categoria":"Red Line Club","coleccionistas":52,"catalogo_ids":["2022-HCV16","2023-HKG62","2023-HKG87","2023-HKL08","2024-HTB09","2024-HTF27","2026-JJK28","2026-JJK51","2026-JJM25"]},{"rank":6,"modelo":"Toyota Supra","grupo":"7-Eleven","categoria":"Silver Series","coleccionistas":50,"catalogo_ids":["2022-HCV16","2023-HKG62","2023-HKG87","2023-HKL08","2024-HTB09","2024-HTF27","2026-JJK28","2026-JJK51","2026-JJM25"]},{"rank":7,"modelo":"1967 Ferrari 330 P4","grupo":"Elite 64","categoria":"Elite 64","coleccionistas":49,"catalogo_ids":[]},{"rank":8,"modelo":"Ferrari F50","grupo":"2025 Timeless Icons","categoria":"Car Culture","coleccionistas":41,"catalogo_ids":[]},{"rank":9,"modelo":"1995 Mitsubishi Eclipse","grupo":"2026 Fast & Furious Premium","categoria":"Fast & Furious Premium","coleccionistas":40,"catalogo_ids":[]},{"rank":10,"modelo":"LaFerrari","grupo":"2025 Eurospeed","categoria":"Car Culture","coleccionistas":39,"catalogo_ids":[]}],"febrero_2026":[{"rank":1,"modelo":"Ferrari SF90 Stradale","coleccionistas":263,"grupo":"2026 Mainline","categoria":"Mainline","catalogo_ids":["2025-HYW34","2025-HYY08","2026-JJJ12","2026-JJK89"]},{"rank":2,"modelo":"83 Chevy Silverado Black Widow","coleccionistas":211,"grupo":"2026 Mainline","categoria":"Mainline","catalogo_ids":["2016-DHR93","2017-DTX78","2020-GHD76","2024-HTC67"]},{"rank":3,"modelo":"Ford Mustang GTD","coleccionistas":164,"grupo":"2026 Mainline","categoria":"Mainline","catalogo_ids":["2016-DHN93","2018-FJW44","2019-FYC31","2020-GHC22","2025-HYW19","2025-JBB93","2026-JJJ14","2026-JJM16"]},{"rank":4,"modelo":"Ferrari F40 Competizione","coleccionistas":162,"grupo":"2026 Mainline","categoria":"Mainline","catalogo_ids":["2025-HYW59","2025-JBB92"]},{"rank":5,"modelo":"Ferrari 365 GTB4 Competizione","coleccionistas":144,"grupo":"2026 Mainline","categoria":"Mainline","catalogo_ids":["2025-HYW48","2025-JBC19"]},{"rank":6,"modelo":"Porsche 911 Carrera T Arctic Grey","coleccionistas":131,"grupo":"2026 Mainline","categoria":"Mainline","catalogo_ids":["2026-JJH33"]},{"rank":7,"modelo":"Datsun 240Z","coleccionistas":130,"grupo":"2026 Mainline","categoria":"Mainline","catalogo_ids":["2017-DTW89","2018-FJX64"]},{"rank":8,"modelo":"Pass n Go","coleccionistas":125,"grupo":"2026 Mainline","categoria":"Mainline","catalogo_ids":[]},{"rank":9,"modelo":"La Liebre","coleccionistas":119,"grupo":"2026 Mainline","categoria":"Mainline","catalogo_ids":["2026-JJH36","2026-JJK77"]},{"rank":10,"modelo":"Optimus Prime Red","coleccionistas":114,"grupo":"2026 Mainline","categoria":"Mainline","catalogo_ids":["2026-JJJ00"]},{"rank":11,"modelo":"Ferrari 12Cilindri","coleccionistas":111,"grupo":"2026 Mainline","categoria":"Mainline","catalogo_ids":[]},{"rank":12,"modelo":"17 Audi RS 6 Avant Yellow","coleccionistas":109,"grupo":"2026 Mainline","categoria":"Mainline","catalogo_ids":[]},{"rank":13,"modelo":"Porsche 911 Turbo Cabriolet","coleccionistas":108,"grupo":"2026 Mainline","categoria":"Mainline","catalogo_ids":["2025-HYW37"]},{"rank":14,"modelo":"McLaren Formula 1 Team","coleccionistas":102,"grupo":"2026 Mainline","categoria":"Mainline","catalogo_ids":["2026-JJH95"]},{"rank":15,"modelo":"Pagani Zonda Cinque","coleccionistas":101,"grupo":"2026 Mainline","categoria":"Mainline","catalogo_ids":["2026-JJH34","2026-JJK75","2026-JJM32"]},{"rank":16,"modelo":"67 Camaro Metalflake Gold","coleccionistas":98,"grupo":"2026 Mainline","categoria":"Mainline","catalogo_ids":[]},{"rank":17,"modelo":"Bugatti Bolide","coleccionistas":97,"grupo":"2026 Mainline","categoria":"Mainline","catalogo_ids":["2023-HKG64","2024-HTC22","2024-HTF08"]},{"rank":18,"modelo":"16 Lamborghini Centenario Roadster Yellow","coleccionistas":95,"grupo":"2026 Mainline","categoria":"Mainline","catalogo_ids":[]},{"rank":19,"modelo":"70 Dodge Hemi Challenger","coleccionistas":86,"grupo":"2026 Mainline","categoria":"Mainline","catalogo_ids":["2025-HYY96","2026-JJJ07","2026-JJK79","2026-JJM38"]},{"rank":20,"modelo":"HW KITT Concept","coleccionistas":84,"grupo":"2026 Mainline","categoria":"Mainline","catalogo_ids":[]}]},"precios_chile":{"fuente":"minidiecast.cl — tienda especializada chilena (Hot Wheels Premium / STH / RLC)","url":"https://www.minidiecast.cl/hot-wheels-premium","moneda":"CLP","fecha_dato":"2026-10-11","nota":"Precios de LISTA de una tienda chilena especializada (asking), no ventas cerradas. En Chile el STH se paga entre $15.000 y $100.000 CLP según el casting.","items":[{"modelo":"HW STH Riley & Scott MK III","linea":"Super Treasure Hunt","clp":15000,"usd":15.28},{"modelo":"HW STH 1968 Cougar","linea":"Super Treasure Hunt","clp":20000,"usd":20.37},{"modelo":"HW STH 1957 Chevy","linea":"Super Treasure Hunt","clp":25000,"usd":25.47},{"modelo":"HW STH 1970 Plymouth Barracuda","linea":"Super Treasure Hunt","clp":30000,"usd":30.56},{"modelo":"HW 2011 Super Treasure Hunt '68 Olds","linea":"Super Treasure Hunt","clp":35000,"usd":35.66},{"modelo":"Hot Wheels 2012 Stockcar Series","linea":"Premium","clp":40000,"usd":40.75},{"modelo":"Hot Wheels STH Chaparral 2","linea":"Super Treasure Hunt","clp":40000,"usd":40.75},{"modelo":"HW STH 1971 Buick Riviera Real Riders","linea":"Super Treasure Hunt","clp":40000,"usd":40.75},{"modelo":"HW STH Dodge Challenger Funny Car","linea":"Super Treasure Hunt","clp":40000,"usd":40.75},{"modelo":"Hot Wheels 2011 Real Riders Tail","linea":"Real Riders","clp":45000,"usd":45.84},{"modelo":"HW STH 1971 Mustang Mach 1","linea":"Super Treasure Hunt","clp":45000,"usd":45.84},{"modelo":"HW 09 Corvette ZR1 Super Treasure Hunt","linea":"Super Treasure Hunt","clp":50000,"usd":50.94},{"modelo":"HW 2009 RLC Large And In Charger","linea":"Red Line Club","clp":50000,"usd":50.94},{"modelo":"HW 2006 6th Nationals Olds 442 Gold","linea":"Convention","clp":60000,"usd":61.12},{"modelo":"HW 18th Annual CC Custom Mustang","linea":"Convention","clp":70000,"usd":71.31},{"modelo":"HW Neo Classic Shelby Cobra 427 SC","linea":"Premium","clp":80000,"usd":81.5},{"modelo":"HW STH '70 Plymouth Superbird","linea":"Super Treasure Hunt","clp":100000,"usd":101.87},{"modelo":"HW 9th Nationals '65 Mustang Fastback","linea":"Convention","clp":120000,"usd":122.25},{"modelo":"Hot Wheels 1:64 Set 5 autos Car Culture","linea":"Car Culture (set 5)","clp":47000,"usd":47.88},{"modelo":"Hot Wheels Premium 1:64 Car Culture","linea":"Car Culture","clp":40000,"usd":40.75},{"modelo":"Hot Wheels 1:64 Car Cultures 2023","linea":"Car Culture (set 5)","clp":49000,"usd":49.92},{"modelo":"Hot Wheels 1:64 Fast & Furious Premium","linea":"Fast & Furious Premium","clp":40000,"usd":40.75},{"modelo":"Hot Wheels 1:64 Car Culture 2024","linea":"Car Culture (set 5)","clp":46000,"usd":46.86},{"modelo":"Hot Wheels 1:64 Fast & Furious Premium 2025","linea":"Fast & Furious Premium","clp":55000,"usd":56.03},{"modelo":"Hot Wheels 1:64 Car Culture 10th Anniversary 2026 V Case Road Trip (Chase)","linea":"Car Culture Chase","clp":130000,"usd":132.44},{"modelo":"Hot Wheels 1:64 Set 10 autos Fast & Furious 7 Premium case","linea":"Fast & Furious Premium (10)","clp":130000,"usd":132.44},{"modelo":"2025 Hot Wheels RLC Collectors Formula 1","linea":"Red Line Club","clp":90000,"usd":91.69},{"modelo":"Hot Wheels 1:64 Team Transport 2024 D Case Fleet Street","linea":"Team Transport","clp":27000,"usd":27.51}]},"ebay_observado":{"fuente":"eBay (listados observados vía búsqueda web)","fecha_dato":"2026-10-11","nota":"Precios PEDIDOS (asking) en listados activos, no ventas cerradas. eBay cerró findCompletedItems en feb-2025.","items":[{"modelo":"'99 Honda Civic Type R (EK9) STH 2022","condicion":"carded","usd_min":200,"usd_max":798,"nota":"varios listados: $798, $550, $299.95, $200; uno loose a $75"},{"modelo":"'71 El Camino STH","condicion":"carded","usd_min":34,"usd_max":36,"nota":"listados 2024"},{"modelo":"2025 STH '71 Mustang Funny Car","condicion":"carded","usd_min":95,"usd_max":95,"nota":"47 watchers"},{"modelo":"Treasure Hunt (categoría general)","condicion":"carded","usd_min":2.49,"usd_max":13.99,"nota":"rango típico; outliers hasta $429"},{"modelo":"STH 2026 Pontiac Firebird 400","condicion":"carded","usd_min":51.3,"usd_max":51.3,"nota":"eBay UK £38,82"},{"modelo":"Lote 30 autos (joblot)","condicion":"nuevo","usd_min":47.2,"usd_max":47.2,"nota":"eBay UK £35,70 → £1,19 por auto"},{"modelo":"Lote 50 autos (clearance joblot)","condicion":"nuevo","usd_min":112.4,"usd_max":112.4,"nota":"eBay UK £85 → £1,70 por auto"}]},"mercadolibre_cl":{"estado":"EXTRACCIÓN AUTOMÁTICA BLOQUEADA","detalle":"MercadoLibre Chile devuelve muro de login ('negative_traffic') a cualquier acceso automatizado sin sesión, y su API pública exige token de aplicación. Se necesita token oficial (developers.mercadolibre.cl) o un colector con navegador desde una IP residencial con sesión iniciada.","terminos_mas_buscados":["hot wheels","hot wheels premium","miniaturas hot wheels","autos hot wheels","hot wheels colección"],"fuente_terminos":"listado.mercadolibre.cl (bloques 'Productos más buscados' y 'Los autos en miniatura más vendidos')","precios_retail_cl":[{"item":"Auto básico","clp":1990,"fuente":"littletoys.cl"},{"item":"Auto básico","clp":2450,"fuente":"isatoyschile.cl"},{"item":"Pack 5 autos","clp":9990,"fuente":"littletoys.cl / Lider.cl"},{"item":"Car Culture","clp":6290,"fuente":"super.lider.cl"},{"item":"Boulevard","clp":7990,"fuente":"super.lider.cl"},{"item":"Collector F&F Datsun","clp":10990,"fuente":"isatoyschile.cl"}]},"cobertura_y_limites":[{"marketplace":"MercadoLibre Chile","automatizable":"Solo con token de API o navegador con sesión","obtenido":"términos más buscados + precios retail locales","bloqueo":"muro de login para accesos automatizados"},{"marketplace":"eBay","automatizable":"API Browse con clave gratuita (solo listados activos)","obtenido":"listados observados de STH/TH y lotes","bloqueo":"páginas de búsqueda bloqueadas a bots; sin ventas cerradas desde feb-2025"},{"marketplace":"Facebook Marketplace","automatizable":"No (requiere sesión; sin API pública de búsqueda)","obtenido":"—","bloqueo":"login obligatorio"},{"marketplace":"TikTok (Shop/videos)","automatizable":"No (sin API pública de búsqueda de productos)","obtenido":"—","bloqueo":"contenido dinámico + sin API"},{"marketplace":"hwpriceguide.com","automatizable":"Parcial (artículos públicos)","obtenido":"ranking real de demanda de coleccionistas (enero y febrero 2026)","bloqueo":"—"},{"marketplace":"Tiendas especializadas chilenas","automatizable":"Sí (HTML simple)","obtenido":"precios reales en CLP de STH, RLC y Car Culture","bloqueo":"—"}]}, CAJ={"meta":{"generado":"2026-10-11","fuente_principal":"Hot Wheels Wiki (Fandom) — tablas de Treasure Hunts y Super Treasure Hunts con columna 'Case (Wave)'","fuente_cruce":"hotwheelstreasure.com (tabla TH↔STH por caja 2026, verificada 29-sep-2026)","nota":"Cada caja (A–Q, sin I ni O) trae UNA Treasure Hunt regular y, en algunos casos, UNA Super Treasure Hunt. La composición completa de ~72 autos por caja solo se conoce por reportes de apertura."},"como_funciona":[{"dato":"El código de caja es una letra (A, B, C… Q). Se imprimen en la caja de surtido y en la tarjeta.","fuente":"allhotwheels.com/news/hot-wheels-cars-list-collector-guide"},{"dato":"Cada caja trae alrededor de 72 autos, con duplicados de los modelos comunes (no son 72 modelos distintos).","fuente":"allhotwheels.com"},{"dato":"Hay 15 cajas por año (A–Q): se omiten las letras I y O para no confundirlas con 1 y 0.","fuente":"hotwheelstreasure.com/treasure-hunts/2026"},{"dato":"Cada caja incluye UNA Treasure Hunt regular. Los coleccionistas estiman ~1 TH por caja de 72 (no es cifra oficial de Mattel).","fuente":"hotwheelstreasure.com (estimación de coleccionistas, leída 2026-09-29)"},{"dato":"La Super Treasure Hunt es mucho más rara: puede haber una por caja o ninguna. En 2026 cada letra tiene su STH publicada.","fuente":"allhotwheels.com + hotwheelstreasure.com"},{"dato":"La composición de una caja mezcla modelos nuevos, retornos y repetidos de modelos populares.","fuente":"allhotwheels.com"},{"dato":"Master Case / Factory Sealed Set: caja con un ejemplar de todos los modelos del año, sus recolors, exclusivos de tienda y sus STH, con sello holográfico. Solo en Mattel Creations para miembros RLC, ~US$600, cantidades limitadas con número de serie.","fuente":"Hot Wheels Wiki — 'Master Case'"}],"codigos_base":{"que_es":"El código grabado en la BASE del auto (también llamado date code / production code) indica la fecha de fabricación: una letra = año, dos dígitos = semana del año.","fuente":"Hot Wheels Wiki — 'Base codes'","letra_a_anio":{"A":2008,"B":2009,"C":2010,"D":2011,"E":2012,"F":2013,"G":2014,"H":2015,"J":2016,"K":2017,"L":2018,"M":2019,"N":2020,"P":2021,"R":2022,"S":2023,"T":2024,"U":2025,"V":2026},"ejemplo":"Código 'M36' → letra M = 2019, semana 36 → fabricado entre el 2 y el 8 de septiembre de 2019.","utilidad":"Sirve para datar un auto suelto sin tarjeta y para detectar variantes de producción entre lotes."},"cajas_por_anio":{"2022":[{"letra":"A","STH":{"modelo":"'55 Chevy","toy":"HCY10","col":"020/250","serie":"Chevy Bel Air 1/5","color":"Spectraflame blue","rueda":"RR5SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/%2755_chevy.jpg","catalogo_id":"2026-JJK21"}},{"letra":"B","STH":{"modelo":"'73 BMW 3.0 CSL Race Car","toy":"HCY20","col":"034/250","serie":"Retro Racers 2/10","color":"Spectraflame gold","rueda":"RR8SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/%2773_BMW_CSL_RACE_CAR.jpg","catalogo_id":"2022-HCW51"}},{"letra":"C","STH":{"modelo":"Dodge Van","toy":"HCY16","col":"055/250","serie":"HW Metro 6/10","color":"Spectraflame lilac","rueda":"MiniC4SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/DODGE_VAN.jpg","catalogo_id":"2024-HTB95"}},{"letra":"D","STH":{"modelo":"'63 Studebaker Champ","toy":"HCY14","col":"093/250","serie":"HW Hot Trucks 5/10","color":"Spectraflame black","rueda":"RR8SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/%E2%80%9863_studebaker.jpg","catalogo_id":null}},{"letra":"E","STH":{"modelo":"2020 Corvette","toy":"HCY11","col":"106/250","serie":"Factory Fresh 3/10","color":"Spectraflame blue","rueda":"RR5SPM","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/2020_corvetteSTH.jpg","catalogo_id":null}},{"letra":"F","STH":{"modelo":"'99 Honda Civic Type R (EK9)","toy":"HCY12","col":"125/250","serie":"HW Hatchbacks 5/5","color":"Spectraflame yellow","rueda":"RR6SPM","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/Civic_EK9.jpg","catalogo_id":"2021-GRX62"}},{"letra":"G","STH":{"modelo":"Volkswagen Käfer Racer","toy":"HCY09","col":"142/250","serie":"HW Contoured 5/5","color":"Spectraflame red","rueda":"C4SPRR","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/Volkswagen_caferracer.jpg","catalogo_id":"2018-FJW06"}},{"letra":"H","STH":{"modelo":"2020 Jaguar F-Type","toy":"HCY17","col":"158/250","serie":"HW Turbo 10/10","color":"Spectraflame black","rueda":"RR10SPM","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/2020_Jaguar_F-Type.jpg","catalogo_id":"2021-GRX29"}},{"letra":"J","STH":{"modelo":"Custom '18 Ford Mustang GT","toy":"HCY18","col":"175/250","serie":"Spoiler Alert 5/5","color":"Spectraflame red","rueda":"RR6SPM","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/O1CN01nW5A7H2Jn1VKsvghQ_%21%21652649465.jpg","catalogo_id":"2025-HYY94"}},{"letra":"K","STH":{"modelo":"Nissan Skyline HT 2000GT-X","toy":"HCY15","col":"187/250","serie":"HW J-Imports 9/10","color":"Spectraflame seafoam green","rueda":"RR8SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/Nissan_skyline_HT_2000GT-X.jpg","catalogo_id":"2026-JJM13"}},{"letra":"L","STH":{"modelo":"'71 Lamborghini Miura SV","toy":"HCY13","col":"202/250","serie":"HW Exotics 5/10","color":"Spectraflame orange","rueda":"RR10SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/E2fb2f06e2d5d4a068556e33c41535f.jpg","catalogo_id":"2026-JJK54"}},{"letra":"M","STH":{"modelo":"'84 Mustang SVO","toy":"HCY19","col":"221/250","serie":"Muscle Mania 4/10","color":"Spectraflame purple","rueda":"RR5SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/84MustangSVO.jpg","catalogo_id":"2024-HTC66"}},{"letra":"N","STH":{"modelo":"'94 Audi Avant RS2","toy":"HCY22","col":"228/250","serie":"HW Wagons 5/5","color":"Spectraflame Brilliant Black","rueda":"RRA","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/%2794_Audi_Avant_RS2.jpg","catalogo_id":"2026-JJK18"}},{"letra":"P","STH":{"modelo":"'32 Ford","toy":"HCY21","col":"237/250","serie":"Rod Squad 5/5","color":"Spectraflame blue","rueda":"RRSteelie","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/Sth_32_ford_gulf.jpg","catalogo_id":"2022-HCV75"}},{"letra":"Q","STH":{"modelo":"'81 Camaro","toy":"HCY23","col":"248/250","serie":"Then and Now 10/10","color":"Spectraflame green","rueda":"RR5SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/%E2%80%9881_Camaro.jpg","catalogo_id":"2022-HCV81"}}],"2023":[{"letra":"A","TH":{"modelo":"Raijin Express","toy":"HKK98","col":"010/250","serie":"HW Haulers 1/5","color":"Red","rueda":"AeroDisc","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/RaijinHauler.jpg","catalogo_id":"2023-HKK98"},"STH":{"modelo":"Classic TV Series Batmobile","toy":"HKL16","col":"003/250","serie":"Batman 1/5","color":"Spectraflame maroon","rueda":"RR5SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/STH_2023A_BATMOBILE.jpg","catalogo_id":"2026-JJH83"}},{"letra":"B","TH":{"modelo":"Surf Crate","toy":"HKL06","col":"050/250","serie":"Surf's Up 3/5","color":"Pink","rueda":"5SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/HKL06.jpg","catalogo_id":"2017-DVC21"},"STH":{"modelo":"Mercedes-Benz 300 SL","toy":"HKL09","col":"027/250","serie":"Retro Racers 3/10","color":"Spectraflame red","rueda":"DDRR","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/Mercedes-benzs300sl.jpg","catalogo_id":"2023-HKH02"}},{"letra":"C","TH":{"modelo":"BMW R nineT Racer","toy":"HKL01","col":"068/250","serie":"HW Moto 2/5","color":"Atomic Blue","rueda":"Chrome ORMC","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/BMWRnineTRacer.jpg","catalogo_id":null},"STH":{"modelo":"'68 COPO Camaro","toy":"HKL12","col":"063/250","serie":"HW Art Cars 5/10","color":"Spectraflame yellow","rueda":"DDRR","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/%2768COPOCamaro.webp.jpg","catalogo_id":"2019-FYD06"}},{"letra":"D","TH":{"modelo":"Mad Propz","toy":"HKK95","col":"092/250","serie":"Sky Show 3/5","color":"Metalflake gold","rueda":"Micro5SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/PropZ.JPG","catalogo_id":"2020-GHC63"},"STH":{"modelo":"Lotus Evija","toy":"HKL13","col":"084/250","serie":"HW Green Speed 5/10","color":"Spectraflame Atomic Red","rueda":"RR10SPM","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/78bccf5402cbd84fbcf3691f00711b5.webp.jpg","catalogo_id":"2022-HCT07"}},{"letra":"E","TH":{"modelo":"Mod Rod","toy":"HKL00","col":"111/250","serie":"HW 55 Race Team 4/5","color":"Matte race team blue","rueda":"AeroDisc & DD8","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/ModRod_2022_HWRaceTeam.jpg","catalogo_id":"2021-GTB16"},"STH":{"modelo":"1968 Mazda Cosmo Sport","toy":"HKL20","col":"118/250","serie":"HW J-Imports 9/10","color":"Spectraflame Orange","rueda":"RRMag","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/Mazda_cosmo.jpg","catalogo_id":null}},{"letra":"F","TH":{"modelo":"Donut Drifter","toy":"HKK97","col":"129/250","serie":"Sweet Rides 5/5","color":"Orange","rueda":"White wheel, Chrome Pink 5SP (front), Chrome Orange 5SP (rear)","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/HKK97.jpg","catalogo_id":"2025-HYW92"},"STH":{"modelo":"Renault Sport R.S. 01","toy":"HKL21","col":"134/250","serie":"HW Turbo 3/5","color":"Spectraflame cherry","rueda":"White RRMC","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/Renault_sport_rs.jpg","catalogo_id":"2017-DVC53"}},{"letra":"G","TH":{"modelo":"Rise 'N Climb","toy":"HKL03","col":"146/250","serie":"HW Sports 5/5","color":"Baby blue","rueda":"DD8","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/HKL03.jpg","catalogo_id":"2018-FJY91"},"STH":{"modelo":"'68 Corvette - Gas Monkey Garage","toy":"HKL10","col":"139/250","serie":"HW Dream Garage 5/5","color":"Spectraflame gold","rueda":"Red rim, Black RR5SPM","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/Monkey_garage.jpg","catalogo_id":"2026-JJK47"}},{"letra":"H","TH":{"modelo":"Ducati 1199 Panigale","toy":"HKL05","col":"164/250","serie":"Factory Fresh 5/5","color":"Arctic White","rueda":"MC3","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/164_-_Ducati_1199_Panigale_%28TH%29.jpg","catalogo_id":"2023-HKL05"},"STH":{"modelo":"Glory Chaser","toy":"HKL11","col":"155/250","serie":"HW Roadsters 9/10","color":"Spectraflame Gulf Racing Blue","rueda":"C4SPRR","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/Glory_chaser.jpg","catalogo_id":null}},{"letra":"J","TH":{"modelo":"'95 Jeep Cherokee","toy":"HKL02","col":"176/250","serie":"Mud Studs 4/5","color":"Off-white","rueda":"\"Muddy\" BLOR","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/HKL02-LOOSE.jpg","catalogo_id":"2023-HKL02"},"STH":{"modelo":"'82 Toyota Supra","toy":"HKL08","col":"167/250","serie":"HW: The '80s 10/10","color":"Spectraflame red","rueda":"RR10SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/%2782_toyota_supra.jpg","catalogo_id":"2026-JJK28"}},{"letra":"K","TH":{"modelo":"Toyota Land Cruiser","toy":"HKL07","col":"194/250","serie":"Then and Now 2/10","color":"Ivory","rueda":"BAJA5","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/194_250.jpg","catalogo_id":"2023-HKL07"},"STH":{"modelo":"'69 Shelby GT-500","toy":"HKL22","col":"195/250","serie":"Muscle Mania 9/10","color":"Spectraflame purple","rueda":"RR5SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/7b52a96a15ff809ca101aee1320d186.jpg","catalogo_id":"2023-HKJ50"}},{"letra":"L","TH":{"modelo":"Madfast","toy":"HKK99","col":"198/250","serie":"HW Drag Strip 10/10","color":"Teal","rueda":"AeroDisc/SK5","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/MadfastDragster.jpg","catalogo_id":"2025-JBB01"},"STH":{"modelo":"'65 Mercury Comet Cyclone","toy":"HKL14","col":"199/250","serie":"HW Gassers 4/5","color":"Spectraflame black","rueda":"RR5SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/2023_07_07_21_24_IMG_8258.jpg","catalogo_id":"2026-JJK06"}},{"letra":"M","TH":{"modelo":"Time Shifter","toy":"HKK94","col":"210/250","serie":"HW Metro 8/10","color":"Gunmetal gray","rueda":"DD8","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/HKK94-LOOSE.jpg","catalogo_id":"2023-HKK94"},"STH":{"modelo":"Mighty K","toy":"HKL18","col":"214/250","serie":"HW Hot Trucks 7/10","color":"Spectraflame red","rueda":"MiniC4SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/2023_07_07_21_22_IMG_8250.jpg","catalogo_id":"2024-HTC17"}},{"letra":"N","TH":{"modelo":"Tooned Volkswagen Golf Mk1","toy":"HKK96","col":"221/250","serie":"Tooned 4/5","color":"Sky blue","rueda":"AeroDisc","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/2023-221_HKK96_Tooned_Golf_mk1_Blue_TH_open-00.jpg","catalogo_id":"2026-JJK16"},"STH":{"modelo":"Porsche 935","toy":"HKL17","col":"223/250","serie":"HW Exotics 7/10","color":"Spectraflame navy blue","rueda":"AeroDisc","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/2023_07_07_21_25_IMG_8265.jpg","catalogo_id":"2023-HKH96"}},{"letra":"P","TH":{"modelo":"2020 Ram 1500 Rebel","toy":"HKL04","col":"238/250","serie":"HW Rescue 7/10","color":"Yellow","rueda":"BLOR","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/CoastPatrolRam.jpg","catalogo_id":"2025-HYW91"},"STH":{"modelo":"Datsun Bluebird Wagon (510)","toy":"HKL15","col":"235/250","serie":"HW Wagons 4/5","color":"Spectraflame watermelon","rueda":"C4SPRR","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/73d9e391cee5f2365232c195406643f.jpg","catalogo_id":"2023-HKH72"}},{"letra":"Q","TH":{"modelo":"Volkswagen \"Baja Bug\"","toy":"HKK93","col":"241/250","serie":"Baja Blazers 9/10","color":"Red","rueda":"Black & \"Muddy\" BLOR","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/2023-241_HKK93_TH_Volkswagen_Baja_Bug_Red_open-1.jpg","catalogo_id":"2023-HKK93"},"STH":{"modelo":"Volvo 240 Drift Wagon","toy":"HKL19","col":"245/250","serie":"HW Slammed 4/5","color":"Spectraflame green","rueda":"RRSteelie & RR10SPM","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20230730215614.jpg","catalogo_id":"2025-JBB40"}}],"2024":[{"letra":"A","STH":{"modelo":"Ford Escort RS2000","toy":"HTF30","col":"023/250","serie":"Factory Fresh 1/10","color":"Spectraflame Green","rueda":"RR8SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/2024_STH_A_CASE_FOERD_ESCORT_RS2000.jpg","catalogo_id":"2024-HTC48"}},{"letra":"B","STH":{"modelo":"'18 Camaro SS","toy":"HTF31","col":"032/250","serie":"HW Dream Garage 2/5","color":"Spectraflame Black","rueda":"RR5SPM","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/2024_STH_B_CASE_18_Camaro_SS.jpg","catalogo_id":"2026-JJK42"}},{"letra":"C","STH":{"modelo":"BMW 507","toy":"HTF32","col":"067/250","serie":"HW Roadsters 4/5","color":"Spectraflame Gelb","rueda":"RR10SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/2024_STH_C_CASE_BMW_507.jpg","catalogo_id":null}},{"letra":"D","STH":{"modelo":"'89 Mercedes-Benz 560 SEC AMG","toy":"HTF33","col":"082/250","serie":"HW Modified 8/10","color":"Spectraflame Red","rueda":"RREx","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/2024_STH_D_CASE_benz_560.jpg","catalogo_id":"2025-JBB11"}},{"letra":"E","STH":{"modelo":"'60s Fiat 500D Modificado","toy":"HTF34","col":"117/250","serie":"Compact Kings 5/5","color":"Spectraflame gold","rueda":"DDRR","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/2024_STH_Fiat.jpg","catalogo_id":null}},{"letra":"F","STH":{"modelo":"'71 El Camino","toy":"HTF35","col":"132/250","serie":"HW Hot Trucks 7/10","color":"Spectraflame purple","rueda":"RR5SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/2024_STH_E_CASE_EL_CAMINO.jpg","catalogo_id":"2020-GHC28"}},{"letra":"G","STH":{"modelo":"Audi 90 quattro","toy":"HTF36","col":"144/250","serie":"HW Turbo 4/5","color":"Spectraflame dark blue","rueda":"RRAero","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/AUDI_90_QUATTRO.jpg","catalogo_id":"2025-JBB20"}},{"letra":"H","STH":{"modelo":"Volvo P1800 Gasser","toy":"HTF37","col":"153/250","serie":"HW Reverse Rake 4/5","color":"Spectraflame blue","rueda":"RRDragD","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/VOLVO_P1800_GASSER01.jpg","catalogo_id":"2023-HKG27"}},{"letra":"J","STH":{"modelo":"Mitsubishi Pajero Evolution","toy":"HTF38","col":"169/250","serie":"HW J-Imports 8/10","color":"Spectraflame copper","rueda":"RR6SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/PAJERO.jpg","catalogo_id":"2024-HTC45"}},{"letra":"K","STH":{"modelo":"Mazda 787B","toy":"HTF39","col":"145/250","serie":"HW Race Day 7/10","color":"Spectraflame orange","rueda":"RRA & RRE","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/Charge787BSTH.jpg","catalogo_id":"2025-JBB39"}},{"letra":"L","STH":{"modelo":"'77 Pontiac Firebird T/A","toy":"HTF40","col":"206/250","serie":"Muscle Mania 4/5","color":"Spectraflame black","rueda":"RR10SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/Pontiac_firebird.jpg","catalogo_id":"2024-HTC60"}},{"letra":"M","STH":{"modelo":"'96 Nissan 180SX Type X","toy":"HTF41","col":"211/250","serie":"HW: The '90s 6/10","color":"Spectraflane Dark Dlue","rueda":"RR6SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/96_Nissan_180sx_type_R.jpg","catalogo_id":"2024-HTB08"}},{"letra":"N","STH":{"modelo":"Celero GT","toy":"HTF42","col":"231/250","serie":"Quarter Mile Heroes 3/5","color":"Spectraflame purple","rueda":"RRA & RR10SPM","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/Tiaozi-%E5%A1%9E%E7%BD%97GT%E8%B6%85%E5%AE%9D.jpg","catalogo_id":"2024-HTB87"}},{"letra":"P","STH":{"modelo":"Lamborghini Huracán LP 620-2 Super Trofeo","toy":"HTF43","col":"239/250","serie":"HW Exotics 8/10","color":"Spectraflame red","rueda":"RRA & RR10SPM","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/2025_Lamborghini_STH.jpg","catalogo_id":"2024-HTC25"}},{"letra":"Q","STH":{"modelo":"'83 Chevy Silverado","toy":"HTF44","col":"249/250","serie":"Then and Now 9/10","color":"Spectraflame blue","rueda":"RR5SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/2024_Then_and_Now_STH.jpg","catalogo_id":"2026-JJJ13"}}],"2025":[{"letra":"A","TH":{"modelo":"Ford Performance Supervan 4","toy":"JBC20","col":"017/250","serie":"HW First Response 1/5","color":"Red","rueda":"PR5","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/FirstResponseSupervan.jpg","catalogo_id":"2025-JBC20"},"STH":{"modelo":"'87 Audi quattro","toy":"JBC35","col":"016/250","serie":"Factory Fresh 2/5","color":"Spectraflame seafoam green","rueda":"White RR10SPM","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/%2787_AUDI_AUQTTRO.jpg","catalogo_id":"2025-HYW72"}},{"letra":"B","TH":{"modelo":"Fish'd & Chip'd","toy":"JBC21","col":"032/250","serie":"HW Designed By 2/5","color":"Brown","rueda":"L4","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/Fish%27dandChip%27d.jpg","catalogo_id":"2025-JBC21"},"STH":{"modelo":"Hirohata Merc","toy":"JBC36","col":"046/250","serie":"Rod Squad 4/10","color":"Spectraflame purple","rueda":"WWMD","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/HIROHATA_MERC.jpg","catalogo_id":"2025-HYW97"}},{"letra":"C","TH":{"modelo":"Mailed It!","toy":"JBC22","col":"057/250","serie":"HW Metro 3/5","color":"Metalflake plum pearl","rueda":"5SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/LubetskyMailedIt.jpg","catalogo_id":"2026-JJK12"},"STH":{"modelo":"Hi-Roller II","toy":"JBC37","col":"061/250","serie":"HW Art Cars 6/10","color":"Spectraflame black","rueda":"White RRA and Black RRA","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/HiRollerII.jpg","catalogo_id":"2024-HRY94"}},{"letra":"D","TH":{"modelo":"Pedal Driver","toy":"JBC23","col":"095/250","serie":"HW Ride-Ons 4/5","color":"Red","rueda":"RA6","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/TreasurePedal.jpg","catalogo_id":null},"STH":{"modelo":"1975 Datsun Sunny Truck (B120)","toy":"JBC38","col":"093/250","serie":"HW Hot Trucks 6/10","color":"Spectraflame blue","rueda":"MiniC4SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/1975_Datsun_Sunny_Truck_%28B120%29.jpg","catalogo_id":null}},{"letra":"E","TH":{"modelo":"Rig Storm","toy":"JBC24","col":"110/250","serie":"X-Raycers 9/10","color":"Transparent Plum","rueda":"AeroDisc","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/2025_Rig_Storm.jpg","catalogo_id":"2018-FJW91"},"STH":{"modelo":"Aston Martin DB4GT High-Speed Edition","toy":"JBC39","col":"107/250","serie":"HW Dream Garage 3/5","color":"Spectraflame yellow","rueda":"MD","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/Aston_Martin_DB4GT_High-Speed_Edition.jpg","catalogo_id":"2024-HRY86"}},{"letra":"F","TH":{"modelo":"'85 Honda City Turbo II","toy":"JBC25","col":"141/250","serie":"HW J-Imports 5/5","color":"Teal","rueda":"5SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/1985HondaCity.jpg","catalogo_id":"2022-HCV25"},"STH":{"modelo":"'20 Jeep Gladiator","toy":"JBC40","col":"130/250","serie":"HW Dirt 6/10","color":"Spectraflame black","rueda":"ORRRBL10SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/20Jeep_Gladiator.jpg","catalogo_id":"2026-JJH91"}},{"letra":"G","TH":{"modelo":"Birthday Burner","toy":"JBC26","col":"143/250","serie":"HW Celebration Racers 5/10","color":"Brown","rueda":"White rim 5SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/TreasureBurner.jpg","catalogo_id":null},"STH":{"modelo":"Porsche 911 Rallye","toy":"JBC41","col":"154/250","serie":"Safari Mode 2/5","color":"Spectraflame green","rueda":"RR5SPM","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/PORSCHE_911_RALLYE.jpg","catalogo_id":"2024-HRY70"}},{"letra":"H","TH":{"modelo":"Chill Mill","toy":"JBC28","col":"180/250","serie":"Fast Foodie 4/5","color":"Metalflake Plum Pearl","rueda":"White rim 5SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/2025_Chill_Mill_%28HWLR%29.jpg","catalogo_id":"2025-JBC28"},"STH":{"modelo":"'71 Mustang Funny Car","toy":"JBC42","col":"175/250","serie":"Mustang 60th 4/5","color":"Spectraflame red","rueda":"GYRRDragS/RR5SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/71_Mustang_Funny_Car.jpg","catalogo_id":"2025-JBB04"}},{"letra":"J","TH":{"modelo":"Nissan Leaf NISMO RC 02","toy":"JBC27","col":"168/250","serie":"HW EV 10/10","color":"Lime green","rueda":"PR5","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/LeafNISMO.jpg","catalogo_id":"2025-JBC27"},"STH":{"modelo":"'62 Corvette Gasser","toy":"JBC43","col":"182/250","serie":"HW Reverse Rake 4/5","color":"Spectraflame black","rueda":"RRPrf/RRDragS","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/%E2%80%9862_Corvette_Gasser.jpg","catalogo_id":"2025-JBB08"}},{"letra":"K","TH":{"modelo":"Chevroletor","toy":"JBC29","col":"202/250","serie":"Track Aces 5/5","color":"Metalflake navy blue","rueda":"WW5SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/2025_General_Motors_Chevroletor.jpg","catalogo_id":"2025-JBC29"},"STH":{"modelo":"McLaren Speedtail","toy":"JBC44","col":"209/250","serie":"HW Exotics 5/5","color":"Spectraflame Volcano Orange","rueda":"Front: Dark chrome RRA Rear: Dark chrome RR10SPM","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/McLaren_Speedtail.jpg","catalogo_id":"2025-JBB28"}},{"letra":"L","TH":{"modelo":"Honda S800 Racing","toy":"JBC30","col":"212/250","serie":"Compact Kings 9/10","color":"Orange","rueda":"L4","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/1968HondaS800.jpg","catalogo_id":"2025-JBC30"},"STH":{"modelo":"'94 Bugatti EB110 SS","toy":"JBC45","col":"221/250","serie":"HW Race Day 9/10","color":"Spectraflame Viola","rueda":"RRA","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/%2794_Bugatti_EB110_SS.jpg","catalogo_id":"2025-JBB36"}},{"letra":"M","TH":{"modelo":"Shark Bite","toy":"JBC31","col":"229/250","serie":"Experimotors 10/10","color":"Green","rueda":"M5SP/5SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/2025_Shark_Bite.jpg","catalogo_id":"2025-JBC31"},"STH":{"modelo":"'73 Honda Civic Custom","toy":"JBC46","col":"231/250","serie":"Then and Now 9/10","color":"Spectraflame red","rueda":"MiniC4SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/%E2%80%9873_HONDA_CIVICE_CUSTOM.jpg","catalogo_id":"2026-JJJ81"}},{"letra":"N","TH":{"modelo":"1966 Triumph Tiger 100","toy":"JBC32","col":"235/250","serie":"HW Moto 5/5","color":"Green","rueda":"MCCR","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/TriumphRaceBike.jpg","catalogo_id":"2025-JBC32"},"STH":{"modelo":"'20 Dodge Charger Hellcat","toy":"JBC47","col":"240/250","serie":"Muscle Mania 9/10","color":"Spectraflame pink","rueda":"RR6SPM","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/%2720_Dodge_Charger_Hellcat.jpg","catalogo_id":"2025-JBB45"}},{"letra":"P","TH":{"modelo":"'84 Audi Sport quattro","toy":"JBC33","col":"246/250","serie":"Wild Widebody 5/5","color":"Metalflake silver","rueda":"AeroDisc","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/1984quattro.jpg","catalogo_id":"2025-JBC33"},"STH":{"modelo":"BMW M3 Wagon","toy":"JBC48","col":"245/250","serie":"HW Wagons 5/5","color":"Spectraflame green","rueda":"RRA","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/BMW_M3_WAGON.jpg","catalogo_id":"2025-JBB48"}},{"letra":"Q","TH":{"modelo":"Triumph TR6","toy":"JBC34","col":"249/250","serie":"HW Track Champs 5/5","color":"Gray","rueda":"DD8","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/2025_Triumph_TR6.jpg","catalogo_id":"2025-JBC34"},"STH":{"modelo":"Ford RS200","toy":"JBC49","col":"247/250","serie":"Peak Pursuit 9/10","color":"Spectraflame Gulf Racing Blue","rueda":"RRA","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/FORD_RS200.jpg","catalogo_id":"2025-JBB49"}}],"2026":[{"letra":"A","TH":{"modelo":"'87 Buick Regal GNX","toy":"JJM00","col":"009/250","serie":"Nightspeed 1/10","color":"Metalflake Purple","rueda":"White rim, black PR5","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/BuickRegal.jpg","catalogo_id":"2026-JJM00"},"STH":{"modelo":"Drift-Ender","toy":"JJM15","col":"013/250","serie":"Truckin' Along 1/5","color":"Spectraflame red","rueda":"Black RRA","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/STH_Drift-Ender.jpg","catalogo_id":"2026-JJH90"}},{"letra":"B","TH":{"modelo":"'92 Dodge Viper RT/10","toy":"JJM01","col":"029/250","serie":"Drop Tops 2/5","color":"White","rueda":"White 5SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/1992Viper.jpg","catalogo_id":"2026-JJM01"},"STH":{"modelo":"Ford Mustang GTD","toy":"JJM16","col":"043/250","serie":"Factory Fresh 3/5","color":"Spectraflame Holographic Blue","rueda":"Gold RR10SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/Ford_Mustang_GTD.jpg","catalogo_id":"2026-JJJ14"}},{"letra":"C","TH":{"modelo":"Electro Silhouette","toy":"JJM02","col":"058/250","serie":"HW EV 5/10","color":"Black","rueda":"Chrome blue AeroDisc and RA6","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/ElectroSilhouetteTH.jpeg","catalogo_id":"2022-HCW43"},"STH":{"modelo":"Ferrari F40 Competizione","toy":"JJM17","col":"063/250","serie":"Ferrari 3/5","color":"Spectraflame Grigio Nardo","rueda":"RRE","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/NardoF40Comp.jpg","catalogo_id":"2025-HYW59"}},{"letra":"D","TH":{"modelo":"Hot Wheengs","toy":"JJM03","col":"081/250","serie":"X-Raycers 4/5","color":"Green","rueda":"Red tire, chrome green RA6","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/HotSauce.jpg","catalogo_id":"2025-HYW42"},"STH":{"modelo":"'64 Impala","toy":"JJM18","col":"095/250","serie":"Layin' Low 4/5","color":"Spectraflame cyan","rueda":"Whitewall D7RR","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/ImpalaSTH.jpg","catalogo_id":null}},{"letra":"E","TH":{"modelo":"Cone Shaker","toy":"JJM04","col":"122/250","serie":"HW Starting Grid 8/10","color":"Neon green","rueda":"Lime tire AeroDisc","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/HotConez.jpg","catalogo_id":null},"STH":{"modelo":"'87 Ford Sierra Cosworth","toy":"JJM19","col":"116/250","serie":"HW Euro 5/10","color":"Spectraflame hot pink","rueda":"Chrome lip, black D7RR","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/2026ML-116B_%28Large%29.JPG","catalogo_id":"2023-HKG79"}},{"letra":"F","TH":{"modelo":"2016 Ford GT Race","toy":"JJM05","col":"124/250","serie":"Exoticars 8/10","color":"Yellow","rueda":"E10SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/2016FordGTLMGTE.jpg","catalogo_id":"2024-HTC71"},"STH":{"modelo":"Honda Civic Custom","toy":"JJM20","col":"159/250","serie":"Drag Racers 8/10","color":"Spectraflame teal","rueda":"TRR/MicroRRA","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/2026H_tiaozi.jpg","catalogo_id":"2026-JJJ81"}},{"letra":"G","TH":{"modelo":"2 Jet Z","toy":"JJM06","col":"147/250","serie":"HW Dream Garage 4/5","color":"Metalflake Gold","rueda":"Chrome red lip, black AeroDisc","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/THJetZ.jpg","catalogo_id":"2020-GHB45"},"STH":{"modelo":"Custom Otto","toy":"JJM21","col":"156/250","serie":"Mattel 5/5","color":"Spectraflame Otto Blue","rueda":"DDNCRL","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/STH_OTTO_o4.jpg","catalogo_id":"2026-JJK03"}},{"letra":"H","TH":{"modelo":"Total Disposal","toy":"JJM07","col":"162/250","serie":"HW Heavyweights 5/5","color":"Gray","rueda":"Gray AeroDisc and DD8","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/%27ToonedTrashTruck.jpg","catalogo_id":"2026-JJM07"},"STH":{"modelo":"Lotus Sport Elise","toy":"JJM22","col":"160/250","serie":"Compact Kings 7/10","color":"Spectraflame orange","rueda":"Black RR5SPM","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/LotusEliseSTH.jpg","catalogo_id":"2026-JJK07"}},{"letra":"J","TH":{"modelo":"Amaru GTC","toy":"JJM08","col":"186/250","serie":"HW Mods 4/5","color":"Blue","rueda":"Bronze ID","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/ModsAmaru.jpg","catalogo_id":"2026-JJM08"},"STH":{"modelo":"Subaru Impreza WRX","toy":"JJM23","col":"176/250","serie":"HW J-Imports 7/10","color":"Spectraflame blue","rueda":"Gold RR10SPM","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/STHImpreza.jpg","catalogo_id":"2026-JJK19"}},{"letra":"K","TH":{"modelo":"Sweet Driver","toy":"JJM09","col":"196/250","serie":"Sweet Rides 4/5","color":"White","rueda":"Pink tire, chrome red AeroDisc","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/CupcakeRacer.jpg","catalogo_id":"2026-JJM09"},"STH":{"modelo":"'94 Toyota Supra","toy":"JJM25","col":"222/250","serie":"Tooned 5/5","color":"Spectraflame black","rueda":"Bronze rim, black C4SPRR","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/INA.jpg","catalogo_id":"2026-JJK51"}},{"letra":"L","TH":{"modelo":"Mad Manga","toy":"JJM10","col":"217/250","serie":"Hot Wheels Let's Race 4/5","color":"White","rueda":"Bronze 5SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/MadManganese.jpg","catalogo_id":"2026-JJM10"},"STH":{"modelo":"Nissan Maxima Drift Car","toy":"JJM26","col":"225/250","serie":"Wagons 10/10","color":"Spectraflame black","rueda":"Bronze RR5SPM","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/Image_Not_Available.jpg","catalogo_id":"2026-JJK53"}},{"letra":"M","TH":{"modelo":"Ford Model A Custom '31","toy":"JJM11","col":"229/250","serie":"Rod Squad 9/10","color":"Matte \"moody\" blue","rueda":"WWIM","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/OldBlue.jpg","catalogo_id":"2026-JJM11"},"STH":{"modelo":"Porsche 911 Carrera RS 2.7","toy":"JJM24","col":"208/250","serie":"Then and Now 9/10","color":"Spectraflame root beer","rueda":"RRF52O","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/1973PorscheRSTH.jpg","catalogo_id":"2026-JJK43"}},{"letra":"N","TH":{"modelo":"Fast Fish","toy":"JJM12","col":"238/250","serie":"Team Wheels 5/5","color":"Hot Wheels Blue","rueda":"Chrome red TRAP5","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/HWRTFish.jpg","catalogo_id":"2026-JJM12"},"STH":{"modelo":"'23 Ram 1500","toy":"JJM27","col":"234/250","serie":"HW Dirt 9/10","color":"Spectraflame purple","rueda":"Chrome lip RR8DOT","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/RamTRXSTH.jpg","catalogo_id":"2026-JJK58"}},{"letra":"P","TH":{"modelo":"Nissan Skyline HT 2000GT-X","toy":"JJM13","col":"244/250","serie":"Screen Time 10/10","color":"Black","rueda":"Black 10SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/Image_Not_Available.jpg","catalogo_id":"2026-JJM13"},"STH":{"modelo":"'70 Plymouth AAR Cuda","toy":"JJM28","col":"245/250","serie":"HW Torque 9/10","color":"Spectraflame gold","rueda":"Chrome Olive HWRTRR10SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/Cuda_TH_2026.jpg","catalogo_id":"2026-JJK63"}},{"letra":"Q","TH":{"modelo":"Gazella GT","toy":"JJM14","col":"247/250","serie":"Trophy Case 4/5","color":"Red","rueda":"Gray 10SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/Image_Not_Available.jpg","catalogo_id":"2026-JJM14"},"STH":{"modelo":"'67 Pontiac Firebird 400","toy":"JJM29","col":"249/250","serie":"Cool Classics 9/10","color":"Spectraflame sky blue","rueda":"RR5SP","pais":"Malaysia","imagen":"https://hotwheels.fandom.com/wiki/Special:FilePath/Firebird_th_2026.jpg","catalogo_id":"2026-JJK64"}}]},"contenido_identificado":{"nota":"Lo que TÚ confirmaste de cada caja (se guarda en la app, no aquí). Sirve para saber qué modelos reales salieron de cada letra en tu zona.","estructura":{"2026-A":{"modelos_encontrados":[],"notas":""}}}}, IDXINFO={"version":"2.0","generado":"2026-10-11","formula":"Índice = 0,30·R + 0,25·D + 0,20·C + 0,15·A + 0,10·M","cambios_v2":["D (demanda) ya NO está vacía: usa los conteos reales de coleccionistas de HW Price Guide (ene/feb 2026); para el resto, proxi por re-ediciones del casting.","M (mercado) ya NO es una constante: usa el momentum real enero→febrero de la demanda + presencia en tienda chilena y en eBay.","A (antigüedad) usa una curva ajustada al rango 2016-2026 (0-60) en vez de una recta.","R (rareza) penaliza castings muy re-editados y premia modelos nuevos.","Se eliminó la renormalización: el índice usa la fórmula completa."],"factores":{"R":{"peso":0.3,"que_mide":"Rareza: clase (STH/TH/Mainline), cantidad de re-ediciones del casting y si es modelo nuevo.","escala":"0-100","fuente":"clase del catálogo + conteo de apariciones 2016-2026"},"D":{"peso":0.25,"que_mide":"Demanda real de coleccionistas.","escala":"0-100 (35 + 65·conteo/máximo)","fuente":"HW Price Guide, rankings de enero y febrero 2026; proxi por re-ediciones cuando no hay medición"},"C":{"peso":0.2,"que_mide":"Condición del ejemplar.","escala":"100 = nuevo en tarjeta · 70 tarjeta dañada · 55 suelto impecable · 40 suelto bueno · 25 jugado","fuente":"escala de coleccionismo; el usuario la ajusta en su colección"},"A":{"peso":0.15,"que_mide":"Antigüedad.","escala":"0-60 para 2016-2026 (5,5 puntos por año hacia atrás)","fuente":"año del registro"},"M":{"peso":0.1,"que_mide":"Tendencia de mercado.","escala":"0-100","fuente":"momentum ene→feb 2026 de la demanda + presencia en tienda chilena (+12) y en eBay (+8)"}},"estadisticas_catalogo":{"n":2177,"min":37.2,"p10":39.6,"p25":41.3,"mediana":43.7,"p75":46.1,"p90":47.8,"max":63.0,"media":44.0},"nota":"D y M se marcan como 'medida' o 'proxi' en la ficha: el usuario siempre ve de dónde sale cada número.","histograma":{"desde":30.0,"hasta":65.0,"bins":[0,0,28,301,470,651,460,134,23,41,37,26,4,2]},"percentiles_disponibles":true}, HIST={"meta":{"descripcion":"Datos históricos, curiosidades y contexto de modelos icónicos de Hot Wheels. Fuente: Hot Wheels Wiki (Fandom), libros oficiales y documentación de Mattel.","licencia":"CC BY-SA 3.0 (atribución a Hot Wheels Wiki)","actualizado":"2026-10-12"},"modelos":{"Bone Shaker":{"historia":"Introducido en 2006, diseñado por Larry Wood. Uno de los castings más populares de la historia reciente. Su motor expuesto y carrocería esquelética lo convirtieron en un ícono instantáneo.","creacion":"Diseñado por Larry Wood, quien se inspiró en hot rods de drag racing de los años 60.","conmemorativo":false,"curiosidades":["Su nombre significa 'sacudidor de huesos' por la vibración de su motor V8 expuesto.","Apareció en la película 'Cars' de Pixar como personaje secundario.","En 2006, un prototipo vendió por más de US$10.000 en eBay.","Tiene 23 variantes de color diferentes entre 2006 y 2024."],"dato_clave":"Larry Wood es uno de los diseñadores más prolíficos de Hot Wheels, con más de 200 castings a su nombre."},"Twin Mill":{"historia":"Diseñado en 1969 por Ira Gilford, es uno de los 16 'Sweet Sixteen' originales de Hot Wheels. Su diseño con dos motores lo hizo único.","creacion":"Ira Gilford, diseñador de Mattel, se inspiró en los hot rods de doble motor de la era espacial.","conmemorativo":false,"curiosidades":["Uno de los 16 modelos originales de 1969 (los 'Sweet Sixteen').","Su nombre 'Twin Mill' significa 'doble molino' por sus dos motores.","En 2009, Mattel celebró su 40º aniversario con una reedición especial.","El diseño original tenía un techo transparente que mostraba los motores."],"dato_clave":"Los Sweet Sixteen originales de 1969 son los modelos más valiosos de Hot Wheels. Un Twin Mill en perfecto estado puede superar los US$100.000."},"Deora II":{"historia":"Diseñado por Nathan Proch, basado en un vehículo conceptual real del mismo nombre. Es uno de los castings más reconocidos del siglo XXI.","creacion":"Nathan Proch diseñó el Deora II en 2000 para la línea 'Concept Cars' de Mattel.","conmemorativo":false,"curiosidades":["El Deora original (1968) fue diseñado por Harry Bentley Bradley.","El Deora II tiene una tabla de surf trasera que se abre para revelar la cabina.","Apareció en la serie 'Hot Wheels World Race' de 2003.","En 2017, se lanzó una versión 'Deora III' con diseño futurista."],"dato_clave":"La familia Deora es una de las pocas que tiene tres generaciones oficiales de diseño."},"Rodger Dodger":{"historia":"Lanzado en 2000, diseñado por Larry Wood. Su motor V8 masivo que sobresale de la carrocería lo convirtió en un favorito instantáneo de los niños.","creacion":"Larry Wood, inspirado en los muscle cars de los años 70.","conmemorativo":false,"curiosidades":["Su motor ocupa más del 50% del vehículo.","En 2003, se lanzó una versión 'Rodger Dodge' como broma interna de Mattel.","Apareció en numerosos videojuegos de Hot Wheels.","Tiene 35+ variantes de color desde 2000."],"dato_clave":"Larry Wood también diseñó el Bone Shaker y el Twin Mill, tres de los castings más icónicos de Hot Wheels."},"Baja Truck":{"historia":"Introducido en 2007, inspirado en las camionetas de carrera Baja 1000. Es uno de los modelos más grandes y detallados de la línea Mainline.","creacion":"Diseñado para capturar la esencia del off-road racing.","conmemorativo":false,"curiosidades":["Su diseño está basado en las camionetas Trophy Truck de la Baja 1000.","Tiene suspensión funcional con ejes que se mueven.","En 2012, se lanzó una versión 'Baja Truck 2' con mejoras.","Es uno de los modelos más pesados de la línea Mainline estándar."],"dato_clave":"Las camionetas Baja son las más rápidas en el desierto, alcanzando velocidades de 160 km/h."},"Ford Mustang GTD":{"historia":"El Mustang GTD es la versión más extrema del Mustang, diseñada para la pista con tecnología de carrera. Su versión Hot Wheels fue Super Treasure Hunt 2026.","creacion":"Ford Performance, basado en el programa de carrera GT3.","conmemorativo":true,"curiosidades":["El GTD significa 'Gran Turismo Daytona', inspired in las 24 Horas de Daytona.","Tiene un motor V8 de 5.2 litros con más de 800 caballos de fuerza.","Solo se fabrican 2.000 unidades del modelo real.","Su versión Hot Wheels STH 2026 tiene el precio de reventa más alto del año."],"dato_clave":"El GTD es el primer Mustang con alerón activo y aerodinámica de competición."},"Drift-Ender":{"historia":"Diseñado como Super Treasure Hunt 2026, inspirado en los coches de drift japoneses. Su diseño aerodinámico y espectacular lo convirtió en el STH más buscado del año.","creacion":"Equipo de diseño de Mattel, inspirado en la cultura del drift y el tuning japonés.","conmemorativo":true,"curiosidades":["Es el Super Treasure Hunt más valioso de 2026.","Su diseño incluye un alerón trasero masivo y kit de carrocería agresivo.","Solo aparece en 1 de cada 20.000 cajas aproximadamente.","En eBay, los precios de reventa superan los US$250."],"dato_clave":"El Drift-Ender fue diseñado por el mismo equipo que creó el Hammerhead."},"Hammerhead":{"historia":"Diseñado por Tony Wu, lanzado en 2014. Su diseño inspirado en martillos y coches de carrera lo hizo único.","creacion":"Tony Wu, diseñador de Mattel especializado en vehículos fantásticos.","conmemorativo":false,"curiosidades":["Su nombre viene de la forma de martillo de la parte delantera.","Tiene 20+ variantes de color desde 2014.","Apareció en la serie 'Hot Wheels Battle Force 5'.","El diseño original era mucho más agresivo que el modelo final."],"dato_clave":"Tony Wu también diseñó el 'Sharkruiser' y el 'Silencer'."},"Nissan Skyline GT-R (BNR34)":{"historia":"El R34 Skyline es uno de los coches japoneses más icónicos de la historia. Su versión Hot Wheels ha sido lanzada múltiples veces desde 2011.","creacion":"Nissan, diseñado por Kozo Watanabe para la quinta generación del Skyline GT-R.","conmemorativo":false,"curiosidades":["Conocido como 'Godzilla' en Australia por su dominio en las carreras.","El R34 tiene el motor RB26DETT, uno de los motores más famosos de la historia.","Solo se fabricaron 13.045 unidades del V-Spec II Nür.","Su versión Hot Wheels más valiosa es la de 2011 en color Bayside Blue."],"dato_clave":"El R34 es el último Skyline GT-R antes de que la línea se separara del GT-R."},"Toyota AE86 Sprinter Trueno":{"historia":"El AE86 es legendario por su papel en el manga 'Initial D' y su manejo perfecto. Su versión Hot Wheels es una de las más buscadas por los fans del anime.","creacion":"Toyota, diseñado por Tetsuya Tada (también creador del GT86).","conmemorativo":false,"curiosidades":["Conocido como 'Hachi-Roku' (ocho-seis) en japonés.","Es tracción trasera con reparto de peso 50:50.","En 'Initial D', el personaje Takumi Fujiwara lo usa para repartir tofu.","Su versión Hot Wheels más buscada es la de 2013 en color blanco y negro."],"dato_clave":"El AE86 es el coche más asociado con la cultura del drift en todo el mundo."}}};const CASEBY={};
Object.keys(CAJ.cajas_por_anio).forEach(function(y){ (CAJ.cajas_por_anio[y]||[]).forEach(function(c){
  ["TH","STH"].forEach(function(t){ if(c[t]&&c[t].catalogo_id) CASEBY[c[t].catalogo_id]={letra:c.letra,anio:y,tipo:t}; }); }); });
const DEM={};
[["enero_2026",TEND.demanda_coleccionistas.enero_2026],["febrero_2026",TEND.demanda_coleccionistas.febrero_2026]]
 .forEach(function(pair){ pair[1].forEach(function(d){ (d.catalogo_ids||[]).forEach(function(cid){
   var prev=DEM[cid]; if(!prev||d.rank<prev.rank) DEM[cid]={rank:d.rank,modelo:d.modelo,coleccionistas:d.coleccionistas,mes:pair[0]}; }); }); });
const IMGV='40';
const VER=u=>{ if(!u) return u; if(u.indexOf('data:')===0) return u; return u + (u.indexOf('?')>=0?'&':'?') + 'v='+IMGV; };
/* Orientación: espejo para uniformar hacia dónde miran los autos.
   - ORIENT (si existe): dirección detectada por imagen  {id:{d:'IZQ'|'DER',c:conf}}
   - FLIPMAN: lo que el usuario fue volteando a mano (por casting)  {nombre:true}
   - state.dir: dirección elegida (DER por defecto) */
const ORI=(typeof ORIENT!=='undefined'&&ORIENT)?ORIENT:{};
let FLIPMAN={}; try{ FLIPMAN=JSON.parse(localStorage.getItem('hw_flip')||'{}')||{}; }catch(e){ FLIPMAN={}; }
const castingKey=c=>String((c&&(c.m||c.i))||'').replace(/\s*\(\d+(st|nd|rd|th) Color[^)]*\)\s*$/i,'').replace(/\s*\(Color Variant[^)]*\)\s*$/i,'').trim();
const FLIP=c=>{
  if(!c) return false;
  const k=castingKey(c);
  if(FLIPMAN[k]!==undefined) return !!FLIPMAN[k];
  const o=ORI[c.i]; if(!o||!o.d||(o.c||0)<0.55) return false;
  return o.d!==state.dir;
};
window.flipCar=function(ev,id){
  if(ev){ev.stopPropagation();ev.preventDefault();}
  const c=(typeof IDX!=='undefined'&&IDX[id])||(typeof CAT!=='undefined'&&CAT.find(x=>x.i===id));
  if(!c) return;
  const k=castingKey(c);
  const ahora=FLIP(c);
  FLIPMAN[k]=!ahora;
  try{ localStorage.setItem('hw_flip',JSON.stringify(FLIPMAN)); }catch(e){}
  render(true);
};
// URL que siempre se puede servir (sin proxy) para el reintento de onerror
const IMG_DIRECTA=f=>{
  if(!f) return '';
  if(f.indexOf('images.weserv.nl')!==-1) return f;
  if(/^https?:\/\//.test(f)) return f;
  return 'img/'+f;
};
// Placeholder profesional para modelos sin foto o fotos rotos.
// Silueta estilizada de auto Hot Wheels + texto, con vars CSS del tema.
// Regla: NUNCA dejar un bloque vacio ni un cuadro roto.
const noPhotoSVG=(w=178,h=178)=>{
  if(!noPhotoSVG._c){
    const s=getComputedStyle(document.documentElement);
    noPhotoSVG._c={
      bg:s.getPropertyValue('--surface').trim()||'#15181e',
      ev:s.getPropertyValue('--elev').trim()||'#1d2128',
      ln:s.getPropertyValue('--line').trim()||'#2a2f38',
      mu:s.getPropertyValue('--muted-foreground').trim()||'#98a1ad',
      ac:s.getPropertyValue('--accent').trim()||'#ff4d00',
      br:s.getPropertyValue('--brand').trim()||'#ff4d00'
    };
  }
  const _r=v=>+(Math.round(v*1000)/1000).toFixed(3); const c=noPhotoSVG._c, m=w*0.106;
  const cx=w/2, fy=h*0.74, r=w*0.073, wl=cx-w*0.25, wr=cx+w*0.25;
  const innerH=w-2*m-24, rx=w*0.034;
  const sv='<svg xmlns="http://www.w3.org/2000/svg" width="'+w+'" height="'+h+'" viewBox="0 0 '+w+' '+h+'">'+'<rect width="'+w+'" height="'+h+'" rx="'+_r(w*0.042)+'" fill="'+c.bg+'"/>'+'<rect x="'+m+'" y="'+m+'" width="'+_r(w-2*m)+'" height="'+_r(innerH)+'" rx="'+_r(rx)+'" fill="'+c.ev+'" stroke="'+c.ln+'" stroke-width="1"/>'+'<ellipse cx="'+_r(cx)+'" cy="'+_r(fy)+'" rx="'+_r((wr-wl)/2+12)+'" ry="'+_r(r*0.42)+'" fill="'+c.ac+'" opacity=".55"/>'+'<circle cx="'+_r(wl)+'" cy="'+_r(fy)+'" r="'+_r(r)+'" fill="'+c.br+'" opacity=".45"/>'+'<circle cx="'+_r(wr)+'" cy="'+_r(fy)+'" r="'+_r(r)+'" fill="'+c.br+'" opacity=".45"/>'+'<circle cx="'+_r(wl)+'" cy="'+_r(fy)+'" r="'+_r(r*0.4)+'" fill="'+c.bg+'"/>'+'<circle cx="'+_r(wr)+'" cy="'+_r(fy)+'" r="'+_r(r*0.4)+'" fill="'+c.bg+'"/>'+'<path d="M'+_r(cx-13)+' '+_r(fy-r*1.6)+' L'+_r(cx)+' '+_r(fy-r*2.4)+' L'+_r(cx+14)+' '+_r(fy-r*1.6)+' Z" fill="#ffffff" opacity=".75"/>'+'<text x="'+_r(cx)+'" y="'+_r(h-8)+'" font-size="11" fill="'+c.mu+'" text-anchor="middle" font-family="system-ui,monospace">Imagen próximamente</text>'+'</svg>';
  return 'data:image/svg+xml,'+encodeURIComponent(sv);
};
// Fallback de imagen: reintenta directo y, si tambien falla, deja el placeholder
// elegante. Garantiza que NUNCA quede un bloque vacio o roto en el DOM.
// data-fallback="1" marca la diferencia entre "el modelo no tiene foto" (diseno
// correcto) y "la foto existia pero no cargo" (fallo real, detectable en auditoria).
// Reintenta directo (weserv) y, si también falla, usa el placeholder profesional
// noPhotoSVG. NUNCA deja un <img> vacío ni queda un bloque roto.
// data-fallback="1" => foto existía pero no cargó (fallo real, auditoría).
const IMGFALLBACK=el=>{
  if(el.dataset.fallbackDone) return;
  const d=el.getAttribute('data-directo');
  if(d){ el.removeAttribute('data-directo'); el.src=d; return; }
  el.dataset.fallbackDone='1';
  el.onerror=null;
  el.classList.add('imgerr');
  el.setAttribute('data-fallback','1');
  const w=Math.max(parseInt(getComputedStyle(el).width)||178,120);
  el.src=noPhotoSVG(w,w);
};
const IMG=f=>{
  if(!f) return '';
  // Si ya viene proxeada por images.weserv.nl, devolverla tal cual (evita doble-proxy)
  if(f.indexOf('images.weserv.nl')!==-1) return VER(f);
  // Si ya es una URL absoluta de Wikia/Fandom, usar proxy images.weserv.nl
  // OJO: encodeURIComponent rompe la URL (codifica :// y weserv devuelve 404).
  // Se quita solo el prefijo http(s):// y se deja el resto intacto.
  // weserv NO resuelve nombres con %25 (el '%' literal de Fandom, ej. 'Bat - 1989 - 03 100%25.jpg'):
  // devuelve 404 aunque el archivo exista. Esos cargan directo desde Wikia.
  if(f.includes('static.wikia.nocookie.net')) {
    if(f.includes('%25')) return VER(f);
    return VER('https://images.weserv.nl/?url=' + f.replace(/^https?:\/\//i,''));
  }
  // Si ya es una URL absoluta http/https, devolver tal cual
  if(/^https?:\/\//.test(f)) return VER(f);
  // Si es ruta local
  return VER('img/'+f);
};
const CLS={
  'MAINLINE':{t:"Mainline",v:[1,5],d:[14,90],f:"hobbyDB listings 2024-2025"},
  'TREASURE HUNT':{t:"Treasure Hunt",v:[5,20],d:[7,30],f:"iCollectEverything 2026"},
  'SUPER TREASURE HUNT':{t:"Super Treasure Hunt",v:[85,250],d:[7,28],f:"autoevolution/resellcalendar 2024-2025"},
  'CAR CULTURE':{t:"Car Culture",v:[6.95,12.5],d:[7,28],f:"eBay listings 2024-2025"},
  'BOULEVARD':{t:"Boulevard",v:[8,12],d:[7,28],f:"eBay listings 2024-2025"},
  'POP CULTURE':{t:"Pop Culture",v:[7,14],d:[7,30],f:"eBay listings 2024-2025"},
  'TEAM TRANSPORT':{t:"Team Transport",v:[12,20],d:[14,40],f:"eBay listings 2024-2025"},
  'RETRO ENTERTAINMENT':{t:"Retro Entertainment",v:[7,14],d:[14,40],f:"eBay listings 2024-2025"},
  'RLC · RED LINE CLUB':{t:"RLC · Red Line Club",v:[29.99,84.99],d:[7,28],f:"99diecast.com 2024-2025"},
  'ELITE 64':{t:"Elite 64",v:[9,15],d:[14,40],f:"eBay listings 2024-2025"},
  'CONVENTION':{t:"Convention",v:[42.99,140],d:[7,28],f:"hobbyDB Blog 2022-2025"},
  'FIRST EDITIONS':{t:"First Editions",v:[2,8],d:[14,60],f:"eBay listings 2024-2025"},
  'NEW MODELS':{t:"New Models",v:[1.5,6],d:[14,60],f:"eBay listings 2024-2025"},
  'MYSTERY MODELS':{t:"Mystery Models",v:[3,10],d:[7,30],f:"eBay listings 2024-2025"},
  'CRACK-UPS':{t:"Crack-Ups",v:[2,6],d:[14,60],f:"eBay listings 2024-2025"},
  'ULTRA HOTS':{t:"Ultra Hots",v:[2,6],d:[14,60],f:"eBay listings 2024-2025"},
  'REAL RIDERS':{t:"Real Riders",v:[2,6],d:[14,60],f:"eBay listings 2024-2025"},
  'COLOR SHIFTERS':{t:"Color Shifters",v:[2,6],d:[14,60],f:"eBay listings 2024-2025"},
  'REDLINE':{t:"Redline",v:[50,3500],d:[30,180],f:"rarityfinder.com 2026"},
  '100% HOT WHEELS':{t:"100% Hot Wheels",v:[15,45],d:[14,60],f:"eBay listings 2024-2025"},
  'MONSTER TRUCKS':{t:"Monster Trucks",v:[4,12],d:[14,60],f:"eBay listings 2024-2025"},
  'SIZZLERS':{t:"Sizzlers",v:[2,6],d:[14,60],f:"eBay listings 2024-2025"},
  'STARSHIPS':{t:"Starships",v:[2,6],d:[14,60],f:"eBay listings 2024-2025"},
  'FLYING COLORS':{t:"Flying Colors",v:[2,6],d:[14,60],f:"eBay listings 2024-2025"},
  'VINTAGE':{t:"Vintage",v:[5,40],d:[14,90],f:"eBay listings 2024-2025"},
  'GRAN ESCALA':{t:"Gran Escala",v:[15,45],d:[14,60],f:"eBay listings 2024-2025"},
  'SPECIAL & EARLY':{t:"Special & Early",v:[2,6],d:[14,60],f:"eBay listings 2024-2025"},
  'COLLECTOR EXCLUSIVES':{t:"Collector Exclusives",v:[30,140],d:[7,28],f:"hobbyDB Blog 2022-2025"},
  'ZAMAC':{t:"ZAMAC",v:[4,12],d:[14,60],f:"eBay listings 2024-2025"}
};
/* fallback seguro: si una categoria no esta en CLS, usa Mainline (nunca rompe el drawer) */
const clsDe=(k)=>CLS[k]||CLS['MAINLINE']||{t:String(k||"Mainline"),v:[1,5],d:[14,90],f:""};
/* slug para clases CSS (categorias en MAYUSCULA -> kebab-case) */
const slugCat=(k)=>String(k||"").toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"");
const COND={"carded-nuevo":{l:"En tarjeta, nuevo",m:1.0},"carded-dañado":{l:"Tarjeta dañada",m:0.7},
 "loose-mint":{l:"Suelto, impecable",m:0.55},"loose-bueno":{l:"Suelto, buen estado",m:0.4},
 "loose-jugado":{l:"Suelto, jugado",m:0.25}};
const IDX={}; CAT.forEach(c=>IDX[c.i]=c);

/* ===== datos actualizados desde el puente (si hay) ===== */
const DATOS_FUENTE=(function(){
  const map={"catalog_web.json":"CAT","cajas.json":"CAJ","tendencias.json":"TEND","mercados.json":"MKT",
             "precios_referencia.json":"PRE","indice.json":"IDXI","owned_collection.json":"OWNED_DEMO","seguimiento.json":"SEG","historias.json":"HIST"};
  let ver=null,usados=0;
  try{ ver=JSON.parse(localStorage.getItem("hw_datos_version")||"null"); }catch(e){}
  if(!ver) return {origen:"integrados en la app",version:null,archivos:0};
  for(const k in map){
    try{
      const raw=localStorage.getItem("hw_datos_"+k); if(!raw) continue;
      const j=JSON.parse(raw);
      if(k==="catalog_web"){ CAT.length=0; j.forEach(c=>CAT.push(c)); }
      else if(k==="cajas"){ CAJ.cajas_por_anio=j.cajas_por_anio||{}; CAJ.codigos_base=j.codigos_base||CAJ.codigos_base||{}; }
      else if(k==="tendencias"){ TEND.demanda_coleccionistas=j.demanda_coleccionistas||TEND.demanda_coleccionistas; }
      else if(k==="mercados"){ MKT.monedas=j.monedas||MKT.monedas; MKT.mercados=j.mercados||MKT.mercados; MKT.calculadora_canales=j.calculadora_canales||MKT.calculadora_canales; }
      else if(k==="precios_referencia"){ PRE.precios=j.precios||PRE.precios; }
      else if(k==="indice"){ IDXI.estadisticas_catalogo=j.estadisticas_catalogo||IDXI.estadisticas_catalogo; }
      else if(k==="owned_collection"){ OWNED_DEMO.items=j.items||OWNED_DEMO.items; }
      else if(k==="seguimiento"){ SEG.modelos=j.modelos||SEG.modelos; }
      usados++;
    }catch(e){}
  }
  return {origen:usados?("actualizados desde el puente · v"+ver.version):"integrados en la app",version:ver.version,archivos:usados};
})();
Object.keys(IDX).forEach(k=>delete IDX[k]); CAT.forEach(c=>IDX[c.i]=c);
Object.keys(CASEBY).forEach(k=>delete CASEBY[k]);
Object.keys(CAJ.cajas_por_anio).forEach(function(y){ (CAJ.cajas_por_anio[y]||[]).forEach(function(c){
  ["TH","STH"].forEach(function(t){ if(c[t]&&c[t].catalogo_id) CASEBY[c[t].catalogo_id]={letra:c.letra,anio:y,tipo:t}; }); }); });
Object.keys(DEM).forEach(k=>delete DEM[k]);
[["enero_2026",TEND.demanda_coleccionistas.enero_2026],["febrero_2026",TEND.demanda_coleccionistas.febrero_2026]]
 .forEach(function(pair){ (pair[1]||[]).forEach(function(d){ (d.catalogo_ids||[]).forEach(function(cid){
   var prev=DEM[cid]; if(!prev||d.rank<prev.rank) DEM[cid]={rank:d.rank,modelo:d.modelo,coleccionistas:d.coleccionistas,mes:pair[0]}; }); }); });
let state={q:"",year:"",clase:"",serie:"",sort:"rel",page:0,per:60,tab:"catalogo",trending:false,dir:(localStorage.getItem("hw_dir")||"DER")};
let col={};

/* ===== moneda ===== */
let cur=(()=>{try{return localStorage.getItem("hwcur")||"CLP";}catch(e){return "CLP";}})();
function conv(usd,to){const m=MKT.monedas[to||cur];return usd*m.por_usd;}
function fmt(usd,to){
  const c=to||cur, m=MKT.monedas[c]; let v=usd*m.por_usd, s;
  if(m.decimales===0){ s=Math.round(v).toLocaleString("es-CL"); }
  else { s=v.toFixed(m.decimales); if(m.sep_dec===",") s=s.replace(".",","); }
  return m.simbolo+s;
}
const money=usd=>fmt(usd);
function setCur(c){cur=c;try{localStorage.setItem("hwcur",c);}catch(e){}
  render(true); renderCol(); renderVal(); renderMkt(); if(document.getElementById("drawer").dataset.open==="1"){/* mantener ficha */}}
function initCur(){
  const s=document.getElementById("cursel"); if(!s) return;
  s.innerHTML=Object.entries(MKT.monedas).map(([k,m])=>`<option value="${k}" ${k===cur?"selected":""}>${k} — ${m.nombre}</option>`).join("");
  s.onchange=()=>setCur(s.value);
  const m=MKT.monedas[cur];
  const n=document.getElementById("currate");
  if(n) n.innerHTML=`1 USD = ${m.simbolo}${m.por_usd.toLocaleString("es-CL")} ${cur} · <span style="opacity:.75">${m.fuente} (${m.fecha})</span>`;
}

/* ===== colección ===== */
function loadCol(){
  try{const s=localStorage.getItem("hwcol");if(s){col=JSON.parse(s);return;}}catch(e){}
  col={}; OWNED_DEMO.items.forEach(it=>{col[it.catalog_id]={q:it.cantidad,c:it.condicion,u:it.ubicacion||""};});
  saveCol();
}
function saveCol(){try{localStorage.setItem("hwcol",JSON.stringify(col));}catch(e){}}
const colCount=()=>Object.values(col).reduce((a,b)=>a+(b.q||0),0);
function valorRef(c,cond){const m=(c.v+c.V)/2,k=(COND[cond]||{m:1}).m;return{min:c.v*k,max:c.V*k,mid:m*k};}
function totales(){
  let min=0,max=0,units=0,byClass={},byYear={},items=0;
  Object.entries(col).forEach(([id,o])=>{const c=IDX[id];if(!c)return;const q=o.q||0;if(!q)return;
    const v=valorRef(c,o.c);min+=v.min*q;max+=v.max*q;units+=q;items++;
    byClass[c.k]=(byClass[c.k]||0)+q;byYear[c.y]=(byYear[c.y]||0)+q;});
  return {min,max,units,items,byClass,byYear};
}

/* ===== catálogo ===== */
function filtered(){
  const q=state.q.trim().toLowerCase();
  let r=CAT.filter(c=>{
    if(state.year&&String(c.y)!==state.year) return false;
    if(state.clase&&c.k!==state.clase) return false;
    if(state.serie&&c.s!==state.serie) return false;
    if(state.cat&&c.k!==state.cat) return false;
    if(state.pais&&c.pais!==state.pais) return false;
    if(state.trending&&!DEM[c.i]) return false;
    if(q&&!(c.m.toLowerCase().includes(q)||c.s.toLowerCase().includes(q)||String(c.t).toLowerCase().includes(q))) return false;
    return true;});
  if(state.sort==="ind") r.sort((a,b)=>b.x-a.x);
  else if(state.sort==="val") r.sort((a,b)=>b.V-a.V);
  else r.sort((a,b)=>b.y-a.y||String(a.c||"").localeCompare(String(b.c||"")));
  return r;
}
function cardHTML(c){
  const o=col[c.i], _slug=slugCat(c.k), badge=`<span class="chipc ${c.k!=="MAINLINE"?_slug:""}">${escT(c.k).toUpperCase()}</span>`;
  const qty=o&&o.q?`<span class="qty">×${o.q}</span>`:"";
  const dm=DEM[c.i];
  const pie=(dm?"TOP "+dm.rank:"")+(c.imr?(dm?" · ":"")+"imagen ref":"");
  const dbadge=pie?`<span class="dem">${pie}</span>`:"";
  const img=c.im?`<img alt="" class="thumb${FLIP(c)?' mirror':''}" loading="lazy" decoding="async" src="${escA(IMG(c.im))}" onerror="IMGFALLBACK(this)" data-directo="${escA(IMG_DIRECTA(c.im))}" style="background:linear-gradient(90deg,var(--elev) 25%,var(--surface) 50%,var(--elev) 75%);background-size:200% 100%;animation:shimmer 1.5s infinite">`:`><img alt="Sin foto: ${escA(c.m)}" class="thumb placeholder" loading="lazy" decoding="async" src="${noPhotoSVG(178,178)}" data-noimg="1">`;
  const flipBtn=`<button class="cardflip${FLIP(c)?' on':''}" onclick="flipCar(event,'${escJ(c.i)}')" title="Voltear este auto (efecto espejo)">⇄</button>`;
  const editBtn=o&&o.q?`<button class="cardedit" onclick="event.stopPropagation();editCar('${escJ(c.i)}')" title="Editar">✎</button>`:"";
  const delBtn=o&&o.q?`<button class="carddel" onclick="event.stopPropagation();if(confirm('Eliminar ${escJ(c.m)}?'))delCar('${escJ(c.i)}')" title="Eliminar">×</button>`:"";
  const bandera=c.pais?`<div style="position:absolute;bottom:4px;right:4px;font-size:14px;background:rgba(0,0,0,.5);border-radius:4px;padding:2px 4px">${c.pais.includes('Malaysia')?'🇲🇾':c.pais.includes('Thailand')?'🇹🇭':c.pais.includes('China')?'🇨🇳':c.pais.includes('Hong Kong')?'🇭🇰':c.pais.includes('USA')?'🇺🇸':'🏳️'}</div>`:'';
  const catLogo=catLogoSVG(c.k);
  const paisInfo=c.pais?`<span style="color:var(--muted-foreground);font-size:11px"> · ${escT(c.pais)}</span>`:'';
  return `<div class="cardwrap">${flipBtn}${editBtn}${delBtn}<button class="card" data-id="${escA(c.i)}">${badge}${qty}${dbadge}${catLogo}${img}${bandera}<div class="body">
    <div class="nm">${escT(c.m)}</div><div class="mt">${c.y} · #${escT(c.c)} · ${escT(c.t)}${paisInfo}</div>
    <div class="idx"><i style="width:${c.x}%;background:${nivelColor(c.x)}"></i></div>
    <div class="idxrow"><span>Índice ${c.x}</span><span>${fmt(c.v)}–${fmt(c.V)}</span></div></div></button></div>`;
}
function render(reset){
  const g=document.getElementById("grid"); if(!g) return;
  const list=filtered();
  if(reset){g.innerHTML="";state.page=0;}
  const start=state.page*state.per, slice=list.slice(start,start+state.per);
  if(!slice.length&&!start) g.innerHTML=`<div class="empty">Sin resultados con estos filtros.</div>`;
  slice.forEach(c=>g.insertAdjacentHTML("beforeend",cardHTML(c)));
  state.page++;
  const more=document.getElementById("more");
  if(more) more.textContent=(state.page*state.per<list.length)?`Mostrando ${Math.min(state.page*state.per,list.length)} de ${list.length}`:`Fin · ${list.length} autos`;
  const rc=document.getElementById("rescount"); if(rc) rc.textContent=list.length.toLocaleString("es");
  const tc=document.getElementById("totcount"); if(tc) tc.textContent=CAT.length.toLocaleString("es");
  const ic2=document.getElementById("imgcount");
  if(ic2) ic2.innerHTML="<b>"+CAT.filter(c=>c.im).length.toLocaleString("es")+"</b> con imagen ("+CAT.filter(c=>c.imr).length+" de referencia)";
}

/* ===== ficha ===== */
function bestChannels(usd,top){
  return MKT.calculadora_canales.map(c=>{
    const pct=c.pct+(c.extra_pct||0);
    return {canal:c.canal,mercado:c.mercado,neto:usd-(usd*pct+c.fijo_usd)};
  }).sort((a,b)=>b.neto-a.neto).slice(0,top||3);
}
function _hist(nombre){ try{ return (HIST && HIST.modelos && HIST.modelos[nombre]) || null; }catch(e){ return null; } }
function drawer(id){
  const c=IDX[id]; if(!c) return;
  const o=col[id]||{q:0,c:"carded-nuevo",u:""}, det=c.indice_detalle||{};
  const bar=(l,v)=>`<div class="fbar"><span>${l}</span><span class="fill"><i style="width:${v}%"></i></span><span class="num">${v}</span></div>`;
  const v=valorRef(c,o.c), mid=(c.v+c.V)/2;
  const bc=bestChannels(mid,3);
  const f=c.ficha||{}, vm=c.valores_mercado||{}, idx=c.indice_coleccionabilidad;
  const catDesc=c.categoria_descripcion?'<div class="note" style="margin-top:6px;font-size:11px;color:var(--muted)">'+escT(c.categoria_descripcion)+'</div>':'';
  const disenador=c.diseñador?DISENADORES[c.diseñador]:null;
  let disHTML='';
  if(disenador){
    let bio='';
    if(disenador.biografia_limpia) bio='<div class="note" style="margin-top:6px;font-size:12px;line-height:1.5">'+escT(disenador.biografia_limpia)+'</div>';
    let per='';
    if(disenador.periodo) per='<div class="note" style="margin-bottom:6px"><b>Período:</b> '+escT(disenador.periodo)+'</div>';
    disHTML='<div class="sec" style="border:1px solid var(--brand);padding:12px;margin-bottom:10px"><h3 style="margin:0 0 8px">Diseñador</h3><div style="font-size:16px;font-weight:600">'+escT(c.diseñador)+'</div><div class="note" style="margin-bottom:6px"><b>Nacionalidad:</b> '+escT(disenador.nacionalidad)+'</div>'+per+bio+'</div>';
  }
  const flang=(typeof document!=='undefined'&&document.documentElement.lang)||'es';
  const fSel=(f[flang]&&Object.keys(f[flang]).length)?f[flang]:f;
  const fichaHTML=(fSel.descripcion||fSel.historia||fSel.curiosidades)?`<div class="sec" style="border:1px solid var(--line);padding:12px;margin-bottom:10px"><h3 style="margin:0 0 8px">Ficha del modelo</h3>${fSel.descripcion?'<div style="margin-bottom:6px"><b>Descripción:</b> '+escT(fSel.descripcion)+'</div>':''}${fSel.historia?'<div style="margin-bottom:6px"><b>Historia:</b> '+escT(fSel.historia)+'</div>':''}${fSel.curiosidades?'<div style="margin-bottom:6px"><b>Curiosidades:</b> '+escT(fSel.curiosidades)+'</div>':''}${fSel.conmemorativo?'<div style="margin-bottom:6px"><b>Conmemorativo:</b> Sí</div>':''}${fSel.dato_clave?'<div><b>Dato clave:</b> '+escT(fSel.dato_clave)+'</div>':''}${catDesc}</div>`:'';
  const idxHTML=idx?`<div class="sec" style="border:1px solid var(--line);padding:12px;margin-bottom:10px"><h3 style="margin:0 0 8px">Índice de coleccionabilidad</h3><div style="font-size:24px;font-weight:700;color:var(--brand)">${idx}</div><div class="note" style="margin-bottom:10px">de 100</div>${Object.keys(det).map(k=>bar(det[k].l,det[k].v)).join('')}</div>`:'';
  const vmHTML=vm.usd?`<div class="sec" style="border:1px solid var(--line);padding:12px;margin-bottom:10px"><h3 style="margin:0 0 8px">Valores de mercado</h3><div style="font-size:13px"><b>USD:</b> $${vm.usd} · <b>CLP:</b> $${vm.clp} · <b>EUR:</b> €${vm.eur}</div><div class="note" style="font-size:10px;margin-top:4px">Fuente: ${escT(vm.fuente||'Cálculo automático')} · ${escT(vm.fecha||'')}</div></div>`:'';
  const d=document.getElementById("drawer");
  d.dataset.open="1"; d.classList.add("open");
  d.innerHTML=`<button class="close" onclick="closeDrawer()">×</button>
    <div class="dh"><img class="${FLIP(c)?'mirror':''}" src="${c.im?escA(IMG(c.im)):escA(noPhotoSVG(120,120))}" alt="${c.im?escA(c.m):escA('Sin foto: '+c.m)}" onerror="IMGFALLBACK(this)" data-directo="${c.im?escA(IMG_DIRECTA(c.im)):escA(noPhotoSVG(120,120))}">
      <div><h2>${escT(c.m)} ${catLogoSVG(c.k)}</h2>
        <div class="mt">${c.y} · Nº de colección ${escT(c.c)} · Toy # ${escT(c.t)}</div>
        ${disHTML}${fichaHTML}${galeriaHTML(c)}${idxHTML}${vmHTML}
       <div class="mt">${escT(c.s)} ${c.n?"("+escT(c.n)+")":""}</div>
       <div class="mt">${escT(clsDe(c.k).t)}${c.nuevo?" · Nuevo modelo":""}${c.variante?" · Variante de color":""}</div></div></div>
   <div class="kv">
     <span class="k">Índice</span><span class="v">${c.x} / 100</span>
     <span class="k">Historia</span><span class="v" style="font-size:13px;line-height:1.5">${_hist(c.m)?.historia||"Sin datos históricos para este modelo."}</span>
     <span class="k">Curiosidades</span><span class="v" style="font-size:13px;line-height:1.5">${_hist(c.m)?.curiosidades?.map(x=>"• "+x).join("<br>")||"—"}</span>
     <span class="k">¿Conmemorativo?</span><span class="v">${_hist(c.m)?.conmemorativo?"Sí":"No"}</span>
     <span class="k">Dato clave</span><span class="v" style="font-size:13px;line-height:1.5">${_hist(c.m)?.dato_clave||"—"}</span>
     <span class="k">Valor ref.</span><span class="v">${fmt(c.v)} – ${fmt(c.V)}</span>
     <span class="k">En USD / CLP / EUR</span><span class="v" style="font-size:11.5px">US$${(c.v||0).toFixed(2)}–${(c.V||0).toFixed(2)} · $${Math.round(conv(c.v,"CLP"))}–${Math.round(conv(c.V,"CLP"))} · €${conv(c.v,"EUR").toFixed(2)}–${conv(c.V,"EUR").toFixed(2)}</span>
     <span class="k">Venta estimada</span><span class="v">${clsDe(c.k).d[0]}–${clsDe(c.k).d[1]} días</span>
     <span class="k">Caja</span><span class="v">${CASEBY[id]?("Caja "+CASEBY[id].letra+" ("+CASEBY[id].anio+") · "+(CASEBY[id].tipo==="STH"?"Super Treasure Hunt":"Treasure Hunt")):"—"}</span>
     <span class="k">Imagen</span><span class="v" style="font-family:var(--f-body);font-size:11.5px">${c.imr?"referencia del casting (no necesariamente del año/color exacto)":"foto de la ficha del año"}</span>
     <span class="k">Fuente valor</span><span class="v" style="font-family:var(--f-body);font-size:11.5px">${clsDe(c.k).f}</span></div>
   <div class="sec"><h3>Índice de coleccionabilidad ${c.x} / 100</h3>
     <div style="display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-bottom:6px">
       <div style="text-align:center">${donut(c.x,c.px||0)}<div class="note" style="font-size:10px">fórmula v2</div></div>
       <div style="flex:1;min-width:210px">${radar(c.f||[0,0,0,0,0])}</div>
     </div>
     ${barrasFactores(c)}
     <div class="note" style="margin-top:10px">Dónde cae este auto dentro del catálogo (2.177 registros):</div>
     ${histo(c.x)}
     <div class="metodo"><b>Fórmula:</b> ${IDXINFO.formula}<br>
       <b>Mediana del catálogo:</b> ${IDXINFO.estadisticas_catalogo.mediana} · <b>p90:</b> ${IDXINFO.estadisticas_catalogo.p90} · <b>máximo:</b> ${IDXINFO.estadisticas_catalogo.max}<br>
       <b>Fuente de la demanda:</b> HW Price Guide (rankings reales de enero y febrero 2026) cuando está medida; si no, proxi por re-ediciones del casting. La ficha marca <span class="medido">medido</span> cuando el dato es real.<br>
       <b>Condición:</b> en el catálogo se asume “nuevo en tarjeta”; en tu colección se ajusta con tu condición real.</div></div>
   <div class="sec"><h3>Mejores canales para vender (mediana ${fmt(mid)})</h3>
     <table class="t"><tbody>${bc.map((x,i)=>`<tr class="${i===0?"best":""}"><td>${x.canal}</td><td class="num">${fmt(x.neto)}</td></tr>`).join("")}</tbody></table>
     <div class="note" style="margin-top:8px">Neto después de comisión y cargo fijo. No incluye envío ni impuestos. Comisiones en <b>data/mercados.json</b>.</div></div>
   <div class="sec"><h3>En mi colección</h3>
     <div class="rowin" style="gap:12px">
       <div class="stepper"><button onclick="bump('${escJ(id)}',-1)">−</button><span class="q" id="dq">${o.q||0}</span><button onclick="bump('${escJ(id)}',1)">+</button></div>
       <select id="dcond" onchange="setCond('${id}',this.value)">${Object.entries(COND).map(([k,vv])=>`<option value="${k}" ${o.c===k?"selected":""}>${vv.l} (×${vv.m})</option>`).join("")}</select>
       <input type="text" id="dloc" placeholder="Ubicación" value="${o.u||""}" onchange="setLoc('${id}',this.value)" style="max-width:170px"></div>
     <div class="note" style="margin-top:10px">Valor de TU ejemplar: <b>${fmt(v.min)} – ${fmt(v.max)}</b> · mediana ${fmt(v.mid)}</div>
     <div class="warn">Estimación de confianza BAJA: es un rango por clase, no comparables del modelo exacto.</div></div>
   <div class="btnrow"><button class="btn" onclick="speak('${escJ(id)}')">Escuchar ficha</button>
     <button class="btn ghost" onclick="closeDrawer()">Cerrar</button></div>`;
  d.dataset.open="1";
}
function closeDrawer(){document.getElementById("drawer").dataset.open="0";}
function bump(id,n){const o=col[id]||{q:0,c:"carded-nuevo",u:""};o.q=Math.max(0,(o.q||0)+n);
  if(!o.q)delete col[id];else col[id]=o;saveCol();refreshAll();
  const el=document.getElementById("dq");if(el)el.textContent=(col[id]?col[id].q:0);}
function setCond(id,v){const o=col[id]||{q:1,c:v,u:""};o.c=v;o.q=o.q||1;col[id]=o;saveCol();refreshAll();drawer(id);}
function setLoc(id,v){const o=col[id]||{q:1,c:"carded-nuevo",u:""};o.u=v;col[id]=o;saveCol();}
function addById(id,n){const o=col[id]||{q:0,c:"carded-nuevo",u:""};o.q=(o.q||0)+n;col[id]=o;saveCol();refreshAll();}
function editCar(id){
  const o=col[id]; if(!o) return;
  const c=IDX[id]; if(!c) return;
  const d=document.getElementById("drawer");
  d.dataset.open="1"; d.classList.add("open");
  d.innerHTML=`<button class="close" onclick="closeDrawer()">×</button>
   <div class="dh"><img alt="" src="${escA(IMG(c.im))}" onerror="IMGFALLBACK(this)" data-directo="${escA(IMG_DIRECTA(c.im))}"><div><h2>Editar: ${c.m}</h2><div class="mt">${c.y} · #${c.c}</div></div></div>
   <div class="sec" style="border:1px solid var(--line);padding:12px;margin-bottom:10px">
     <h3 style="margin-bottom:8px">Cantidad</h3>
     <div class="rowin"><button class="stepper" onclick="editQty('${escJ(id)}',-1)">−</button><span class="stepper q" id="eq">${o.q||0}</span><button class="stepper" onclick="editQty('${escJ(id)}',1)">+</button></div>
   </div>
   <div class="sec" style="border:1px solid var(--line);padding:12px;margin-bottom:10px">
     <h3 style="margin-bottom:8px">Condición</h3>
     <select id="ec" style="width:100%;padding:8px;background:var(--elev);color:var(--ink);border:1px solid var(--line);border-radius:4px">
       ${Object.entries(COND).map(([k,v])=>`<option value="${k}"${o.c===k?" selected":""}>${v.l}</option>`).join("")}
     </select>
   </div>
   <div class="sec" style="border:1px solid var(--line);padding:12px;margin-bottom:10px">
     <h3 style="margin-bottom:8px">Ubicación</h3>
     <input id="eu" value="${o.u||""}" placeholder="Ej: Caja A, Estante 3" style="width:100%;padding:8px;background:var(--elev);color:var(--ink);border:1px solid var(--line);border-radius:4px">
   </div>
   <div class="sec" style="border:1px solid var(--line);padding:12px;margin-bottom:10px">
     <h3 style="margin-bottom:8px">Notas</h3>
     <textarea id="en" rows="2" style="width:100%;padding:8px;background:var(--elev);color:var(--ink);border:1px solid var(--line);border-radius:4px">${o.notas||""}</textarea>
   </div>
   <div class="sec" style="border:1px solid var(--line);padding:12px;margin-bottom:10px">
     <h3 style="margin-bottom:8px">Subcolección</h3>
     <input id="es" value="${o.subcoleccion||""}" placeholder="Ej: Muscle Cars, JDM, STH 2026..." style="width:100%;padding:8px;background:var(--elev);color:var(--ink);border:1px solid var(--line);border-radius:4px">
   </div>
   <div class="btnrow">
     <button class="btn" onclick="saveEdit('${escJ(id)}')">Guardar</button>
     <button class="btn ghost" onclick="closeDrawer()">Cancelar</button>
   </div>
   <div style="margin-top:10px"><button class="btn ghost" style="color:#e74c3c;border-color:#e74c3c" onclick="delCar('${escJ(id)}')">Eliminar de mi colección</button></div>`;
}
function editQty(id,n){const o=col[id];o.q=Math.max(0,(o.q||0)+n);document.getElementById("eq").textContent=o.q;}
function saveEdit(id){
  const o=col[id]; if(!o) return;
  o.c=document.getElementById("ec").value;
  o.u=document.getElementById("eu").value;
  o.notas=document.getElementById("en").value;
  o.subcoleccion=document.getElementById("es").value;
  saveCol(); closeDrawer(); refreshAll();
  logMsg("i","Cambios guardados.");
}
function delCar(id){
  if(!confirm("¿Eliminar este auto de tu colección?")) return;
  delete col[id]; saveCol(); closeDrawer(); refreshAll();
  logMsg("a","Auto eliminado de tu colección.");
}

/* ===== voz ===== */
function tts(text){
  if(!("speechSynthesis" in window)){logMsg("a","Tu navegador no soporta síntesis de voz.");return;}
  speechSynthesis.cancel();
  const u=new SpeechSynthesisUtterance(text);
  const vs=speechSynthesis.getVoices();
  const es=vs.find(v=>/es[-_]/i.test(v.lang))||vs.find(v=>/^es/i.test(v.lang));
  if(es) u.voice=es;
  u.lang=es?es.lang:"es-ES"; u.rate=1.0;
  speechSynthesis.speak(u);
}
function hablarMoneda(usd){
  const c=cur;
  const nombres={USD:"dólares",CLP:"pesos chilenos",EUR:"euros",GBP:"libras"};
  return `${Math.round(conv(usd))} ${nombres[c]||c}`;
}
function speak(id){
  const c=IDX[id]; if(!c) return;
  tts(guion(c, col[id]||{q:0,c:"carded-nuevo"}));
}
function logMsg(who,text,src){
  const l=document.getElementById("log"); if(!l) return;
  l.insertAdjacentHTML("beforeend",`<div class="msg ${who}">${text}${src?`<span class="src">${src}</span>`:""}</div>`);
  l.scrollTop=l.scrollHeight;
}
/* ===== asistente ===== */
function buscar(txt){
  const q=txt.toLowerCase().replace(/[¿?¡!]/g,"").trim();
  const stop=["cuanto","vale","cuesta","busca","buscar","dime","sobre","el","la","los","las","un","una","de","del","auto","autos","hot","wheels","precio","valor","tengo","cuantos","agrega","añade","agregar","en","pesos","dolares","dólares","euros"];
  const words=q.split(/\s+/).filter(w=>w.length>2&&!stop.includes(w));
  if(!words.length) return null;
  let best=null,score=0;
  CAT.forEach(c=>{const m=c.m.toLowerCase();let s=0;words.forEach(w=>{if(m.includes(w))s+=w.length;});if(s>score){score=s;best=c;}});
  return score>=3?best:null;
}
function responder(txt){
  logMsg("u",txt);
  const t=txt.toLowerCase();
  const mc=t.match(/caja\s*([a-q])\b/)||t.match(/case\s*([a-q])\b/);
  if(mc&&/trae|contiene|sale|hay|tiene|viene/.test(t)){
    const L=mc[1].toUpperCase();
    const anio=(t.match(/20\d\d/)||[])[0]||cajYear;
    const c=(CAJ.cajas_por_anio[anio]||[]).filter(function(x){return x.letra===L;})[0];
    if(c){
      const th=c.TH?("<b>TH: "+c.TH.modelo+"</b> ("+c.TH.serie+" · "+c.TH.col+")"):"TH: sin dato publicado";
      const sth=c.STH?("<b>STH: "+c.STH.modelo+"</b> ("+c.STH.serie+" · "+c.STH.col+" · "+c.STH.color+")"):"STH: sin dato";
      logMsg("a","Caja "+L+" de "+anio+" → "+th+" · "+sth+". Recordá: cada caja trae ~72 autos con duplicados y una sola TH.",
        "Fuente: Hot Wheels Wiki (columna Case/Wave) + hotwheelstreasure.com");
      tts("La caja "+L+" de "+anio+" trae la Treasure Hunt "+c.TH.modelo+(c.STH?", y la Super Treasure Hunt "+c.STH.modelo:"")+".");
      return;
    }
    logMsg("a","No tengo datos de la caja "+L+" para "+anio+". Las letras publicadas son A, B, C, D, E, F, G, H, J, K, L, M, N, P y Q.","");return;
  }
  const mb=t.match(/([a-z])\s*-?\s*(\d{1,2})\b/);
  if(mb&&/c[oó]digo|base|fabricad|significa|a[nñ]o/.test(t)){
    const anio=CAJ.codigos_base.letra_a_anio[mb[1].toUpperCase()], sem=parseInt(mb[2],10);
    if(anio&&sem>=1&&sem<=53){
      logMsg("a","El código "+mb[1].toUpperCase()+sem+" indica fabricación en <b>"+anio+"</b>, semana <b>"+sem+"</b>.",
        "Fuente: Hot Wheels Wiki — Base codes");
      tts("Ese código es del año "+anio+", semana "+sem+".");return;
    }
  }
  if(/peso|chile|clp/.test(t)&&/cu[aá]nto|vale|precio/.test(t)){
    const c=buscar(txt);
    if(c){logMsg("a",`<b>${c.m}</b> (${c.y}): ${fmt(c.v)} – ${fmt(c.V)} en pesos chilenos, o sea US$${(c.v||0).toFixed(2)}–${(c.V||0).toFixed(2)}. `+
      `Tipo de cambio: 1 USD = $${MKT.monedas.CLP.por_usd.toLocaleString("es-CL")} (mindicador.cl, ${MKT.monedas.CLP.fecha}).`,
      "Fuente: catálogo Hot Wheels Wiki + rangos por clase (confianza baja)");
      tts(`${c.m}. Entre ${hablarMoneda(c.v)} y ${hablarMoneda(c.V)}.`);return;}
  }
  if(/impuesto|aduana|importar|traer de|arancel/.test(t)){
    logMsg("a",`Traer autos a Chile: hasta <b>US$500</b> pagás <b>solo IVA 19%</b> (sin arancel). Sobre US$500: <b>6% de arancel + 19% de IVA</b> sobre el CIF. `+
      `Envíos entre personas (C2C) de hasta US$500 son <b>exentos</b> si son ocasionales y no comerciales. Para Europa, desde el 1-jul-2026 hay un <b>arancel fijo de €3 por ítem</b> en envíos de hasta €150, más IVA.`,
      "Fuente: aduana.cl y sii.cl (Ley 21.713, vigente 25-oct-2025) · taxation-customs.ec.europa.eu");
    tts("Hasta quinientos dólares pagás solo el diecinueve por ciento de IVA. Sobre ese monto se suma un seis por ciento de arancel.");return;
  }
  if(/d[oó]nde vendo|mejor mercado|donde vender|conviene vender|vender/.test(t)){
    const T=totales(), mid=(T.min+T.max)/2/(T.units||1);
    const bc=bestChannels(mid,3);
    logMsg("a",`Para una pieza de ${fmt(mid)} los mejores canales son: `+bc.map((x,i)=>`<b>${i+1}. ${x.canal}</b> (${fmt(x.neto)})`).join(" · ")+
      `. Recordá: eBay EE.UU. cobra 13,25%+US$0,40, MercadoLibre Chile 8–17% + cargo fijo, y en el Reino Unido los particulares pagan 0%.`,
      "Fuente: data/mercados.json (comisiones verificadas: eBay, MercadoLibre CL, Mercado Pago)");
    tts(`El mejor canal para esa pieza es ${bc[0].canal}, con un neto de ${hablarMoneda(bc[0].neto)}.`);return;
  }
  if(/colecci[oó]n|cu[aá]ntos tengo|mi coleccion/.test(t)){
    const T=totales();
    logMsg("a",`Tenés <b>${T.units}</b> autos en ${T.items} modelos distintos. Valor de referencia: <b>${fmt(T.min)} – ${fmt(T.max)}</b>. `+
      `Ese rango asume venta pieza por pieza; en lote completo aplicá 50–70% de descuento.`,
      "Fuente: data/owned_collection.json + rangos por clase (confianza baja)");
    tts(`Tenés ${T.units} autos en tu colección. El valor de referencia está entre ${hablarMoneda(T.min)} y ${hablarMoneda(T.max)}.`);return;
  }
  const c=buscar(txt);
  if(c){
    const o=col[c.i]||{q:0};
    logMsg("a",`<b>${c.m}</b> (${c.y}, #${c.c}, ${c.s}). Clase ${clsDe(c.k).t}. Índice ${c.x}/100. `+
      `Valor ref. ${fmt(c.v)}–${fmt(c.V)}. Venta estimada ${clsDe(c.k).d[0]}-${clsDe(c.k).d[1]} días. Tenés ×${o.q||0}.`,
      "Fuente: Hot Wheels Wiki (catálogo) + rangos por clase (confianza baja)");
    tts(`${c.m}, año ${c.y}. Índice ${c.x}. Entre ${hablarMoneda(c.v)} y ${hablarMoneda(c.V)}.`);return;
  }
  logMsg("a","No encontré ese modelo en el catálogo de 4.214 registros (1968-2027). Probá con el nombre exacto: <i>Skyline</i>, <i>El Camino</i>, <i>Mustang GTD</i>. También podés preguntar cuánto pago de impuestos si lo traigo o dónde conviene vender.");
  if(iaKey()) preguntarIA(txt);
}

/* ===== IA para preguntas abiertas (Groq free tier) ===== */
const GROQ_URL="https://api.groq.com/openai/v1/chat/completions";
const GROQ_MODEL="openai/gpt-oss-120b";
function iaKey(){ try{ return localStorage.getItem("hw_ia_key")||""; }catch(e){ return ""; } }
function setIaKey(v){
  v=(v||"").trim();
  try{ localStorage.setItem("hw_ia_key",v); }catch(e){}
  const s=document.getElementById("iainfo");
  if(s) s.innerHTML = v ? "IA activada con <b>Groq</b> (1.000 consultas/día gratis). La key queda solo en este navegador."
                        : "Sin key: el asistente responde solo con el catálogo. Con key: además responde preguntas abiertas con IA.";
  logMsg("i", v ? "API key guardada en este navegador (nunca se sube al repositorio)." : "API key borrada.");
}
function contextoAuto(c){
  if(!c) return "";
  const h=_hist(c.m);
  return "Auto del catálogo: "+c.m+", año "+c.y+", nº de colección "+c.c+", toy "+c.t+", serie "+c.s+
    ", clase "+c.k+" ("+clsDe(c.k).t+"), índice de coleccionabilidad "+c.x+"/100 (percentil "+c.px+
    "), valor de referencia US$"+c.v+"-"+c.V+", venta estimada "+clsDe(c.k).d[0]+"-"+clsDe(c.k).d[1]+" días."+
    (h?" Historia: "+h.historia:"");
}
async function preguntarIA(texto){
  const key=iaKey();
  if(!key){
    logMsg("a","Para preguntas abiertas necesitás una API key gratuita de <b>Groq</b>: entrá a <b>console.groq.com</b>, creá una key (sin tarjeta) y pegala en el campo “IA” del panel de arriba.");
    return;
  }
  logMsg("i","Consultando a la IA…");
  const c=buscar(texto);
  const sys="Sos un asistente experto en Hot Wheels para un coleccionista chileno. Respondés en español de Chile, breve (máximo 120 palabras), con datos concretos y sin relleno. NO inventes precios ni datos: si no sabés algo, decilo. Rangos reales de referencia: Mainline US$1-5, Treasure Hunt US$5-20, Super Treasure Hunt US$85-250. El catálogo del usuario tiene 4.214 registros (1968-2027). "+contextoAuto(c);
  try{
    const r=await fetch(GROQ_URL,{method:"POST",
      headers:{"Content-Type":"application/json","Authorization":"Bearer "+key},
      body:JSON.stringify({model:GROQ_MODEL,temperature:0.6,max_tokens:400,
        messages:[{role:"system",content:sys},{role:"user",content:texto}]})});
    if(!r.ok){
      const e=await r.text();
      const msg = r.status===401 ? "La API key no es válida. Revisala en console.groq.com."
                : r.status===429 ? "Se agotó la cuota gratuita del día (1.000 consultas). Se renueva mañana."
                : ("Error "+r.status+": "+e.slice(0,140));
      logMsg("a","La IA no pudo responder. "+msg); return;
    }
    const j=await r.json();
    const resp=j.choices&&j.choices[0]&&j.choices[0].message?j.choices[0].message.content.trim():"";
    if(resp){ logMsg("a","<b>IA:</b> "+resp.replace(/\n/g,"<br>"),"Fuente: Groq · "+GROQ_MODEL); tts(resp); }
    else logMsg("a","La IA no devolvió respuesta.");
  }catch(e){ logMsg("a","No se pudo conectar con la IA: "+e.message); }
}
function stt(){
  const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  if(!SR){logMsg("a","Tu navegador no soporta reconocimiento de voz (usá Chrome o Edge). Podés escribir la pregunta.");return;}
  const r=new SR(); r.lang="es-ES"; r.interimResults=false; r.maxAlternatives=1;
  r.onresult=e=>{const t=e.results[0][0].transcript;document.getElementById("q2").value=t;responder(t);};
  r.onerror=e=>logMsg("a","Error de micrófono: "+e.error);
  r.start(); logMsg("a","Escuchando…");
}

/* ===== escáner (flujo) ===== */
function scanFile(inp){
  const f=inp.files&&inp.files[0]; if(!f) return;
  const url=URL.createObjectURL(f);
  document.getElementById("scanbox").innerHTML=`<img alt="" src="${url}" style="max-width:100%;max-height:260px;border:1px solid var(--line)">`;
  document.getElementById("scanout").innerHTML=`<div class="note">Foto cargada: <b>${f.name}</b>. En este prototipo la identificación automática por IA no está conectada: el plan (§5 y §7) especifica el backend con Gemini 2.5 Flash + CLIP + OCR del blister. Acá se simula el flujo real: escribí el modelo y confirmá el match.</div>`;
}
function doScanSearch(){
  const c=buscar(document.getElementById("scanq").value), o=document.getElementById("scanout");
  if(!c){o.innerHTML+=`<div class="warn">Sin match. Probá con otro nombre.</div>`;return;}
  o.innerHTML=`<div class="sec" style="border:1px solid var(--line);padding:12px">
    <div style="display:flex;gap:12px"><img alt="" src="${IMG(c.im)}" style="width:90px;height:90px;object-fit:contain;background:var(--elev)">
    <div><b>${c.m}</b><div class="mt">${c.y} · #${c.c} · ${c.s}</div><div class="mt">Índice ${c.x} · ${fmt(c.v)}–${fmt(c.V)}</div></div></div>
    <div class="btnrow" style="padding:12px 0 0"><button class="btn" onclick="addById('${escJ(c.i)}',1);render(true)">Confirmar y agregar a mi colección</button></div></div>`;
}

/* ===== escáner de código de barras con cámara ===== */
let scanStream=null, scanInterval=null;
async function startScan(){
  const o=document.getElementById("scanout");
  if(!o) return;
  if(!navigator.mediaDevices||!navigator.mediaDevices.getUserMedia){
    o.innerHTML=`<div class="warn">Tu navegador no soporta acceso a la cámara. Usá Chrome o Edge en HTTPS.</div>`; return;
  }
  try{
    scanStream=await navigator.mediaDevices.getUserMedia({video:{facingMode:"environment"}});
    const v=document.createElement("video");
    v.autoplay=true; v.playsInline=true; v.srcObject=scanStream;
    v.style.cssText="width:100%;max-height:200px;border-radius:8px;background:#000";
    o.innerHTML=""; o.appendChild(v);
    o.insertAdjacentHTML("beforeend",`<div class="note" style="margin-top:6px">Apuntá al código de barras del auto o de la caja. Se detecta solo.</div>`);
    const detector=("BarcodeDetector" in window)?new BarcodeDetector({formats:["ean_13","ean_8","upc_a","upc_e","code_128","code_39","qr_code"]}):null;
    if(!detector){o.innerHTML+=`<div class="warn">Tu navegador no tiene BarcodeDetector. Usá Chrome en Android o Edge.</div>`; return;}
    scanInterval=setInterval(async()=>{
      try{
        const codes=await detector.detect(v);
        if(codes&&codes.length){
          const code=codes[0].rawValue;
          stopScan();
          const match=CAT.find(c=>c.t===code||c.c===code||(c.barcode&&c.barcode===code));
          if(match){
            o.innerHTML=`<div class="sec" style="border:1px solid var(--line);padding:12px">
              <div style="display:flex;gap:12px"><img alt="" src="${IMG(match.im)}" style="width:90px;height:90px;object-fit:contain;background:var(--elev)">
              <div><b>${match.m}</b><div class="mt">${match.y} · #${match.c} · ${match.s}</div><div class="mt">Índice ${match.x} · ${fmt(match.v)}–${fmt(match.V)}</div></div></div>
              <div class="btnrow" style="padding:12px 0 0"><button class="btn" onclick="addById('${escJ(match.i)}',1);render(true)">Agregar a mi colección</button></div></div>`;
            logMsg("i","Código escaneado: <b>"+code+"</b> → "+match.m);
          } else {
            o.innerHTML+=`<div class="warn">Código detectado: <b>${code}</b> — no coincide con ningún auto del catálogo. Probá con el nombre.</div>`;
          }
        }
      }catch(e){/* sin código en este frame */}
    },400);
  }catch(e){
    o.innerHTML=`<div class="warn">No se pudo acceder a la cámara: ${e.message}. Verificá los permisos.</div>`;
  }
}
function stopScan(){
  if(scanStream){scanStream.getTracks().forEach(t=>t.stop());scanStream=null;}
  if(scanInterval){clearInterval(scanInterval);scanInterval=null;}
}

/* ===== cuenta: registro / login / perfil ===== */
function toggleCuenta(){
  const m=document.getElementById('cuentamodal');
  if(m.style.display==='none'){ m.style.display='flex'; abrirCuenta(); }
  else m.style.display='none';
}
async function abrirCuenta(){
  const el=document.getElementById('cuentacontenido');
  const tit=document.getElementById('cuentatitulo');
  if(!SBClient.estaLogueado()){
    tit.textContent='Crear cuenta';
    el.innerHTML=`
      <div class="note" style="margin-bottom:12px">Tu colección se guarda en este navegador. Con cuenta, se sincroniza en la nube y podés entrar desde cualquier dispositivo.</div>
      <div class="sec" style="border:1px solid var(--line);padding:12px;margin-bottom:10px">
        <h4 style="margin:0 0 8px">Registrar</h4>
        <input id="regnombre" placeholder="Nombre de perfil" style="width:100%;padding:8px;margin-bottom:8px;background:var(--elev);color:var(--ink);border:1px solid var(--line);border-radius:4px">
        <input id="regemail" type="email" placeholder="Email" style="width:100%;padding:8px;margin-bottom:8px;background:var(--elev);color:var(--ink);border:1px solid var(--line);border-radius:4px">
        <input id="regpass" type="password" placeholder="Contraseña (mín. 8 caracteres)" style="width:100%;padding:8px;margin-bottom:10px;background:var(--elev);color:var(--ink);border:1px solid var(--line);border-radius:4px">
        <button class="btn" style="width:100%" onclick="hacerRegistro()">Crear cuenta</button>
        <div class="note" style="margin-top:6px">Te va a llegar un email de confirmación.</div>
      </div>
      <div class="sec" style="border:1px solid var(--line);padding:12px">
        <h4 style="margin:0 0 8px">Ya tenés cuenta</h4>
        <input id="logemail" type="email" placeholder="Email" style="width:100%;padding:8px;margin-bottom:8px;background:var(--elev);color:var(--ink);border:1px solid var(--line);border-radius:4px">
        <input id="logpass" type="password" placeholder="Contraseña" style="width:100%;padding:8px;margin-bottom:10px;background:var(--elev);color:var(--ink);border:1px solid var(--line);border-radius:4px">
        <button class="btn" style="width:100%" onclick="hacerLogin()">Entrar</button>
      </div>`;
  } else {
    tit.textContent='Mi perfil';
    const p=await SBClient.getPerfil(true);
    const vis=p?.visibilidad||'privada';
    const email=SBClient.getEmail()||'';
    const avatar=avatarURL(email);
    const stats=calcularStatsPerfil();
    const TIPOS=[['privado','Coleccionista privado'],['vendedor','Coleccionista que vende'],['revendedor','Revendedor'],['inversor','Inversor']];
    el.innerHTML=`
      <div style="display:flex;gap:12px;align-items:center;margin-bottom:14px">
        <img src="${avatar}" style="width:72px;height:72px;border-radius:50%;background:var(--elev);border:2px solid var(--line)" alt="avatar">
        <div>
          <div style="font-size:18px;font-weight:600">${p?.nombre_perfil||email.split('@')[0]}</div>
          <div class="note">${p?.tipo_coleccionista?TIPOS.find(t=>t[0]===p.tipo_coleccionista)?.[1]||p.tipo_coleccionista:'Sin tipo definido'}</div>
        </div>
      </div>
      <div style="display:flex;gap:12px;margin-bottom:14px;flex-wrap:wrap">
        <div style="background:var(--elev);border-radius:6px;padding:8px 12px;text-align:center"><div style="font-size:20px;font-weight:700">${stats.autos}</div><div class="note">autos</div></div>
        <div style="background:var(--elev);border-radius:6px;padding:8px 12px;text-align:center"><div style="font-size:20px;font-weight:700">${stats.modelos}</div><div class="note">modelos</div></div>
        <div style="background:var(--elev);border-radius:6px;padding:8px 12px;text-align:center"><div style="font-size:20px;font-weight:700">${fmt(stats.valor)}</div><div class="note">valor ref.</div></div>
      </div>
      <div class="sec" style="border:1px solid var(--line);padding:12px;margin-bottom:10px">
        <h4 style="margin:0 0 8px">Datos del perfil</h4>
        <div class="note" style="margin-bottom:8px">Email: <b>${email}</b></div>
        <label class="note">Nombre de perfil:</label>
        <input id="pfnombre" value="${p?.nombre_perfil||''}" style="width:100%;padding:8px;margin-bottom:10px;background:var(--elev);color:var(--ink);border:1px solid var(--line);border-radius:4px">
        <label class="note">Tipo de coleccionista:</label>
        <select id="pftipo" style="width:100%;padding:8px;margin-bottom:10px;background:var(--elev);color:var(--ink);border:1px solid var(--line);border-radius:4px">
          <option value="">Sin especificar</option>
          ${TIPOS.map(([v,n])=>`<option value="${v}"${p?.tipo_coleccionista===v?' selected':''}>${n}</option>`).join('')}
        </select>
        <label class="note">Bio (máx. 200 caracteres):</label>
        <textarea id="pfbio" rows="2" maxlength="200" style="width:100%;padding:8px;margin-bottom:4px;background:var(--elev);color:var(--ink);border:1px solid var(--line);border-radius:4px;resize:vertical">${p?.bio||''}</textarea>
        <div class="note" style="text-align:right"><span id="pfbiocount">0</span>/200</div>
        <button class="btn" onclick="guardarPerfil()">Guardar datos</button>
      </div>
      <div class="sec" style="border:1px solid var(--line);padding:12px;margin-bottom:10px">
        <h4 style="margin:0 0 8px">Privacidad de tu colección</h4>
        <div class="note" style="margin-bottom:8px">¿Quién puede ver tu colección?</div>
        <select id="pfvis" style="width:100%;padding:8px;margin-bottom:10px;background:var(--elev);color:var(--ink);border:1px solid var(--line);border-radius:4px">
          <option value="privada"${vis==='privada'?' selected':''}>Privada — solo vos</option>
          <option value="compartida"${vis==='compartida'?' selected':''}>Compartida — vos y el staff</option>
          <option value="publica"${vis==='publica'?' selected':''}>Pública — cualquiera</option>
        </select>
        <div class="note" style="margin-bottom:10px">Los admins nunca ven colecciones <b>privadas</b> (Ley 21.719).</div>
        <label style="display:flex;align-items:center;gap:8px;margin-bottom:6px"><input type="checkbox" id="pfgeo"${p?.geo_consentida?' checked':''}> Compartir mi comuna en el mapa</label>
        <label style="display:flex;align-items:center;gap:8px"><input type="checkbox" id="pfstats"${p?.stats_anonimas?' checked':''}> Aportar a estadísticas anónimas</label>
      </div>
      <div class="sec" style="border:1px solid var(--line);padding:12px;margin-bottom:10px">
        <h4 style="margin:0 0 8px">Sincronización</h4>
        <div class="note" style="margin-bottom:8px">Tu colección se sube a la nube automáticamente cuando hacés cambios.</div>
        <button class="btn ghost" onclick="forzarSync()">Sincronizar ahora</button>
      </div>
      <button class="btn ghost" style="width:100%;color:#e74c3c;border-color:#e74c3c" onclick="SBClient.cerrarSesion();toggleCuenta()">Cerrar sesión</button>`;
    const bio=document.getElementById('pfbio');
    if(bio){
      const cont=document.getElementById('pfbiocount');
      const act=()=>{ if(cont) cont.textContent=bio.value.length; };
      bio.addEventListener('input',act); act();
    }
  }
}
async function hacerRegistro(){
  const email=document.getElementById('regemail').value.trim();
  const pass=document.getElementById('regpass').value;
  const nombre=document.getElementById('regnombre').value.trim()||email.split('@')[0];
  if(!email||!pass){logMsg('a','Completá email y contraseña.');return;}
  if(pass.length<8){logMsg('a','La contraseña debe tener al menos 8 caracteres.');return;}
  logMsg('i','Creando cuenta...');
  const r=await SBClient.registrar(email,pass,nombre);
  if(r.error){logMsg('a',r.error);return;}
  logMsg('i', r.necesitaConfirmar
    ? 'Cuenta creada. <b>Revisá tu email</b> para confirmarla.'
    : 'Cuenta creada y sesión iniciada. ¡Bienvenido!');
  toggleCuenta();
  if(!r.necesitaConfirmar) SBClient.refrescarBadgeCuenta();
}
async function hacerLogin(){
  const email=document.getElementById('logemail').value.trim();
  const pass=document.getElementById('logpass').value;
  if(!email||!pass){logMsg('a','Completá email y contraseña.');return;}
  logMsg('i','Entrando...');
  const r=await SBClient.iniciarSesion(email,pass);
  if(r.error){logMsg('a',r.error);return;}
  logMsg('i','Bienvenido de nuevo.');
  toggleCuenta();
  SBClient.refrescarBadgeCuenta();
  SBClient.sincronizarDesde().catch(()=>{});
}
async function guardarPerfil(){
  const bio=document.getElementById('pfbio')?.value||'';
  const r=await SBClient.actualizarPerfil({
    nombre_perfil:document.getElementById('pfnombre').value.trim(),
    bio: bio.slice(0,200),
    tipo_coleccionista: document.getElementById('pftipo').value||null,
  });
  if(r.error){logMsg('a',r.error);return;}
  logMsg('i','Datos guardados.');
  const prof=await SBClient.getPerfil();
  if(document.getElementById('pfvis').value!==prof?.visibilidad){
    await SBClient.actualizarPerfil({ visibilidad:document.getElementById('pfvis').value });
  }
  await SBClient.actualizarPerfil({
    geo_consentida:document.getElementById('pfgeo').checked,
    stats_anonimas:document.getElementById('pfstats').checked
  });
  logMsg('i','Privacidad guardada.');
}

function avatarURL(email){
  const seed=(email||'default').trim().toLowerCase();
  return 'https://api.dicebear.com/10.x/pixel-art/svg?seed='+encodeURIComponent(seed);
}

function calcularStatsPerfil(){
  let autos=0,modelos=0,valor=0;
  OWN.forEach(o=>{
    const c=CAT.find(x=>x.i===o.id);
    autos+=o.q||0; modelos++;
    if(c) valor+=(o.q||0)*(PRE[c.k]?.r||100);
  });
  return {autos, modelos, valor};
}
async function forzarSync(){
  logMsg('i','Sincronizando...');
  const r=await SBClient.sincronizarAhora();
  if(r.error){logMsg('a',r.error);return;}
  logMsg('i','Sincronizado.');
}

/* ===== onboarding: colección base de 10 autos ===== */
let onboardAutos=[];
function abrirOnboard(){
  document.getElementById('onboardmodal').style.display='flex';
  renderOnboard();
}
function renderOnboard(){
  const n=onboardAutos.length;
  document.getElementById('onboardcount').textContent=n+' / 10';
  document.getElementById('onboardbar').style.width=Math.min(100,n*10)+'%';
  const body=document.getElementById('onboardbody');
  const resumen=document.getElementById('onboardresumen');
  if(n>=10){
    body.style.display='none';
    resumen.style.display='';
    const total=onboardAutos.reduce((a,b)=>a+(b.q||0),0);
    resumen.innerHTML=`<div class="sec" style="border:1px solid var(--line);padding:12px">
      <h4 style="margin:0 0 8px">¡Colección base completa! 🎉</h4>
      <div class="note">Tenés <b>${n}</b> modelos (${total} unidades).</div>
      <div class="note" style="margin-top:6px">Podés seguir agregando más autos, o cerrar y usar la app normalmente.</div>
      <div class="btnrow" style="margin-top:10px">
        <button class="btn" onclick="cerrarOnboard()">Listo, cerrar</button>
        <button class="btn ghost" onclick="onboardAutos=[];renderOnboard()">Empezar de nuevo</button>
      </div></div>`;
  } else {
    resumen.style.display='none';
    body.style.display='';
    body.innerHTML=`
      <div class="rowin" style="margin-bottom:10px">
        <input id="onboardq" placeholder="Buscar por nombre..." style="flex:1;padding:8px;background:var(--elev);color:var(--ink);border:1px solid var(--line);border-radius:4px">
        <button class="btn" onclick="onboardBuscar()">Buscar</button>
        <button class="btn ghost" onclick="startScan()">📷</button>
      </div>
      <div id="onboardresult"></div>
      <div class="sec" style="border:1px solid var(--line);padding:10px;margin-top:10px">
        <div class="note">Los autos que ya agregaste (${n}):</div>
        <div id="onboardlist" style="margin-top:6px"></div>
      </div>`;
    renderOnboardList();
  }
}
function renderOnboardList(){
  const el=document.getElementById('onboardlist');
  if(!el) return;
  if(!onboardAutos.length){el.innerHTML='<span class="note">Todavía no agregaste ninguno.</span>';return;}
  el.innerHTML=onboardAutos.map((a,i)=>`<div style="display:flex;justify-content:space-between;align-items:center;padding:4px 0;border-bottom:1px solid var(--line)">
    <span>${a.m}</span><span><span class="note">×${a.q}</span>
    <button class="btn ghost" style="padding:2px 6px;font-size:12px;margin-left:6px" onclick="onboardQuitar(${i})">quitar</button></span></div>`).join('');
}
function onboardBuscar(){
  const q=(document.getElementById('onboardq').value||'').trim();
  const el=document.getElementById('onboardresult');
  if(!q){el.innerHTML='<div class="note">Escribí al menos 2 caracteres.</div>';return;}
  const cs=buscar(q);
  if(!cs){el.innerHTML='<div class="warn">No encontré ese modelo.</div>';return;}
  el.innerHTML=cs.slice(0,5).map(c=>`<div style="display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid var(--line)">
    <span><b>${c.m}</b> <span class="note">${c.y} · ${c.k}</span></span>
    <button class="btn" style="padding:4px 10px;font-size:12px" onclick="onboardAgregar('${escJ(c.i)}','${c.m.replace(/'/g,"")}')">+ agregar</button></div>`).join('');
}
function onboardAgregar(id,nombre){
  const existe=onboardAutos.find(a=>a.id===id);
  if(existe) existe.q=(existe.q||0)+1;
  else onboardAutos.push({id,m:nombre,q:1,c:'carded-nuevo'});
  SBClient.marcaPendiente();
  renderOnboard();
}
function onboardQuitar(i){
  onboardAutos.splice(i,1);
  renderOnboard();
}
function cerrarOnboard(){
  document.getElementById('onboardmodal').style.display='none';
}
/* ===== escaneo OCR + barcode ===== */
let scanZX=null;

async function abrirScan(){
  document.getElementById('scanmodal').style.display='flex';
  document.getElementById('scanresult').innerHTML='';
  const video=document.getElementById('scanvideo');
  try{
    scanStream=await navigator.mediaDevices.getUserMedia({
      video:{facingMode:'environment',width:{ideal:1280},height:{ideal:720}}
    });
    video.srcObject=scanStream;
    await video.play();
    // ZXing: escanear código de barras en tiempo real
    if(typeof ZXing!=='undefined'){
      try{
        scanZX=new ZXing.BrowserMultiFormatReader();
        const onDecode=(result,err)=>{
          if(result){
            const code=result.getText();
            if(code && code.length>=3){
              detenerScan();
              procesarCodigo(code);
            }
          }
        };
        if(typeof scanZX.decodeFromVideoDevice==='function'){
          scanZX.decodeFromVideoDevice(undefined,video,onDecode);
        }else if(typeof scanZX.decodeFromVideoElement==='function'){
          scanZX.decodeFromVideoElement(video,onDecode);
        }else{
          throw new Error('API de escaneo no disponible en esta versión de ZXing');
        }
        logMsg('i','Escáner ZXing activo. Apuntá al código de barras o tocá "Capturar (OCR)".');
      }catch(zxErr){
        logMsg('w','ZXing no disponible ('+zxErr.message+'). Usá Capturar (OCR).');
        scanZX=null;
      }
    }else{
      logMsg('w','ZXing no cargado. Usá Capturar (OCR) con Tesseract.js.');
    }
  }catch(e){
    logMsg('a','No se pudo acceder a la cámara: '+e.message);
    document.getElementById('scanmodal').style.display='none';
  }
}

function detenerScan(){
  if(scanZX){ try{scanZX.reset();}catch(e){} scanZX=null; }
  if(scanStream){
    scanStream.getTracks().forEach(t=>t.stop());
    scanStream=null;
  }
  const video=document.getElementById('scanvideo');
  if(video) video.srcObject=null;
}

function cerrarScan(){
  detenerScan();
  document.getElementById('scanmodal').style.display='none';
}

async function capturarOCR(){
  const video=document.getElementById('scanvideo');
  if(!video || !scanStream){ logMsg('a','Cámara no activa.'); return; }
  logMsg('i','Capturando imagen...');
  // Capturar frame actual
  const canvas=document.createElement('canvas');
  canvas.width=video.videoWidth||1280;
  canvas.height=video.videoHeight||720;
  const ctx=canvas.getContext('2d');
  ctx.drawImage(video,0,0);
  logMsg('i','Procesando OCR (Tesseract.js)...');
  try{
    if(typeof Tesseract==='undefined') throw new Error('Tesseract.js no cargado');
    const result=await Tesseract.recognize(canvas,'eng',{
      logger:m=>{ if(m.status==='recognizing text') logMsg('i','OCR: '+Math.round(m.progress*100)+'%'); }
    });
    const texto=result.data.text||'';
    logMsg('i','Texto detectado: "'+texto.trim().substring(0,80)+'"');
    // Extraer códigos del texto
    const codigos=extraerCodigos(texto);
    if(codigos.length){
      logMsg('i','Códigos encontrados: '+codigos.join(', '));
      detenerScan();
      procesarCodigo(codigos[0]);
    } else {
      logMsg('a','No se detectaron códigos válidos en la imagen. Intentá con mejor iluminación o acercá el código al centro del recuadro.');
    }
  }catch(e){
    logMsg('a','Error en OCR: '+e.message+'. Verificá que Tesseract.js se cargó correctamente.');
  }
}

function extraerCodigos(texto){
  const codigos=[];
  // Patrones de códigos Hot Wheels (mejorados)
  const patrones=[
    /\b[LlCcFfGg]\d{4}\b/,           // Asortación: L2593, C4982, F5785
    /\b[A-Z]{3}\d{2}\b/,             // Modelo: FRN78, JKX06
    /\b[A-Z]\d{4}-?\d{3}[A-Z]\b/,    // Case: L2593-976K
    /\bAsst\.?\s*[A-Z]?\d{4}\b/i,    // "Asst. C4982"
    /\b\d{3}[A-Z]\b/,                // Códigos cortos: 976K
    /\b[A-Z]{2}\d{4}\b/,             // Códigos de 2 letras + 4 números
    /\b\d{4}[A-Z]\b/,                // Códigos de 4 números + letra
  ];
  for(const p of patrones){
    const matches=texto.match(new RegExp(p.source,p.flags.includes('g')?p.flags:p.flags+'g'));
    if(matches){
      matches.forEach(m=>codigos.push(m.toUpperCase().replace(/\s+/g,'')));
    }
  }
  return [...new Set(codigos)];
}

function procesarCodigo(codigo){
  if(!codigo) return;
  codigo=codigo.trim().toUpperCase();
  const res=document.getElementById('scanresult');
  // Normalizar código para búsqueda (quitar caracteres especiales)
  const codigoNorm=codigo.replace(/[^A-Z0-9]/g,'');
  // Buscar en el catálogo local (intento múltiple)
  const encontrado=buscarPorCodigo(codigo)||buscarPorCodigo(codigoNorm);
  if(encontrado){
    res.innerHTML=`
      <div class="sec" style="border:1px solid var(--brand);padding:12px">
        <h4 style="margin:0 0 8px">✅ Modelo encontrado</h4>
        <div style="font-size:16px;font-weight:600">${encontrado.m}</div>
        <div class="note">Código: ${encontrado.i} · Serie: ${encontrado.k}</div>
        <div class="note">Año: ${encontrado.y}</div>
        ${encontrado.img?`<img alt="" src="${encontrado.img}" style="width:80px;height:80px;object-fit:cover;border-radius:4px;margin-top:8px">`:''}
        <div class="btnrow" style="margin-top:10px">
          <button class="btn" onclick="agregarEscaneado('${escJ(encontrado.i)}')">+ Agregar a mi colección</button>
          <button class="btn ghost" onclick="verFicha('${escJ(encontrado.i)}')">Ver ficha</button>
        </div>
      </div>`;
    logMsg('i','Modelo encontrado: '+encontrado.m);
  } else {
    res.innerHTML=`
      <div class="sec" style="border:1px solid #e74c3c;padding:12px">
        <h4 style="margin:0 0 8px">❌ Código no encontrado</h4>
        <div class="note">El código <b>${codigo}</b> no existe en el catálogo local.</div>
        <div class="note" style="margin:8px 0">¿Querés buscar en internet o agregar manualmente?</div>
        <div class="btnrow">
          <button class="btn" onclick="buscarEnInternet('${escJ(codigo)}')">🔍 Buscar en internet</button>
          <button class="btn ghost" onclick="agregarManual('${escJ(codigo)}')">Agregar manualmente</button>
        </div>
      </div>`;
    logMsg('a','Código no encontrado: '+codigo);
  }
}

function buscarPorCodigo(codigo){
  if(!codigo) return null;
  const codigoNorm=codigo.replace(/[^A-Z0-9]/g,'').toUpperCase();
  // Buscar por ID exacto o por código de asortación (normalizado)
  return CAT.find(c=>{
    const ciNorm=c.i.replace(/[^A-Z0-9]/g,'').toUpperCase();
    return c.i===codigo || ciNorm===codigoNorm || ciNorm.includes(codigoNorm) || codigoNorm.includes(ciNorm);
  });
}

async function agregarEscaneado(id){
  const c=CAT.find(x=>x.i===id);
  if(!c) return;
  OWN.push({id:c.i,m:c.m,q:1,c:'carded-nuevo'});
  guardarOWN();
  logMsg('i','Agregado a tu colección: '+c.m);
  cerrarScan();
  renderTab();
}

async function buscarEnInternet(codigo){
  const res=document.getElementById('scanresult');
  logMsg('i','🔍 Búsqueda en internet para: '+codigo);
  res.innerHTML=`
    <div class="sec" style="border:1px solid var(--brand);padding:12px">
      <h4 style="margin:0 0 8px">🔍 Buscar en internet</h4>
      <div class="note" style="margin-bottom:8px">Para buscar el código <b>${codigo}</b> en internet, ejecutá el siguiente comando en tu terminal:</div>
      <pre class="note" style="background:var(--elev);padding:12px;border-radius:6px;overflow-x:auto;font-size:13px;margin:0">python build/scraper_rescate.py "${codigo}"</pre>
      <div class="note" style="margin-top:12px">El scraper buscará en:</div>
      <ul class="note" style="margin:8px 0;padding-left:20px">
        <li>SmartWheelers</li>
        <li>HW Wiki</li>
        <li>HW Price Guide</li>
        <li>Reddit</li>
        <li>eBay</li>
        <li>Mercado Libre</li>
      </ul>
      <div class="note">Si el scraper encuentra el modelo, los datos se guardan en caché por 7 días.</div>
    </div>`;
}

function agregarManual(codigo){
  const res=document.getElementById('scanresult');
  const nombre=prompt('Nombre del modelo (ej: \'18 Dodge Challenger):');
  if(!nombre) return;
  const nuevo={i:codigo,m:nombre,k:'Desconocido',y:new Date().getFullYear(),img:''};
  CAT.push(nuevo);
  guardarCAT();
  logMsg('i','Modelo agregado manualmente: '+nombre);
  res.innerHTML='<div class="sec" style="border:1px solid var(--brand);padding:12px"><h4 style="margin:0 0 8px">✅ Agregado al catálogo</h4><div class="note">'+nombre+' ('+codigo+')</div></div>';
}

/* ===== pestañas ===== */
function tabTo(t){
  state.tab=t;
  document.querySelectorAll("nav.tabs button").forEach(b=>b.setAttribute("aria-selected",String(b.dataset.tab===t)));
  document.querySelectorAll("[data-view]").forEach(v=>v.style.display=(v.dataset.view===t?"":"none"));
  if(t==="coleccion") renderCol();
  if(t==="valorar") renderVal(); if(t==="series") renderSeries();
  if(t==="mercados") renderMkt();
  if(t==="seguimiento") renderSeg();
  if(t==="tendencias") renderSeg();
  if(t==="cajas") renderCajas();
  if(t==="catalogo") render(true);
  if(t==="ruedas") initRuedas();
}
function renderCol(){
  const T=totales(), g=document.getElementById("gridcol"); if(!g) return;
  document.getElementById("cs1").textContent=T.units;
  document.getElementById("cs2").textContent=T.items;
  document.getElementById("cs3").textContent=fmt(T.min)+"–"+fmt(T.max);
  document.getElementById("cs4").textContent=Object.entries(T.byClass).sort((a,b)=>b[1]-a[1]).map(([k,v])=>k+" "+v).join(" · ")||"—";
  const ids=Object.keys(col).filter(id=>col[id].q>0);
  if(!ids.length) g.innerHTML=`<div class="empty">Tu colección está vacía. Andá al catálogo y sumá autos con el botón + en la ficha.</div>`;
  else { const rows=ids.map(id=>IDX[id]).filter(Boolean).sort((a,b)=>b.x-a.x); g.innerHTML=rows.map(c=>cardHTML(c)).join(""); }
  const yrs=Object.entries(T.byYear).sort((a,b)=>b[0]-a[0]).slice(0,10), mx=Math.max(1,...yrs.map(y=>y[1]));
  document.getElementById("distyear").innerHTML=yrs.map(([y,n])=>`<div class="row"><span>${y}</span><span class="fill"><i style="width:${n/mx*100}%"></i></span><span class="num">${n}</span></div>`).join("")||"<div class='note'>Sin datos.</div>";
  const cls=Object.entries(T.byClass).sort((a,b)=>b[1]-a[1]), mxc=Math.max(1,...cls.map(c=>c[1]));
  document.getElementById("distclass").innerHTML=cls.map(([k,n])=>`<div class="row"><span>${k}</span><span class="fill"><i style="width:${n/mxc*100}%"></i></span><span class="num">${n}</span></div>`).join("")||"<div class='note'>Sin datos.</div>";
}
function renderVal(){
  const T=totales();
  const plan=[["Lotes de lo común (< US$10)","1-4 semanas","eBay lotes / Facebook Marketplace","13,25%+US$0,40 / 0%"],
    ["Piezas US$15-50","1-2 semanas","eBay subasta","13,25%+US$0,40"],
    ["Piezas US$50-200","1-4 semanas","eBay subasta","13,25%+US$0,40"],
    ["Piezas > US$200","1-6 meses","eBay subasta / casa de subastas","13,25%+US$0,40"]];
  document.getElementById("plan").innerHTML=plan.map(p=>`<tr><td>${p[0]}</td><td>${p[1]}</td><td>${p[2]}</td><td class="num">${p[3]}</td></tr>`).join("");
  const lotes=[["Lote pequeño (2-6)",0.15],["Lote mediano (20-50)",0.4],["Colección completa (100+)",0.6],["A revendedor",0.6]];
  document.getElementById("lotes").innerHTML=lotes.map(l=>{const net=(T.min+T.max)/2*(1-l[1]);
    return `<tr><td>${l[0]}</td><td class="num">${Math.round(l[1]*100)}%</td><td class="num">${fmt(net)}</td></tr>`;}).join("");
  document.getElementById("valnote").innerHTML=`Colección: <b>${T.units}</b> autos · pieza por pieza <b>${fmt(T.min)} – ${fmt(T.max)}</b> · mediana ${fmt((T.min+T.max)/2)}. Con eBay (13,25%+US$0,40) el neto individual baja ~14%.`;
}

/* ===== mercados ===== */
function renderMkt(){
  if(!document.getElementById("netv")) return;
  calcNet(); calcImp();
}
function calcNet(){
  const v=parseFloat(document.getElementById("netv").value)||0;
  const rows=MKT.calculadora_canales.map(c=>{
    const pct=c.pct+(c.extra_pct||0), fee=v*pct+c.fijo_usd;
    return {canal:c.canal,mercado:c.mercado,pct,fee,neto:v-fee,extra:c.extra_pct||0};});
  rows.sort((a,b)=>b.neto-a.neto);
  document.getElementById("netrows").innerHTML=rows.map((r,i)=>`<tr class="${i===0?"best":""}">
    <td>${r.canal}</td><td class="num">${(r.pct*100).toFixed(1)}%${r.extra?"+"+(r.extra*100).toFixed(1)+"%":""}</td>
    <td class="num">${fmt(r.fee)}</td><td class="num"><b>${fmt(r.neto)}</b></td>
    <td class="num">${(r.neto/v*100).toFixed(0)}%</td></tr>`).join("");
  const b=rows[0];
  document.getElementById("netbest").innerHTML=`Mejor canal para <b>${fmt(v)}</b>: <b>${b.canal}</b> → neto <b>${fmt(b.neto)}</b> (${(b.neto/v*100).toFixed(0)}% del precio).`;
}
function calcImp(){
  const v=parseFloat(document.getElementById("impv").value)||0;
  const f=parseFloat(document.getElementById("impf").value)||0;
  const c2c=document.getElementById("impc2c").checked;
  const CL=MKT.mercados.find(m=>m.id==="CL").importacion;
  const cif=v+f;
  let iva=0,ar=0,nota="";
  if(c2c&&cif<=CL.exencion_c2c){nota="Envío entre personas naturales (C2C) de hasta US$500, ocasional y no comercial: <b>exento</b> de IVA y de derechos.";}
  else{iva=cif*CL.iva; if(cif>CL.umbral_arancel) ar=cif*CL.arancel_sobre;
    nota=(cif>CL.umbral_arancel)?"Sobre US$500: <b>6% de arancel + 19% de IVA</b> sobre el CIF.":"Hasta US$500: <b>solo IVA 19%</b>, sin arancel.";}
  const total=cif+iva+ar;
  const EU=MKT.mercados.find(m=>m.id==="EU").importacion;
  const euIva=cif*0.19, euTotal=cif+euIva+EU.arancel_fijo;
  document.getElementById("imprt").innerHTML=`
    <tr><td>Valor del producto + envío (CIF)</td><td class="num">${fmt(cif)}</td><td class="num">US$${cif.toFixed(2)}</td></tr>
    <tr><td>IVA Chile (19%)</td><td class="num">${fmt(iva)}</td><td class="num">US$${iva.toFixed(2)}</td></tr>
    <tr><td>Arancel (6%, solo sobre US$500)</td><td class="num">${fmt(ar)}</td><td class="num">US$${ar.toFixed(2)}</td></tr>
    <tr class="best"><td><b>Costo final en Chile</b></td><td class="num"><b>${fmt(total)}</b></td><td class="num"><b>US$${total.toFixed(2)}</b></td></tr>
    <tr><td>Alternativa UE (IVA 19% + €3 fijos)</td><td class="num">${fmt(euTotal)}</td><td class="num">US$${euTotal.toFixed(2)}</td></tr>`;
  document.getElementById("impnote").innerHTML=nota+` <span style="opacity:.8">Sobre-coste sobre el valor: <b>${((total/cif-1)*100).toFixed(1)}%</b>.</span>`;
}

/* ===== seguimiento, alertas y demanda ===== */
function segCfg(){ try{ return JSON.parse(localStorage.getItem("hwseg")||"{}"); }catch(e){ return {}; } }
function segSet(id,obj){ const s=segCfg(); s[id]=Object.assign(s[id]||{},obj); try{localStorage.setItem("hwseg",JSON.stringify(s));}catch(e){} }
function segItem(id){
  const base=SEG.items[id]||{}, cfg=segCfg()[id]||{};
  return Object.assign({},base,{alertas:Object.assign({},base.alertas||{},cfg),
    historial:(cfg.historial||base.historial||[]), fecha_actualizacion:cfg.fecha_actualizacion||base.fecha_actualizacion,
    valor_actual_usd:(cfg.valor_actual_usd!=null?cfg.valor_actual_usd:base.valor_actual_usd),
    valor_anterior_usd:(cfg.valor_anterior_usd!=null?cfg.valor_anterior_usd:base.valor_anterior_usd),
    cantidad:(col[id]&&col[id].q)||base.cantidad||1});
}
function frescura(fecha){
  const dias=Math.floor((Date.now()-new Date((fecha||"2000-01-01")+"T00:00:00").getTime())/86400000);
  const f=SEG.meta.frescura_dias||{fresco:7,aceptable:30};
  return {dias:dias, estado: dias<=f.fresco?"fresco":(dias<=f.aceptable?"aceptable":"viejo")};
}
/* Señal de precio más específica disponible para un auto (de más a menos confiable). */
function senalPrecio(id){
  const c=IDX[id]||{}, nombre=(c.m||"").toLowerCase();
  const ch=(TEND.precios_chile&&TEND.precios_chile.items)||[];
  let mejor=null;
  ch.forEach(function(x){ const n=x.modelo.toLowerCase();
    if(nombre&&(n.indexOf(nombre)>=0||nombre.indexOf(n.replace(/^hw\s+/,""))>=0)) if(!mejor||x.usd<mejor.usd) mejor=x; });
  if(mejor) return {usd:mejor.usd, fuente:"minidiecast.cl (tienda Chile) "+mejor.linea, confianza:"media"};
  const eb=(TEND.ebay_observado&&TEND.ebay_observado.items)||[];
  let me=null;
  eb.forEach(function(x){ const n=x.modelo.toLowerCase();
    if(nombre&&n.indexOf(nombre.split(" ")[0])>=0) if(!me||x.usd_min<me.usd) me={usd:x.usd_min,fuente:"eBay (listado observado)"}; });
  if(me) return {usd:me.usd, fuente:me.fuente, confianza:"media"};
  if(c.v!=null) return {usd:(c.v+c.V)/2, fuente:"rango por clase "+c.k, confianza:"baja"};
  return null;
}
const SEVC={alta:0,media:1,baja:2};
function evaluarAlertas(){
  const out=[];
  Object.keys(SEG.items).forEach(function(id){
    const it=segItem(id), fr=frescura(it.fecha_actualizacion);
    if(fr.estado==="viejo") out.push({id:id,tipo:"DATOS",sev:"media",msg:it.modelo+": datos de hace "+fr.dias+" días.",accion:"Actualizar"});
    const obj=(it.alertas||{}).precio_objetivo_usd, va=it.valor_actual_usd, cpct=(it.alertas||{}).cambio_pct||20;
    if(obj&&va&&va>=obj) out.push({id:id,tipo:"VENTA",sev:"alta",msg:it.modelo+": US$"+va.toFixed(2)+" alcanzó tu objetivo de US$"+obj.toFixed(2)+".",accion:"Publicar en "+((it.alertas||{}).canal_preferido||"MercadoLibre Chile")});
    if(va&&it.valor_anterior_usd){
      const ch=(va-it.valor_anterior_usd)/it.valor_anterior_usd*100;
      if(ch>=cpct) out.push({id:id,tipo:"SUBE",sev:"media",msg:it.modelo+": subió "+ch.toFixed(0)+"% (US$"+it.valor_anterior_usd.toFixed(2)+" → US$"+va.toFixed(2)+").",accion:"Revisar precio"});
      else if(ch<=-cpct) out.push({id:id,tipo:"COMPRA",sev:"media",msg:it.modelo+": bajó "+Math.abs(ch).toFixed(0)+"%. Oportunidad para completar la serie.",accion:"Buscar compra"});
    }
    if(it.confianza==="baja") out.push({id:id,tipo:"DATOS",sev:"baja",msg:it.modelo+": valor por clase (confianza baja), no comparable del modelo exacto.",accion:"Cargar comparables"});
    const r=DEM[id];
    if(r&&r.rank<=10) out.push({id:id,tipo:"DEMANDA",sev:"alta",msg:it.modelo+": top "+r.rank+" de demanda real de coleccionistas ("+r.coleccionistas+" en "+r.mes.replace("_"," ")+").",accion:"Vender individual, no en lote"});
  });
  return out;
}
function spark(hist){
  if(!hist||hist.length<2) return '<span class="note" style="font-size:10px">historial de 1 punto</span>';
  const v=hist.map(function(h){return h.usd;}), mn=Math.min.apply(null,v), mx=Math.max.apply(null,v), r=(mx-mn)||1;
  const pts=v.map(function(y,i){ return (i/(v.length-1)*100).toFixed(1)+","+(26-(y-mn)/r*22).toFixed(1); }).join(" ");
  return '<svg viewBox="0 0 100 28" preserveAspectRatio="none" style="width:84px;height:24px"><polyline points="'+pts+'" fill="none" stroke="#ff4d00" stroke-width="2"/></svg>';
}
function renderSeg(){
  const wrap=document.getElementById("segrows"); if(!wrap) return;
  const ids=Object.keys(SEG.items), al=evaluarAlertas().sort(function(a,b){return SEVC[a.sev]-SEVC[b.sev];});
  let tot=0, units=0;
  ids.forEach(function(id){ const it=segItem(id); tot+=(it.valor_actual_usd||0)*(it.cantidad||1); units+=it.cantidad||1; });
  const g=function(i){return document.getElementById(i);};
  if(g("sg1")) g("sg1").textContent=ids.length;
  if(g("sg2")) g("sg2").textContent=units;
  if(g("sg3")) g("sg3").textContent=fmt(tot);
  if(g("sg4")) g("sg4").textContent=al.filter(function(a){return a.sev==="alta";}).length;
  const bd=g("albadge"); if(bd){ bd.textContent=al.length; bd.style.display=al.length?"inline-block":"none"; }
  wrap.innerHTML=ids.map(function(id){
    const it=segItem(id), fr=frescura(it.fecha_actualizacion), r=DEM[id], d=IDX[id]||{};
    return '<div class="segrow"><img alt="" src="'+IMG(d.im||"")+'" onerror="this.style.visibility=\'hidden\'">'
      +'<div class="sinfo"><b>'+it.modelo+'</b><span class="mt">'+it.anio+' · '+it.clase+' · ×'+it.cantidad+'</span>'
      +(r?'<span class="dem">TOP '+r.rank+' demanda</span>':'')+'</div>'
      +'<div class="sval"><span class="mt">valor actual</span><b>'+fmt(it.valor_actual_usd||0)+'</b>'+spark(it.historial)+'</div>'
      +'<div class="sfr"><span class="fchip '+fr.estado+'">'+fr.estado+' · '+fr.dias+' d</span>'
      +'<span class="mt">objetivo '+fmt((it.alertas||{}).precio_objetivo_usd||0)+'</span>'
      +'<span class="mt">'+((it.alertas||{}).canal_preferido||"")+'</span></div>'
      +'<div class="sacc"><button class="btn ghost" onclick="updItem(\''+id+'\')">Actualizar</button>'
      +'<button class="btn ghost" onclick="editAlerta(\''+id+'\')">Alerta</button></div></div>';
  }).join("");
  const sl=g("seglist");
  if(sl) sl.innerHTML=al.map(function(a){ return '<div class="alrow '+a.sev+'"><span class="altipo">'+a.tipo+'</span>'
    +'<div>'+a.msg+'<span class="src">Acción: '+a.accion+'</span></div></div>'; }).join("")
    || '<div class="note">Sin alertas activas.</div>';
  const st=g("segstamp");
  if(st) st.textContent="Última corrida del motor: "+SEG.meta.actualizado+" · "+al.length+" alertas · "+(TEND.meta&&TEND.meta.generado?"señales de mercado del "+TEND.meta.generado:"sin señales");
}
function updItem(id){
  const it=segItem(id), s=senalPrecio(id);
  const hoy=new Date().toISOString().slice(0,10);
  if(!s){ logMsg("a","Sin señal de precio para ese auto."); return; }
  const hist=(it.historial||[]).slice();
  hist.push({fecha:hoy, usd:s.usd, fuente:s.fuente});
  segSet(id,{historial:hist, fecha_actualizacion:hoy, valor_anterior_usd:it.valor_actual_usd, valor_actual_usd:s.usd});
  renderSeg();
  logMsg("a","<b>"+it.modelo+"</b> actualizado a "+fmt(s.usd)+" (US$"+s.usd.toFixed(2)+").<span class=\"src\">Fuente: "+s.fuente+" · confianza "+s.confianza+"</span>");
}
function editAlerta(id){
  const it=segItem(id);
  const p=prompt("Precio objetivo de venta en USD para "+it.modelo+":", (it.alertas||{}).precio_objetivo_usd||10);
  if(p===null) return;
  const c=prompt("Avisarme si el valor cambia más de este % (sube o baja):", (it.alertas||{}).cambio_pct||20);
  if(c===null) return;
  const canal=prompt("Canal preferido de venta:", (it.alertas||{}).canal_preferido||"MercadoLibre Chile");
  segSet(id,{alertas:{precio_objetivo_usd:parseFloat(p)||10, cambio_pct:parseFloat(c)||20, canal_preferido:canal||"MercadoLibre Chile"}});
  renderSeg();
}
function updAll(){ Object.keys(SEG.items).forEach(function(id){ const it=segItem(id), s=senalPrecio(id);
    if(!s) return; const hoy=new Date().toISOString().slice(0,10), hist=(it.historial||[]).slice();
    hist.push({fecha:hoy, usd:s.usd, fuente:s.fuente});
    segSet(id,{historial:hist, fecha_actualizacion:hoy, valor_anterior_usd:it.valor_actual_usd, valor_actual_usd:s.usd}); });
  renderSeg(); renderCol(); }

/* ===== cajas: códigos, contenido posible e identificado ===== */
let cajYear=(CAJ.cajas_por_anio["2026"]?"2026":Object.keys(CAJ.cajas_por_anio).sort().pop());
function cajCfg(){ try{ return JSON.parse(localStorage.getItem("hwcaj")||"{}"); }catch(e){ return {}; } }
function cajSet(k,obj){ const s=cajCfg(); s[k]=Object.assign(s[k]||{},obj); try{localStorage.setItem("hwcaj",JSON.stringify(s));}catch(e){} }
function markCase(anio,letra,tipo){
  const k=anio+"-"+letra, s=cajCfg()[k]||{}, ids=s.ids||[];
  const i=ids.indexOf(tipo);
  if(i>=0) ids.splice(i,1); else ids.push(tipo);
  cajSet(k,{ids:ids}); renderCajas();
}
function caseNote(anio,letra,val){ cajSet(anio+"-"+letra,{nota:val}); }
function renderCajas(){
  const wrap=document.getElementById("casegrid"); if(!wrap) return;
  const lista=CAJ.cajas_por_anio[cajYear]||[], cfg=cajCfg();
  const th=lista.filter(c=>c.TH).length, sth=lista.filter(c=>c.STH).length;
  const g=function(i){return document.getElementById(i);};
  if(g("cj1")) g("cj1").textContent=lista.length;
  if(g("cj2")) g("cj2").textContent=th||"n/d";
  if(g("cj3")) g("cj3").textContent=sth||"n/d";
  if(g("cj4")) g("cj4").textContent=Object.keys(cfg).filter(k=>k.indexOf(cajYear+"-")===0).length;
  wrap.innerHTML=lista.map(function(c){
    const k=cajYear+"-"+c.letra, ids=(cfg[k]||{}).ids||[], nota=(cfg[k]||{}).nota||"";
    const bloque=function(t,tipo){
      const x=c[t]; if(!x) return '<div class="crow"><span class="tag '+tipo.toLowerCase()+'">'+tipo+'</span><div class="cinfo"><span class="note">'+
        (tipo==="TH"?"La wiki no publica la TH de este año.":"Sin dato")+'</span></div></div>';
      const d=IDX[x.catalogo_id]||{};
      return '<div class="crow">'+(d.im?'<img alt="" src="'+IMG(d.im)+'" onerror="this.style.visibility=\'hidden\'">':'<img alt="">')
        +'<div class="cinfo"><span class="tag '+tipo.toLowerCase()+'">'+tipo+'</span><b>'+x.modelo+'</b>'
        +'<span class="mt">'+(x.serie||"")+' · '+(x.col||"")+'</span>'
        +(x.color?'<span class="mt">'+x.color+(x.rueda?' · '+x.rueda:"")+'</span>':'')
        +'<button class="mark '+(ids.indexOf(tipo)>=0?"on":"")+'" onclick="markCase(\''+cajYear+'\',\''+c.letra+'\',\''+tipo+'\')">'
        +(ids.indexOf(tipo)>=0?"✓ identificado":"marcar identificado")+'</button></div></div>';
    };
    return '<div class="casecard '+(ids.length?"marked":"")+'"><div class="ch"><b>CAJA '+c.letra+'</b><span>'+cajYear+'</span></div>'
      +'<div class="cbody">'+bloque("TH","TH")+bloque("STH","STH")
      +'<textarea placeholder="Qué modelos salieron realmente en esta caja (contenido identificado)…" onchange="caseNote(\''+cajYear+'\',\''+c.letra+'\',this.value)">'+nota+'</textarea>'
      +'</div></div>';
  }).join("") || '<div class="empty">Sin datos de cajas para ese año.</div>';
}
function decodificar(){
  const v=(document.getElementById("decin").value||"").trim().toUpperCase();
  const out=document.getElementById("decout");
  const m=v.match(/^([A-Z])\s*-?\s*(\d{1,2})$/);
  if(!m){ out.innerHTML='<span style="color:var(--warn)">Formato esperado: letra + semana, por ejemplo <b>M36</b> (base del auto).</span>'; return; }
  const anio=CAJ.codigos_base.letra_a_anio[m[1]], sem=parseInt(m[2],10);
  if(!anio){ out.innerHTML='<span style="color:var(--warn)">Letra '+m[1]+' no está en la tabla publicada.</span>'; return; }
  const ini=new Date(anio,0,1+ (sem-1)*7);
  out.innerHTML='Letra <b>'+m[1]+'</b> → año de fabricación <b>'+anio+'</b> · semana <b>'+sem+'</b> → aproximadamente <b>'
    +ini.toLocaleDateString("es-CL",{day:"2-digit",month:"long",year:"numeric"})+'</b>.<span class="src">Fuente: Hot Wheels Wiki — Base codes</span>';
  tts("Ese código corresponde al año "+anio+", semana "+sem+".");
}
function setCajYear(y){ cajYear=y; renderCajas(); }

/* ===== visualizaciones del índice ===== */
function nivelColor(v){ return v>=58?"#ff4d00":(v>=44?"#ff8c1a":"#c9ccd4"); }
function catLogoSVG(k){
  k=String(k||"");
  const L={
    'MAINLINE':'<path d="M13 2 4 14h6l-1 8 9-12h-6l1-8z" fill="#fff"/>',
    'TREASURE HUNT':'<path d="M12 2c2 3 5 5 5 9a5 5 0 0 1-10 0c0-4 3-6 5-9z" fill="#fff"/><path d="M12 9c1 1.5 2 2.5 2 4a2 2 0 0 1-4 0c0-1.5 1-2.5 2-4z" fill="#f59e0b"/>',
    'SUPER TREASURE HUNT':'<path d="M6 3h12l4 6-10 12L2 9l4-6z" fill="#fff"/>',
    'CAR CULTURE':'<path d="M12 2 3 6v6c0 5 3.8 8.4 9 10 5.2-1.6 9-5 9-10V6l-9-4zm0 5 4 1.5V13l-4 4-4-4V8.5L12 7z" fill="#fff"/>',
    'BOULEVARD':'<path d="M12 2c-1 3-2 5-2 7s1 4 2 5c1-1 2-3 2-5s-1-4-2-7zm0 12v8" stroke="#fff" stroke-width="2" fill="none"/>',
    'POP CULTURE':'<path d="M12 2l2.6 6 6.6.4-5 4.2 1.5 6.4L12 15.5 6.3 19l1.5-6.4-5-4.2 6.6-.4L12 2z" fill="#fff"/>',
    'MONSTER TRUCKS':'<path d="M2 15h20l-2 5H4l-2-5zm3-8h14v5H5V7z" fill="#fff"/>',
    'GRAN ESCALA':'<path d="M3 7h11v8H3zM14 10h4l3 3v2h-7z" fill="#fff"/><circle cx="7" cy="17" r="2" fill="#fff"/><circle cx="17" cy="17" r="2" fill="#fff"/>',
    'MYSTERY MODELS':'<circle cx="12" cy="12" r="10" stroke="#fff" stroke-width="2" fill="none"/><path d="M9.5 9a2.5 2.5 0 1 1 3.6 2.2c-.8.4-1.1 1-1.1 1.8" stroke="#fff" stroke-width="2" fill="none"/><circle cx="12" cy="17" r="1.3" fill="#fff"/>',
    'FLYING COLORS':'<path d="M12 2l4 8-4 12-4-12 4-8z" fill="#fff"/><path d="M8 12l4 6 4-6" stroke="#fff" stroke-width="1.6" fill="none"/>',
    'FIRST EDITIONS':'<circle cx="12" cy="12" r="10" stroke="#fff" stroke-width="2" fill="none"/><path d="M11 7h2v10h-2zM9 9h4" stroke="#fff" stroke-width="2" fill="none"/>',
    'NEW MODELS':'<path d="M12 3v18M5 8l7-5 7 5" stroke="#fff" stroke-width="2" fill="none"/>',
    'ELITE 64':'<path d="M12 2l3 6 6.6.4-5 4.2 1.5 6.4L12 15.5 6.3 19l1.5-6.4-5-4.2L9.4 8 12 2z" fill="#fff"/>',
    'SPECIAL & EARLY':'<path d="M12 2a10 10 0 0 0 0 20c2 0 3-1.3 3-2.6 0-1.5-1.4-2.1-1.4-3.4 0-1 .8-2 2-2h2.4A4.4 4.4 0 0 0 22 9.6C22 5.4 17.5 2 12 2z" fill="#fff"/>',
    'SIZZLERS':'<path d="M12 2c2 4 6 6 6 10a6 6 0 0 1-12 0c0-4 4-6 6-10z" fill="#fff"/>',
    '100% HOT WHEELS':'<circle cx="12" cy="12" r="9" stroke="#fff" stroke-width="2" fill="none"/><text x="12" y="15" font-size="7" fill="#fff" text-anchor="middle" font-family="Arial">100%</text>',
    'REAL RIDERS':'<circle cx="12" cy="12" r="9" stroke="#fff" stroke-width="2" fill="none"/><circle cx="12" cy="12" r="4" stroke="#fff" stroke-width="2" fill="none"/>',
    'CRACK-UPS':'<path d="M12 2l2 6 4 1-3 3 1 4-4-2-4 2 1-4-3-3 4-1 2-6z" fill="#fff"/>',
    'COLLECTOR EXCLUSIVES':'<path d="M6 3h12v4a6 6 0 0 1-12 0V3zm-2 1h2v6H4V4zm16 0h2v6h-2V4zM12 13v4m-4 3h8" stroke="#fff" stroke-width="1.8" fill="none"/>',
    'COLOR SHIFTERS':'<circle cx="12" cy="12" r="9" fill="none" stroke="#fff" stroke-width="2"/><path d="M12 3a9 9 0 0 1 0 18z" fill="#fff" opacity=".7"/>',
    'RLC · RED LINE CLUB':'<path d="M4 12h16M4 8h16M4 16h16" stroke="#fff" stroke-width="2"/>',
    'VINTAGE':'<path d="M12 3 2 8l10 5 10-5-10-5zM4 10v5l8 4 8-4v-5" stroke="#fff" stroke-width="1.8" fill="none"/>',
    'REDLINE':'<circle cx="12" cy="12" r="9" stroke="#fff" stroke-width="3" fill="none"/><circle cx="12" cy="12" r="5" stroke="#fff" stroke-width="2" fill="none"/>',
    'TEAM TRANSPORT':'<path d="M2 7h13v9H2zM15 10h4l3 3v3h-7z" fill="#fff"/>',
    'RETRO ENTERTAINMENT':'<rect x="3" y="6" width="18" height="12" rx="2" fill="none" stroke="#fff" stroke-width="2"/><path d="M10 10l5 2-5 2v-4z" fill="#fff"/>',
    'CONVENTION':'<path d="M12 2l2 6h-4l2-6zm-6 8h12l-2 12H8L6 10z" fill="#fff"/>',
    'ZAMAC':'<path d="M12 2l9 5v10l-9 5-9-5V7l9-5z" fill="none" stroke="#fff" stroke-width="2"/>'
  };
  const C={
    'MAINLINE':'#ff4d00','TREASURE HUNT':'#f59e0b','SUPER TREASURE HUNT':'#dc2626',
    'CAR CULTURE':'#ff4d00','BOULEVARD':'#8b5cf6','POP CULTURE':'#ec4899',
    'MONSTER TRUCKS':'#3b82f6','GRAN ESCALA':'#3b82f6','MYSTERY MODELS':'#6366f1',
    'FLYING COLORS':'#f97316','FIRST EDITIONS':'#ff8c1a','NEW MODELS':'#ff8c1a',
    'ELITE 64':'#a855f7','SPECIAL & EARLY':'#14b8a6','SIZZLERS':'#ef4444',
    '100% HOT WHEELS':'#0ea5e9','REAL RIDERS':'#64748b','CRACK-UPS':'#f43f5e',
    'COLLECTOR EXCLUSIVES':'#eab308','COLOR SHIFTERS':'#06b6d4',
    'RLC · RED LINE CLUB':'#dc2626','VINTAGE':'#a16207','REDLINE':'#dc2626',
    'TEAM TRANSPORT':'#f97316','RETRO ENTERTAINMENT':'#a855f7','CONVENTION':'#eab308','ZAMAC':'#94a3b8'
  };
  if(!L[k]) return '';
  return `<span class="catlogo" title="${k}" style="background:${C[k]||'#ff4d00'}"><svg viewBox="0 0 24 24" width="12" height="12" aria-hidden="true">${L[k]}</svg></span>`;
}

function donut(v,px){
  const R=34, C=2*Math.PI*R, off=C*(1-Math.min(100,v)/100), col=nivelColor(v);
  return '<svg viewBox="0 0 90 90" width="92" height="92">'
   +'<circle cx="45" cy="45" r="'+R+'" fill="none" stroke="#1d2128" stroke-width="9"/>'
   +'<circle cx="45" cy="45" r="'+R+'" fill="none" stroke="'+col+'" stroke-width="9" stroke-linecap="round" '
   +'stroke-dasharray="'+C+'" stroke-dashoffset="'+off+'" transform="rotate(-90 45 45)"/>'
   +'<text x="45" y="44" text-anchor="middle" fill="#eef1f5" font-size="19" font-family="var(--f-mono)">'+v+'</text>'
   +'<text x="45" y="58" text-anchor="middle" fill="#98a1ad" font-size="8" font-family="var(--f-display)">PERCENTIL '+px+'</text></svg>';
}
function radar(f){
  const d={R:f[0]||0,D:f[1]||0,C:f[2]||0,A:f[3]||0,M:f[4]||0};
  const cx=112, cy=100, R=74;
  const axes=[["R","Rareza",d.R],["D","Demanda",d.D],["C","Condición",d.C],["A","Antigüedad",d.A],["M","Mercado",d.M]];
  const pt=(i,v)=>{ const a=-Math.PI/2 + i*2*Math.PI/5, r=R*Math.min(100,v)/100; return [cx+r*Math.cos(a), cy+r*Math.sin(a)]; };
  let grid="";
  [25,50,75,100].forEach(g=>{ grid+='<polygon points="'+axes.map((_,i)=>pt(i,g).map(n=>n.toFixed(1)).join(",")).join(" ")+'" fill="none" stroke="#2a2f38" stroke-width="1"/>'; });
  axes.forEach((_,i)=>{ const p=pt(i,100); grid+='<line x1="'+cx+'" y1="'+cy+'" x2="'+p[0].toFixed(1)+'" y2="'+p[1].toFixed(1)+'" stroke="#2a2f38"/>'; });
  const poly=axes.map((a,i)=>pt(i,a[2]).map(n=>n.toFixed(1)).join(",")).join(" ");
  const dots=axes.map((a,i)=>{const p=pt(i,a[2]);return '<circle cx="'+p[0].toFixed(1)+'" cy="'+p[1].toFixed(1)+'" r="3" fill="#ff4d00"/>';}).join("");
  const labels=axes.map((a,i)=>{const p=pt(i,124);return '<text x="'+p[0].toFixed(1)+'" y="'+p[1].toFixed(1)+'" text-anchor="middle" fill="#98a1ad" font-size="9.5" font-family="var(--f-display)">'+a[0]+' '+Math.round(a[2])+'</text>';}).join("");
  return '<svg viewBox="0 0 224 214" width="100%" style="max-width:250px">'+grid
    +'<polygon points="'+poly+'" fill="rgba(255,77,0,.20)" stroke="#ff4d00" stroke-width="2"/>'+dots+labels+'</svg>';
}
function histo(x){
  const H=IDXINFO.histograma, max=Math.max.apply(null,H.bins), W=320, h=56, bw=W/H.bins.length;
  let bars="";
  H.bins.forEach((n,i)=>{ const bh=n/max*(h-8), xx=i*bw;
    const desde=H.desde+(H.hasta-H.desde)*i/H.bins.length, hasta=H.desde+(H.hasta-H.desde)*(i+1)/H.bins.length;
    const aqui = x>=desde && x<hasta;
    bars+='<rect x="'+(xx+1).toFixed(1)+'" y="'+(h-bh).toFixed(1)+'" width="'+(bw-2).toFixed(1)+'" height="'+bh.toFixed(1)+'" fill="'+(aqui?"#ff4d00":"#2a2f38")+'"/>'; });
  const mx=(Math.min(H.hasta,Math.max(H.desde,x))-H.desde)/(H.hasta-H.desde)*W;
  return '<svg viewBox="0 0 '+W+' '+(h+14)+'" width="100%" style="max-width:340px">'+bars
    +'<line x1="'+mx.toFixed(1)+'" y1="0" x2="'+mx.toFixed(1)+'" y2="'+h+'" stroke="#e8b23a" stroke-width="2" stroke-dasharray="3 2"/>'
    +'<text x="0" y="'+(h+11)+'" fill="#98a1ad" font-size="8">'+H.desde+'</text>'
    +'<text x="'+W+'" y="'+(h+11)+'" text-anchor="end" fill="#98a1ad" font-size="8">'+H.hasta+'</text></svg>';
}
function fuenteFactor(c, letra){
  const dm=c.dm, ap=c.ap||1;
  if(letra==="R") return ap+" aparición(es) en el catálogo"+(c.nuevo?" · modelo nuevo":"");
  if(letra==="D") return dm? "medida: coleccionistas (HW Price Guide)" : "proxi: "+ap+" re-ediciones del casting";
  if(letra==="C") return "referencia: nuevo en tarjeta";
  if(letra==="A") return "año "+c.y;
  if(letra==="M"){
    let t = c.mm!=null ? "momentum ene→feb "+c.mm+"%" : "sin señal específica";
    if(c.ch) t += " · con precio en tienda chilena";
    if(c.eb) t += " · listado en eBay";
    return t;
  }
  return "";
}
function barrasFactores(c){
  const f=c.f||[0,0,0,0,0];
  const def=[["R","Rareza",f[0],"30%"],["D","Demanda",f[1],"25%"],["C","Condición",f[2],"20%"],
             ["A","Antigüedad",f[3],"15%"],["M","Mercado",f[4],"10%"]];
  return def.map(function(x){
    const v=Math.round(x[2]||0), col=nivelColor(v), src=fuenteFactor(c,x[0]);
    const med = (x[0]==="D"&&c.dm)||(x[0]==="M"&&c.mm!=null);
    return '<div class="fbar2"><div class="fl"><b>'+x[0]+'</b> '+x[1]+' <span class="peso">'+x[3]+'</span></div>'
      +'<div class="ftrack"><i style="width:'+v+'%;background:'+col+'"></i><span class="fnum">'+v+'</span></div>'
      +'<div class="fsrc">'+src+(med?' <span class="medido">medido</span>':'')+'</div></div>';
  }).join("");
}

/* ===== voz: selector de voces y personas ===== */
let vozPref="", persona=(function(){ try{ return localStorage.getItem("hwpersona")||"asistente"; }catch(e){ return "asistente"; } })();
const PERSONAS={
  asistente:{n:"Asistente",rate:1.0,pitch:1.0,desc:"Neutral, datos con fuente."},
  pokedex:{n:"Pokédex",rate:0.93,pitch:0.75,desc:"Formato Pokédex, voz más grave y pausada."},
  clarkson:{n:"Clarkson",rate:1.06,pitch:1.05,desc:"Humor cáustico con los datos reales."}
};
function vocesES(){ return (window.speechSynthesis?speechSynthesis.getVoices():[]).filter(function(v){ return /^es/i.test(v.lang); }); }
function mejorVozES(){
  const vs=vocesES(); if(!vs.length) return null;
  if(vozPref){ const p=vs.filter(function(v){return v.name===vozPref;})[0]; if(p) return p; }
  const pref=["es-MX","es-US","es-419","es-AR","es-CL","es-CO","es-PE","es-ES"];
  for(const l of pref){ const f=vs.filter(function(v){ return v.lang.replace("_","-").toLowerCase().indexOf(l.toLowerCase())===0; })[0]; if(f) return f; }
  return vs[0];
}
let edgeVoces=[];
let vozEdge=(function(){ try{ return localStorage.getItem("hwvozedge")||""; }catch(e){ return ""; } })();
const TTS_SRV=(location.protocol==="file:")?null:"tts";
async function cargarEdgeVoces(){
  if(!TTS_SRV) return;
  try{
    const r=await fetch("tts-voices"); if(!r.ok) return;
    const j=await r.json();
    edgeVoces=(j.piper||[]).map(function(v){ return {id:v.id, nombre:v.nombre+" · neuronal local (Piper)", tipo:"piper"}; })
      .concat((j.edge||[]).map(function(v){ return {id:"edge:"+v.id, nombre:v.nombre+" · nube (puede fallar)", tipo:"edge"}; }));
    if(!vozEdge && edgeVoces.length) vozEdge=edgeVoces[0].id;
    llenarVoces();
  }catch(e){ /* sin servidor local: se usan las voces del sistema */ }
}
function llenarVoces(){
  const s=document.getElementById("vozsel"); if(!s) return;
  let html="";
  if(edgeVoces.length){
    html+='<optgroup label="Voces neuronales (servidor local)">'+edgeVoces.map(function(v){
      return '<option value="edge:'+v.id+'"'+(vozEdge===v.id?" selected":"")+'>'+v.nombre+'</option>'; }).join("")+'</optgroup>';
  }
  const vs=vocesES();
  if(vs.length){
    html+='<optgroup label="Voces del sistema">'+vs.map(function(v){
      return '<option value="sys:'+v.name+'"'+(vozPref===v.name?" selected":"")+'>'+v.name+' ('+v.lang+')</option>'; }).join("")+'</optgroup>';
  }
  s.innerHTML=html||'<option value="">(sin voces disponibles)</option>';
  const n=document.getElementById("vozinfo");
  if(n){
    let t = edgeVoces.length ? ("Servidor local activo: <b>"+edgeVoces.length+" voces neuronales</b> (Piper local + opciones de nube). ") : "Sin servidor local: se usan las voces del sistema. Levantá <b>python serve.py</b> para la voz neuronal local. ";
    t += vs.length ? (vs.length+" voces del sistema en español disponibles.") : "El navegador todavía no cargó las voces del sistema.";
    n.innerHTML=t;
  }
}
function setVoz(val){
  if(val.indexOf("edge:")===0){ vozEdge=val.slice(5); try{localStorage.setItem("hwvozedge",vozEdge);}catch(e){} }
  else if(val.indexOf("sys:")===0){ vozPref=val.slice(4); try{localStorage.setItem("hwvoz",vozPref);}catch(e){} }
  llenarVoces();
}
function setPersona(p){
  persona=p; try{localStorage.setItem("hwpersona",p);}catch(e){}
  document.querySelectorAll("[data-persona]").forEach(function(b){ b.setAttribute("aria-pressed",String(b.dataset.persona===p)); });
  const d=document.getElementById("personadesc"); if(d) d.textContent=PERSONAS[p].desc;
}
/* Habla: primero intenta la voz neuronal del servidor local; si no, la del sistema. */
async function tts(text){
  if(TTS_SRV && edgeVoces.length){
    try{
      const url=TTS_SRV+"?voice="+encodeURIComponent(vozEdge)+"&text="+encodeURIComponent(String(text).slice(0,800));
      const r=await fetch(url);
      if(r.ok){ const b=await r.blob(); const a=new Audio(URL.createObjectURL(b)); a.play(); return; }
    }catch(e){}
  }
  ttsNavegador(text);
}
function ttsNavegador(text){
  if(!("speechSynthesis" in window)){ logMsg("a","Tu navegador no soporta síntesis de voz."); return; }
  speechSynthesis.cancel();
  const u=new SpeechSynthesisUtterance(text);
  const v=mejorVozES(); if(v) u.voice=v;
  u.lang=v?v.lang:"es-MX";
  const P=PERSONAS[persona]||PERSONAS.asistente;
  u.rate=P.rate; u.pitch=P.pitch;
  speechSynthesis.speak(u);
}

/* ===== puente celular <-> asistente ===== */
const PUENTE=(location.protocol==="file:")?null:"./";
const COLA_KEY="hw_cola_local", ULTID="hw_ultima_id";
function colaLocal(){ try{ return JSON.parse(localStorage.getItem(COLA_KEY)||"[]"); }catch(e){ return []; } }
function guardarCola(c){ try{ localStorage.setItem(COLA_KEY,JSON.stringify(c)); }catch(e){} }
function pintarAgente(vivo,enCola){
  const b=document.getElementById("agbadge"); if(!b) return;
  if(!PUENTE){ b.style.display="none"; return; }
  b.style.display="";
  b.textContent = vivo ? ("asistente"+(enCola?(" · "+enCola+" en cola"):"")) : "asistente caído";
  b.className="fchip "+(vivo?(enCola?"viejo":"nuevo"):"viejo");
  const e=document.getElementById("agentestado");
  if(e) e.innerHTML = vivo
    ? "Puente conectado: <b>motor de datos local</b> — responde al instante y sin internet."
    : "Sin conexión con la puente. Las preguntas se <b>guardan en el teléfono</b> y salen solas cuando hay red.";
}
async function sincronizarDatos(manual,m){
  if(!PUENTE) return;
  try{
    if(!m){
      const r=await fetch(PUENTE+"agent/status",{cache:"no-store"});
      if(!r.ok){ if(manual) logMsg("a","No hay conexión con el puente (¿está corriendo en la PC?)."); return; }
      const st=await r.json(); m=st.datos;
    }
    let prev=null; try{ prev=JSON.parse(localStorage.getItem("hw_datos_version")||"null"); }catch(e){}
    if(prev&&prev.version===m.version){ if(manual) logMsg("i","Datos al día: "+m.archivos.length+" archivos (v"+m.version+")."); return; }
    const prevMap={}; (prev&&prev.archivos?prev.archivos:[]).forEach(a=>prevMap[a.nombre]=a.hash);
    let bajados=0;
    for(const a of m.archivos){
      if(prevMap[a.nombre]===a.hash) continue;
      try{ const rr=await fetch(PUENTE+"sync/file?name="+encodeURIComponent(a.nombre));
        if(rr.ok){ const j=await rr.json(); localStorage.setItem("hw_datos_"+a.nombre,JSON.stringify(j)); bajados++; } }catch(e){}
    }
    localStorage.setItem("hw_datos_version",JSON.stringify(m));
    if(bajados) logMsg("i","Actualización: "+bajados+" archivo(s) de datos nuevos. Recargá la app para usarlos.");
    else if(manual) logMsg("i","Datos al día (v"+m.version+").");
  }catch(e){ if(manual) logMsg("a","Error al sincronizar: "+e.message); }
}
async function enviarCola(){
  if(!PUENTE) return;
  const c=colaLocal(); if(!c.length) return;
  try{
    const r=await fetch(PUENTE+"agent/push",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({preguntas:c.map(x=>x.pregunta)})});
    if(r.ok){ const j=await r.json();
      if(j.recibidas){ guardarCola([]); logMsg("i","Se enviaron "+j.recibidas+" pregunta(s) al asistente ("+j.respondidas+" respondidas al instante)."); } }
  }catch(e){}
}
function idsVistas(){ try{ return new Set(JSON.parse(localStorage.getItem("hw_resp_vistas")||"[]")); }catch(e){ return new Set(); } }
function guardarIdsVistas(s){ try{ localStorage.setItem("hw_resp_vistas",JSON.stringify([...s].slice(-200))); }catch(e){} }
async function bajarRespuestas(){
  if(!PUENTE) return;
  let ult=""; try{ ult=localStorage.getItem(ULTID)||""; }catch(e){}
  try{
    const r=await fetch(PUENTE+"agent/answers?desde="+encodeURIComponent(ult));
    if(!r.ok) return;
    const j=await r.json();
    if(j.respuestas&&j.respuestas.length){
      const vistas=idsVistas(); let nuevo=false;
      j.respuestas.forEach(x=>{
        if(vistas.has(x.id)) return;
        vistas.add(x.id); nuevo=true;
        logMsg("a","<b>Asistente:</b> "+x.respuesta.replace(/\n/g,"<br>"));
      });
      if(nuevo) guardarIdsVistas(vistas);
      if(j.ultima_id) localStorage.setItem(ULTID, j.ultima_id);
    }
  }catch(e){}
}
async function preguntarAlAgente(q){
  q=(q||"").trim(); if(!q) return;
  document.getElementById("qagente").value="";
  if(!PUENTE){ logMsg("a","Sin servidor local: abrí la app desde http://<ip-pc>:8080/ para conectarla al asistente."); return; }
  try{
    const r=await fetch(PUENTE+"agent/ask?q="+encodeURIComponent(q.slice(0,600)));
    if(!r.ok) throw new Error("sin respuesta");
    const j=await r.json();
    if(j.estado==="respondida"){ const v=idsVistas(); v.add(j.id); guardarIdsVistas(v);
      logMsg("a","<b>Asistente:</b> "+j.respuesta.replace(/\n/g,"<br>")); }
    else{ const c=colaLocal(); c.push({pregunta:q,fecha:new Date().toISOString()}); guardarCola(c);
      logMsg("a","<b>En cola:</b> el asistente la contestará cuando pueda. ("+c.length+" pendiente(s))"); }
  }catch(e){
    const c=colaLocal(); c.push({pregunta:q,fecha:new Date().toISOString()}); guardarCola(c);
    logMsg("a","<b>Sin conexión con el asistente.</b> Quedó en cola ("+c.length+"); se enviará sola cuando vuelva la red.");
  }
}
async function cicloPuente(){
  if(!PUENTE){ pintarAgente(false,0); return; }
  let st=null;
  try{ const r=await fetch(PUENTE+"agent/status",{cache:"no-store"}); if(r.ok) st=await r.json(); }catch(e){}
  const vivo=!!st;
  pintarAgente(vivo,colaLocal().length);
  if(!vivo) return;
  await sincronizarDatos(false, st?st.datos:null);
  await enviarCola();
  await bajarRespuestas();
  pintarAgente(true,colaLocal().length);
}
function pick(seed,n){ let h=0; const s=String(seed); for(let i=0;i<s.length;i++) h=(h*31+s.charCodeAt(i))>>>0; return h%n; }
/* --- guiones por persona, siempre con datos reales --- */
function guionAsistente(c,o){
  return c.m+", año "+c.y+", número de colección "+c.c+", serie "+c.s+". Clase "+clsDe(c.k).t+". "
    +"Índice de coleccionabilidad "+c.x+" sobre 100, percentil "+c.px+" del catálogo. "
    +"Valor de referencia entre "+hablarMoneda(c.v)+" y "+hablarMoneda(c.V)+". "
    +"Tiempo estimado de venta: entre "+clsDe(c.k).d[0]+" y "+clsDe(c.k).d[1]+" días. "
    +"En tu colección tenés "+(o.q||0)+" unidades en condición "+((COND[o.c]||{l:""}).l)+".";
}
function guionPokedex(c,o){
  const cat = c.k==="STH" ? "el Super Treasure Hunt legendario" : (c.k==="TH" ? "el Treasure Hunt escurridizo" : "un Hot Wheels de la línea básica");
  const cb = CASEBY[c.i];
  const col = c.k==="STH" ? "Pintura Spectraflame y ruedas de goma. Solo aparece en una de cada muchísimas cajas." :
              (c.k==="TH" ? "Lleva el símbolo de llama en la carrocería. Uno por caja." :
               "Fabricado en enormes cantidades. Se reproduce por millones.");
  const rareza = c.x>=58 ? "Su rareza es notable." : (c.x>=44 ? "Su rareza es moderada." : "Es extremadamente común.");
  return c.m+", "+cat+". Número "+c.c+" de la colección del año "+c.y+", de la serie "+c.s+". "
    +col+" "+(cb?("Se le ha visto en la caja "+cb.letra+" del año "+cb.anio+". "):"")
    +rareza+" Índice de coleccionabilidad: "+c.x+" sobre 100. Percentil "+c.px+". "
    +"Su valor estimado va de "+hablarMoneda(c.v)+" a "+hablarMoneda(c.V)+". "
    +"Registrado en tu colección: "+(o.q||0)+" ejemplares. Datos completados.";
}
function guionClarkson(c,o){
  const caro = (c.v+c.V)/2 >= 20, barato = (c.v+c.V)/2 < 4;
  const abierto=[
    "Este es el "+c.m+". Y sí, es exactamente lo que parece: metal con ruedas que caben en un bolsillo.",
    "Aquí tenemos el "+c.m+", año "+c.y+". Un objeto que cuesta menos que el café que te vas a tomar mientras lo mirás.",
    "El "+c.m+". Un Hot Wheels de la serie "+c.s+", número "+c.c+". Emocionante, ¿no?",
    "Miren esto: "+c.m+". Plástico, pintura, y dos euros de nada. ¿Es esto la cima de la ingeniería humana? No. ¿Es divertido? Absolutamente sí.",
    "El "+c.m+". En inglés se llama '"+c.m+"'. En español también. Porque algunos nombres no necesitan traducción, como Ferrari o decepción.",
    "Y aquí, señores, el "+c.m+". Un coche que tu hijo va a querer, tu esposa va a pisar, y tu perro va a morder. Perfecto."
  ];
  const medio = c.k==="STH"
    ? "Y acá viene lo bueno: es un Super Treasure Hunt. Spectraflame, ruedas de verdad, y una probabilidad de encontrarlo en tienda que roza el milagro. Si lo ves colgado en la estantería, no camines: corré. Literalmente. Corré como si te fuera la vida, porque en unos minutos va a estar en el bolsillo de otro."
    : (c.k==="TH"
      ? "Es un Treasure Hunt, o sea que Mattel escondió uno por caja para que vos compres diez cajas. Astuto. Brillante, incluso. La misma táctica que usan los casinos: te hacen gastar más para ganar menos."
      : (barato ? "Es tan común que en las ferias lo usan de vuelto. Y aun así, hay gente que lo colecciona. El mundo está lleno de milagros, señores. Milagros pequeños, de plástico, pero milagros al fin."
                : "No es raro, pero tampoco es basura. Está en ese punto medio donde uno dice: total, cuesta poco. Es como comprar un café: caro para lo que es, pero barato para lo que te hace sentir."));
  const plata = caro
    ? "Su índice de coleccionabilidad es "+c.x+", percentil "+c.px+". En plata: entre "+hablarMoneda(c.v)+" y "+hablarMoneda(c.V)+". Eso sí, después de comisiones, envíos e impuestos te queda lo justo para un completo. Un completo de verdad, no esos de tres pesos."
    : "Vale entre "+hablarMoneda(c.v)+" y "+hablarMoneda(c.V)+". Sí, leíste bien. No te va a pagar el arriendo, pero te va a dar una alegría. Y en este mundo, las alegrías pequeñas son las únicas que podemos permitirnos.";
  const cierre=[
    "Y eso, queridos amigos, es todo lo que sabemos.",
    "Algunos dicen que coleccionar esto es una inversión. Otros dicen que es un auto de juguete. Los dos tienen razón. Y ambos están equivocados al mismo tiempo. Bienvenido a la vida.",
    "Si te gusta, compralo. Si no, dejalo. Pero no me hagas mirar otra foto de una caja cerrada, por favor. Odio las cajas cerradas. Odio no saber qué hay adentro. Es como la curiosidad, pero con más cartón.",
    "Recuerden: en la vida, o eres coleccionista o eres normal. Y ser normal es aburrido. Muy aburrido. Así que coleccionen. Coleccionen todo. Y si alguien pregunta por qué, díganles que es una inversión. Funciona siempre.",
    "Y ahora, si me disculpan, tengo que irme a buscar un Hot Wheels. Es una emergencia. De las buenas."
  ];
  const venta = (c.v+c.V)/2 < 10 ? "Y si pensás venderlo: hacelo en lote, porque de a uno no vale el viaje. Es como vender un solo fósforo: técnicamente possible, pero nadie te lo compra." : "Y sí, se puede vender en eBay. Cobran trece por ciento, por supuesto. Trece por ciento por el privilegio de vender algo que ya es tuyo. El capitalismo, señores, es hermoso.";
  const historia = c.k==="STH" ? "Este modelo es tan escaso que si lo pierdes, tu descendencia te va a maldecir por treinta generaciones." : (c.k==="TH" ? "Este es el tipo de auto que los coleccionistas buscan durante años. Como el amor, pero con más plástico." : "Es un auto común, pero cada auto común tiene su historia. Este, por ejemplo, fue diseñado para ser olvidado. Y sin embargo, aquí está. Como todos nosotros.");
  return abierto[pick(c.i+"a",abierto.length)]+" "+medio+" "+plata+" "+venta+" "
    +"En tu colección tenés "+(o.q||0)+" ejemplares. "+historia+" "+cierre[pick(c.i+"c",cierre.length)];
}
function guion(c,o){
  if(persona==="pokedex") return guionPokedex(c,o);
  if(persona==="clarkson") return guionClarkson(c,o);
  return guionAsistente(c,o);
}
function probarVoz(){
  const c=CAT.filter(function(x){ return x.k==="STH"; })[0]||CAT[0];
  tts(guion(c, col[c.i]||{q:0,c:"carded-nuevo"}));
  logMsg("a","Voz de prueba ("+PERSONAS[persona].n+"): "+c.m+".<span class=\"src\">Cambiá la persona o la voz en el panel de arriba.</span>");
}

/* ===== PWA: instalación, service worker y estado de red ===== */
let deferredPrompt=null;
function instalar(){
  if(deferredPrompt){ deferredPrompt.prompt();
    deferredPrompt.userChoice.then(function(r){ logMsg("a", r.outcome==="accepted"?"Instalando la app…":"Instalación cancelada."); deferredPrompt=null;
      const b=document.getElementById("installbtn"); if(b) b.style.display="none"; }); return; }
  const ua=navigator.userAgent||"";
  const ios=/iPad|iPhone|iPod/.test(ua);
  alert(ios
    ? "En iPhone/iPad: tocá el botón Compartir (□↑) y elegí «Agregar a pantalla de inicio»."
    : "Abrí el menú del navegador (⋮) y elegí «Instalar app» o «Agregar a pantalla de inicio».");
}
function netBadge(){
  const b=document.getElementById("netbadge");
  if(b) b.style.display = navigator.onLine ? "none" : "inline-block";
}
function initPWA(){
  window.addEventListener("beforeinstallprompt", function(e){ e.preventDefault(); deferredPrompt=e;
    const b=document.getElementById("installbtn"); if(b) b.style.display="inline-block"; });
  window.addEventListener("appinstalled", function(){ logMsg("a","App instalada en el dispositivo. Ya funciona sin conexión."); });
  window.addEventListener("online", netBadge); window.addEventListener("offline", netBadge); netBadge();
  if("serviceWorker" in navigator && location.protocol!=="file:"){
    var _swReloading=false;
    navigator.serviceWorker.addEventListener("controllerchange",function(){
      if(_swReloading) return; _swReloading=true; location.reload();
    });
    navigator.serviceWorker.register("sw.js").then(function(reg){
      logMsg("a","Modo app activado: funciona sin conexión y se puede instalar en el celular.",
        "Service worker registrado · "+(navigator.onLine?"en línea":"sin conexión"));
      try{ reg.update(); }catch(e){}
      setInterval(function(){ try{ reg.update(); }catch(e){} }, 60000);
      if(reg.waiting){ try{ reg.waiting.postMessage({type:"SKIP_WAITING"}); }catch(e){} }
      reg.addEventListener("updatefound",function(){
        var nw=reg.installing; if(!nw) return;
        nw.addEventListener("statechange",function(){
          if(nw.state==="installed" && navigator.serviceWorker.controller){ try{ nw.postMessage({type:"SKIP_WAITING"}); }catch(e){} }
        });
      });
    }).catch(function(e){ /* en file:// no aplica */ });
  } else if(location.protocol==="file:"){
    const b=document.getElementById("installbtn");
    if(b){ b.style.display="inline-block"; b.onclick=function(){ alert("Estás abriendo el archivo directamente (file://).\\n\\nPara instalar la app en el celular hay que servirla por HTTPS:\\n\\n1) python serve.py  (red local)\\n2) o publicarla en GitHub Pages / Cloudflare Pages (ver DEPLOY.md)"); }; }
  }
}

/* ===== init ===== */
function refreshAll(){ if(state.tab==="coleccion") renderCol(); const t=document.getElementById("totcol"); if(t) t.textContent=colCount(); }
function initPage(){
  loadCol(); initCur();
  const ys=[...new Set(CAT.map(c=>c.y).filter(y=>y!=null))].sort((a,b)=>b-a), selY=document.getElementById("fyear");
  if(selY) selY.innerHTML=`<option value="">Todos los años</option>`+ys.map(y=>`<option value="${y}">${y}</option>`).join("");
  const ss=[...new Set(CAT.map(c=>c.s))].sort(), selS=document.getElementById("fserie");
  if(selS) selS.innerHTML=`<option value="">Todas las series</option>`+ss.map(s=>`<option value="${s}">${s}</option>`).join("");
  const cats=[...new Set(CAT.map(c=>c.k).filter(Boolean))].sort(), selC=document.getElementById("fcat");
  if(selC) selC.innerHTML=`<option value="">TODAS LAS CATEGORÍAS</option>`+cats.map(c=>`<option value="${c}">${String(c).toUpperCase()}</option>`).join("");
  const paises=[...new Set(CAT.map(c=>c.pais).filter(Boolean))].sort(), selP=document.getElementById("fpais");
  if(selP) selP.innerHTML=`<option value="">Todos los países</option>`+paises.map(p=>`<option value="${p}">${p}</option>`).join("");
  document.querySelectorAll("nav.tabs button").forEach(b=>b.onclick=()=>tabTo(b.dataset.tab));
  const sq=document.getElementById("q"); if(sq) sq.oninput=()=>{state.q=sq.value;render(true);};
  if(selY) selY.onchange=()=>{state.year=selY.value;render(true);};
  if(selS) selS.onchange=()=>{state.serie=selS.value;render(true);};
  if(selC) selC.onchange=()=>{state.cat=selC.value;render(true);};
  if(selP) selP.onchange=()=>{state.pais=selP.value;render(true);};
  // Renderizar grilla de diseñadores
  const disaGrid=document.getElementById('disaGrid');
  if(disaGrid&&typeof DISENADORES!=='undefined'){
        const disaKeys=Object.keys(DISENADORES).sort((a,b)=>a.localeCompare(b));
        disaGrid.innerHTML=disaKeys.map(k=>{
          const d=DISENADORES[k];
      const foto=d.foto?`<img alt="" src="${VER(d.foto)}" style="width:48px;height:48px;border-radius:50%;object-fit:cover;margin-right:10px;border:2px solid var(--brand-primary)">`:'';
      return `<div style="display:flex;align-items:center;padding:10px;border:1px solid var(--border-color);border-radius:8px;cursor:pointer;background:var(--bg-surface)" onclick="mostrarDiseñador('${escJ(k)}')">${foto}<div><b>${esc(k)}</b><br><small>${esc(d.nacionalidad||'')} · ${esc(d.periodo||'')}</small></div></div>`;
    }).join('');
  }
  // Footer diseñadores destacados
  const footerDisa=document.getElementById('footerDisa');
  if(footerDisa&&typeof DISENADORES!=='undefined'){
    const disaKeys=Object.keys(DISENADORES).filter(k=>DISENADORES[k].proyectos&&DISENADORES[k].proyectos.length>=10).sort((a,b)=>(DISENADORES[b].proyectos||[]).length-(DISENADORES[a].proyectos||[]).length).slice(0,20);
    footerDisa.innerHTML=disaKeys.map(k=>`<div style="padding:8px;background:var(--elev);border-radius:6px;font-size:12px"><b>${k}</b> (${DISENADORES[k].proyectos.length} modelos)</div>`).join('');
  }
  // Guía de códigos
  const guiaDiv=document.getElementById('guiaCodigos');
  if(guiaDiv){
    guiaDiv.innerHTML=`<div style="display:grid;gap:12px">${[
      {n:'Código de Asortación',d:'Identifica la caja/case de 72 autos',f:'3-4 letras + 4 números',e:['L2593','C4982','5785'],l:'Lateral de la caja, código de barras'},
      {n:'Código de Modelo/Tool Number',d:'Código único del modelo (casting)',f:'3 letras + 2 números',e:['FRN78','JKX06','JJJ02'],l:'Base del auto, junto al número de serie'},
      {n:'Número de Serie (Toy Number)',d:'Número de producción del modelo',f:'4-5 números',e:['6451','56388','2020'],l:'Base del auto, grabado o impreso'},
      {n:'País de Manufactura',d:'Dónde fue fabricado',f:'Texto',e:['USA','Hong Kong','Malaysia','Thailand','China','Mexico'],l:'Base del auto, junto al tool number'},
      {n:'Tipo de Ruedas',d:'Tipo de ruedas del modelo',f:'Abreviatura',e:['RL (Redline)','BW (Butterfly)','5SP (5 Spoke)','RR (Real Riders)','DD8 (Deep Dish)'],l:'Base del auto, indica el tipo de ruedas'},
      {n:'Tipo de Base',d:'Material del chasis',f:'Texto',e:['Metal','Plastic','ZAMAC'],l:'Base del auto, material del chasis'}
    ].map(s=>`<div style="padding:12px;background:var(--elev);border-radius:6px;border:1px solid var(--line)"><div style="font-weight:600;font-size:14px">${s.n}</div><div class="note" style="margin-top:4px">${s.d}</div><div style="font-size:12px;margin-top:4px"><b>Formato:</b> ${s.f}</div><div style="font-size:12px"><b>Ejemplos:</b> ${s.e.join(', ')}</div><div style="font-size:12px"><b>Dónde aparece:</b> ${s.l}</div></div>`).join('')}</div>`;
  }
  // Anatomía de la caja
  const anatomiaDiv=document.getElementById('anatomiaCaja');
  if(anatomiaDiv){
    anatomiaDiv.innerHTML=`<div style="display:grid;gap:12px">${[
      {n:'Frontal',e:['Logo Hot Wheels','Imagen del auto','Nombre del modelo','Número de serie','Edad recomendada']},
      {n:'Lateral izquierdo',e:['Código de asortación','Código de barras','Precio','País de origen']},
      {n:'Lateral derecho',e:['Código de asortación','Lista de autos del case','Información de seguridad']},
      {n:'Superior',e:['Logo Hot Wheels','Tipo (Mainline/TH/STH)','Año de producción']},
      {n:'Inferior',e:['Código de asortación','Dirección del fabricante','Código de reciclaje']},
      {n:'Interior (blister)',e:['El auto en sí','Tarjeta de colección (TH/STH)','Sticker sheet (algunos modelos)']}
    ].map(p=>`<div style="padding:12px;background:var(--elev);border-radius:6px;border:1px solid var(--line)"><div style="font-weight:600;font-size:14px">${p.n}</div><ul style="margin:8px 0 0;padding-left:20px;font-size:13px">${p.e.map(x=>`<li>${x}</li>`).join('')}</ul></div>`).join('')}</div>`;
  }
  // Categorías especiales
  const catEspDiv=document.getElementById('categoriasEspeciales');
  if(catEspDiv){
    catEspDiv.innerHTML=`<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:8px">${[
      {n:'Spider-Man',c:10,a:'2022-2026',t:'personajes'},
      {n:'Clásicos',c:4189,a:'1976-2026',t:'linea'},
      {n:'RLC & NFT Garage',c:23,a:'2024-2025',t:'club'},
      {n:'Mario Kart',c:112,a:'2019-2025',t:'colaboracion'},
      {n:'Marvel',c:30,a:'2015-2021',t:'personajes'},
      {n:'X-Men',c:5,a:'2023',t:'personajes'},
      {n:'Acceleracers',c:22,a:'',t:'serie'},
      {n:'Racerverse',c:39,a:'2023-2025',t:'serie'},
      {n:'Mainline Themed',c:217,a:'2018-2025',t:'serie'},
      {n:'Daniel Arsham',c:8,a:'2023-2024',t:'colaboracion'},
      {n:'Star Trek 50',c:6,a:'2015-2016',t:'colaboracion'},
      {n:'Despicable Me',c:6,a:'2017',t:'personajes'}
    ].map(c=>`<div style="padding:8px;background:var(--elev);border-radius:6px;font-size:12px"><b>${c.n}</b> (${c.c} modelos)<br><span class="note">${c.a} · ${c.t}</span></div>`).join('')}</div>`;
  }
  // Indicador de versión
  const versionDiv=document.getElementById('versionText');
  if(versionDiv){
    const BUILD='2026-10-18';
    const version='v2.1.0';
    const nModelos=(typeof CAT!=='undefined')?CAT.length:0;
    const nDis=(typeof DISENADORES!=='undefined')?Object.keys(DISENADORES).length:0;
    const nRuedas=(typeof WHEELTYPES!=='undefined')?WHEELTYPES.length:0;
    const nSeries=(typeof SERIES!=='undefined')?SERIES.length:0;
    versionDiv.innerHTML='<b>Versión:</b> '+version+' · <b>Compilado:</b> '+BUILD+
      ' · <b>Modelos:</b> '+nModelos.toLocaleString('es-CL')+
      ' · <b>Diseñadores:</b> '+nDis+
      ' · <b>Ruedas:</b> '+nRuedas+
      ' · <b>Series:</b> '+nSeries;
  }
  const so=document.getElementById("fsort"); if(so) so.onchange=()=>{state.sort=so.value;render(true);};
  // Uniformar orientación de los autos
  const fd=document.getElementById("fdir"), fdt=document.getElementById("fdirTxt");
  const pintaDir=()=>{ if(fdt) fdt.textContent=(state.dir==="DER"?"→":"←"); };
  pintaDir();
  if(fd) fd.onclick=()=>{ state.dir=(state.dir==="DER"?"IZQ":"DER"); localStorage.setItem("hw_dir",state.dir); pintaDir(); render(true); };
  document.querySelectorAll(".chip[data-clase]").forEach(ch=>ch.onclick=()=>{
    state.clase=(state.clase===ch.dataset.clase)?"":ch.dataset.clase;
    document.querySelectorAll(".chip[data-clase]").forEach(x=>x.setAttribute("aria-pressed",String(x.dataset.clase===state.clase)));
    render(true);});
  document.addEventListener("click",e=>{const b=e.target.closest(".card"); if(b) drawer(b.dataset.id);});
  const sent=document.getElementById("sentinel");
  if(sent) new IntersectionObserver(es=>{if(es[0].isIntersecting) render(false);},{rootMargin:"600px"}).observe(sent);
  const qin=document.getElementById("q2"); if(qin) qin.onkeydown=e=>{if(e.key==="Enter"){responder(qin.value);qin.value="";}};
  const tb=document.getElementById("talkbtn"); if(tb) tb.onclick=stt;
  const nv=document.getElementById("netv"); if(nv) nv.oninput=calcNet;
  ["impv","impf"].forEach(id=>{const e=document.getElementById(id); if(e) e.oninput=calcImp;});
  const ic=document.getElementById("impc2c"); if(ic) ic.onchange=calcImp;
  const trc=document.getElementById("ftrend");
  if(trc) trc.onclick=()=>{ state.trending=!state.trending; trc.setAttribute("aria-pressed",String(state.trending)); render(true); };
  if("speechSynthesis" in window){ speechSynthesis.onvoiceschanged=llenarVoces; llenarVoces(); setTimeout(llenarVoces,600); }
  cargarEdgeVoces();
  setPersona(persona);
  try{ document.getElementById("datosfuente").textContent="Datos: "+DATOS_FUENTE.origen; }catch(e){}
  try{ if(iaKey()){ const s=document.getElementById("iainfo"); if(s) s.innerHTML="IA activada con <b>Groq</b> (1.000 consultas/día gratis). La key queda solo en este navegador."; } }catch(e){}
  try{ SBClient.init(); SBClient.refrescarBadgeCuenta(); }catch(e){}
  cicloPuente(); setInterval(cicloPuente,60000);

  // Funciones de formulario de modelos
  window.guardarModelo=function(){
    const nombre=document.getElementById('fNombre')?.value?.trim();
    const anio=parseInt(document.getElementById('fAnio')?.value);
    const tool=document.getElementById('fTool')?.value?.trim();
    const serie=document.getElementById('fSerie')?.value?.trim();
    const msg=document.getElementById('formMsg');
    if(!nombre||!anio||!tool||!serie){ if(msg) msg.innerHTML='<span style="color:#e74c3c">⚠️ Completá todos los campos obligatorios (*)</span>'; return; }
    const col=document.getElementById('fCol')?.value?.trim()||'';
    const clase=document.getElementById('fClase')?.value||'Mainline';
    const pais=document.getElementById('fPais')?.value||'';
    const imagen=document.getElementById('fImagen')?.value?.trim()||'';
    const imagenLocal=document.getElementById('fImagenLocal')?.value?.trim()||'';
    const descripcion=document.getElementById('fDescripcion')?.value?.trim()||'';
    const historia=document.getElementById('fHistoria')?.value?.trim()||'';
    const curiosidades=document.getElementById('fCuriosidades')?.value?.trim()||'';
    const datoClave=document.getElementById('fDatoClave')?.value?.trim()||'';
    const id=anio+'-'+tool.toUpperCase();
    const nuevo={i:id,m:nombre,y:anio,t:tool.toUpperCase(),c:col,s:serie,k:clase,pais,im:imagenLocal||imagen,ficha:{descripcion,historia,curiosidades,dato_clave:datoClave,conmemorativo:false},valores_mercado:{usd:1,clp:950,eur:0.92,fecha:new Date().toISOString(),fuente:'Cálculo manual'},indice_coleccionabilidad:50,categorias_fandom:[]};
    const idx=CAT.findIndex(c=>c.i===id);
    if(idx>=0){ CAT[idx]=nuevo; if(msg) msg.innerHTML='<span style="color:#2ecc71">✅ Modelo actualizado</span>'; }
    else{ CAT.push(nuevo); if(msg) msg.innerHTML='<span style="color:#2ecc71">✅ Modelo agregado</span>'; }
    render(true);
  };
  window.limpiarFormulario=function(){
    ['fNombre','fAnio','fTool','fCol','fSerie','fImagen','fImagenLocal','fDescripcion','fHistoria','fCuriosidades','fDatoClave'].forEach(id=>{ const e=document.getElementById(id); if(e) e.value=''; });
    const msg=document.getElementById('formMsg'); if(msg) msg.innerHTML='';
  };

  // Modal del diseñador - Diseño unificado y profesional
  window.mostrarDiseñador=function(nombre){
    if(typeof DISENADORES==='undefined'||!DISENADORES[nombre])return;
    const d=DISENADORES[nombre];
    const iniciales=nombre.split(' ').filter(Boolean).map(w=>w[0]).join('').substring(0,2).toUpperCase();
    const lang=document.documentElement.lang||'es';
    const bio=d['bio_'+lang+'_v2']||d['bio_'+lang]||d.bio_es_v2||d.biografia_limpia||d.bio_es||'Biografía no disponible para este diseñador.';
    const castings=Array.isArray(d.castings)?d.castings:[];
    const nCast=(d.n_castings!=null)?d.n_castings:castings.length;
    const idx=Object.keys(DISENADORES).indexOf(nombre)+1;
    const num=String(idx).padStart(3,'0');
    const fuente=d.fuente||('https://hotwheels.fandom.com/wiki/'+encodeURIComponent(nombre.replace(/ /g,'_')));
    const meta=d.meta||{};
    const rol=meta.title||(d.tipo==='grafico'?'Diseñador gráfico':'Diseñador de castings');
    const periodo=d.periodo||meta.years||'';
    const foto=d.foto
      ? '<img src="'+VER(d.foto)+'" alt="'+esc(nombre)+'" onerror="this.outerHTML=\'<div class=&quot;fc-ini&quot;>'+iniciales+'</div>\'">'
      : '<div class="fc-ini">'+iniciales+'</div>';
    // años activos desde los castings
    const anios=[...new Set(castings.map(c=>c.anio).filter(Boolean))].sort();
    const rangoAnios=anios.length?(anios[0]+'–'+anios[anios.length-1]):(periodo||'—');
    // series principales
    const serieCnt={};
    castings.forEach(c=>{const s=(c.serie||'').trim();if(s)serieCnt[s]=(serieCnt[s]||0)+1;});
    const topSeries=Object.entries(serieCnt).sort((a,b)=>b[1]-a[1]).slice(0,4);
    const seriesHtml=topSeries.length?topSeries.map(([s,n])=>'<span class="fc-tag">'+esc(s)+' <b>'+n+'</b></span>').join(''):'<span class="fc-tag fc-tag-off">sin datos</span>';
    // tabla de castings (TODOS)
    const filas=castings.map(c=>'<tr><td class="y">'+esc(c.anio||'')+'</td><td class="n">'+esc(c.nombre||'')+'</td><td>'+esc(c.serie||'')+'</td><td class="t">'+esc(c.toy||c.edicion||'')+'</td></tr>').join('');
    const tablaHtml=nCast?('<div class="fc-cast"><table><thead><tr><th>Año</th><th>Casting</th><th>Serie de debut</th><th>Nº</th></tr></thead><tbody>'+filas+'</tbody></table></div>'):'<div class="fc-empty">No se han documentado castings de este diseñador en la fuente.</div>';
    // código de barras decorativo derivado del nombre
    let h=0;for(let i=0;i<nombre.length;i++)h=(h*31+nombre.charCodeAt(i))>>>0;
    const barras=Array.from({length:44},(_,i)=>((h>>(i%30))&1)?'<i style="height:'+(16+((h>>(i%7))&7)*2)+'px"></i>':'<i style="height:'+(10+((h>>(i%5))&3)*3)+'px"></i>').join('');
    let html='<div class="fc-wrap" onclick="if(event.target===this)this.remove()">'
      +'<div class="fc-card">'
      +'<div class="fc-head">'
        +'<span class="fc-num">#'+num+'</span>'
        +'<img src="assets/logo-header.png" alt="HW Collector">'
        +'<div class="fc-series">Designer Series<small>Colección de diseñadores</small></div>'
        +'<button class="fc-x" onclick="this.closest(\'.fc-wrap\').remove()" aria-label="Cerrar">&times;</button>'
      +'</div>'
      +'<div class="fc-hero">'
        +'<div class="fc-blister">'+foto+'</div>'
        +'<div class="fc-heroinfo">'
          +'<div class="fc-name">'+esc(nombre)+'</div>'
          +'<div class="fc-role">'+esc(rol)+'</div>'
          +(periodo?'<div class="fc-yrs">Activo: '+esc(periodo)+'</div>':'')
          +(d.nacionalidad?'<div class="fc-yrs">Origen: '+esc(d.nacionalidad)+'</div>':'')
        +'</div>'
      +'</div>'
      +'<div class="fc-stats">'
        +'<div class="fc-stat"><b>'+nCast.toLocaleString('es-CL')+'</b><span>Castings</span></div>'
        +'<div class="fc-stat"><b>'+esc(rangoAnios)+'</b><span>Años activo</span></div>'
        +'<div class="fc-stat"><b>'+Object.keys(serieCnt).length+'</b><span>Series</span></div>'
        +'<div class="fc-stat"><b>'+anios.length+'</b><span>Años con lanzamientos</span></div>'
      +'</div>'
      +'<div class="fc-sec"><h4>Biografía</h4><div class="fc-bio">'+esc(bio)+'</div></div>'
      +'<div class="fc-sec"><h4>Series en las que participó</h4><div class="fc-tags">'+seriesHtml+'</div></div>'
      +'<div class="fc-sec"><h4>Todos sus castings ('+nCast.toLocaleString('es-CL')+')</h4>'+tablaHtml+'</div>'
      +'<div class="fc-foot">'
        +'<div class="fc-src">Fuente: <a href="'+esc(fuente)+'" target="_blank" rel="noopener">Hot Wheels Wiki (Fandom)</a> · CC BY-SA 3.0<br>Datos curados por la comunidad · HW Collector</div>'
        +'<div class="fc-bar">'+barras+'</div>'
      +'</div>'
      +'</div></div>';
    document.body.insertAdjacentHTML('beforeend',html);
  };
  // Funciones de compartir y ranking
  window.compartirSitio=function(){
    const url=window.location.href;
    const shareCount=parseInt(localStorage.getItem('hw_share_count')||'0')+1;
    localStorage.setItem('hw_share_count',shareCount);
    const qrUrl='https://api.qrserver.com/v1/create-qr-code/?size=300x300&data='+encodeURIComponent(url);
    let html=`<div id="shareModal" style="position:fixed;inset:0;background:rgba(0,0,0,.92);z-index:200;display:flex;align-items:center;justify-content:center;padding:16px;overflow-y:auto" onclick="if(event.target===this)this.remove()">
      <div style="background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);border:1px solid rgba(255,255,255,.1);border-radius:20px;max-width:440px;width:100%;max-height:92vh;overflow-y:auto;padding:28px;box-shadow:0 25px 50px rgba(0,0,0,.5);color:#fff;font-family:system-ui,-apple-system,sans-serif">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px">
          <h3 style="margin:0;font-size:22px;font-weight:700;letter-spacing:.5px">📤 Compartir</h3>
          <button onclick="document.getElementById('shareModal').remove()" style="background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);color:#fff;width:36px;height:36px;border-radius:8px;cursor:pointer;font-size:20px;display:flex;align-items:center;justify-content:center">×</button>
        </div>
        <div style="display:flex;justify-content:center;margin-bottom:16px">
          <div style="background:#fff;padding:12px;border-radius:12px;box-shadow:0 4px 15px rgba(0,0,0,.3)">
            <img src="${qrUrl}" alt="QR" style="width:200px;height:200px;display:block" onerror="this.src='https://via.placeholder.com/200?text=QR'">
          </div>
        </div>
        <div style="font-size:13px;color:rgba(255,255,255,.7);margin-bottom:12px;text-align:center">Escaneá para abrir en tu celular</div>
        <div style="font-size:11px;color:rgba(255,255,255,.5);word-break:break-all;background:rgba(255,255,255,.05);padding:10px;border-radius:8px;margin-bottom:16px;text-align:center">${url}</div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:20px">
          <button onclick="navigator.clipboard.writeText('${escJ(url)}');this.textContent='✅ Copiado';setTimeout(()=>this.textContent='📋 Copiar',2000)" style="background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);color:#fff;padding:12px 8px;border-radius:8px;cursor:pointer;font-size:13px;font-weight:600">📋 Copiar</button>
          <button onclick="window.open('https://wa.me/?text=${encodeURIComponent(url)}','_blank')" style="background:#25D366;border:none;color:#fff;padding:12px 8px;border-radius:8px;cursor:pointer;font-size:13px;font-weight:600">💬 WhatsApp</button>
          <button onclick="window.open('https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}','_blank')" style="background:#1DA1F2;border:none;color:#fff;padding:12px 8px;border-radius:8px;cursor:pointer;font-size:13px;font-weight:600">🐦 Twitter</button>
        </div>
        <div style="border-top:1px solid rgba(255,255,255,.1);padding-top:16px;margin-top:16px">
          <div style="font-weight:600;font-size:13px;margin-bottom:10px;color:rgba(255,255,255,.6);letter-spacing:.5px">📊 ESTADÍSTICAS</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;font-size:13px">
            <div style="padding:10px;background:rgba(255,255,255,.05);border-radius:8px;text-align:center">
              <div style="font-size:20px;font-weight:700">${shareCount}</div>
              <div style="color:rgba(255,255,255,.5);font-size:11px">Compartidos</div>
            </div>
            <div style="padding:10px;background:rgba(255,255,255,.05);border-radius:8px;text-align:center">
              <div style="font-size:20px;font-weight:700">${localStorage.getItem('hw_visit_count')||'1'}</div>
              <div style="color:rgba(255,255,255,.5);font-size:11px">Visitas</div>
            </div>
          </div>
        </div>
      </div>
    </div>`;
    document.body.insertAdjacentHTML('beforeend',html);
  };
  // Contador de visitas
  (function(){const v=parseInt(localStorage.getItem('hw_visit_count')||'0')+1;localStorage.setItem('hw_visit_count',v);})();
  document.addEventListener("visibilitychange",()=>{ if(!document.hidden) cicloPuente(); });
  const t=document.getElementById("totcol"); if(t) t.textContent=colCount();
  const tc=document.getElementById("totcount"); if(tc) tc.textContent=CAT.length.toLocaleString("es");
  const ic2=document.getElementById("imgcount");
  if(ic2) ic2.innerHTML="<b>"+CAT.filter(c=>c.im).length.toLocaleString("es")+"</b> con imagen ("+CAT.filter(c=>c.imr).length+" de referencia)";
  render(true); renderCol(); renderVal(); renderMkt(); renderSeg(); renderCajas();
  initPWA();
  _cargar_trends_activas();
}
window.addEventListener("DOMContentLoaded",initPage);

/* ===== tendencias activas ===== */
function _cargar_trends_activas(){
  var el=document.getElementById("trends-content");
  if(!el) return;
  if(typeof PUENTE==="undefined"||!PUENTE){
    el.innerHTML="<span class='note'>Sin servidor local: tendencias no disponibles.</span>";
    return;
  }
  fetch(PUENTE+"trends",{cache:"no-store"}).then(function(r){
    if(!r.ok) throw new Error("sin datos");
    return r.json();
  }).then(function(d){
    var alertas=d.alertas||[];
    var indice=d.indice_tendencia||{};
    var html="";
    if(alertas.length){
      html+="<div class='warn' style='margin-bottom:10px'><b>⚠ Alertas de tu colección:</b></div>";
      html+=alertas.map(function(a){
        return "<div style='padding:4px 0;border-bottom:1px solid var(--line)'>• <b>"+a.modelo+"</b>: índice "+a.indice_tendencia+" | momentum "+a.momentum+"% | <span class='note'>"+a.nivel+"</span></div>";
      }).join("");
    }
    var top=Object.entries(indice).slice(0,15);
    if(top.length){
      html+="<div style='margin-top:10px'><b>Top tendencia global:</b></div>";
      html+=top.map(function(e){
        return "<div style='display:flex;justify-content:space-between;padding:3px 0;border-bottom:1px solid var(--line)'><span>"+e[0]+"</span><b>"+e[1].toFixed(1)+"</b></div>";
      }).join("");
    }
    if(!html) html="<span class='note'>Sin datos todavía. Ejecutá: python build/trend_watcher.py --sync</span>";
    el.innerHTML=html;
  }).catch(function(){
    el.innerHTML="<span class='note'>Sin conexión con el puente.</span>";
  });
}
setInterval(_cargar_trends_activas,60000);

/* ===== WHEEL TYPES DATA ===== */
;

/* ===== SERIES ===== */
;

function renderSeries(){
  var grid=document.getElementById('seriesGrid');
  if(!grid) return;
  var search=(document.getElementById('serieSearch').value||'').toLowerCase();
  var sort=document.getElementById('serieSort').value;
  var filtered=SERIES.filter(function(s){return !search || s.n.toLowerCase().indexOf(search)>=0;});
  if(sort==='az') filtered.sort(function(a,b){return a.n.localeCompare(b.n);});
  else filtered.sort(function(a,b){return b.cant-a.cant;});
  var html='';
  if(filtered.length===0){html='<div class="note" style="grid-column:1/-1;text-align:center;padding:40px">No se encontraron series.</div>';}
  else{
    html=filtered.slice(0,300).map(function(s){
      var ini=s.n.substring(0,2).toUpperCase();
      var img=s.img?'<img src="'+s.img+'" alt="" style="width:100%;height:80px;object-fit:contain;background:#fff" onerror="this.outerHTML=\'<div style=\'width:100%;height:80px;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:700;color:#ff6b35\'>'+ini+'</div>\'">':'<div style="width:100%;height:80px;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:700;color:#ff6b35;background:linear-gradient(135deg,#2a2a3e,#1a1a2e)">'+ini+'</div>';
      return '<div onclick="showSerieDetail(\''+s.n.replace(/'/g,"\\'")+'\')" style="background:var(--elev);border:1px solid var(--line);border-radius:12px;overflow:hidden;cursor:pointer;transition:transform .2s,border-color .2s" onmouseover="this.style.borderColor=\'#ff4d00\';this.style.transform=\'translateY(-2px)\'" onmouseout="this.style.borderColor=\'var(--line)\';this.style.transform=\'none\'">'+
        img+
        '<div style="padding:10px">'+
        '<div style="font-weight:600;font-size:14px;color:var(--text)">'+s.n+'</div>'+
        '<div style="font-size:11px;color:var(--muted);margin-top:3px">'+s.y+' · '+s.cant+' modelos</div>'+
        '</div></div>';
    }).join('');
  }
  grid.innerHTML=html;
  var c=document.getElementById('serieCounter');
  if(c) c.textContent=filtered.length+' series';
}
function showSerieDetail(nombre){
  var s=SERIES.find(function(x){return x.n===nombre;});
  if(!s) return;
  var content=document.getElementById('serieModalContent');
  content.innerHTML='<h3 style="margin:0 0 6px;color:#ff6b35">'+s.n+'</h3>'+
    '<div style="color:var(--muted);font-size:13px;margin-bottom:14px">'+s.y+' · '+s.cant+' modelos en el catálogo</div>'+
    '<div style="background:var(--elev);border:1px solid var(--line);border-radius:8px;padding:14px;margin-bottom:16px">'+
    '<div style="font-weight:600;font-size:12px;color:var(--muted);margin-bottom:6px">DESCRIPCIÓN</div>'+
    '<div style="font-size:14px;line-height:1.6;color:var(--text)">'+(s.d||'Sin descripción disponible.')+'</div></div>'+
    '<div style="display:flex;gap:8px;justify-content:center"><button onclick="closeSerieModal()" style="padding:10px 20px;background:var(--brand);color:#fff;border:none;border-radius:8px;cursor:pointer">Cerrar</button></div>';
  document.getElementById('serieModal').style.display='block';
}
function closeSerieModal(){document.getElementById('serieModal').style.display='none';}


/* ===== ICONO CSS DE RUEDA ===== */
function wheelIcon(spokes, color, size) {
  size = size || 60;
  var half = size / 2;
  var c = color || '#ff4d00';
  var s = spokes || 0;
  var spokesHtml = '';
  if (s > 0) {
    for (var i = 0; i < s; i++) {
      var angle = (360 / s) * i;
      spokesHtml += '<div style="position:absolute;top:50%;left:50%;width:2px;height:' + (half-4) + 'px;background:' + c + ';transform-origin:0 0;transform:rotate(' + angle + 'deg) translateY(-100%);border-radius:1px"></div>';
    }
  }
  return '<div style="position:relative;width:' + size + 'px;height:' + size + 'px;border-radius:50%;background:radial-gradient(circle,#333 0%,#111 70%);border:3px solid ' + c + ';margin:0 auto;box-shadow:inset 0 0 10px rgba(0,0,0,0.5)">' +
    '<div style="position:absolute;top:50%;left:50%;width:' + (size*0.3) + 'px;height:' + (size*0.3) + 'px;border-radius:50%;background:#222;border:2px solid ' + c + ';transform:translate(-50%,-50%)"></div>' +
    spokesHtml + '</div>';
}

/* ===== RENDER RUEDAS ===== */
function renderRuedas() {
  var grid = document.getElementById('wheelGrid');
  if (!grid) return;
  var search = (document.getElementById('ruedaSearch').value || '').toLowerCase();
  var yearFilter = document.getElementById('ruedaYearFilter').value;
  var catFilter = document.getElementById('ruedaCatFilter').value;
  
  var filtered = WHEELTYPES.filter(function(w) {
    var matchSearch = !search || w.c.toLowerCase().indexOf(search) >= 0 || w.n.toLowerCase().indexOf(search) >= 0;
    var matchCat = !catFilter || w.cat === catFilter;
    var matchYear = true;
    if (yearFilter) {
      var yr = parseInt(yearFilter);
      var years = w.y.split('-');
      var start = parseInt(years[0]);
      var end = years[1] === 'presente' ? 2026 : parseInt(years[1]);
      matchYear = yr >= start && yr <= end;
    }
    return matchSearch && matchCat && matchYear;
  });
  
  var html = '';
  if (filtered.length === 0) {
    html = '<div class="note" style="grid-column:1/-1;text-align:center;padding:40px">No se encontraron ruedas con esos criterios.</div>';
  } else {
    html = filtered.map(function(w) {
      return '<div onclick="showWheelDetail(\'' + w.c + '\')" style="background:var(--elev);border:1px solid var(--line);border-radius:12px;padding:14px;cursor:pointer;transition:transform 0.2s,border-color 0.2s" onmouseover="this.style.borderColor=\'#ff4d00\';this.style.transform=\'translateY(-2px)\'" onmouseout="this.style.borderColor=\'var(--line)\';this.style.transform=\'none\'">' +
        '<div style="text-align:center;margin-bottom:8px">' + (w.img ? '<img src="' + VER(w.img) + '" alt="' + w.c + '" style="width:60px;height:60px;object-fit:contain;border-radius:50%;background:#fff;border:2px solid ' + w.col + ';padding:4px" onerror="this.outerHTML=wheelIcon(' + w.s + ',\'' + w.col + '\',50)">' : wheelIcon(w.s, w.col, 50)) + '</div>' +
        '<div style="text-align:center;font-weight:600;font-size:14px;color:var(--text)">' + w.c + '</div>' +
        '<div style="text-align:center;font-size:12px;color:var(--muted);margin-top:2px">' + (w.n_es || w.n) + '</div>' +
        '<div style="text-align:center;font-size:11px;color:var(--muted);margin-top:4px">' + w.y + '</div>' +
        '</div>';
    }).join('');
  }
  grid.innerHTML = html;
  
  // Actualizar contador
  var counter = document.getElementById('ruedaCounter');
  if (counter) counter.textContent = filtered.length + ' ruedas';
}

/* ===== MODAL DETALLE RUEDA ===== */
function showWheelDetail(code) {
  var w = WHEELTYPES.find(function(x) { return x.c === code; });
  if (!w) return;
  var lang = 'es';
  try { lang = (localStorage.getItem('hw_lang') || 'es').substring(0,2); } catch(e) {}
  var desc = w.d[lang] || w.d['es'] || '';
  var content = document.getElementById('wheelModalContent');
  content.innerHTML = '<div style="text-align:center;margin-bottom:16px">' + (w.img ? '<img src="' + VER(w.img) + '" alt="' + w.c + '" style="width:140px;height:140px;object-fit:contain;border-radius:50%;background:#fff;border:3px solid ' + w.col + ';padding:8px" onerror="this.outerHTML=wheelIcon(' + w.s + ',\'' + w.col + '\',100)">' : wheelIcon(w.s, w.col, 100)) + '</div>' +
    '<h3 style="text-align:center;margin:0 0 4px;color:var(--text)">' + w.c + ' - ' + (w.n_es || w.n) + '</h3>' +
    '<div style="text-align:center;color:var(--muted);font-size:14px;margin-bottom:16px">Años: ' + w.y + '</div>' +
    '<div style="background:var(--elev);border:1px solid var(--line);border-radius:8px;padding:14px;margin-bottom:16px">' +
    '<div style="font-weight:600;font-size:13px;color:var(--muted);margin-bottom:6px">DESCRIPCIÓN</div>' +
    '<div style="font-size:14px;line-height:1.6;color:var(--text)">' + desc + '</div></div>' +
    '<div style="display:flex;gap:8px;justify-content:center">' +
    '<button onclick="closeWheelModal()" style="padding:10px 20px;background:var(--brand);color:#fff;border:none;border-radius:8px;cursor:pointer">Cerrar</button>' +
    '</div>';
  document.getElementById('wheelModal').style.display = 'block';
}

function closeWheelModal() {
  document.getElementById('wheelModal').style.display = 'none';
}

/* ===== INIT RUEDAS ===== */
function initRuedas() {
  // Poblar filtro de años
  var yearSelect = document.getElementById('ruedaYearFilter');
  if (yearSelect) {
    for (var yr = 1968; yr <= 2026; yr++) {
      var opt = document.createElement('option');
      opt.value = yr;
      opt.textContent = yr;
      yearSelect.appendChild(opt);
    }
  }
  renderRuedas();
}



/* ===== Galeria de la ficha + lightbox (movido aqui: usa IMG/VER del script principal) ===== */

// Popular lista de recientes
(function(){
  var list = document.getElementById('recentList');
  if(!list || typeof CAT === 'undefined') return;
  var recientes = CAT.slice(0, 8);
  list.innerHTML = recientes.map(function(c){
    var img = c.im ? '<img src="'+IMG(c.im)+'" alt="" onerror="this.style.display=\'none\'">' : '<div style="width:40px;height:40px;background:var(--card-bg)"></div>';
    return '<div class="mini-card" onclick="drawer(\''+c.i+'\')">' + img + '<span class="nm">'+esc(c.m)+'</span><span class="tag">'+esc(c.y||'')+'</span></div>';
  }).join('');
})();


/* ===== Galería de la ficha + lightbox ===== */
window.abrirGaleria=function(urls,idx){
  if(!urls||!urls.length) return;
  idx=idx||0;
  let lb=document.createElement('div'); lb.className='lightbox';
  const pinta=()=>{
    lb.innerHTML='<button class="lb-x" onclick="this.parentElement.remove()">&times;</button>'
      +'<img src="'+VER(urls[idx])+'" alt="" onerror="this.style.opacity=.3">'
      +'<div class="lb-nav"><button onclick="event.stopPropagation();window._lbPrev()">&larr;</button>'
      +'<span class="lb-count">'+(idx+1)+' / '+urls.length+'</span>'
      +'<button onclick="event.stopPropagation();window._lbNext()">&rarr;</button></div>';
  };
  window._lbPrev=()=>{ idx=(idx-1+urls.length)%urls.length; pinta(); };
  window._lbNext=()=>{ idx=(idx+1)%urls.length; pinta(); };
  lb.onclick=e=>{ if(e.target===lb) lb.remove(); };
  document.addEventListener('keydown',function k(e){ if(!document.body.contains(lb)){document.removeEventListener('keydown',k);return;} if(e.key==='Escape')lb.remove(); if(e.key==='ArrowLeft')window._lbPrev(); if(e.key==='ArrowRight')window._lbNext(); });
  document.body.appendChild(lb); pinta();
};
window.galeriaHTML=function(c){
  const g=(c&&c.galeria)||[];
  if(!g.length) return '';
  const prim=g[0];
  const resto=g.slice(1);
  const thumbs=g.slice(0,8).map((u,i)=>'<img src="'+VER(u)+'" alt="" loading="lazy" onclick="abrirGaleria('+JSON.stringify(g).replace(/"/g,'&quot;')+','+i+')" onerror="this.style.visibility=\'hidden\'">').join('');
  return '<div class="sec" style="border:1px solid var(--line);padding:12px;margin-bottom:10px"><h3 style="margin:0 0 8px">Galería ('+g.length+')</h3><div class="galeria-grid">'+thumbs+'</div>'
    +((g.length>8)?'<div class="galeria-vacia">+ '+(g.length-8)+' imágenes más (hacé clic para recorrerlas)</div>':'')+'</div>';
};


