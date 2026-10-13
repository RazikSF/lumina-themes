"""Six-ink harmonisation of every Lumina flavor, on the Nuancier standard.

Standard (measured on the Nuancier palette the user calls perfect):
  - six inks, one per role (functions, keywords, types, strings, constants, builtins);
  - six hues spread over the whole circle, no gap above 95 degrees;
  - one weight: same OKLCH lightness, a step below the text, chroma about 0.10
    (yellows lower, since they read brighter);
  - every pair at least 8.5 dE apart;
  - frequent roles (keywords, strings) on cool hues, warm hues on rare roles,
    unless the flavor is a warm family;
  - identity: hues stay close to the flavor's current ones; flavors stay apart.

Usage: python3 tools/explore/harmony.py   -> generators/harmony.json (+ report)
"""
import json, math, random, sys
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "generators"))
from oklch import contrast, fit_chroma, from_hex, to_hex
import lumina_gen as g

ROLES = ["keywords", "strings", "type", "builtin", "constants", "functions"]
WEIGHT = {"keywords": .40, "strings": .14, "type": .13, "builtin": .13, "constants": .13, "functions": .07}
FIXED = {  # the standard itself, as measured on the slide
    "nuancier": {"functions": "#EC907E", "keywords": "#77B8E7", "type": "#F7C054", "strings": "#87C3AB",
                 "constants": "#B5A4EA", "builtin": "#E297BA"}}
CHROMA = {"dawn": .10, "oxblood": .10, "tide": .10, "canopy": .10, "slate": .10, "vesper": .105, "sienne": .105,
          "indigo": .105, "azur": .125, "nocturne": .125, "amethyst": .125, "prisma": .125, "sirocco": .105, "celadon": .105,
          "sumi": .10, "pivoine": .10}
INK_L = {"pivoine": .80}
LOVED = {"vesper", "sienne"}
ORDER = ["vesper", "sienne", "dawn", "oxblood", "tide", "canopy", "slate", "nocturne", "amethyst", "prisma",
         "indigo", "azur", "sirocco", "celadon", "sumi", "pivoine"]


def lab(c):
    L, C, h = c; return L, C * math.cos(math.radians(h)), C * math.sin(math.radians(h))


def de(a, b): return 100 * math.dist(lab(a), lab(b))


def ang(a, b): return abs((a - b + 180) % 360 - 180)


def warm(h): return 20 <= h <= 110


NUANCIER_PROFILE = [(32, -.015, .116), (82, .078, .138), (168, .009, .071), (241, -.003, .095), (295, -.001, .100), (350, .001, .100)]


def profile(h):
    """Lightness offset and chroma of the Nuancier palette at hue h, interpolated around the circle."""
    pts = sorted(NUANCIER_PROFILE)
    for i, (h0, l0, c0) in enumerate(pts):
        h1, l1, c1 = pts[(i + 1) % len(pts)]
        span = (h1 - h0) % 360
        t = ((h - h0) % 360) / span if span else 0
        if 0 <= t <= 1:
            return l0 + (l1 - l0) * t, c0 + (c1 - c0) * t
    return 0, .1


def ink(L, h, C=.10):
    dl, c = profile(h)
    L2 = L + dl
    return (L2, fit_chroma(L2, c * C / .10, h), h)


def light_ink(h, paper, C):
    """Same hue as an ink on paper (Radix step-11 lightness). Yellows turn to deep amber and yellow-greens lean
    to green, since both go olive when darkened."""
    if 50 <= h <= 115:
        hh, L, c = 62, .54, .16
    elif 115 < h < 160:
        hh, L, c = h + 12, .51, min(.15, C * 1.45)
    else:
        hh, L, c = h, .51, min(.15, C * 1.45)
    col = (L, fit_chroma(L, c, hh), hh)
    while contrast(to_hex(*col), paper) < 4.6 and col[0] > .3:
        col = (col[0] - .01, fit_chroma(col[0] - .01, c, hh), hh)
    return col


spec = json.loads(g.SPEC.read_text())["flavors"]
origin = json.loads((ROOT / "tools/explore/out/lumina-before-harmony.json").read_text())["flavors"]
CONCEPT = {  # the colour each flavor is named after stays on its role (hue in degrees)
    "dawn": {"functions": 88}, "oxblood": {"functions": 345}, "tide": {"functions": 235}, "canopy": {"functions": 150},
    "slate": {"functions": 255}, "nocturne": {"functions": 60}, "amethyst": {"functions": 95, "keywords": 330},
    "prisma": {"functions": 305}, "indigo": {"keywords": 255}, "azur": {"keywords": 240}, "sirocco": {"functions": 235},
    "celadon": {"functions": 50}, "sumi": {"functions": 150, "keywords": 35}, "pivoine": {"functions": 150, "keywords": 340}}


