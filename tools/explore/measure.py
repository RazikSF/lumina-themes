"""Measure the structure of chosen reference themes: ground, text, roles (L, C, h), hue count, chroma, dominance.

Usage: python3 tools/explore/measure.py theme [theme ...]  (lumina-* themes are read from emacs/themes)
"""
import glob, json, math, os, statistics, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "generators")); sys.path.insert(0, str(ROOT / "tools/explore"))
from oklch import from_hex, contrast
import explore

B = Path.home() / ".config/emacs/.local/straight/build-30.2"
ROLES = {"keywords": "font-lock-keyword-face", "functions": "font-lock-function-name-face", "strings": "font-lock-string-face",
         "types": "font-lock-type-face", "constants": "font-lock-constant-face", "builtin": "font-lock-builtin-face", "variables": "font-lock-variable-name-face"}


def render(name):
    hits = glob.glob(str(B / f"*/{name}-theme.el")) + glob.glob(str(B / f"*/themes/{name}-theme.el")) + glob.glob(str(Path.home() / f".doom.d/themes/{name}-theme.el")) + glob.glob(str(ROOT / f"emacs/themes/{name}-theme.el"))
    if not hits:
        print("introuvable :", name); return None
    d = Path(hits[0]).parent
    env = dict(os.environ, R_THEME=name, R_OUT=str(explore.OUT / f"m-{name}.json"), R_PATH=f"{d}:{d.parent}:{B / 'doom-themes'}:{B / 'doom-themes' / 'themes'}",
               R_DIR=str(ROOT / "tools/preview"), R_PY=str(ROOT / "docs/sample.py"))
    env.pop("R_LIGHT", None)
    if name.startswith("doom-"):
        env["R_DOOM"] = "1"
    subprocess.run(["emacs", "-Q", "--batch", "-l", str(ROOT / "tools/preview/render.el")], env=env, capture_output=True, timeout=90)
    out = explore.OUT / f"m-{name}.json"
    if not out.exists():
        print("rendu impossible :", name); return None
    return json.loads(out.read_text())


def measure(name):
    r = render(name)
    if not r:
        return None
    d = r["faces"]
    def col(f):
        v = (d.get(f) or {}).get("fg"); return v if v and v.startswith("#") else None
    bg = (d.get("default") or {}).get("bg"); fg = (d.get("default") or {}).get("fg")
    if not (bg and fg and bg.startswith("#") and fg.startswith("#")):
        return None
    roles = {r: col(f) for r, f in ROLES.items()}
    roles = {r: v for r, v in roles.items() if v and v != fg}
    lab = {r: from_hex(v) for r, v in roles.items()}
    hues = []
    for r, (L, C, h) in lab.items():
        if C < .04:
            continue
        if not any(min(abs(h - x), 360 - abs(h - x)) < 25 for x in hues):
            hues.append(h)
    Ls = [v[0] for v in lab.values()]; Cs = [v[1] for v in lab.values() if v[1] >= .04]
    dom = max(lab.items(), key=lambda kv: kv[1][1])[0] if lab else "-"
    light = max(lab.items(), key=lambda kv: kv[1][0])[0] if lab else "-"
    cm = col("font-lock-comment-face")
    return dict(name=name, bgL=from_hex(bg)[0], bgC=from_hex(bg)[1], bgh=from_hex(bg)[2], fgL=from_hex(fg)[0], fgC=from_hex(fg)[1], fgk=contrast(fg, bg),
                cmk=contrast(cm, bg) if cm else 0, nh=len(hues), cmean=statistics.mean(Cs) if Cs else 0, cmin=min(Cs) if Cs else 0, cmax=max(Cs) if Cs else 0,
                lmin=min(Ls) if Ls else 0, lmax=max(Ls) if Ls else 0, dom=dom, light=light, roles={r: v for r, v in roles.items()})


def main(names):
    rows = [m for m in (measure(n) for n in names) if m]
    print(f"{'theme':34s} bgL  bgC  bgh  fgL  fg:1 cm:1 nh cmean cmin cmax lmin lmax dominant  lightest")
    for m in rows:
        print(f"{m['name']:34s} {m['bgL']:.2f} {m['bgC']:.3f} {m['bgh']:3.0f} {m['fgL']:.2f} {m['fgk']:4.1f} {m['cmk']:4.1f} {m['nh']:2d} {m['cmean']:.3f} {m['cmin']:.2f} {m['cmax']:.2f} {m['lmin']:.2f} {m['lmax']:.2f} {m['dom']:9s} {m['light']}")
    ref = [m for m in rows if not m["name"].startswith("lumina")]
    if ref:
        med = lambda k: statistics.median(m[k] for m in ref)
        print(f"\nMÉDIANE des références : bgL {med('bgL'):.2f} bgC {med('bgC'):.3f} | fgL {med('fgL'):.2f} fg {med('fgk'):.1f}:1 | commentaires {med('cmk'):.1f}:1 | teintes {med('nh'):.0f} | chroma moy {med('cmean'):.3f} (min {med('cmin'):.2f}, max {med('cmax'):.2f}) | clartés {med('lmin'):.2f}-{med('lmax'):.2f}")
        from collections import Counter
        print("rôle le plus saturé :", Counter(m["dom"] for m in ref).most_common(4), "| rôle le plus clair :", Counter(m["light"] for m in ref).most_common(4))
    json.dump(rows, open(explore.OUT / "measure.json", "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1:])
