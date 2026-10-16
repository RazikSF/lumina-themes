#!/usr/bin/env python3
"""Gemini's lesson for the harmonised flavors: each one draws its six inks from a family of hues set by its
scene (warm room, ocean, forest...), not from six hues spread evenly round the circle.

Hues are chosen by hand per flavor; a random search then sets lightness (.68-.84) and chroma (.06-.13) so
every pair stays apart (OKLab distance x100), close hues being told apart by lightness as in Vesper. Light
inks: same hue (yellows to amber), searched between 4.6:1 and 8:1 for the widest distance.
Lucide keeps its inks apart under simulated deuteranopia and protanopia as well. Usage: families.py [flavor ...]
Writes the flavors into generators/harmony.json; the error red stays as it is there.
"""
import itertools
import json
import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "generators")); sys.path.insert(0, str(ROOT / "tools/explore"))
from oklch import fit_chroma, to_hex, from_hex
from gemini_import import at_contrast, r4

ROLES = ["keywords", "functions", "type", "strings", "constants", "builtin"]
FAMILIES = {  # keywords, functions, type, strings, constants, builtin
    "dawn": (30, 78, 5, 165, 50, 95),        # sepia room: terracotta, amber lamp, rose, peach, sand; one sage
    "oxblood": (300, 350, 80, 195, 25, 325),  # theatre: rose spotlight, violet, mauve, coral, gold; one slate teal
    "tide": (180, 228, 275, 155, 35, 205),    # ocean: teal, sky, periwinkle, seafoam, cyan; one coral
    "canopy": (225, 145, 75, 170, 35, 200),   # forest: leaf, mint, aqua, sky through leaves; amber and bark
    "slate": (215, 255, 285, 180, 20, 160),   # graphite: steel, sky, lavender, teal, mint; one rose whisper
    "nocturne": (290, 60, 230, 260, 330, 200),  # city night: violet, sky, periwinkle, orchid, cyan; sodium lamp
    "amethyst": (320, 90, 285, 250, 345, 210),  # geode: orchid, lavender, periwinkle, pink, ice; citrine shard
    "indigo": (250, 85, 45, 320, 20, 65),     # desert night: azure; gold sand, copper, rose, amber, dusk mauve
    "azur": (245, 55, 300, 95, 175, 20),      # blue slate under a clear sky, the vivid one
    "sirocco": (80, 225, 35, 355, 300, 160),  # desert wind: sand, terracotta, rose, dusk mauve, sage; sky lamp
    "celadon": (210, 50, 160, 180, 250, 140), # jade porcelain: sky, jade, celadon, indigo, green; peach lamp
    "sumi": (30, 150, 320, 220, 60, 350),     # ink: vermilion, matcha, plum, sky, ochre, rose
    "pivoine": (350, 165, 320, 20, 60, 280),  # peony: peony, orchid, salmon, apricot, lavender; mint lamp
    "cafe": (200, 70, 185, 45, 230, 330),     # espresso in a blue cup: caramel, cinnamon, cocoa mauve; sky, teal, slate
    "petrole": (195, 80, 45, 165, 310, 240),  # petrol blue: cyan, jade, steel, oil-sheen violet; brass lamp, copper
    "synthwave": (290, 340, 90, 200, 50, 355),  # eighties sunset: violet, magenta, sun yellow, cyan, orange, hot pink
    "brume": (265, 205, 230, 170, 30, 300),   # morning mist on a lake: periwinkle, aqua, steel, mint, lilac; one warm sun
    "lucide": (235, 65, 100, 165, 340, 40),   # Okabe-Ito hues: sky, orange, yellow, bluish green, reddish purple, vermilion
    "encre": (250, 70, 250, 70, 70, 250),     # two inks, blue and amber, told apart by lightness and chroma
}
CHROMA = {"azur": (.10, .14), "nocturne": (.08, .13), "synthwave": (.15, .21), "encre": (.05, .13), "brume": (.05, .10)}
LIGHTNESS = {"brume": (.76, .88), "encre": (.64, .88), "lucide": (.62, .88)}  # Brume sits on a mid-dark ground; Encre tells its two hues apart by lightness
SPREAD_MAX = {"encre": .24, "lucide": .24}
OLIVE_GUARD = {"brume", "lucide", "encre"}  # flavors made after the guard; the earlier ones keep their approved inks
CVD = {"lucide"}  # inks kept apart for deuteranopes and protanopes too (Machado 2009, full severity)
MACHADO = {"deutan": ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881)),
           "protan": ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216), (-0.003882, -0.048116, 1.051998))}
