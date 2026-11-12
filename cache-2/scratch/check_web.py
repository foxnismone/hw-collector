import os, hashlib
for p in ['index.html','web/index.html']:
    if os.path.exists(p):
        data=open(p,'rb').read()
        print(p, "bytes=",len(data), "md5=",hashlib.md5(data).hexdigest()[:12])
    else:
        print(p, "NO EXISTE")
print()
# git tracking
import subprocess
r=subprocess.run(['git','ls-files','index.html','web/index.html'],capture_output=True,text=True)
print("trackidos:\n", r.stdout)
# config de pages
for f in ['_config.yml','.nojekyll','CNAME']:
    print(f, os.path.exists(f))
