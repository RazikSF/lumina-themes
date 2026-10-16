#!/usr/bin/env python3
"""Beauty of each flavor by colour-design theory, no comparison with other themes.

1. Ou & Luo (2006), two-colour harmony model (CIELAB): mean harmony of every ink pair and ink/ground pair.
2. Matsuda's hue templates as used by Cohen-Or et al. (2006): chroma-weighted angular distance of the inks
   to the best-fitting template (i, V, L, I, T, Y, X, any rotation).
3. Albers: chroma coherence, the spread of the inks' saturation.
Usage: beaute.py   (dark and light, ranked)
"""
import itertools, json, math, statistics as st, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "generators"))
import lumina_gen as g

ROLES = ["keywords", "functions", "type", "strings", "constants", "builtin"]


def lab(hexc):
    """sRGB hex -> CIELAB (D65)."""
    rgb = [int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    r, gg, b = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in rgb]
    X = (.4124 * r + .3576 * gg + .1805 * b) / .95047
    Y = .2126 * r + .7152 * gg + .0722 * b
    Z = (.0193 * r + .1192 * gg + .9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > .008856 else 7.787 * t + 16 / 116
    L, a, bb = 116 * f(Y) - 16, 500 * (f(X) - f(Y)), 200 * (f(Y) - f(Z))
    return L, a, bb, math.hypot(a, bb), math.degrees(math.atan2(bb, a)) % 360


def ou_luo(c1, c2):
    """Ou & Luo 2006: CH = HC + HL + HH; higher is more harmonious (about -1 to +1.5)."""
    L1, a1, b1, C1, h1 = c1; L2, a2, b2, C2, h2 = c2
    dH = 2 * math.sqrt(C1 * C2) * math.sin(math.radians(((h1 - h2 + 180) % 360 - 180) / 2))
    dC = math.sqrt(dH ** 2 + ((C1 - C2) / 1.46) ** 2)
    HC = .04 + .53 * math.tanh(.8 - .045 * dC)
    HL = .28 + .54 * math.tanh(-3.88 + .029 * (L1 + L2)) + .14 + .15 * math.tanh(-2 + .2 * abs(L1 - L2))

    def hsy(L, C, h):
        EC = .5 + .5 * math.tanh(-2 + .5 * C)
        HS = -.08 - .14 * math.sin(math.radians(h + 50)) - .07 * math.sin(math.radians(2 * h + 90))
        EY = ((.22 * L - 12.8) / 10) * math.exp((90 - h) / 10 - math.exp((90 - h) / 10))
        return EC * (HS + EY)
    return HC + HL + hsy(L1, C1, h1) + hsy(L2, C2, h2)


TEMPLATES = {"i": [(0, 18)], "V": [(0, 93.6)], "L": [(0, 18), (90, 79.2)], "I": [(0, 18), (180, 18)],
             "T": [(0, 180)], "Y": [(0, 93.6), (180, 18)], "X": [(0, 93.6), (180, 93.6)]}


def template_cost(hc):
    """Mean chroma-weighted degrees outside the best template (hc: [(hue, chroma)])."""
    best = 1e9
    for secs in TEMPLATES.values():
        for rot in range(0, 360, 2):
            cost = 0
            for h, C in hc:
                d = min(max(0, abs((h - (rot + c) + 180) % 360 - 180) - w / 2) for c, w in secs)
                cost += d * C
            best = min(best, cost)
    return best / sum(C for _, C in hc)


def scores(c, sch):
    bg = lab(g.C(c, "bg"))
    inks = [lab(g.resolve_ref(r, c, sch)) for r in ROLES]
    oul = st.mean([ou_luo(a, b) for a, b in itertools.combinations(inks, 2)] + [ou_luo(i, bg) for i in inks])
    tmpl = template_cost([(i[4], i[3]) for i in inks])
    coh = st.pstdev([i[3] for i in inks])
    s1 = min(1, max(0, (oul + .2) / 1.2))
    s2 = max(0, 1 - tmpl / 30)
    s3 = max(0, 1 - coh / 30)
    return s1, s2, s3, oul, tmpl, coh


def main():
    spec = json.loads((ROOT / "spec/lumina.json").read_text())["flavors"]
    rows = []
    for f, m in spec.items():
        d = scores(m["dark"]["colors"], g.schema_for(f, "dark"))
        l = scores(m["light"]["colors"], g.schema_for(f, "light"))
        total = round(100 * sum(d[:3] + l[:3]) / 6)
        rows.append((total, f, d, l))
    print("rang saveur     beauté | sombre : Ou-Luo  gabarit(°)  écart C | clair : idem")
    for i, (t, f, d, l) in enumerate(sorted(rows, reverse=True), 1):
        print(f"{i:2} {f:11} {t:3}  | {d[3]:5.2f} {d[4]:5.1f} {d[5]:5.1f} | {l[3]:5.2f} {l[4]:5.1f} {l[5]:5.1f}")


if __name__ == "__main__":
    main()
