"""Perceptual distance (OKLab ΔE x100) between Lumina themes, on key syntax roles."""
import itertools, json, math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "generators"))
from oklch import from_hex
import lumina_gen as g

ROLES = ["bg", "schema.lead", "keywords", "functions", "strings", "type", "comments"]


def lab(h):
    L, C, hh = from_hex(h)
    return L, C * math.cos(math.radians(hh)), C * math.sin(math.radians(hh))


spec = json.loads(g.SPEC.read_text())["flavors"]
T = {t["theme"]: [g.resolve_ref(r, t["colors"], g.SCHEMAS[f]) for r in ROLES]
     for f, modes in spec.items() for t in modes.values()}
for suffix in sys.argv[1:] or ["dark", "light"]:
    names = [n for n in T if n.endswith("-" + suffix)]
    pairs = sorted((sum(100 * math.dist(lab(a), lab(b)) for a, b in zip(T[x], T[y])) / len(ROLES), x, y)
                   for x, y in itertools.combinations(names, 2))
    print(suffix + ": " + " | ".join(f"{x[7:-len(suffix)-1]}~{y[7:-len(suffix)-1]} {d:.1f}" for d, x, y in pairs[:5]))