def current(f, src=None):
    c = (src or spec)[f]["dark"]["colors"]; sch = g.SCHEMAS[f]
    hexes = {r: g.resolve_ref(r, c, sch) for r in ROLES}
    return {r: from_hex(v) for r, v in hexes.items()}, from_hex(g.C(c, "fg")), from_hex(g.C(c, "bg"))


def design(f, done, seed=1):
    cur, fg, bg = current(f, origin)
    Lk = INK_L.get(f, .76)
    Cf = CHROMA[f]
    idw = 2.0 if f in LOVED else 1.0
    warmfam = bool(g.SCHEMAS[f].get("warm_family"))
    cur_h = {r: cur[r][2] for r in ROLES}
    distinct = []
    for r in ROLES:
        if all(ang(cur_h[r], x) > 12 for x in distinct):
            distinct.append(cur_h[r])

    paper = to_hex(*from_hex(g.C(spec[f]["light"]["colors"], "bg")))

    def score(H):
        cols = {r: ink(Lk, H[r], Cf) for r in ROLES}
        sep = min(de(cols[a], cols[b]) for a, b in combinations(ROLES, 2))
        hs = sorted(H.values()); gaps = [(hs[(i + 1) % 6] - hs[i]) % 360 for i in range(6)]
        s = min(sep, 13) * 1.0
        if sep < 8.5: s -= (8.5 - sep) * 30
        if max(gaps) > 95: s -= (max(gaps) - 95) * .3
        if min(gaps) < 50: s -= (50 - min(gaps)) * .4
        s -= idw * sum(WEIGHT[r] * ang(H[r], cur_h[r]) for r in ROLES) / 180 * 10
        s -= idw * sum(min(ang(x, H[r]) for r in ROLES) for x in distinct) / len(distinct) / 180 * 8
        s -= 25 * sum(1 for r in ROLES if 90 < H[r] < 140)
        s -= sum(ang(H[r], h0) for r, h0 in CONCEPT.get(f, {}).items()) / 10
        if not warmfam:
            s -= 3 * sum(1 for r in ("keywords", "strings") if warm(H[r]))
        mine = sorted(H.values())
        lcols = {r: light_ink(H[r], paper, Cf) for r in ROLES}
        for other in done.values():
            d = sum(de(cols[r], other["dark"][r]) for r in ("keywords", "strings", "functions", "type")) / 4
            if d < 9: s -= (9 - d) * 8
            if "light" in other:
                dl = sum(de(lcols[r], other["light"][r]) for r in ("keywords", "strings", "functions", "type")) / 4
                if dl < 9: s -= (9 - dl) * 8
            oh = [c[2] for c in other["dark"].values()]
            setd = sum(min(ang(x, y) for y in oh) for x in mine) / 6
            near_ground = ang(other.get("bg", (0, 0, -999))[2], bg[2]) < 40 and other.get("bg", (0, 0, 0))[1] > .012 and bg[1] > .012
            if near_ground and setd < 15: s -= (15 - setd) * 2.5
            elif setd < 9 and abs(other.get("C", .1) - Cf) < .015: s -= (9 - setd) * .8
        return s, sep, max(gaps)

    rnd = random.Random(seed)
    best = None
    for start in range(30):
        if start % 3 == 2:
            H = {r: rnd.randrange(0, 360, 5) for r in ROLES}
        else:
            H = {r: (cur_h[r] + rnd.choice([0, 0, 15, -15, 30, -30])) % 360 for r in ROLES}
        sc = score(H)[0]
        for it in range(3000):
            N = dict(H)
            u = rnd.random()
            if u < .2:
                a, b = rnd.sample(ROLES, 2); N[a], N[b] = N[b], N[a]
            elif u < .3:
                N[rnd.choice(ROLES)] = rnd.randrange(0, 360, 5)
            else:
                r = rnd.choice(ROLES); N[r] = (N[r] + rnd.choice([-20, -10, -5, 5, 10, 20])) % 360
            s2 = score(N)[0]
            if s2 >= sc:
                H, sc = N, s2
        if best is None or sc > best[0]:
            best = (sc, H)
    H = best[1]
    _, sep, gmax = score(H)
    paper = to_hex(*from_hex(g.C(spec[f]["light"]["colors"], "bg")))
    return {"L": Lk, "C": Cf, "bg": bg, "hues": H, "dark": {r: ink(Lk, H[r], Cf) for r in ROLES},
            "light": {r: light_ink(H[r], paper, Cf) for r in ROLES}, "sep": sep, "gmax": gmax, "cur": cur_h}


