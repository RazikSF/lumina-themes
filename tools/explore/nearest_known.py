"""Distance from a candidate palette to every installed Emacs theme, role by role (OKLab dE x100).

Usage: python3 tools/explore/nearest_known.py   (prints the closest themes for combos 19 and 23)
"""
import glob, json, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "generators")); sys.path.insert(0, str(ROOT / "tools/explore"))
from oklch import from_hex
import explore, measure

INK = {"or": "#F7C054", "saumon": "#EC907E", "menthe": "#87C3AB", "ciel": "#77B8E7"}
BG, FG = "#1D2130", "#E8E9E7"
CANDS = {
    "19": dict(keywords="ciel", functions="saumon", types="or", strings="menthe", constants="saumon"),
    "23": dict(keywords="ciel", functions="saumon", types="or", strings="menthe", constants="ciel"),
}
ROLES = ["keywords", "functions", "strings", "types", "constants"]


def lab(h):
    L, C, hh = from_hex(h); return L, C * math.cos(math.radians(hh)), C * math.sin(math.radians(hh))


def de(a, b): return 100 * math.dist(lab(a), lab(b))


names = set()
for pat in [str(measure.B / "*/themes/*-theme.el"), str(measure.B / "*/*-theme.el")]:
    for f in glob.glob(pat):
        n = Path(f).name[:-len("-theme.el")]
        if not n.startswith(("lumina", "doom-lumina")) and "light" not in n and "day" not in n:
            names.add(n)
rows = []
for n in sorted(names):
    cache = explore.OUT / f"m-{n}.json"
    data = json.loads(cache.read_text()) if cache.exists() else measure.render(n)
    if not data:
        continue
    d = data["faces"]
    bg = (d.get("default") or {}).get("bg"); fg = (d.get("default") or {}).get("fg")
    if not (bg and fg and bg.startswith("#") and fg.startswith("#")):
        continue
    if from_hex(bg)[0] > .5:
        continue
    roles = {r: (d.get(measure.ROLES[r]) or {}).get("fg") for r in ROLES}
    if not all(v and v.startswith("#") for v in roles.values()):
        continue
    for cname, cand in CANDS.items():
        parts = [de(bg, BG), de(fg, FG)] + [de(roles[r], INK[cand[r]]) for r in ROLES]
        code = sum(de(roles[r], INK[cand[r]]) for r in ROLES) / len(ROLES)
        rows.append((sum(parts) / len(parts), code, cname, n, roles, bg))
for cname in CANDS:
    print(f"== n° {cname} : les plus proches (moyenne fond+texte+5 rôles ; code seul)")
    for tot, code, c, n, roles, bg in sorted(r for r in rows if r[2] == cname)[:8]:
        print(f"  {n:34} {tot:5.1f}  code {code:5.1f}  fond {bg}  " + " ".join(f"{r[:3]}={roles[r]}" for r in ROLES))
print(len({r[3] for r in rows}), "thèmes sombres comparés")
