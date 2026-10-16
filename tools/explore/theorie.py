#!/usr/bin/env python3
"""Harmonise every flavor by colour-design theory (tools/explore/beaute.py), keeping its ground and scene.

For each flavor and mode, starting from its current six inks: the best Matsuda template is fixed, then a
deterministic hill climb moves hue (within 25 degrees of the current one), lightness and chroma to raise
the beauty score (Ou-Luo harmony, template fit, chroma coherence) while keeping the inks legible (>= 4.6:1)
and apart (OKLab distance >= 9 at night, 8 on paper), at most 8.5:1 on paper, with the flavor's mean
saturation kept (no ink below 70 % of it). The error red is then placed furthest from the inks. Writes generators/harmony.json.
Usage: theorie.py [flavor ...]
"""
import itertools, json, math, random, statistics as st, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "generators")); sys.path.insert(0, str(ROOT / "tools/explore"))
import lumina_gen as g
from oklch import from_hex, to_hex, fit_chroma, contrast
from beaute import lab, ou_luo, TEMPLATES, ROLES
from families import dist as cvd_dist

CVD = {"lucide": {"dark": 8.5, "light": 7.0}}  # Lucide keeps its inks apart for deuteranopes and protanopes

MIN_DE = {"dark": 9.0, "light": 8.0}
SPREAD = {"encre": .24}  # lightness spread allowed; Encre tells its two hues apart by lightness
RED_HUES = range(22, 33, 2)


def okde(a, b):
    p = lambda c: (c[0], c[1] * math.cos(math.radians(c[2])), c[1] * math.sin(math.radians(c[2])))
    return 100 * math.dist(p(a), p(b))


def best_template(labs):
    best = (1e9, None)
    for name, secs in TEMPLATES.items():
        for rot in range(0, 360, 2):
            cost = sum(min(max(0, abs((l[4] - (rot + c) + 180) % 360 - 180) - w / 2) for c, w in secs) * l[3] for l in labs)
            best = min(best, (cost, (name, rot)))
    return best[1]


def tcost(labs, tpl):
    secs = TEMPLATES[tpl[0]]
    return sum(min(max(0, abs((l[4] - (tpl[1] + c) + 180) % 360 - 180) - w / 2) for c, w in secs) * l[3] for l in labs) / sum(l[3] for l in labs)


def score(inks, bg_hex, bg_lab, tpl, mode, c0, spread_max, cvd=None):
    hexes = [to_hex(*c) for c in inks]
    labs = [lab(h) for h in hexes]
    oul = st.mean([ou_luo(a, b) for a, b in itertools.combinations(labs, 2)] + [ou_luo(l, bg_lab) for l in labs])
    s = min(1, max(0, (oul + .2) / 1.2)) + max(0, 1 - tcost(labs, tpl) / 30) + max(0, 1 - st.pstdev([l[3] for l in labs]) / 30)
    pen = 0
    for a, b in itertools.combinations(inks, 2):
        pen += max(0, MIN_DE[mode] - okde(a, b)) * .2
    for h in hexes:
        k = contrast(h, bg_hex)
        pen += max(0, 4.6 - k) * .5 + (max(0, k - 8.5) * .3 if mode == "light" else 0)
    mc = st.mean(c[1] for c in inks)
    pen += max(0, abs(mc - c0) - .01) * 20  # the flavor keeps its saturation: harmony without washing out
    pen += sum(max(0, .7 * c0 - c[1]) * 20 for c in inks)
    spread = max(c[0] for c in inks) - min(c[0] for c in inks)
    pen += max(0, spread - spread_max) * 20  # no ink lit above the others like a lamp
    if cvd:
        pen += max(0, cvd - cvd_dist(inks, True)) * .3
    for L, C, hh in inks:
        if 86 <= hh <= 125 and (L < .80 if mode == "dark" else True):  # dim yellow is olive; on paper yellows go amber
            pen += .5
    return s - pen


def error_red(inks, bg_hex, mode):
    """The error red (hue 22-32) furthest from every ink, legible on the ground."""
    best = (-1, None)
    for h in RED_HUES:
        for L in [x / 100 for x in (range(58, 76) if mode == "dark" else range(36, 56))]:
            c = (L, fit_chroma(L, .20, h), h)
            if contrast(to_hex(*c), bg_hex) < (5.2 if mode == "dark" else 4.6):  # legible on its own tinted ground too
                continue
            best = max(best, (min(okde(c, i) for i in inks), c))
    return best[1]


def climb(inks, bg_hex, mode, spread_max=.15, cvd=None, seed=0):
    rnd = random.Random(seed)
    bg_lab = lab(bg_hex)
    tpl = best_template([lab(to_hex(*c)) for c in inks])
    h0 = [c[2] for c in inks]
    c0 = st.mean(c[1] for c in inks)
    cur, cs = list(inks), score(inks, bg_hex, bg_lab, tpl, mode, c0, spread_max, cvd)
    lo, hi = (.62, .90) if mode == "dark" else (.38, .66)
    for it in range(3000):
        i = rnd.randrange(6)
        L, C, h = cur[i]
        k = rnd.random()
        if k < .4:
            h = h0[i] + max(-25, min(25, ((h + rnd.gauss(0, 6)) - h0[i] + 180) % 360 - 180))
        elif k < .7:
            L = min(hi, max(lo, L + rnd.gauss(0, .02)))
        else:
            C = max(.02, C + rnd.gauss(0, .01))
        cand = list(cur)
        cand[i] = (L, fit_chroma(L, C, h % 360), h % 360)
        s = score(cand, bg_hex, bg_lab, tpl, mode, c0, spread_max, cvd)
        if s >= cs:
            cur, cs = cand, s
    return cur, cs, tpl


def main():
    spec = json.loads((ROOT / "spec/lumina.json").read_text())["flavors"]
    path = ROOT / "generators/harmony.json"
    harmony = json.loads(path.read_text())
    only = sys.argv[1:]
    for f, m in spec.items():
        if only and f not in only:
            continue
        entry = harmony.setdefault(f, {})
        for mode in ("dark", "light"):
            c = m[mode]["colors"]; sch = g.schema_for(f, mode)
            inks = [from_hex(g.resolve_ref(r, c, sch)) for r in ROLES]
            bg = g.C(c, "bg")
            new, s, tpl = climb(inks, bg, mode, SPREAD.get(f, .15), CVD.get(f, {}).get(mode))
            entry[mode] = {r: [round(x, 4) for x in v] for r, v in zip(ROLES, new)}
            entry.setdefault("red", {})[mode] = [round(x, 4) for x in error_red(new, bg, mode)]
            print(f"{f:11} {mode:5} {tpl[0]}{tpl[1]:<4} score {s:.2f}  " + " ".join(to_hex(*v) for v in new))
    path.write_text(json.dumps(harmony, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
