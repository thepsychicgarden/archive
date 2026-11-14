import os, re, json, sys, html
from PIL import Image, ImageOps
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.dirname(HERE)
FULL, THUMB = os.path.join(OUT, "images"), os.path.join(OUT, "thumbs")
os.makedirs(FULL, exist_ok=True); os.makedirs(THUMB, exist_ok=True)
start, end = int(sys.argv[1]), int(sys.argv[2])
files = sorted(f for f in os.listdir(SRC) if re.search(r'\.(jpe?g|png|webp)$', f, re.I))
def slug(s):
    s = re.sub(r'\.[^.]+$', '', s).lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')
seen = {}
items = []
for f in files:
    sl = slug(f)
    if sl in seen: seen[sl] += 1; sl = f"{sl}-{seen[sl]}"
    else: seen[sl] = 0
    items.append((f, sl))
meta_path = os.path.join(HERE, "meta.json")
meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
for f, sl in items[start:end]:
    fo, to = os.path.join(FULL, sl + ".webp"), os.path.join(THUMB, sl + ".webp")
    if sl in meta and os.path.exists(fo) and os.path.exists(to): continue
    im = Image.open(os.path.join(SRC, f)); im = ImageOps.exif_transpose(im)
    im = im.convert("RGBA" if im.mode in ("RGBA","LA","P") else "RGB")
    if im.mode == "RGBA":
        bg = Image.new("RGB", im.size, (0,0,0)); bg.paste(im, mask=im.split()[3]); im = bg
    w, h = im.size
    big = im.copy(); big.thumbnail((2000, 2000), Image.LANCZOS); big.save(fo, "WEBP", quality=84, method=5)
    th = im.copy(); th.thumbnail((640, 1280), Image.LANCZOS); th.save(to, "WEBP", quality=78, method=5)
    meta[sl] = {"w": th.size[0], "h": th.size[1]}
    json.dump(meta, open(meta_path, "w"))
print(len(items), len(meta))
