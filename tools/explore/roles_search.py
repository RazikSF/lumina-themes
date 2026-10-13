"""Search role assignments for one flavor: maximise the worst internal role separation and
the distance to every other flavor. Usage: python3 tools/explore/roles_search.py FLAVOR [N]"""
import itertools, json, math, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "generators"))
from oklch import to_hex, from_hex
import v2_palettes as v
import lumina_gen as g

fl, top = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 8
pal = v.PALETTES[fl]; lead = g.SCHEMAS[fl]["lead"]
EXCLUDE = set(sys.argv[3].split(",")) if len(sys.argv) > 3 else set()
SLOTS = [s for s in ("teal", "cyan", "blue", "green", "yellow", "orange", "magenta", "violet") if s != lead and s not in EXCLUDE]
spec = json.loads(g.SPEC.read_text())["flavors"]
KEYS = ["bg", "schema.lead", "keywords", "functions", "strings", "type", "comments"]


def lab(h):
    L, C, hh = from_hex(h); return L, C * math.cos(math.radians(hh)), C * math.sin(math.radians(hh))


def de(a, b): return 100 * math.dist(lab(a), lab(b))


others = {mode: [[g.resolve_ref(k, t[mode]["colors"], g.SCHEMAS[f]) for k in KEYS]
                 for f, t in spec.items() if f != fl] for mode in ("dark", "light")}
hexes = {mode: {k: to_hex(*c) for k, c in pal[mode].items()} for mode in ("dark", "light")}
res = []
for kw, ty, st, co in itertools.permutations(SLOTS, 4):
    worst_in, worst_out = 99, 99
    for mode in ("dark", "light"):
        H = hexes[mode]
        used = [H[lead], H[kw], H[ty], H[st], H[co]]
        worst_in = min(worst_in, min(de(a, b) for a, b in itertools.combinations(used, 2)), de(H[co], H["red"]), de(H[st], H["red"]))
        mine = [H["bg"], H[lead], H[kw], H[lead], H[st], H[ty], H["comments"]]
        worst_out = min(worst_out, min(sum(de(a, b) for a, b in zip(mine, o)) / len(KEYS) for o in others[mode]))
    res.append((min(worst_in / 10, worst_out / 7), worst_in, worst_out, kw, ty, st, co))
for sc, wi, wo, kw, ty, st, co in sorted(res, reverse=True)[:top]:
    print(f"interne {wi:4.1f}  autres {wo:4.1f} | keywords={kw} type={ty} strings={st} constants={co}")
