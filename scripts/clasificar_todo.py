#!/usr/bin/env python3
"""Clasifica la orientación de TODAS las imágenes del catálogo con CLIP zero-shot.

Salida: data/orientacion.json  ->  { "<id modelo>": {"dir":"IZQ|DER", "conf":0.0-1.0} }
Luego la app aplica transform:scaleX(-1) a las que miran al lado opuesto al elegido.
"""
import os, sys, json, time, io
import numpy as np
from PIL import Image
import onnxruntime as ort
from tokenizers import Tokenizer
import urllib.request

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/'
CLIP = BASE + 'tools/clip/'
MEAN = np.array([0.48145466, 0.4578275, 0.40821073], dtype=np.float32)
STD  = np.array([0.26862954, 0.26130258, 0.27577711], dtype=np.float32)

# Variantes de prompt (la D dio 100% en la muestra etiquetada)
VARIANTES = [
    ["a toy car seen from the side, driving towards the left",
     "a toy car seen from the side, driving towards the right"],
    ["a photo of a car facing left, side view profile",
     "a photo of a car facing right, side view profile"],
]

def preprocess(img):
    img = img.convert('RGB')
    w, h = img.size
    s = 224 / min(w, h)
    img = img.resize((max(1, round(w*s)), max(1, round(h*s))), Image.BICUBIC)
    w, h = img.size
    l, t = (w-224)//2, (h-224)//2
    img = img.crop((l, t, l+224, t+224))
    a = np.asarray(img, dtype=np.float32)/255.0
    a = (a - MEAN)/STD
    return a.transpose(2,0,1)[None,...].astype(np.float32)

class ClipOrient:
    def __init__(self):
        so = ort.SessionOptions()
        so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        self.vis = ort.InferenceSession(CLIP+'vision_model_quantized.onnx', so, providers=['CPUExecutionProvider'])
        self.txt = ort.InferenceSession(CLIP+'text_model_quantized.onnx', so, providers=['CPUExecutionProvider'])
        self.tok = Tokenizer.from_file(CLIP+'tokenizer.json')
        self.tok.enable_truncation(max_length=77); self.tok.enable_padding(length=77)
        self.vis_in = [i.name for i in self.vis.get_inputs()]
        self.txt_in = [i.name for i in self.txt.get_inputs()]
        self.txt_out = [o.name for o in self.txt.get_outputs()]
        self.vis_out = [o.name for o in self.vis.get_outputs()]
        self.text_emb = self._text_embeddings()

    def _text_embeddings(self):
        embs = []
        for prompts in VARIANTES:
            enc = self.tok.encode_batch(prompts)
            ids = np.array([e.ids for e in enc], dtype=np.int64)
            mask = np.array([e.attention_mask for e in enc], dtype=np.int64)
            feed = {}
            for n in self.txt_in:
                if 'input_ids' in n: feed[n] = ids
                elif 'attention_mask' in n: feed[n] = mask
                elif 'pixel_values' in n: feed[n] = np.zeros((len(prompts),3,224,224), dtype=np.float32)
            out = self.txt.run(self.txt_out, feed)
            e = None
            for o in out:
                if o.ndim == 3: e = o[:,0,:]
                elif o.ndim == 2 and o.shape[0] == len(prompts): e = o
            e = np.asarray(e, dtype=np.float32); e = e/np.linalg.norm(e, axis=-1, keepdims=True)
            embs.append(e)
        return embs

    def classify(self, img):
        px = preprocess(img)
        feed = {n: px for n in self.vis_in}
        out = self.vis.run(self.vis_out, feed)
        e = None
        for o in out:
            if o.ndim == 3: e = o[:,0,:]
            elif o.ndim == 2 and o.shape[0] == 1: e = o
        e = np.asarray(e, dtype=np.float32); e = e/np.linalg.norm(e, axis=-1, keepdims=True)
        s = np.zeros(2)
        for te in self.text_emb:
            lg = (100.0 * e @ te.T)[0]
            s += lg
        p = np.exp(s - s.max()); p = p/p.sum()
        return ('IZQ' if p[0] >= p[1] else 'DER'), float(max(p))

def cargar_imagen(im, cache_dir):
    """Devuelve un objeto PIL de una imagen local o remota (con caché en disco)."""
    if not im:
        return None
    if im.startswith('data:'):
        return None
    if im.startswith('http'):
        import hashlib
        h = hashlib.sha1(im.encode()).hexdigest()[:16]
        p = os.path.join(cache_dir, h + '.img')
        if os.path.exists(p) and os.path.getsize(p) > 500:
            try: return Image.open(p)
            except Exception: pass
        try:
            r = urllib.request.Request(im); r.add_header('User-Agent','Mozilla/5.0')
            with urllib.request.urlopen(r, timeout=25) as resp:
                data = resp.read()
            if len(data) < 500: return None
            open(p,'wb').write(data)
            return Image.open(io.BytesIO(data))
        except Exception:
            return None
    p = BASE + 'img/' + im
    if os.path.exists(p):
        try: return Image.open(p)
        except Exception: return None
    return None

def main():
    cache_dir = BASE + 'tools/clip/cache'
    os.makedirs(cache_dir, exist_ok=True)
    salida = BASE + 'data/orientacion.json'
    res = {}
    if os.path.exists(salida):
        res = json.load(open(salida, encoding='utf-8'))

    cat = json.load(open(BASE + 'data/catalog_web.json', encoding='utf-8'))
    pend = [m for m in cat if m.get('im') and m.get('i') not in res]
    print(f"Total: {len(cat)} | ya clasificados: {len(res)} | pendientes: {len(pend)}")

    c = ClipOrient()
    print("CLIP listo")
    ok = err = 0
    t0 = time.time()
    for i, m in enumerate(pend):
        img = cargar_imagen(m.get('im',''), cache_dir)
        if img is None:
            err += 1
            res[m['i']] = {'dir': None, 'conf': 0.0, 'err': 'sin imagen'}
            continue
        try:
            lab, conf = c.classify(img)
            res[m['i']] = {'dir': lab, 'conf': round(conf,3)}
            ok += 1
        except Exception as e:
            err += 1
            res[m['i']] = {'dir': None, 'conf': 0.0, 'err': str(e)[:40]}
        if (i+1) % 100 == 0:
            json.dump(res, open(salida,'w',encoding='utf-8'), ensure_ascii=False)
            el = time.time()-t0
            print(f"  {i+1}/{len(pend)} ok={ok} err={err} ({el:.0f}s, {100*(i+1)/max(len(pend),1):.0f}%)")
    json.dump(res, open(salida,'w',encoding='utf-8'), ensure_ascii=False)
    izq = sum(1 for v in res.values() if v.get('dir')=='IZQ')
    der = sum(1 for v in res.values() if v.get('dir')=='DER')
    print(f"\nCOMPLETADO: {len(res)} clasificados | IZQ={izq} DER={der} sin_dato={len(res)-izq-der}")

if __name__ == '__main__':
    main()