def tune_light(light, paper, others=(), seed=3):
    """Nudge light inks (hue +/-25, L +/-.04) until every pair is at least 8.5 apart, staying readable."""
    rnd = random.Random(seed)
    base = dict(light)

    def ok(col):
        return contrast(to_hex(*col), paper) >= 4.6

    def score(Lt):
        sep = min(de(Lt[a], Lt[b]) for a, b in combinations(ROLES, 2))
        dev = sum(ang(Lt[r][2], base[r][2]) / 25 + abs(Lt[r][0] - base[r][0]) / .04 for r in ROLES)
        pen = 0
        for o in others:
            d = sum(de(Lt[r], o[r]) for r in ("keywords", "strings", "functions", "type")) / 4
            if d < 9: pen += (9 - d) * 3
        return min(sep, 11) - (8.5 - sep) * 10 * (sep < 8.5) - dev * .15 - pen
    cur = dict(base); sc = score(cur)
    for _ in range(9000):
        r = rnd.choice(ROLES); L, C, h = base[r]
        h2 = (h + rnd.uniform(-25, 25)) % 360; L2 = L + rnd.uniform(-.04, .04)
        cand = (L2, fit_chroma(L2, C, h2), h2)
        if not ok(cand):
            continue
        N = dict(cur); N[r] = cand
        s2 = score(N)
        if s2 >= sc:
            cur, sc = N, s2
    return cur


def _mix(a, b, t):
    A, B = lab(a), lab(b); L, x, y = [p + (q - p) * t for p, q in zip(A, B)]
    return (L, math.hypot(x, y), math.degrees(math.atan2(y, x)) % 360)


def error_red(inks, ground, dark):
    """A true red (hue 22-32), the one farthest from the six inks, readable on the ground."""
    best = None
    for h in range(22, 33, 2):
        for L in ([x / 100 for x in range(66, 78)] if dark else [x / 100 for x in range(40, 53)]):
            col = (L, fit_chroma(L, .21, h), h)
            if contrast(to_hex(*col), ground) < 4.5:
                continue
            if dark and contrast(to_hex(*col), to_hex(*_mix(from_hex(ground), col, .16))) < 4.2:
                continue
            d = min(de(col, v) for v in inks.values())
            if best is None or d > best[0]:
                best = (d, col)
    return best[1]


def main():
    done = {}
    for f, cols in FIXED.items():
        done[f] = {"dark": {r: from_hex(v) for r, v in cols.items()}, "fixed": True, "C": .10, "bg": from_hex("#1D2130"),
                   "light": {r: light_ink(from_hex(v)[2], "#F6F7FA", .10) for r, v in cols.items()}}
    for f in LOVED:
        done[f] = {"dark": current(f)[0], "fixed": True, "C": CHROMA[f], "bg": current(f)[2],
                   "light": {r: from_hex(g.resolve_ref(r, spec[f]["light"]["colors"], g.SCHEMAS[f])) for r in ROLES}}
    for f in ORDER:
        if f in LOVED:
            continue
        done[f] = design(f, {k: v for k, v in done.items()})
    out = {}
    for f, d in done.items():
        if f in LOVED:
            continue
        out[f] = {"dark": {r: [round(x, 4) for x in v] for r, v in d["dark"].items()}}
        if "light" in d:
            out[f]["light"] = {r: [round(x, 4) for x in v] for r, v in d["light"].items()}
        if not d.get("fixed"):
            print(f"{f:9} L{d['L']:.2f} C{d['C']:.3f} séparation {d['sep']:4.1f} trou max {d['gmax']:3.0f}° | "
                  + " ".join(f"{r[:3]} {d['cur'][r]:3.0f}->{d['hues'][r]:3.0f}" for r in ROLES))
    grounds = {"nuancier": ("#1D2130", "#F6F7FA")}
    tuned = [{r: from_hex(g.resolve_ref(r, spec[f]["light"]["colors"], g.SCHEMAS[f])) for r in ROLES} for f in LOVED]
    for f, entry in out.items():
        if f in grounds:
            bg, paper = grounds[f]
            if "light" not in entry:
                entry["light"] = {r: list(light_ink(v[2], paper, .10)) for r, v in entry["dark"].items()}
        else:
            bg = to_hex(*from_hex(g.C(spec[f]["dark"]["colors"], "bg")))
            paper = to_hex(*from_hex(g.C(spec[f]["light"]["colors"], "bg")))
        lt = tune_light({r: tuple(v) for r, v in entry["light"].items()}, paper, tuned)
        tuned.append(lt)
        entry["light"] = {r: [round(x, 4) for x in v] for r, v in lt.items()}
        dk = {r: tuple(v) for r, v in entry["dark"].items()}
        entry["red"] = {"dark": [round(x, 4) for x in error_red(dk, bg, True)],
                        "light": [round(x, 4) for x in error_red(lt, paper, False)]}
        sep_l = min(de(lt[a], lt[b]) for a, b in combinations(ROLES, 2))
        print(f"{f:9} clair : séparation {sep_l:4.1f} | rouge d'erreur sombre {to_hex(*entry['red']['dark'])} clair {to_hex(*entry['red']['light'])}"
              f" (écart min {min(de(tuple(entry['red']['dark']), v) for v in dk.values()):.1f} / {min(de(tuple(entry['red']['light']), v) for v in lt.values()):.1f})")
    (ROOT / "tools/explore/out/harmony-proposal.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