MIN_DE = 9.0


def lab(L, C, h):
    return L, C * math.cos(math.radians(h)), C * math.sin(math.radians(h))


def de(a, b):
    return 100 * math.dist(lab(*a), lab(*b))


def simulate(c, kind):
    """OKLCH colour as seen with a full colour-vision deficiency."""
    h = to_hex(*c)
    lin = [(v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4) for v in (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))]
    out = [min(max(sum(m * x for m, x in zip(row, lin)), 0), 1) for row in MACHADO[kind]]
    srgb = [round(255 * (12.92 * v if v <= .0031308 else 1.055 * v ** (1 / 2.4) - .055)) for v in out]
    return from_hex("#%02X%02X%02X" % tuple(srgb))


def dist(inks, cvd):
    pairs = list(itertools.combinations(inks, 2))
    m = min(de(a, b) for a, b in pairs)
    if cvd:
        for kind in MACHADO:
            sim = [simulate(c, kind) for c in inks]
            m = min(m, min(de(a, b) for a, b in itertools.combinations(sim, 2)))
    return m


def search(hues, crange, lrange=(.68, .84), spread_max=.14, cvd=False, olive_guard=False, seed=0):
    rnd = random.Random(seed)
    best, score = None, -1e9
    mid = .75 if lrange == (.68, .84) else sum(lrange) / 2
    for _ in range(20000 if not cvd else 6000):
        inks = []
        for h in hues:
            L = rnd.uniform(max(lrange[0], .80) if olive_guard and 86 <= h <= 125 else lrange[0], lrange[1])  # a dim yellow is olive
            inks.append((L, fit_chroma(L, rnd.uniform(*crange), h), h))
        m = dist(inks, cvd)
        spread = max(i[0] for i in inks) - min(i[0] for i in inks)
        s = min(m, MIN_DE + 1) - 4 * max(0, spread - spread_max) - 2 * abs(sum(i[0] for i in inks) / 6 - mid)
        if s > score:
            best, score = inks, s
    return best


def search_light(dark, lbg, cvd=False, wide=False, seed=0):
    """Paper inks: same hues (yellows to amber), each between 4.6:1 and 8:1 (10:1 for the wide flavors), apart."""
    rnd = random.Random(seed)
    span = {}
    for r, (L, C, h) in dark.items():
        h2 = 78 if 86 <= h <= 125 else h
        hi = at_contrast(C * 1.3, h2, lbg, 4.6)[0]
        lo = at_contrast(C * 1.3, h2, lbg, 10.0 if wide else 8.0)[0]
        span[r] = (lo, hi, C * 1.3, h2)
    best, score = None, -1e9
    for _ in range(20000 if not cvd else 6000):
        inks = {}
        for r, (lo, hi, C, h) in span.items():
            L = rnd.uniform(lo, hi)
            inks[r] = (L, fit_chroma(L, C, h), h)
        m = dist(list(inks.values()), cvd)
        if m > score:
            best, score = inks, m
    return best


def main():
    path = ROOT / "generators" / "harmony.json"
    harmony = json.loads(path.read_text())
    sys.path.insert(0, str(ROOT / "generators"))
    import v2_palettes as v2
    for f, hues in FAMILIES.items():
        if sys.argv[1:] and f not in sys.argv[1:]:
            continue
        cvd = f in CVD
        dark = dict(zip(ROLES, search(hues, CHROMA.get(f, (.07, .12)), LIGHTNESS.get(f, (.68, .84)), SPREAD_MAX.get(f, .14), cvd, f in OLIVE_GUARD)))
        lbg = v2.to_hex(*v2.PALETTES[f]["light"]["bg"])
        light = search_light(dark, lbg, cvd, f in SPREAD_MAX)
        harmony[f]["dark"] = {r: r4(v) for r, v in dark.items()}
        harmony[f]["light"] = {r: r4(v) for r, v in light.items()}
        m, ml = dist(list(dark.values()), cvd), dist(list(light.values()), cvd)
        print(f"{f:9} min dE {m:4.1f} / {ml:4.1f}  " + " ".join(f"{r[:4]}:{v2.to_hex(*v)}" for r, v in dark.items()))
    path.write_text(json.dumps(harmony, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
