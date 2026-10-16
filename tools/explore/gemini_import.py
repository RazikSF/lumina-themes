#!/usr/bin/env python3
"""Gemini's dark themes (oct. 2026) as Lumina flavors: dark inks kept exactly, light inks derived.

Dark: Gemini's ground and six role inks, untouched. Light: Gemini's light paper, text and comments where
it proposed them; each ink keeps its dark hue and chroma (fitted to the gamut) and takes the lightness that
keeps on paper the lightness steps it had at night (Vesper method), around 5:1; yellows past 86°
turn to amber on paper, olive otherwise.
Writes the entries into generators/harmony.json and prints the FLAVORS fields.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "generators"))
from oklch import contrast, from_hex, to_hex, fit_chroma

LIGHT_INK = 5.3
SPREAD = .22  # contrast change per 0.1 of dark lightness: an ink lighter at night stays lighter on paper
ROLES = ["keywords", "strings", "type", "builtin", "constants", "functions"]

G = {
    "neon-cyber": dict(bg="#0C0D19", fg="#E8EEF2", comment="#6A6B9E", red="#FF2A6D",
                  inks=dict(keywords="#FF007F", strings="#39FF14", functions="#00F0FF", type="#FFE600", constants="#FF5F1F", builtin="#FF66B2"),
                  light=dict(bg="#F6F6FB", fg="#1C1B33", comment="#6A6B9E")),
    "borealis": dict(bg="#101614", fg="#D0DCD9", comment="#697B76", red="#C97A85",
                     inks=dict(keywords="#9F94C2", strings="#88C0A8", functions="#68B5A6", type="#D4B26A", constants="#D18A78", builtin="#E0A96D"),
                     light=dict(bg="#F0F5F3", fg="#1A2E2A", comment="#6A827B")),
    "cashmere": dict(bg="#181416", fg="#ECE1D3", comment="#8E8183", red="#E07A5F",
                     inks=dict(keywords="#E5989B", strings="#B5C99A", functions="#F0B97B", type="#F4A27E", constants="#E29578", builtin="#F7C59F"),
                     light=dict(bg="#FAF6F0", fg="#362F2D", comment="#8C7B76")),
    "aethelgard": dict(bg="#0B0F19", fg="#E2D9CE", comment="#7A859E", red="#FF5C8A",
                       inks=dict(keywords="#CF8EF0", strings="#99E1D9", functions="#4FD6BE", type="#FFD166", constants="#FF9F80", builtin="#F4A261"),
                       light=dict(bg="#F5F7FA", fg="#202938", comment="#7E8B9E")),
}


def at_contrast(C, h, bg, target):
    """Darkest-first search of the lightness giving `target` contrast on a light bg."""
    lo, hi = .2, .95
    for _ in range(40):
        mid = (lo + hi) / 2
        c = fit_chroma(mid, C, h)
        if contrast(to_hex(mid, c, h), bg) >= target:
            lo = mid
        else:
            hi = mid
    return lo, fit_chroma(lo, C, h), h


def r4(t):
    return [round(x, 4) for x in t]


def main():
    path = ROOT / "generators" / "harmony.json"
    harmony = json.loads(path.read_text())
    for name, g in G.items():
        dark = {r: from_hex(g["inks"][r]) for r in ROLES}
        lbg = g["light"]["bg"]
        chroma = [r for r in ROLES if dark[r][1] >= .02]
        mean = sum(dark[r][0] for r in chroma) / len(chroma)
        light = {}
        for r in ROLES:
            L, C, h = dark[r]
            h = 78 if 86 <= h <= 125 else h
            light[r] = at_contrast(C, h, lbg, 9.0 if C < .02 else max(4.6, LIGHT_INK * (1 - SPREAD * (L - mean) / .1)))
        red_d = from_hex(g["red"])
        harmony[name] = {"dark": {r: r4(v) for r, v in dark.items()},
                         "light": {r: r4(v) for r, v in light.items()},
                         "red": {"dark": r4(red_d), "light": r4(at_contrast(red_d[1], red_d[2], lbg, 5.5))}}
        print(name, " ".join(f"{r}:{to_hex(*light[r])} {contrast(to_hex(*light[r]), lbg):.1f}" for r in ROLES))
    path.write_text(json.dumps(harmony, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
