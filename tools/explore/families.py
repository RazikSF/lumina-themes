#!/usr/bin/env python3
"""Gemini's lesson for the harmonised flavors: each one draws its six inks from a family of hues set by its
scene (warm room, ocean, forest...), not from six hues spread evenly round the circle.

Hues are chosen by hand per flavor; a random search then sets lightness (.68-.84) and chroma (.06-.13) so
every pair stays apart (OKLab distance x100), close hues being told apart by lightness as in Vesper. Light
inks: same hue (yellows to amber), searched between 4.6:1 and 8:1 for the widest distance.
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
from oklch import fit_chroma
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
}
CHROMA = {"azur": (.10, .14), "nocturne": (.08, .13), "synthwave": (.15, .21)}
MIN_DE = 9.0


def lab(L, C, h):
    return L, C * math.cos(math.radians(h)), C * math.sin(math.radians(h))


def de(a, b):
    return 100 * math.dist(lab(*a), lab(*b))


def search(hues, crange, seed=0):
    rnd = random.Random(seed)
    best, score = None, -1e9
    for _ in range(20000):
        inks = []
        for h in hues:
            L = rnd.uniform(.68, .84)
            inks.append((L, fit_chroma(L, rnd.uniform(*crange), h), h))
        m = min(de(a, b) for a, b in itertools.combinations(inks, 2))
        spread = max(i[0] for i in inks) - min(i[0] for i in inks)
        s = min(m, MIN_DE + 1) - 4 * max(0, spread - .14) - 2 * abs(sum(i[0] for i in inks) / 6 - .75)
        if s > score:
            best, score = inks, s
    return best


def search_light(dark, lbg, seed=0):
    """Paper inks: same hues (yellows to amber), each between 4.6:1 and 8:1, apart from one another."""
    rnd = random.Random(seed)
    span = {}
    for r, (L, C, h) in dark.items():
        h2 = 78 if 86 <= h <= 125 else h
        hi = at_contrast(C * 1.3, h2, lbg, 4.6)[0]
        lo = at_contrast(C * 1.3, h2, lbg, 8.0)[0]
        span[r] = (lo, hi, C * 1.3, h2)
    best, score = None, -1e9
    for _ in range(20000):
        inks = {}
        for r, (lo, hi, C, h) in span.items():
            L = rnd.uniform(lo, hi)
            inks[r] = (L, fit_chroma(L, C, h), h)
        m = min(de(a, b) for a, b in itertools.combinations(inks.values(), 2))
        if m > score:
            best, score = inks, m
    return best


def main():
    path = ROOT / "generators" / "harmony.json"
    harmony = json.loads(path.read_text())
    sys.path.insert(0, str(ROOT / "generators"))
    import v2_palettes as v2
    for f, hues in FAMILIES.items():
        dark = dict(zip(ROLES, search(hues, CHROMA.get(f, (.07, .12)))))
        lbg = v2.to_hex(*v2.PALETTES[f]["light"]["bg"])
        light = search_light(dark, lbg)
        harmony[f]["dark"] = {r: r4(v) for r, v in dark.items()}
        harmony[f]["light"] = {r: r4(v) for r, v in light.items()}
        m = min(de(a, b) for a, b in itertools.combinations(dark.values(), 2))
        ml = min(de(a, b) for a, b in itertools.combinations(light.values(), 2))
        print(f"{f:9} min dE {m:4.1f} / {ml:4.1f}  " + " ".join(f"{r[:4]}:{v2.to_hex(*v)}" for r, v in dark.items()))
    path.write_text(json.dumps(harmony, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
