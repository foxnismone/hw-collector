# -*- coding: utf-8 -*-
"""
Generador de las páginas HTML de HW Collector.

Uso:  python build/build_app.py

Lee  : data/catalog_web.json, data/precios_referencia.json,
       data/owned_collection.json, data/mercados.json
Escribe: web/index.html, web/galeria_catalogo.html, web/galeria_coleccion.html

Todo el JSON se embebe en el HTML a propósito: fetch() de archivos locales
está bloqueado por CORS en file://, y las galerías deben abrirse con doble clic.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(name):
    with open(os.path.join(ROOT, "data", name), encoding="utf-8") as f:
        return json.load(f)


CAT = load("catalog_web.json")
PRE = load("precios_referencia.json")
OWNED = load("owned_collection.json")
MKT = load("mercados.json")
SEG = load("seguimiento.json")
TEND = load("tendencias.json")
CAJ = load("cajas.json")
HIST = load("historias.json")
IDXI = load("indice.json")

CSS = """
*{box-sizing:border-box}
:root{
 --base:#0c0e12; --surface:#15181e; --elev:#1d2128; --line:#2a2f38;
 --ink:#eef1f5; --muted:#98a1ad; --accent:#ff4d00; --ok:#2fbf71; --warn:#e8b23a;
 --f-display:"Bahnschrift","DIN Alternate","Segoe UI Variable Display",system-ui,sans-serif;
 --f-body:"Segoe UI","Segoe UI Variable Text",system-ui,-apple-system,sans-serif;
 --f-mono:"Cascadia Mono",Consolas,"SF Mono",monospace;
}
html,body{margin:0;background:var(--base);color:var(--ink);font-family:var(--f-body);font-size:14px}
a{color:var(--accent);text-decoration:none}
header.top{position:sticky;top:0;z-index:40;background:var(--surface);border-bottom:1px solid var(--line)}
.bar{display:flex;align-items:center;gap:14px;padding:10px 18px;flex-wrap:wrap}
.brand{display:flex;align-items:baseline;gap:10px}
.brand h1{font-family:var(--f-display);font-size:19px;letter-spacing:.5px;margin:0;text-transform:uppercase;font-weight:700}
.brand h1 span{color:var(--accent)}
.brand .sub{color:var(--muted);font-size:11px;letter-spacing:.6px;text-transform:uppercase}
nav.tabs{display:flex;gap:2px;margin-left:auto;flex-wrap:wrap}
nav.tabs button{background:transparent;border:1px solid transparent;color:var(--muted);padding:7px 12px;font-size:12.5px;
 font-family:var(--f-display);letter-spacing:.6px;text-transform:uppercase;cursor:pointer;border-radius:2px}
nav.tabs button:hover{color:var(--ink)}
nav.tabs button[aria-selected="true"]{background:var(--elev);color:var(--ink);border-color:var(--line)}
.cur{display:flex;align-items:center;gap:6px;font-size:11px;color:var(--muted)}
.cur select{min-height:30px;padding:5px 8px;font-size:12px}
.filters{display:flex;gap:10px;align-items:center;padding:10px 18px;border-top:1px solid var(--line);flex-wrap:wrap;background:var(--base)}
input[type=search],input[type=text],input[type=number],select{background:var(--elev);border:1px solid var(--line);color:var(--ink);
 padding:8px 10px;border-radius:2px;font-family:var(--f-body);font-size:13px;min-height:34px}
input[type=search]{min-width:250px}
input:focus,select:focus{outline:2px solid var(--accent)}
.chips{display:flex;gap:6px;flex-wrap:wrap}
.chip{background:var(--elev);border:1px solid var(--line);color:var(--muted);padding:6px 11px;border-radius:2px;
 cursor:pointer;font-size:12px;font-family:var(--f-display);letter-spacing:.5px}
.chip[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:#fff}
main{padding:16px 18px 60px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;background:var(--line);border:1px solid var(--line);margin-bottom:16px}
.stat{background:var(--surface);padding:12px 14px}
.stat .k{font-size:10.5px;letter-spacing:.8px;text-transform:uppercase;color:var(--muted);font-family:var(--f-display)}
.stat .v{font-family:var(--f-mono);font-size:23px;margin-top:3px;font-variant-numeric:tabular-nums}
.stat .n{font-size:11px;color:var(--muted);margin-top:2px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(178px,1fr));gap:12px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:3px;overflow:hidden;cursor:pointer;position:relative;
 display:flex;flex-direction:column;text-align:left;padding:0;color:inherit;font:inherit}
.card:hover{border-color:var(--accent)}
.thumb{aspect-ratio:1/1;background:var(--elev);display:block;width:100%;object-fit:contain;padding:8px}
.card .body{padding:9px 10px 10px;display:flex;flex-direction:column;gap:5px;flex:1}
.card .nm{font-size:12.8px;font-weight:600;line-height:1.25}
.card .mt{font-size:11px;color:var(--muted);font-family:var(--f-mono)}
.chipc{position:absolute;top:7px;left:7px;font-size:9.5px;font-family:var(--f-display);letter-spacing:.7px;
 padding:2px 6px;border-radius:2px;background:var(--elev);border:1px solid var(--line);color:var(--muted);text-transform:uppercase}
