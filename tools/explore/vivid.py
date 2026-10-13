"""Relative vividness of the code roles: chroma as a share of the sRGB maximum at the same L and hue.

Usage: python3 tools/explore/vivid.py [dark|light]
"""
import json, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "generators"))
from oklch import from_hex
import lumina_gen as g

ROLES = ["functions", "keywords", "type", "strings", "constants", "builtin"]


def in_gamut(L, C, h):
    a, b = C * math.cos(math.radians(h)), C * math.sin(math.radians(h))
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    rgb = [4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
           -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
           -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s]
    return all(-1e-4 <= x <= 1 + 1e-4 for x in rgb)


def cmax(L, h):
    lo, hi = 0.0, 0.4
    for _ in range(30):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if in_gamut(L, mid, h) else (lo, mid)
    return lo


def vivid(hexc):
    L, C, h = from_hex(hexc)
    return C / max(cmax(L, h), 1e-3)


if __name__ == "__main__":
    modes = sys.argv[1:] or ["dark", "light"]
    spec = json.loads(g.SPEC.read_text())["flavors"]
    for mode in modes:
        print(f"--- {mode}: part du maximum par rôle | écart (max - min)")
        for f, m in spec.items():
            c = m[mode]["colors"]
            v = [(r, vivid(g.resolve_ref(r, c, g.SCHEMAS[f]))) for r in ROLES]
            s = [x for _, x in v]
            print(f"{f:9} " + " ".join(f"{r[:4]}={x:.2f}" for r, x in v) + f" | {max(s) - min(s):.2f}")
