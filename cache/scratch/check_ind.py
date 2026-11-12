import json, os
os.chdir(r'C:/Users/GODZILLA24H2/Desktop/hotwheels_collector/data')
for f in ['indice.json']:
    if os.path.exists(f):
        d = json.load(open(f, encoding='utf-8'))
        print(f"{f}: tipo {type(d).__name__}")
        if isinstance(d, dict):
            print("  claves:", list(d.keys())[:8])
            for k in list(d.keys())[:3]:
                print(f"  {k}: {str(d[k])[:200]}")
