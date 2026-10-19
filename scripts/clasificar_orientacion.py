#!/usr/bin/env python3
"""Clasifica la orientación (IZQ/DER) de las imágenes de autos con CLIP zero-shot.

Usa onnxruntime + tokenizers (sin torch). Detecta hacia dónde mira cada auto
para poder aplicar un efecto espejo y uniformar el catálogo.
"""
import os, sys, json, time
import numpy as np
from PIL import Image
import onnxruntime as ort
from tokenizers import Tokenizer

BASE = 'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/'
CLIP = BASE + 'tools/clip/'

# Preprocesado CLIP ViT-B/32
MEAN = np.array([0.48145466, 0.4578275, 0.40821073], dtype=np.float32)
STD  = np.array([0.26862954, 0.26130258, 0.27577711], dtype=np.float32)

PROMPTS = [
    "a photo of a car facing left, side view profile",
    "a photo of a car facing right, side view profile",
]

def preprocess(img):
    img = img.convert('RGB')
    w, h = img.size
    s = 224 / min(w, h)
    img = img.resize((max(1, round(w * s)), max(1, round(h * s))), Image.BICUBIC)
    w, h = img.size
    l, t = (w - 224) // 2, (h - 224) // 2
    img = img.crop((l, t, l + 224, t + 224))
    a = np.asarray(img, dtype=np.float32) / 255.0
    a = (a - MEAN) / STD
    return a.transpose(2, 0, 1)[None, ...].astype(np.float32)

class ClipOrient:
    def __init__(self):
        so = ort.SessionOptions()
        so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        so.intra_op_num_threads = 0
        self.vis = ort.InferenceSession(CLIP + 'vision_model_quantized.onnx', so, providers=['CPUExecutionProvider'])
        self.txt = ort.InferenceSession(CLIP + 'text_model_quantized.onnx', so, providers=['CPUExecutionProvider'])
        self.tok = Tokenizer.from_file(CLIP + 'tokenizer.json')
        self.tok.enable_truncation(max_length=77)
        self.tok.enable_padding(length=77)
        self.vis_in = [i.name for i in self.vis.get_inputs()]
        self.txt_in = [i.name for i in self.txt.get_inputs()]
        self.txt_out = [o.name for o in self.txt.get_outputs()]
        self.text_emb = self._text_embeddings()
        self.vis_out = [o.name for o in self.vis.get_outputs()]

    def _text_embeddings(self):
        enc = self.tok.encode_batch(PROMPTS)
        ids = np.array([e.ids for e in enc], dtype=np.int64)
        mask = np.array([e.attention_mask for e in enc], dtype=np.int64)
        feed = {}
        for n in self.txt_in:
            if 'input_ids' in n: feed[n] = ids
            elif 'attention_mask' in n: feed[n] = mask
            elif 'pixel_values' in n: feed[n] = np.zeros((len(PROMPTS), 3, 224, 224), dtype=np.float32)
        out = self.txt.run(self.txt_out, feed)
        # buscar la salida de embeddings de texto (la de mayor rango con dim oculta)
        emb = None
        for o in out:
            if o.ndim == 3: emb = o[:, 0, :]
            elif o.ndim == 2 and o.shape[0] == len(PROMPTS): emb = o
        if emb is None: emb = out[0]
        emb = np.asarray(emb, dtype=np.float32)
        emb = emb / np.linalg.norm(emb, axis=-1, keepdims=True)
        return emb

    def classify(self, img):
        px = preprocess(img)
        feed = {}
        for n in self.vis_in:
            feed[n] = px
        out = self.vis.run(self.vis_out, feed)
        emb = None
        for o in out:
            if o.ndim == 3: emb = o[:, 0, :]
            elif o.ndim == 2 and o.shape[0] == 1: emb = o
        emb = np.asarray(emb, dtype=np.float32)
        emb = emb / np.linalg.norm(emb, axis=-1, keepdims=True)
        logits = (100.0 * emb @ self.text_emb.T)[0]
        p = np.exp(logits - logits.max()); p = p / p.sum()
        return ('IZQ' if p[0] >= p[1] else 'DER'), float(p[0]), float(p[1])

if __name__ == '__main__':
    c = ClipOrient()
    print("CLIP listo. Probando con la muestra etiquetada...")
    cat = json.load(open(BASE + 'data/catalog_web.json', encoding='utf-8'))
    import random
    random.seed(3)
    locales = [x for x in cat if x.get('im') and not x['im'].startswith('http') and os.path.exists(BASE + 'img/' + x['im'])]
    muestra = random.sample(locales, 12)
    verdad = ['DER','IZQ','DER',None,'IZQ','IZQ','IZQ','IZQ','DER','DER','IZQ','IZQ']
    ok = tot = 0
    for i, m in enumerate(muestra):
        img = Image.open(BASE + 'img/' + m['im'])
        lab, pl, pr = c.classify(img)
        v = verdad[i]
        if v:
            tot += 1; ok += 1 if lab == v else 0
        print(f"{i+1:3d} {m['m'][:26]:28s} -> {lab}  (izq={pl:.2f} der={pr:.2f})  verdad={v} {'✓' if v==lab else ('✗' if v else '')}")
    print(f"\nAciertos CLIP: {ok}/{tot} = {100*ok//max(tot,1)}%")
