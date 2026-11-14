import os, re, json
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.dirname(HERE)
meta = json.load(open(os.path.join(HERE, "meta.json")))
files = sorted(f for f in os.listdir(SRC) if re.search(r'\.(jpe?g|png|webp)$', f, re.I))
def slug(s):
    s = re.sub(r'\.[^.]+$', '', s).lower(); return re.sub(r'[^a-z0-9]+', '-', s).strip('-')
seen = {}; data = []
for f in files:
    sl = slug(f)
    if sl in seen: seen[sl] += 1; sl = f"{sl}-{seen[sl]}"
    else: seen[sl] = 0
    base = re.sub(r'\.[^.]+$', '', f)
    m = re.match(r'(\d{4}-\d{2}-\d{2})\s*(.*)', base)
    date, title = (m.group(1), m.group(2)) if m else ("", base)
    tag = ""
    t = re.search(r'\s*\(([^)]*)\)\s*$', title)
    if t: tag = t.group(1); title = title[:t.start()]
    title = title.replace("_", "'").strip() or "Untitled"
    data.append({"s": sl, "d": date, "t": title, "g": tag, "w": meta[sl]["w"], "h": meta[sl]["h"]})
data.reverse()  # newest first
tpl = open(os.path.join(HERE, "template.html")).read()
open(os.path.join(OUT, "index.html"), "w").write(tpl.replace("__DATA__", json.dumps(data, separators=(",", ":"))))
open(os.path.join(OUT, ".nojekyll"), "w").write("")
print(len(data))