.chipc.STH{background:#4a1200;border-color:var(--accent);color:#ffb795}
.chipc.TH{background:#3a2c00;border-color:var(--warn);color:#f0d28a}
.qty{position:absolute;top:7px;right:7px;background:var(--accent);color:#fff;font-family:var(--f-mono);font-size:11px;}
.cardwrap{position:relative;display:inline-block}
.cardedit{position:absolute;top:4px;right:4px;background:var(--elev);border:1px solid var(--line);color:var(--ink);width:28px;height:28px;border-radius:4px;cursor:pointer;font-size:14px;display:flex;align-items:center;justify-content:center;z-index:2}
.cardedit:hover{background:var(--brand)}
.carddel{position:absolute;top:4px;right:36px;background:var(--elev);border:1px solid #e74c3c;color:#e74c3c;width:28px;height:28px;border-radius:4px;cursor:pointer;font-size:14px;display:flex;align-items:center;justify-content:center;z-index:2}
.carddel:hover{background:#e74c3c;color:#fff}
.dem{position:absolute;bottom:0;left:0;right:0;background:#1b1206;border-top:1px solid var(--warn);color:var(--warn);
 font-family:var(--f-display);font-size:9.5px;letter-spacing:.7px;text-align:center;padding:2px 0;text-transform:uppercase}
.segrow{display:grid;grid-template-columns:56px 1fr 150px 150px 190px;gap:12px;align-items:center;background:var(--surface);
 border:1px solid var(--line);padding:9px 11px;margin-bottom:7px}
.segrow img{width:56px;height:56px;object-fit:contain;background:var(--elev)}
.segrow .sinfo{display:flex;flex-direction:column;gap:2px;min-width:0}
.segrow .sinfo b{font-size:13px}
.segrow .sval{display:flex;flex-direction:column;align-items:flex-start;gap:1px}
.segrow .sfr{display:flex;flex-direction:column;gap:4px}
.segrow .sacc{display:flex;gap:6px;flex-wrap:wrap}
.segrow .dem{position:static;display:inline-block;border:1px solid var(--warn);padding:1px 6px;width:max-content}
.fchip{font-family:var(--f-mono);font-size:10.5px;padding:2px 7px;border:1px solid var(--line);border-radius:2px;width:max-content}
.fchip.fresco{border-color:var(--ok);color:var(--ok)}
.fchip.aceptable{border-color:var(--warn);color:var(--warn)}
.fchip.viejo{border-color:#c0392b;color:#ff9b8a}
.alrow{display:flex;gap:10px;align-items:flex-start;padding:9px 11px;border:1px solid var(--line);background:var(--surface);margin-bottom:6px;font-size:12.5px}
.alrow.alta{border-left:3px solid var(--accent)}
.alrow.media{border-left:3px solid var(--warn)}
.alrow.baja{border-left:3px solid var(--line)}
.altipo{font-family:var(--f-display);font-size:10px;letter-spacing:.7px;min-width:66px;color:var(--muted)}
#albadge{display:none;background:var(--accent);color:#fff;font-family:var(--f-mono);font-size:11px;padding:2px 7px;border-radius:2px}
.casegrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}
.casecard{background:var(--surface);border:1px solid var(--line)}
.casecard.marked{border-color:var(--ok)}
.casecard .ch{display:flex;align-items:center;justify-content:space-between;padding:10px 12px;border-bottom:1px solid var(--line);background:var(--elev)}
.casecard .ch b{font-family:var(--f-display);font-size:15px;letter-spacing:1px;text-transform:uppercase}
.casecard .ch span{font-family:var(--f-mono);font-size:11px;color:var(--muted)}
.casecard .cbody{padding:10px 12px;display:flex;flex-direction:column;gap:9px}
.crow{display:flex;gap:9px;align-items:flex-start}
.crow img{width:52px;height:52px;object-fit:contain;background:var(--elev);flex:0 0 auto}
.crow .cinfo{display:flex;flex-direction:column;gap:2px;min-width:0;flex:1}
.crow .cinfo b{font-size:12.5px}
.tag{font-family:var(--f-display);font-size:9px;letter-spacing:.7px;padding:1px 5px;border-radius:2px;border:1px solid var(--line);width:max-content}
.tag.th{background:#3a2c00;border-color:var(--warn);color:#f0d28a}
.tag.sth{background:#4a1200;border-color:var(--accent);color:#ffb795}
.mark{background:transparent;border:1px solid var(--line);color:var(--muted);font-size:10.5px;padding:3px 7px;cursor:pointer;border-radius:2px;width:max-content}
.mark.on{border-color:var(--ok);color:var(--ok)}
.casecard textarea{width:100%;background:var(--elev);border:1px solid var(--line);color:var(--ink);font-family:var(--f-body);font-size:11.5px;padding:6px;resize:vertical;min-height:38px}
.decoder{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.decoder input{max-width:110px;text-transform:uppercase}
#decout{font-family:var(--f-mono);font-size:12.5px}
.idx{height:4px;background:var(--elev);border-radius:2px;overflow:hidden}
.idx i{display:block;height:100%;background:var(--accent)}
.fbar2{margin-bottom:11px}
.fbar2 .fl{font-size:11.5px;color:var(--muted);font-family:var(--f-display);letter-spacing:.4px;margin-bottom:3px}
.fbar2 .fl b{color:var(--ink)}
.fbar2 .peso{float:right;font-family:var(--f-mono);font-size:10.5px;opacity:.75}
.fbar2 .ftrack{position:relative;height:14px;background:var(--elev);border-radius:2px;overflow:hidden}
.fbar2 .ftrack i{display:block;height:100%;border-radius:2px}
.fbar2 .fnum{position:absolute;right:5px;top:0;line-height:14px;font-family:var(--f-mono);font-size:10.5px;color:#0c0e12;font-weight:700;mix-blend-mode:normal}
.fbar2 .fsrc{font-size:10.5px;color:var(--muted);margin-top:2px;line-height:1.4}
.medido{background:#0f2418;border:1px solid var(--ok);color:var(--ok);font-size:9px;padding:0 4px;border-radius:2px;font-family:var(--f-display)}
.metodo{margin-top:10px;background:var(--elev);border-left:3px solid var(--accent);padding:9px 11px;font-size:11px;line-height:1.55;color:var(--muted)}
.idxrow{display:flex;justify-content:space-between;font-size:10.5px;color:var(--muted);font-family:var(--f-mono)}
.empty{padding:40px;text-align:center;color:var(--muted);border:1px dashed var(--line);grid-column:1/-1}
#sentinel{height:1px}
.drawer{position:fixed;inset:0 0 0 auto;width:min(560px,100%);background:var(--surface);border-left:1px solid var(--line);
 transform:translateX(100%);transition:transform .18s ease;z-index:60;overflow-y:auto;box-shadow:-20px 0 40px rgba(0,0,0,.5)}
.drawer[data-open="1"]{transform:none}
.drawer .dh{display:flex;gap:14px;padding:16px;border-bottom:1px solid var(--line);align-items:flex-start;position:sticky;top:0;background:var(--surface)}
.drawer .dh img{width:120px;height:120px;object-fit:contain;background:var(--elev);border:1px solid var(--line)}
.drawer h2{font-family:var(--f-display);font-size:17px;margin:0 0 6px;line-height:1.2}
.kv{display:grid;grid-template-columns:130px 1fr;gap:6px 12px;padding:14px 16px;font-size:12.5px;border-bottom:1px solid var(--line)}
.kv .k{color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.6px;font-family:var(--f-display)}
.kv .v{font-family:var(--f-mono)}
.sec{padding:14px 16px;border-bottom:1px solid var(--line)}
.sec h3{font-family:var(--f-display);font-size:12px;letter-spacing:.9px;text-transform:uppercase;color:var(--muted);margin:0 0 10px}
.fbar{display:grid;grid-template-columns:120px 1fr 46px;gap:9px;align-items:center;font-size:12px;margin-bottom:7px}
.fbar .fill{height:8px;background:var(--elev);border-radius:2px;overflow:hidden}
.fbar .fill i{display:block;height:100%;background:var(--accent)}
.fbar .num{font-family:var(--f-mono);text-align:right;font-size:11.5px}
.btn{background:var(--accent);color:#fff;border:1px solid var(--accent);padding:9px 14px;border-radius:2px;cursor:pointer;
 font-family:var(--f-display);letter-spacing:.6px;text-transform:uppercase;font-size:12px;min-height:38px}
.btn.ghost{background:transparent;color:var(--ink);border-color:var(--line)}
.btn.ghost:hover{border-color:var(--accent);color:var(--accent)}
.btnrow{display:flex;gap:8px;flex-wrap:wrap;padding:14px 16px}
.warn{background:#2a2205;border:1px solid var(--warn);color:#f0d9a0;padding:9px 11px;font-size:11.5px;border-radius:2px;margin-top:9px}
.okbox{background:#0f2418;border:1px solid var(--ok);color:#a9e6c4;padding:9px 11px;font-size:11.5px;border-radius:2px;margin-top:9px}
.close{position:absolute;right:12px;top:12px;background:var(--elev);border:1px solid var(--line);color:var(--ink);
 width:32px;height:32px;border-radius:2px;cursor:pointer;font-size:16px}
table.t{width:100%;border-collapse:collapse;font-size:12px}
table.t th,table.t td{text-align:left;padding:7px 9px;border-bottom:1px solid var(--line);vertical-align:top}
table.t th{color:var(--muted);font-size:10.5px;letter-spacing:.7px;text-transform:uppercase;font-family:var(--f-display);font-weight:400}
table.t td.num{font-family:var(--f-mono);text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
table.t tr.best td{background:#1a1408}
table.t tr.best td:first-child{box-shadow:inset 3px 0 0 var(--accent)}
.dist{display:grid;gap:5px}
.dist .row{display:grid;grid-template-columns:78px 1fr 46px;gap:9px;align-items:center;font-size:11.5px}
.dist .fill{height:9px;background:var(--elev);border-radius:2px;overflow:hidden}
.dist .fill i{display:block;height:100%;background:var(--accent)}
.dist .num{font-family:var(--f-mono);text-align:right;color:var(--muted)}
.note{color:var(--muted);font-size:11.5px;line-height:1.55}
.mktgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:12px;margin-bottom:14px}
.mktcard{background:var(--surface);border:1px solid var(--line);padding:0 0 10px}
.mktcard .mh{display:flex;align-items:center;justify-content:space-between;padding:11px 13px;border-bottom:1px solid var(--line)}
.mktcard .mh b{font-family:var(--f-display);letter-spacing:.6px;text-transform:uppercase;font-size:12.5px}
.mktcard .mh span{font-family:var(--f-mono);font-size:11px;color:var(--muted)}
.mktcard table.t{font-size:11.5px}
.assistant{display:grid;grid-template-columns:1fr;gap:12px;max-width:900px}
.log{background:var(--surface);border:1px solid var(--line);padding:12px;min-height:220px;max-height:420px;overflow-y:auto;
 display:flex;flex-direction:column;gap:9px}
.msg{padding:9px 11px;border-radius:2px;font-size:13px;line-height:1.5;max-width:88%}
.msg.u{background:var(--elev);align-self:flex-end;border:1px solid var(--line)}
.msg.a{background:#20160f;border-left:3px solid var(--accent)}
.msg .src{display:block;margin-top:5px;font-size:10.5px;color:var(--muted);font-family:var(--f-mono)}
.rowin{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.rowin input{flex:1;min-width:120px}
.stepper{display:flex;align-items:center;border:1px solid var(--line);border-radius:2px;overflow:hidden}
.stepper button{background:var(--elev);border:0;color:var(--ink);width:30px;height:30px;cursor:pointer;font-size:15px}
.stepper .q{font-family:var(--f-mono);min-width:34px;text-align:center}
@media(max-width:640px){
 .grid{grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:9px}
 input[type=search]{min-width:100%;width:100%}
 .drawer{width:100%}
 .kv{grid-template-columns:104px 1fr}
 main{padding:12px}
 .mktgrid{grid-template-columns:1fr}
}
"""

JS = r"""
/* ===== datos embebidos ===== */
const CAT=__CAT__, PRE=__PRE__, OWNED_DEMO=__OWNED__, MKT=__MKT__, SEG=__SEG__, TEND=__TEND__, CAJ=__CAJ__, IDXINFO=__IDXI__, HIST=__HIST__;
const CASEBY={};
Object.keys(CAJ.cajas_por_anio).forEach(function(y){ (CAJ.cajas_por_anio[y]||[]).forEach(function(c){
  ["TH","STH"].forEach(function(t){ if(c[t]&&c[t].catalogo_id) CASEBY[c[t].catalogo_id]={letra:c.letra,anio:y,tipo:t}; }); }); });
const DEM={};
[["enero_2026",TEND.demanda_coleccionistas.enero_2026],["febrero_2026",TEND.demanda_coleccionistas.febrero_2026]]
 .forEach(function(pair){ pair[1].forEach(function(d){ (d.catalogo_ids||[]).forEach(function(cid){
   var prev=DEM[cid]; if(!prev||d.rank<prev.rank) DEM[cid]={rank:d.rank,modelo:d.modelo,coleccionistas:d.coleccionistas,mes:pair[0]}; }); }); });
const IMG=f=>f?(/^https?:\/\//.test(f)?f:"img/"+f):"";
const CLS={STH:{t:"Super Treasure Hunt",v:[85,250],d:[7,28],f:"autoevolution/resellcalendar 2024-2025"},
           TH:{t:"Treasure Hunt",v:[5,20],d:[7,30],f:"iCollectEverything 2026"},
           Mainline:{t:"Mainline",v:[1,5],d:[14,90],f:"hobbyDB listings 2024-2025"}};
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
let state={q:"",year:"",clase:"",serie:"",sort:"rel",page:0,per:60,tab:"catalogo",trending:false};
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
    if(state.trending&&!DEM[c.i]) return false;
    if(q&&!(c.m.toLowerCase().includes(q)||c.s.toLowerCase().includes(q)||String(c.t).toLowerCase().includes(q))) return false;
    return true;});
  if(state.sort==="ind") r.sort((a,b)=>b.x-a.x);
  else if(state.sort==="val") r.sort((a,b)=>b.V-a.V);
  else r.sort((a,b)=>b.y-a.y||a.c.localeCompare(b.c));
  return r;
}
function cardHTML(c){
  const o=col[c.i], badge=`<span class="chipc ${c.k!=="Mainline"?c.k:""}">${c.k}</span>`;
  const qty=o&&o.q?`<span class="qty">×${o.q}</span>`:"";
  const dm=DEM[c.i];
  const pie=(dm?"TOP "+dm.rank:"")+(c.imr?(dm?" · ":"")+"imagen ref":"");
  const dbadge=pie?`<span class="dem">${pie}</span>`:"";
  const img=c.im?`<img class="thumb" loading="eager" src="${IMG(c.im)}" alt="" onerror="this.style.visibility='hidden'">`:`<div class="thumb"></div>`;
  const editBtn=o&&o.q?`<button class="cardedit" onclick="event.stopPropagation();editCar('${c.i}')" title="Editar">✎</button>`:"";
  const delBtn=o&&o.q?`<button class="carddel" onclick="event.stopPropagation();if(confirm('Eliminar ${c.m}?'))delCar('${c.i}')" title="Eliminar">×</button>`:"";
  return `<div class="cardwrap">${editBtn}${delBtn}<button class="card" data-id="${c.i}">${badge}${qty}${dbadge}${img}<div class="body">
    <div class="nm">${c.m}</div><div class="mt">${c.y} · #${c.c} · ${String(c.t)}</div>
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
  const catDesc=c.categoria_descripcion?'<div class="note" style="margin-top:6px;font-size:11px;color:var(--muted)">'+c.categoria_descripcion+'</div>':'';
  const fichaHTML=(f.descripcion||f.historia||f.curiosidades)?`<div class="sec" style="border:1px solid var(--line);padding:12px;margin-bottom:10px"><h3 style="margin:0 0 8px">Ficha del modelo</h3>${f.descripcion?'<div style="margin-bottom:6px"><b>Descripción:</b> '+f.descripcion+'</div>':''}${f.historia?'<div style="margin-bottom:6px"><b>Historia:</b> '+f.historia+'</div>':''}${f.curiosidades?'<div style="margin-bottom:6px"><b>Curiosidades:</b> '+f.curiosidades+'</div>':''}${f.conmemorativo?'<div style="margin-bottom:6px"><b>Conmemorativo:</b> Sí</div>':''}${f.dato_clave?'<div><b>Dato clave:</b> '+f.dato_clave+'</div>':''}${catDesc}</div>`:'';
  const idxHTML=idx?`<div class="sec" style="border:1px solid var(--line);padding:12px;margin-bottom:10px"><h3 style="margin:0 0 8px">Índice de coleccionabilidad</h3><div style="font-size:24px;font-weight:700;color:var(--brand)">${idx}</div><div class="note">de 100</div></div>`:'';
  const vmHTML=vm.usd?`<div class="sec" style="border:1px solid var(--line);padding:12px;margin-bottom:10px"><h3 style="margin:0 0 8px">Valores de mercado</h3><div style="font-size:13px"><b>USD:</b> $${vm.usd} · <b>CLP:</b> $${vm.clp} · <b>EUR:</b> €${vm.eur}</div><div class="note" style="font-size:10px;margin-top:4px">Fuente: ${vm.fuente||'Cálculo automático'} · ${vm.fecha||''}</div></div>`:'';
  const d=document.getElementById("drawer");
  d.innerHTML=`<button class="close" onclick="closeDrawer()">×</button>
    <div class="dh"><img src="${IMG(c.im)}" alt="" onerror="this.style.visibility='hidden'">
      <div><h2>${c.m}</h2>
        <div class="mt">${c.y} · Nº de colección ${c.c} · Toy # ${c.t}</div>
        ${fichaHTML}${idxHTML}${vmHTML}
       <div class="mt">${c.s} ${c.n?"("+c.n+")":""}</div>
       <div class="mt">${CLS[c.k].t}${c.nuevo?" · Nuevo modelo":""}${c.variante?" · Variante de color":""}</div></div></div>
   <div class="kv">
     <span class="k">Índice</span><span class="v">${c.x} / 100</span>
     <span class="k">Historia</span><span class="v" style="font-size:13px;line-height:1.5">${_hist(c.m)?.historia||"Sin datos históricos para este modelo."}</span>
     <span class="k">Curiosidades</span><span class="v" style="font-size:13px;line-height:1.5">${_hist(c.m)?.curiosidades?.map(x=>"• "+x).join("<br>")||"—"}</span>
     <span class="k">¿Conmemorativo?</span><span class="v">${_hist(c.m)?.conmemorativo?"Sí":"No"}</span>
     <span class="k">Dato clave</span><span class="v" style="font-size:13px;line-height:1.5">${_hist(c.m)?.dato_clave||"—"}</span>
     <span class="k">Valor ref.</span><span class="v">${fmt(c.v)} – ${fmt(c.V)}</span>
     <span class="k">En USD / CLP / EUR</span><span class="v" style="font-size:11.5px">US$${c.v.toFixed(2)}–${c.V.toFixed(2)} · $${Math.round(conv(c.v,"CLP"))}–${Math.round(conv(c.V,"CLP"))} · €${conv(c.v,"EUR").toFixed(2)}–${conv(c.V,"EUR").toFixed(2)}</span>
     <span class="k">Venta estimada</span><span class="v">${CLS[c.k].d[0]}–${CLS[c.k].d[1]} días</span>
     <span class="k">Caja</span><span class="v">${CASEBY[id]?("Caja "+CASEBY[id].letra+" ("+CASEBY[id].anio+") · "+(CASEBY[id].tipo==="STH"?"Super Treasure Hunt":"Treasure Hunt")):"—"}</span>
     <span class="k">Imagen</span><span class="v" style="font-family:var(--f-body);font-size:11.5px">${c.imr?"referencia del casting (no necesariamente del año/color exacto)":"foto de la ficha del año"}</span>
     <span class="k">Fuente valor</span><span class="v" style="font-family:var(--f-body);font-size:11.5px">${CLS[c.k].f}</span></div>
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
       <div class="stepper"><button onclick="bump('${id}',-1)">−</button><span class="q" id="dq">${o.q||0}</span><button onclick="bump('${id}',1)">+</button></div>
       <select id="dcond" onchange="setCond('${id}',this.value)">${Object.entries(COND).map(([k,vv])=>`<option value="${k}" ${o.c===k?"selected":""}>${vv.l} (×${vv.m})</option>`).join("")}</select>
       <input type="text" id="dloc" placeholder="Ubicación" value="${o.u||""}" onchange="setLoc('${id}',this.value)" style="max-width:170px"></div>
     <div class="note" style="margin-top:10px">Valor de TU ejemplar: <b>${fmt(v.min)} – ${fmt(v.max)}</b> · mediana ${fmt(v.mid)}</div>
     <div class="warn">Estimación de confianza BAJA: es un rango por clase, no comparables del modelo exacto.</div></div>
   <div class="btnrow"><button class="btn" onclick="speak('${id}')">Escuchar ficha</button>
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
   <div class="dh"><img src="${IMG(c.im)}" onerror="this.style.visibility='hidden'"><div><h2>Editar: ${c.m}</h2><div class="mt">${c.y} · #${c.c}</div></div></div>
   <div class="sec" style="border:1px solid var(--line);padding:12px;margin-bottom:10px">
     <h3 style="margin-bottom:8px">Cantidad</h3>
     <div class="rowin"><button class="stepper" onclick="editQty('${id}',-1)">−</button><span class="stepper q" id="eq">${o.q||0}</span><button class="stepper" onclick="editQty('${id}',1)">+</button></div>
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
     <button class="btn" onclick="saveEdit('${id}')">Guardar</button>
     <button class="btn ghost" onclick="closeDrawer()">Cancelar</button>
   </div>
   <div style="margin-top:10px"><button class="btn ghost" style="color:#e74c3c;border-color:#e74c3c" onclick="delCar('${id}')">Eliminar de mi colección</button></div>`;
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
    if(c){logMsg("a",`<b>${c.m}</b> (${c.y}): ${fmt(c.v)} – ${fmt(c.V)} en pesos chilenos, o sea US$${c.v.toFixed(2)}–${c.V.toFixed(2)}. `+
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
    logMsg("a",`<b>${c.m}</b> (${c.y}, #${c.c}, ${c.s}). Clase ${CLS[c.k].t}. Índice ${c.x}/100. `+
      `Valor ref. ${fmt(c.v)}–${fmt(c.V)}. Venta estimada ${CLS[c.k].d[0]}-${CLS[c.k].d[1]} días. Tenés ×${o.q||0}.`,
      "Fuente: Hot Wheels Wiki (catálogo) + rangos por clase (confianza baja)");
    tts(`${c.m}, año ${c.y}. Índice ${c.x}. Entre ${hablarMoneda(c.v)} y ${hablarMoneda(c.V)}.`);return;
  }
  logMsg("a","No encontré ese modelo en el catálogo de 2.644 registros (1968-2027). Probá con el nombre exacto: <i>Skyline</i>, <i>El Camino</i>, <i>Mustang GTD</i>. También podés preguntar cuánto pago de impuestos si lo traigo o dónde conviene vender.");
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
    ", clase "+c.k+" ("+CLS[c.k].t+"), índice de coleccionabilidad "+c.x+"/100 (percentil "+c.px+
    "), valor de referencia US$"+c.v+"-"+c.V+", venta estimada "+CLS[c.k].d[0]+"-"+CLS[c.k].d[1]+" días."+
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
  const sys="Sos un asistente experto en Hot Wheels para un coleccionista chileno. Respondés en español de Chile, breve (máximo 120 palabras), con datos concretos y sin relleno. NO inventes precios ni datos: si no sabés algo, decilo. Rangos reales de referencia: Mainline US$1-5, Treasure Hunt US$5-20, Super Treasure Hunt US$85-250. El catálogo del usuario tiene 2.644 registros (1968-2027). "+contextoAuto(c);
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
  document.getElementById("scanbox").innerHTML=`<img src="${url}" style="max-width:100%;max-height:260px;border:1px solid var(--line)">`;
  document.getElementById("scanout").innerHTML=`<div class="note">Foto cargada: <b>${f.name}</b>. En este prototipo la identificación automática por IA no está conectada: el plan (§5 y §7) especifica el backend con Gemini 2.5 Flash + CLIP + OCR del blister. Acá se simula el flujo real: escribí el modelo y confirmá el match.</div>`;
}
function doScanSearch(){
  const c=buscar(document.getElementById("scanq").value), o=document.getElementById("scanout");
  if(!c){o.innerHTML+=`<div class="warn">Sin match. Probá con otro nombre.</div>`;return;}
  o.innerHTML=`<div class="sec" style="border:1px solid var(--line);padding:12px">
    <div style="display:flex;gap:12px"><img src="${IMG(c.im)}" style="width:90px;height:90px;object-fit:contain;background:var(--elev)">
    <div><b>${c.m}</b><div class="mt">${c.y} · #${c.c} · ${c.s}</div><div class="mt">Índice ${c.x} · ${fmt(c.v)}–${fmt(c.V)}</div></div></div>
    <div class="btnrow" style="padding:12px 0 0"><button class="btn" onclick="addById('${c.i}',1);render(true)">Confirmar y agregar a mi colección</button></div></div>`;
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
              <div style="display:flex;gap:12px"><img src="${IMG(match.im)}" style="width:90px;height:90px;object-fit:contain;background:var(--elev)">
              <div><b>${match.m}</b><div class="mt">${match.y} · #${match.c} · ${match.s}</div><div class="mt">Índice ${match.x} · ${fmt(match.v)}–${fmt(match.V)}</div></div></div>
              <div class="btnrow" style="padding:12px 0 0"><button class="btn" onclick="addById('${match.i}',1);render(true)">Agregar a mi colección</button></div></div>`;
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
    <button class="btn" style="padding:4px 10px;font-size:12px" onclick="onboardAgregar('${c.i}','${c.m.replace(/'/g,"")}')">+ agregar</button></div>`).join('');
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
      scanZX=new ZXing.BrowserMultiFormatReader();
      scanZX.decodeFromVideoDevice(undefined,video,(result,err)=>{
        if(result){
          const code=result.getText();
          if(code && code.length>=3){
            detenerScan();
            procesarCodigo(code);
          }
        }
      });
    }
    logMsg('i','Escáner activo. Apuntá al código de barras o tocá "Capturar (OCR)".');
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
      logMsg('a','No se detectaron códigos válidos en la imagen.');
    }
  }catch(e){
    logMsg('a','Error en OCR: '+e.message);
  }
}

function extraerCodigos(texto){
  const codigos=[];
  // Patrones de códigos Hot Wheels
  const patrones=[
    /\b[LlCcFfGg]\d{4}\b/,           // Asortación: L2593, C4982, 5785
    /\b[A-Z]{3}\d{2}\b/,             // Modelo: FRN78, JKX06
    /\b[A-Z]\d{4}-?\d{3}[A-Z]\b/,    // Case: L2593-976K
    /\bAsst\.?\s*[A-Z]?\d{4}\b/i,    // "Asst. C4982"
  ];
  for(const p of patrones){
    const m=texto.match(p);
    if(m) codigos.push(m[0].toUpperCase());
  }
  return [...new Set(codigos)];
}

function procesarCodigo(codigo){
  if(!codigo) return;
  codigo=codigo.trim().toUpperCase();
  const res=document.getElementById('scanresult');
  // Buscar en el catálogo local
  const encontrado=buscarPorCodigo(codigo);
  if(encontrado){
    res.innerHTML=`
      <div class="sec" style="border:1px solid var(--brand);padding:12px">
        <h4 style="margin:0 0 8px">✅ Modelo encontrado</h4>
        <div style="font-size:16px;font-weight:600">${encontrado.m}</div>
        <div class="note">Código: ${encontrado.i} · Serie: ${encontrado.k}</div>
        <div class="note">Año: ${encontrado.y}</div>
        ${encontrado.img?`<img src="${encontrado.img}" style="width:80px;height:80px;object-fit:cover;border-radius:4px;margin-top:8px">`:''}
        <div class="btnrow" style="margin-top:10px">
          <button class="btn" onclick="agregarEscaneado('${encontrado.i}')">+ Agregar a mi colección</button>
          <button class="btn ghost" onclick="verFicha('${encontrado.i}')">Ver ficha</button>
        </div>
      </div>`;
    logMsg('i','Modelo encontrado: '+encontrado.m);
  } else {
    res.innerHTML=`
      <div class="sec" style="border:1px solid #e74c3c;padding:12px">
        <h4 style="margin:0 0 8px">❌ Código no encontrado</h4>
        <div class="note">El código <b>${codigo}</b> no existe en la catálogo local.</div>
        <div class="note" style="margin:8px 0">¿Querés buscar en internet?</div>
        <div class="btnrow">
          <button class="btn" onclick="buscarEnInternet('${codigo}')">🔍 Buscar en internet</button>
          <button class="btn ghost" onclick="agregarManual('${codigo}')">Agregar manualmente</button>
        </div>
      </div>`;
    logMsg('a','Código no encontrado: '+codigo);
  }
}

function buscarPorCodigo(codigo){
  // Buscar por ID exacto o por código de asortación
  return CAT.find(c=>c.i===codigo || c.i.includes(codigo) || codigo.includes(c.i));
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
  logMsg('i','🔍 Scraping de rescate para: '+codigo);
  res.innerHTML='<div class="note">🔍 Buscando en internet...<br><br>Ejecutá el scraper de rescate en tu PC:</div>';
  res.innerHTML+='<pre class="note" style="background:var(--elev);padding:8px;border-radius:4px;overflow-x:auto;font-size:12px">python build/scraper_rescate.py "'+codigo+'"</pre>';
  res.innerHTML+='<div class="note" style="margin-top:8px">El scraper buscará en SmartWheelers, HW Wiki, HW Price Guide, Reddit, eBay y Mercado Libre.<br><br>Si el scraper encuentra el modelo, los datos se guardan en caché por 7 días.</div>';
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
  if(t==="valorar") renderVal();
  if(t==="mercados") renderMkt();
  if(t==="seguimiento") renderSeg();
  if(t==="tendencias") renderSeg();
  if(t==="cajas") renderCajas();
  if(t==="catalogo") render(true);
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
    return '<div class="segrow"><img src="'+IMG(d.im||"")+'" onerror="this.style.visibility=\'hidden\'">'
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
      return '<div class="crow">'+(d.im?'<img src="'+IMG(d.im)+'" onerror="this.style.visibility=\'hidden\'">':'<img>')
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
function nivelColor(v){ return v>=58?"#2fbf71":(v>=44?"#e8b23a":"#8a94a3"); }
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
  return c.m+", año "+c.y+", número de colección "+c.c+", serie "+c.s+". Clase "+CLS[c.k].t+". "
    +"Índice de coleccionabilidad "+c.x+" sobre 100, percentil "+c.px+" del catálogo. "
    +"Valor de referencia entre "+hablarMoneda(c.v)+" y "+hablarMoneda(c.V)+". "
    +"Tiempo estimado de venta: entre "+CLS[c.k].d[0]+" y "+CLS[c.k].d[1]+" días. "
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
    navigator.serviceWorker.register("sw.js").then(function(){
      logMsg("a","Modo app activado: funciona sin conexión y se puede instalar en el celular.",
        "Service worker registrado · "+(navigator.onLine?"en línea":"sin conexión"));
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
  document.querySelectorAll("nav.tabs button").forEach(b=>b.onclick=()=>tabTo(b.dataset.tab));
  const sq=document.getElementById("q"); if(sq) sq.oninput=()=>{state.q=sq.value;render(true);};
  if(selY) selY.onchange=()=>{state.year=selY.value;render(true);};
  if(selS) selS.onchange=()=>{state.serie=selS.value;render(true);};
  const so=document.getElementById("fsort"); if(so) so.onchange=()=>{state.sort=so.value;render(true);};
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
  window.addEventListener("online",cicloPuente);
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
"""


def tabla(headers, rows):
    th = "".join(f"<th>{h}</th>" for h in headers)
    tr = "".join("<tr>" + "".join(f'<td class="{"num" if str(c).startswith("$") or str(c).startswith("US$") or str(c).startswith("€") or str(c).startswith("£") else ""}">{c}</td>' for c in r) + "</tr>" for r in rows)
    return f'<table class="t"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def mercados_html():
    # Tarjetas por mercado con precios retail observados
    cards = ""
    for m in MKT["mercados"]:
        rows = "".join(
            f'<tr><td>{r["item"]}</td><td class="num">{MKT["monedas"][m["moneda"]]["simbolo"]}{r["precio_local"]:,}</td>'
            f'<td class="num">US${r["usd"]:.2f}</td><td class="note">{r["fuente"]}</td></tr>'.replace(",", ".")
            for r in m["retail"])
        imp = m["importacion"]
        cards += (f'<div class="mktcard"><div class="mh"><b>{m["nombre"]}</b>'
                  f'<span>moneda {m["moneda"]}</span></div>'
                  f'<table class="t"><thead><tr><th>Producto observado</th><th>Local</th><th>USD</th><th>Fuente</th></tr></thead>'
                  f'<tbody>{rows}</tbody></table>'
                  f'<div class="note" style="padding:10px 13px 0"><b>Importación:</b> {imp["regla"]}'
                  f'<br><span style="opacity:.8">Fuente: {imp["fuente"]}</span></div></div>')
    # Comparación por clase
    comp_rows = []
    for c in MKT["comparacion_clase"]:
        comp_rows.append([f'<b>{c["clase"]}</b>', "<br>".join(c["US"]), "<br>".join(c["CL"]),
                          "<br>".join(c["EU"]), "<br>".join(c["UK"]), f'<span class="note">{c["lectura"]}</span>'])
    comp = tabla(["Clase", "EE.UU.", "Chile", "Europa", "Reino Unido", "Lectura"], comp_rows)
    # Factores
    fact = tabla(["Factor", "Efecto en el precio", "Fuente"],
                 [[f["factor"], f["efecto"], f'<span class="note">{f["fuente"]}</span>'] for f in MKT["por_que_difieren"]])
    # Canales por mercado (referencia)
    ch_rows = []
    for m in MKT["mercados"]:
        for c in m["canales"]:
            ch_rows.append([m["nombre"], c["canal"], c["comision"],
                            c.get("fijo", "—"), c.get("envio", "—"), f'<span class="note">{c["fuente"]}</span>'])
    ch = tabla(["Mercado", "Canal", "Comisión", "Cargo fijo", "Envío", "Fuente"], ch_rows)
    return f"""
<section data-view="mercados" style="display:none">
  <div class="note" style="margin-bottom:12px">Tipos de cambio cargados: <b>1 USD = ${MKT['monedas']['CLP']['por_usd']:,} CLP</b> (mindicador.cl, dólar observado, {MKT['monedas']['CLP']['fecha']}) ·
  <b>1 EUR = US${MKT['monedas']['EUR']['por_usd']:.4f}</b> · <b>1 GBP = US${MKT['monedas']['GBP']['por_usd']:.4f}</b> (exchangerate-api.com, {MKT['monedas']['EUR']['fecha']}).
  EUR/CLP y GBP/CLP son <b>tipos cruzados</b>. Cambiá la moneda con el selector de arriba.</div>

  <div class="sec" style="border:1px solid var(--line);margin-bottom:14px">
    <h3>Precios reales observados por mercado</h3>
    <div class="mktgrid">{cards}</div></div>

  <div class="sec" style="border:1px solid var(--line);margin-bottom:14px">
    <h3>Comparación de venta entre mercados, por clase</h3>{comp}
    <div class="warn">Los precios europeos y británicos son <b>listados observados</b> (asking), no ventas cerradas: sirven para comparar niveles, no para fijar un precio exacto.</div></div>

  <div class="sec" style="border:1px solid var(--line);margin-bottom:14px">
    <h3>¿Cuánto me queda según el canal? (neto después de comisiones)</h3>
    <div class="rowin" style="margin-bottom:10px">
      <label class="note">Precio de venta (USD):</label>
      <input type="number" id="netv" value="25" min="1" step="1" style="max-width:120px">
      <span class="note">Se recalcula solo.</span></div>
    <table class="t"><thead><tr><th>Canal</th><th style="text-align:right">Comisión</th><th style="text-align:right">Cargos</th><th style="text-align:right">Neto</th><th style="text-align:right">% del precio</th></tr></thead>
    <tbody id="netrows"></tbody></table>
    <div class="okbox" id="netbest"></div>
    <div class="note" style="margin-top:8px">Comisiones verificadas en las páginas oficiales de cada plataforma (ver <b>data/mercados.json</b> → <i>calculadora_canales</i>). No incluye envío, embalaje ni impuestos locales.</div></div>

  <div class="sec" style="border:1px solid var(--line);margin-bottom:14px">
    <h3>Calculadora de importación (traer autos a Chile)</h3>
    <div class="rowin" style="margin-bottom:10px">
      <label class="note">Valor del producto (USD):</label><input type="number" id="impv" value="120" min="0" step="1" style="max-width:120px">
      <label class="note">Envío (USD):</label><input type="number" id="impf" value="30" min="0" step="1" style="max-width:110px">
      <label class="note"><input type="checkbox" id="impc2c" style="min-height:auto"> Envío entre personas (C2C, ocasional)</label>
    </div>
    <table class="t"><thead><tr><th>Concepto</th><th style="text-align:right">En tu moneda</th><th style="text-align:right">USD</th></tr></thead>
    <tbody id="imprt"></tbody></table>
    <div class="okbox" id="impnote"></div>
    <div class="note" style="margin-top:8px">Reglas: aduana.cl y sii.cl (Ley N°21.713, vigente 25-oct-2025) y, para la UE, taxation-customs.ec.europa.eu (Reglamento (UE) 2026/382: arancel fijo de €3 por ítem en envíos ≤ €150 desde el 1-jul-2026).</div></div>

  <div class="sec" style="border:1px solid var(--line);margin-bottom:14px">
    <h3>Canales y comisiones por mercado</h3>{ch}</div>

  <div class="sec" style="border:1px solid var(--line)">
    <h3>Por qué los precios difieren entre mercados</h3>{fact}</div>
</section>"""


def seguimiento_html():
    return """
<section data-view="seguimiento" style="display:none">
  <div class="stats">
    <div class="stat"><div class="k">Autos monitoreados</div><div class="v" id="sg1">0</div><div class="n">seguimiento uno a uno</div></div>
    <div class="stat"><div class="k">Unidades</div><div class="v" id="sg2">0</div><div class="n">total en la colección</div></div>
    <div class="stat"><div class="k">Valor actual</div><div class="v" id="sg3" style="font-size:16px">—</div><div class="n">última señal por auto</div></div>
    <div class="stat"><div class="k">Alertas altas</div><div class="v" id="sg4">0</div><div class="n">acciones sugeridas</div></div>
  </div>
  <div class="rowin" style="margin-bottom:12px">
    <button class="btn" onclick="updAll()">Actualizar todos</button>
    <button class="btn ghost" onclick="renderSeg()">Recalcular alertas</button>
    <span class="note" id="segstamp"></span></div>
  <div id="segrows"></div>
  <div class="sec" style="border:1px solid var(--line);margin-top:16px">
    <h3>Alertas activas y opciones de venta</h3><div id="seglist"></div>
    <div class="warn">Las alertas se evalúan con las señales de <b>data/tendencias.json</b> más tu configuración guardada en este navegador.
      Para datos en vivo: <b>python build/refresh_market.py --api</b> (token gratuito de MercadoLibre/eBay) o <b>--browser</b> (navegador real desde tu conexión).
      Facebook Marketplace y TikTok no tienen API pública: se cargan a mano.</div></div>
</section>"""


TRENDS_SCRIPT = ""

def tendencias_html():
    d = TEND["demanda_coleccionistas"]
    def rank_table(lista, mes):
        rows = []
        for x in lista:
            en_cat = len(x.get("catalogo_ids") or [])
            rows.append([f"#{x['rank']}", f"<b>{x['modelo']}</b>", x.get("grupo", ""),
                         f'<span class="note">{x.get("categoria","")}</span>',
                         f'{x["coleccionistas"]} coleccionistas',
                         "sí" if en_cat else "—"])
        return tabla([f"Ranking {mes}", "Modelo", "Grupo", "Categoría", "Demanda medida", "En catálogo"], rows)
    r_ene = rank_table(d["enero_2026"], "enero 2026")
    r_feb = rank_table(d["febrero_2026"], "febrero 2026")
    ch = TEND["precios_chile"]
    ch_rows = [[f"<b>{x['modelo']}</b>", x["linea"], f"${x['clp']:,}".replace(",", "."), f"US${x['usd']:.2f}"]
               for x in ch["items"]]
    t_ch = tabla(["Modelo", "Línea", "Precio CLP", "USD"], ch_rows)
    eb = TEND["ebay_observado"]
    eb_rows = []
    for x in eb["items"]:
        rng = f"US${x['usd_min']:.2f}" if x["usd_min"] == x["usd_max"] else f"US${x['usd_min']:.2f} – US${x['usd_max']:.2f}"
        eb_rows.append([f"<b>{x['modelo']}</b>", x["condicion"], rng, f'<span class="note">{x["nota"]}</span>'])
    t_eb = tabla(["Modelo", "Condición", "Rango observado", "Nota"], eb_rows)
    ml = TEND["mercadolibre_cl"]
    ml_rows = [[x["item"], f"${x['clp']:,}".replace(",", "."), x["fuente"]] for x in ml["precios_retail_cl"]]
    t_ml = tabla(["Producto", "CLP", "Fuente"], ml_rows)
    cov_rows = [[f"<b>{x['marketplace']}</b>", x["automatizable"], x["obtenido"], f'<span class="note">{x["bloqueo"]}</span>']
                for x in TEND["cobertura_y_limites"]]
    t_cov = tabla(["Marketplace", "¿Automatizable?", "Qué obtuvimos", "Bloqueo / límite"], cov_rows)
    return f"""
<section data-view="tendencias" style="display:none">
  <div class="sec" style="border:1px solid var(--line);margin-bottom:14px">
    <h3>Modelos más coleccionados del mundo (dato real, no estimación)</h3>
    <div class="note" style="margin-bottom:10px">{d['metodologia']}<br><b>Fuente:</b> {d['fuente']} · <a href="{d['url']}" target="_blank">ver artículo</a></div>
    <div class="mktgrid"><div class="mktcard"><div class="mh"><b>Enero 2026</b><span>top 10</span></div>{r_ene}</div>
      <div class="mktcard"><div class="mh"><b>Febrero 2026</b><span>top 20</span></div>{r_feb}</div></div>
    <div class="okbox">Estos rankings marcan con <b>TOP n</b> los autos de tu catálogo en la pestaña Catálogo (hay un filtro “Solo trending”).</div></div>

  <div class="sec" style="border:1px solid var(--line);margin-bottom:14px">
    <h3>Precios reales en Chile — tienda especializada (CLP)</h3>
    <div class="note" style="margin-bottom:10px"><b>Fuente:</b> <a href="{ch['url']}" target="_blank">{ch['fuente']}</a> · fecha del dato {ch['fecha_dato']}<br>{ch['nota']}</div>
    {t_ch}</div>

  <div class="sec" style="border:1px solid var(--line);margin-bottom:14px">
    <h3>eBay — listados observados (USD)</h3>
    <div class="note" style="margin-bottom:10px"><b>Fuente:</b> {eb['fuente']} · {eb['fecha_dato']}<br>{eb['nota']}</div>
    {t_eb}</div>

  <div class="sec" style="border:1px solid var(--line);margin-bottom:14px">
    <h3>Mercado Libre Chile — estado de la extracción</h3>
    <div class="warn" style="margin-bottom:10px"><b>{ml['estado']}.</b> {ml['detalle']}</div>
    <div class="note" style="margin-bottom:8px"><b>Términos más buscados en ML Chile:</b> {", ".join(ml['terminos_mas_buscados'])} · <span style="opacity:.8">{ml['fuente_terminos']}</span></div>
    <div class="note" style="margin-bottom:10px"><b>Precios retail locales observados</b> (fuentes chilenas):</div>
    {t_ml}</div>

  <div class="sec" style="border:1px solid var(--line)">
    <h3>Qué se puede automatizar por marketplace (y qué no)</h3>
    {t_cov}
    <div class="warn">Nada de esto se inventa: cada cifra de esta pestaña tiene fuente y fecha. Lo que no se pudo obtener está declarado como bloqueo, no rellenado con estimaciones.</div></div>

  <div class="sec" style="border:1px solid var(--line);margin-top:14px" id="trends-activas">
    <h3>Tendencias activas <span class="note">(análisis automático)</span></h3>
    <div class="note" style="margin-bottom:8px">Índice compuesto 0-100: <b>Google Trends 40%</b> + <b>Reddit 30%</b> + <b>Demanda interna 30%</b>. Se actualiza con <code>python build/trend_watcher.py --sync</code>.</div>
    <div id="trends-content"><span class="note">Cargando...</span></div>
  </div>
</section>""" + TRENDS_SCRIPT


def cajas_html():
    anios = sorted(CAJ["cajas_por_anio"].keys(), reverse=True)
    botones = "".join(
        f'<button class="chip" onclick="setCajYear(\'{a}\')" id="cajy{a}">{a}</button>' for a in anios)
    facts = tabla(["Dato verificado", "Fuente"],
                  [[f["dato"], f'<span class="note">{f["fuente"]}</span>'] for f in CAJ["como_funciona"]])
    bc = CAJ["codigos_base"]
    letras = " · ".join(f"<b>{k}</b>={v}" for k, v in sorted(bc["letra_a_anio"].items(), key=lambda x: x[1]))
    return f"""
<section data-view="cajas" style="display:none">
  <div class="stats">
    <div class="stat"><div class="k">Cajas del año</div><div class="v" id="cj1">0</div><div class="n">letras A–Q (sin I ni O)</div></div>
    <div class="stat"><div class="k">Cajas con TH</div><div class="v" id="cj2">0</div><div class="n">una Treasure Hunt por caja</div></div>
    <div class="stat"><div class="k">Cajas con STH</div><div class="v" id="cj3">0</div><div class="n">Super Treasure Hunt</div></div>
    <div class="stat"><div class="k">Identificadas por vos</div><div class="v" id="cj4">0</div><div class="n">cajas que ya marcaste</div></div>
  </div>
  <div class="rowin" style="margin-bottom:12px"><span class="note">Año:</span>{botones}
    <span class="note">· Tocá “marcar identificado” cuando confirmes qué salió de esa caja: queda guardado en este navegador.</span></div>
  <div class="casegrid" id="casegrid"></div>

  <div class="sec" style="border:1px solid var(--line);margin-top:16px">
    <h3>Decodificador de código de base (el código grabado en el auto)</h3>
    <div class="decoder">
      <input type="text" id="decin" placeholder="M36" maxlength="4">
      <button class="btn" onclick="decodificar()">Decodificar</button>
      <span id="decout"></span></div>
    <div class="note" style="margin-top:8px">{bc['que_es']} <b>Ejemplo:</b> {bc['ejemplo']} <b>Para qué sirve:</b> {bc['utilidad']}
      <br><span style="opacity:.85">{letras}</span><br><b>Fuente:</b> {bc['fuente']}</div></div>

  <div class="sec" style="border:1px solid var(--line);margin-top:16px">
    <h3>Cómo funcionan los códigos de caja</h3>{facts}
    <div class="warn">La composición completa de los ~72 autos de cada caja solo se conoce por reportes de apertura: la wiki publica con certeza la <b>Treasure Hunt</b> y la <b>Super Treasure Hunt</b> de cada letra. Por eso “contenido posible” = TH/STH confirmadas, y “contenido identificado” = lo que vos cargues.</div></div>
</section>"""


def page(title, mode):
    tabs = [("catalogo", "Catálogo"), ("coleccion", "Mi colección"), ("seguimiento", "Seguimiento"),
            ("tendencias", "Tendencias"), ("cajas", "Cajas"), ("escanear", "Escanear"), ("valorar", "Valorar"),
            ("mercados", "Mercados"), ("asistente", "Asistente")]
    if mode == "catalogo":
        tabs = [("catalogo", "Catálogo"), ("cajas", "Cajas"), ("tendencias", "Tendencias")]
    if mode == "coleccion":
        tabs = [("coleccion", "Mi colección"), ("seguimiento", "Seguimiento"), ("cajas", "Cajas"),
                ("tendencias", "Tendencias"), ("valorar", "Valorar"), ("mercados", "Mercados")]
    default = "catalogo" if mode in ("app", "catalogo") else "coleccion"
    tabs_html = "".join(
        f'<button data-tab="{k}" aria-selected="{"true" if k == default else "false"}">{v}</button>'
        for k, v in tabs)
    views = ""
    if mode in ("app", "catalogo"):
        views += f"""
<section data-view="catalogo" style="display:{'block' if default=='catalogo' else 'none'}">
  <div class="filters" style="border:1px solid var(--line);margin-bottom:14px">
    <input type="search" id="q" placeholder="Buscar modelo, serie o toy # (ej: Skyline, El Camino, JBC20)">
    <select id="fyear"></select><select id="fserie"></select>
    <select id="fsort"><option value="rel">Orden: año / nº</option><option value="ind">Índice ↓</option><option value="val">Valor ↓</option></select>
    <div class="chips">
      <button class="chip" data-clase="Mainline" aria-pressed="false">Mainline</button>
      <button class="chip" data-clase="TH" aria-pressed="false">Treasure Hunt</button>
      <button class="chip" data-clase="STH" aria-pressed="false">Super TH</button>
      <button class="chip" id="ftrend" aria-pressed="false">Solo trending</button>
    </div>
    <div class="note"><b id="rescount">0</b> de <b id="totcount">0</b> registros · <span id="imgcount"></span></div>
  </div>
  <div class="grid" id="grid"></div><div id="sentinel"></div><div class="note" id="more" style="padding:10px 0"></div>
</section>"""
    if mode in ("app", "coleccion"):
        views += f"""
<section data-view="coleccion" style="display:{'block' if default=='coleccion' else 'none'}">
  <div class="stats">
    <div class="stat"><div class="k">Autos en colección</div><div class="v" id="cs1">0</div><div class="n">unidades totales</div></div>
    <div class="stat"><div class="k">Modelos distintos</div><div class="v" id="cs2">0</div><div class="n">referencias únicas</div></div>
    <div class="stat"><div class="k">Valor de referencia</div><div class="v" id="cs3" style="font-size:16px">—</div><div class="n">pieza por pieza · confianza baja</div></div>
    <div class="stat"><div class="k">Por clase</div><div class="v" id="cs4" style="font-size:13px">—</div><div class="n">unidades</div></div>
  </div>
  <div class="note" style="margin:-6px 0 14px">Usá <b>+</b> en la ficha de cada auto del catálogo para sumar unidades. Se guarda en este navegador (localStorage). Los datos iniciales son de EJEMPLO.</div>
  <div class="grid" id="gridcol"></div>
</section>
<section data-view="valorar" style="display:{'block' if default=='coleccion' else 'none'}">
  <div class="sec" style="border:1px solid var(--line);padding:0 14px 8px;margin-bottom:14px">
    <h3 style="padding-top:14px">Distribución por año (unidades)</h3><div class="dist" id="distyear"></div></div>
  <div class="sec" style="border:1px solid var(--line);padding:0 14px 8px;margin-bottom:14px">
    <h3 style="padding-top:14px">Distribución por clase</h3><div class="dist" id="distclass"></div></div>
  <div class="sec" style="border:1px solid var(--line);padding:0 14px 8px;margin-bottom:14px">
    <h3 style="padding-top:14px">Plan de venta por tramo de precio</h3>
    <table class="t"><thead><tr><th>Tramo</th><th>Tiempo típico</th><th>Canal</th><th style="text-align:right">Comisión</th></tr></thead><tbody id="plan"></tbody></table>
    <div class="note" id="valnote" style="padding:10px 0"></div></div>
  <div class="sec" style="border:1px solid var(--line);padding:0 14px 8px">
    <h3 style="padding-top:14px">Si vendo en lote (descuento por volumen)</h3>
    <table class="t"><thead><tr><th>Tipo de lote</th><th style="text-align:right">Descuento</th><th style="text-align:right">Neto estimado</th></tr></thead><tbody id="lotes"></tbody></table>
    <div class="warn">Descuentos y comisiones de research/02_mercado_y_valores.md §5-6 (eBay seller fees, Mercari, Whatnot, reddit r/HotWheels).</div></div>
</section>"""
    if mode in ("app", "catalogo", "coleccion"):
        views += mercados_html()
    if mode in ("app", "coleccion"):
        views += seguimiento_html()
    if mode in ("app", "catalogo", "coleccion"):
        views += tendencias_html()
    if mode in ("app", "catalogo", "coleccion"):
        views += cajas_html()
    if mode == "app":
        views += f"""
<section data-view="escanear" style="display:none">
  <div class="sec" style="border:1px solid var(--line);max-width:760px">
    <h3>Escanear un auto (prototipo del flujo)</h3>
    <input type="file" accept="image/*" capture="environment" onchange="scanFile(this)" style="margin-bottom:12px">
    <div id="scanbox" style="margin-bottom:12px"></div>
    <div class="rowin"><input type="text" id="scanq" placeholder="Escribí el modelo identificado (ej: Mustang GTD)">
      <button class="btn" onclick="doScanSearch()">Buscar match</button>
      <button class="btn ghost" onclick="startScan()">📷 Código de barras</button></div>
    <div id="scanout"></div>
    <div class="warn">La identificación automática por foto NO está conectada en este prototipo offline. El plan §5 y §7 define el backend real:
      IA de visión (Gemini 2.5 Flash free tier) para describir + OCR del blister + CLIP contra el catálogo, devolviendo top-5 candidatos.
      Precisión honesta esperada: 60-80% identificando el casting, 30-50% la variante exacta. El usuario siempre confirma.</div>
  </div>
</section>
<section data-view="asistente" style="display:none">
  <div class="assistant">
    <div class="sec" style="border:1px solid var(--line);padding:12px 14px">
      <h3 style="margin-bottom:8px">IA para preguntas abiertas <span class="note">(Groq · gratis)</span></h3>
      <div class="rowin" style="margin-bottom:8px">
        <input type="password" id="iakey" placeholder="Pegá tu API key de Groq (gsk_...)" style="flex:1;min-width:200px">
        <button class="btn" onclick="setIaKey(document.getElementById('iakey').value)">Guardar</button>
        <button class="btn ghost" onclick="setIaKey('')">Borrar</button>
      </div>
      <div class="note" id="iainfo">Sin key: el asistente responde solo con el catálogo. Con key: además responde preguntas abiertas con IA.</div>
      <div class="note" style="margin-top:6px">Conseguí una gratis en <b>console.groq.com</b> (sin tarjeta, 1.000 consultas/día, modelo gpt-oss-120b). La key se guarda <b>solo en este navegador</b> y nunca se sube al repositorio. El motor local sigue respondiendo primero: la IA solo entra cuando el catálogo no alcanza.</div>
    </div>
    <div class="sec" style="border:1px solid var(--line);padding:12px 14px">
      <h3 style="margin-bottom:8px">Voz y personalidad</h3>
      <div class="rowin" style="margin-bottom:10px">
        <span class="note">Persona:</span>
        <button class="chip" data-persona="asistente" aria-pressed="true" onclick="setPersona('asistente')">Asistente</button>
        <button class="chip" data-persona="pokedex" aria-pressed="false" onclick="setPersona('pokedex')">Pokédex</button>
        <button class="chip" data-persona="clarkson" aria-pressed="false" onclick="setPersona('clarkson')">Clarkson</button>
        <span class="note" id="personadesc"></span>
      </div>
      <div class="rowin">
        <span class="note">Voz del sistema:</span><select id="vozsel" onchange="setVoz(this.value)" style="min-width:230px"></select>
        <button class="btn ghost" onclick="probarVoz()">Probar voz</button>
      </div>
      <div class="note" id="vozinfo" style="margin-top:7px"></div>
      <div class="warn">Las voces son las del sistema/navegador (se prefieren las latinoamericanas: es-MX, es-US, es-AR, es-CL). La voz original del Pokédex y la de Jeremy Clarkson son interpretaciones con derechos: para clonarlas hace falta un servicio de voz (ElevenLabs u otro) — el formato Pokédex y el humor de Clarkson ya están implementados en el guion.</div>
    </div>
    <div class="sec" style="border:1px solid var(--line);padding:12px 14px;margin-bottom:12px">
      <h3 style="margin-bottom:8px">Asistente remoto <span class="note">(puente con la PC)</span></h3>
      <div class="rowin" style="margin-bottom:8px">
        <span class="note" id="agentestado">…</span>
        <button class="btn ghost" onclick="sincronizarDatos(true)">Actualizar datos</button>
      </div>
      <div class="rowin">
        <input type="text" id="qagente" placeholder="Preguntale al asistente (ej.: cuánto vale el Skyline en pesos)" style="flex:1">
        <button class="btn" onclick="preguntarAlAgente(document.getElementById('qagente').value)">Preguntar</button>
      </div>
      <div class="note" style="margin-top:7px">Si no hay red o el puente está caído, la pregunta queda <b>en cola en el teléfono</b> y se envía sola cuando vuelve. Los datos se actualizan desde la PC.</div>
    </div>
    <div class="note">Asistente con voz: habla con <b>speechSynthesis</b> y escucha con <b>Web Speech API</b> (Chrome/Edge).
      Responde SOLO con datos del catálogo, precios y mercados con fuente; nunca inventa valores. Entiende preguntas en pesos, dólares o euros.</div>
    <div class="log" id="log"><div class="msg a">Hola. Probá: <i>“cuántos autos tengo”</i>, <i>“cuánto vale el Skyline en pesos”</i>,
      <i>“qué trae la caja A de 2026”</i>, <i>“qué significa el código M36”</i> o <i>“dónde conviene vender”</i>.
      <span class="src">Catálogo: Hot Wheels Wiki (2.644 registros 1968-2027) · Precios y mercados: research/02 + data/mercados.json</span></div></div>
    <div class="rowin"><input type="text" id="q2" placeholder="Escribí tu pregunta…"><button class="btn" id="talkbtn">Hablar</button></div>
  </div>
</section>"""
    return f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#ff4d00">
<meta name="description" content="Catálogo real de Hot Wheels, colección con cantidades, seguimiento con alertas, códigos de caja y valoración en CLP/USD/EUR.">
<link rel="icon" href="icons/favicon-32.png" sizes="32x32">
<link rel="icon" href="icons/icon-192.png" sizes="192x192">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="HW Collector">
<meta name="format-detection" content="telephone=no">
<style>{CSS}</style></head><body>
<header class="top"><div class="bar">
  <div class="brand"><h1>HW <span>Collector</span></h1><span class="sub">Catálogo · Colección · Mercados</span></div>
  <nav class="tabs">{tabs_html}</nav>
  <div class="cur"><span class="note">Moneda:</span><select id="cursel"></select>
    <span class="note">En colección: <b id="totcol">0</b></span>
    <span id="albadge">0</span>
    <span id="netbadge" class="fchip viejo" style="display:none">sin conexión</span>
    <span id="agbadge" class="fchip viejo" style="display:none">asistente</span>
    <span id="ctabadge" class="fchip nuevo" style="display:none">cuenta</span>
    <button class="btn ghost" id="scanbtn" onclick="abrirScan()">📷 Escanear</button>
    <button class="btn ghost" id="ctabtn" onclick="toggleCuenta()">Cuenta</button>
    <span class="note" id="datosfuente"></span>
    <button class="btn ghost" id="installbtn" style="display:none" onclick="instalar()">Instalar app</button></div></div>
  <div class="note" id="currate" style="padding:0 18px 8px"></div></header>
<main>{views}</main>
<aside class="drawer" id="drawer" data-open="0"></aside>

<!-- ===== Modal de cuenta (registro / login / perfil) ===== -->
<div id="cuentamodal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:100;align-items:center;justify-content:center;padding:16px">
  <div style="background:var(--surface);border:1px solid var(--line);border-radius:8px;max-width:420px;width:100%;max-height:90vh;overflow-y:auto;padding:20px">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
      <h3 id="cuentatitulo" style="margin:0">Cuenta</h3>
      <button class="close" onclick="document.getElementById('cuentamodal').style.display='none'">×</button>
    </div>
    <div id="cuentacontenido"></div>
  </div>
</div>

<!-- ===== Modal de escaneo (OCR + barcode) ===== -->
<div id="scanmodal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.85);z-index:110;align-items:center;justify-content:center;padding:16px">
  <div style="background:var(--surface);border:1px solid var(--line);border-radius:8px;max-width:480px;width:100%;max-height:95vh;overflow-y:auto;padding:20px">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
      <h3 style="margin:0">📷 Escanear Hot Wheels</h3>
      <button class="close" onclick="cerrarScan()">×</button>
    </div>
    <div id="scanbody">
      <div style="position:relative;background:#000;border-radius:6px;overflow:hidden;margin-bottom:12px">
        <video id="scanvideo" style="width:100%;display:block" autoplay playsinline muted></video>
        <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:200px;height:120px;border:2px solid var(--brand);border-radius:4px;pointer-events:none"></div>
      </div>
      <div class="note" style="margin-bottom:10px">Apuntá al código de barras o al texto del card (asortación, modelo, case)</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
        <button class="btn" onclick="capturarOCR()">📷 Capturar (OCR)</button>
        <button class="btn ghost" onclick="cerrarScan()">✕ Cerrar</button>
      </div>
      <div id="scanresult" style="margin-top:12px"></div>
    </div>
  </div>
</div>

<!-- ===== Modal de onboarding (colección base de 10 autos) ===== -->
<div id="onboardmodal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:100;align-items:center;justify-content:center;padding:16px">
  <div style="background:var(--surface);border:1px solid var(--line);border-radius:8px;max-width:520px;width:100%;max-height:90vh;overflow-y:auto;padding:20px">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
      <h3 style="margin:0">Armá tu colección base</h3>
      <button class="close" onclick="document.getElementById('onboardmodal').style.display='none'">×</button>
    </div>
    <div class="note" style="margin-bottom:12px">Escaneá o buscá <b>10 autos</b> para crear tu colección base. Podés hacerlo ahora o después — no bloquea nada.</div>
    <div style="margin-bottom:14px">
      <div style="display:flex;justify-content:space-between;margin-bottom:4px"><span class="note">Progreso</span><b id="onboardcount">0 / 10</b></div>
      <div style="background:var(--elev);border-radius:4px;height:8px;overflow:hidden"><div id="onboardbar" style="height:100%;width:0%;background:var(--brand);transition:width .3s"></div></div>
    </div>
    <div id="onboardbody"></div>
    <div id="onboardresumen" style="display:none;margin-top:14px"></div>
  </div>
</div>

<script src="vendor/supabase.js"></script>
<script src="js/supabase-client.js"></script>
<script src="https://unpkg.com/@zxing/library@0.21.3/umd/index.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js"></script>
<script>{JS.replace("__CAT__", json.dumps(CAT, ensure_ascii=False, separators=(",", ":")))
            .replace("__PRE__", json.dumps(PRE, ensure_ascii=False, separators=(",", ":")))
            .replace("__OWNED__", json.dumps(OWNED, ensure_ascii=False, separators=(",", ":")))
            .replace("__SEG__", json.dumps(SEG, ensure_ascii=False, separators=(",", ":")))
            .replace("__TEND__", json.dumps(TEND, ensure_ascii=False, separators=(",", ":")))
            .replace("__CAJ__", json.dumps(CAJ, ensure_ascii=False, separators=(",", ":")))
            .replace("__IDXI__", json.dumps(IDXI, ensure_ascii=False, separators=(",", ":")))
            .replace("__HIST__", json.dumps(HIST, ensure_ascii=False, separators=(",", ":")))
            .replace("__MKT__", json.dumps(MKT, ensure_ascii=False, separators=(",", ":")))}</script>
</body></html>"""


def main():
    out = os.path.join(ROOT, "web")
    os.makedirs(out, exist_ok=True)
    for fname, title, mode in [("galeria_catalogo.html", "Galería del catálogo Hot Wheels", "catalogo"),
                               ("galeria_coleccion.html", "Mi colección Hot Wheels", "coleccion"),
                               ("index.html", "HW Collector — app (catálogo, colección, mercados, asistente)", "app")]:
        html = page(title, mode)
        with open(os.path.join(out, fname), "w", encoding="utf-8") as f:
            f.write(html)
        print(f"{fname}  {len(html)/1024:.1f} KB")


if __name__ == "__main__":
    main()
