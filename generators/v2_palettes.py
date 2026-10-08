#!/usr/bin/env python3
"""Lumina 2 palettes, defined in OKLCH (L, C, h) and written to spec/lumina.json.

Usage:
    python3 generators/v2_palettes.py [flavor ...]   # default: every flavor below
"""
import json
import math
import sys
from pathlib import Path

from oklch import contrast, to_hex

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "spec" / "lumina.json"

PALETTES = {
    "dawn": {
        "dark": {
            "bg": (.215, .012, 65), "bg-alt": (.190, .011, 65), "fg": (.86, .025, 82), "fg-alt": (.74, .025, 78),
            "base0": (.165, .010, 65), "base1": (.235, .013, 65), "base2": (.27, .014, 65), "base3": (.31, .013, 65),
            "base4": (.40, .015, 68), "base5": (.52, .018, 70), "base6": (.63, .02, 72), "base7": (.75, .022, 76),
            "base8": (.86, .025, 82), "surface": (.245, .014, 65),
            "yellow": (.77, .105, 75), "orange": (.71, .095, 48), "red": (.67, .115, 28), "green": (.73, .075, 120),
            "teal": (.72, .055, 160), "cyan": (.71, .05, 205), "blue": (.71, .05, 240), "dark-blue": (.60, .05, 240),
            "violet": (.70, .05, 295), "magenta": (.69, .065, 350), "dark-cyan": (.60, .045, 205),
            "comments": (.60, .025, 72), "doc-comments": (.66, .03, 75), "strings": (.73, .075, 120),
            "diff-added-bg": (.27, .03, 135), "diff-removed-bg": (.27, .035, 28), "diff-changed-bg": (.27, .035, 80),
            "diff-added-refine": (.34, .06, 135), "diff-removed-refine": (.34, .07, 28),
        },
        "light": {
            "bg": (.965, .012, 82), "bg-alt": (.935, .015, 80), "fg": (.33, .02, 60), "fg-alt": (.42, .02, 62),
            "base0": (.99, .006, 82), "base1": (.945, .014, 80), "base2": (.91, .016, 80), "base3": (.86, .018, 78),
            "base4": (.76, .02, 76), "base5": (.62, .02, 72), "base6": (.50, .02, 68), "base7": (.40, .02, 64),
            "base8": (.33, .02, 60), "surface": (.945, .014, 80),
            "yellow": (.535, .11, 70), "orange": (.53, .11, 45), "red": (.51, .13, 28), "green": (.52, .09, 125),
            "teal": (.52, .07, 165), "cyan": (.52, .06, 210), "blue": (.51, .07, 245), "dark-blue": (.42, .07, 245),
            "violet": (.51, .07, 295), "magenta": (.50, .08, 350), "dark-cyan": (.42, .06, 210),
            "comments": (.535, .025, 70), "doc-comments": (.48, .025, 70), "strings": (.52, .09, 125),
            "diff-added-bg": (.93, .03, 135), "diff-removed-bg": (.93, .03, 28), "diff-changed-bg": (.93, .04, 85),
            "diff-added-refine": (.87, .07, 135), "diff-removed-refine": (.87, .07, 28),
        },
        "refs": {
            "grey": "base5", "highlight": "yellow", "vertical-bar": "base3", "builtin": "magenta",
            "constants": "magenta", "functions": "yellow", "keywords": "orange", "methods": "blue",
            "operators": "base6", "type": "teal", "variables": "fg", "numbers": "violet", "error": "red",
            "warning": "orange", "success": "green", "vc-modified": "yellow", "vc-added": "green",
            "vc-deleted": "red",
        },
        "commentary": {
            "dark": "Lumina Dawn, dark variant.\nWarm sepia room lit by a single amber lamp; muted inks of rust, olive, sage, slate and plum at equal weight.",
            "light": "Lumina Dawn, light variant.\nWarm ivory paper under the same amber lamp; deep muted inks of rust, olive, sage, slate and plum at equal weight.",
        },
    },
    "tide": {
        "dark": {
            "bg": (.22, .022, 212), "bg-alt": (.195, .02, 212), "fg": (.87, .012, 200), "fg-alt": (.74, .02, 200),
            "base0": (.17, .018, 212), "base1": (.24, .024, 212), "base2": (.28, .026, 212), "base3": (.32, .028, 212),
            "base4": (.41, .03, 210), "base5": (.52, .032, 208), "base6": (.63, .032, 205), "base7": (.75, .03, 202),
            "base8": (.87, .012, 200), "surface": (.25, .025, 212),
            "teal": (.80, .11, 178), "green": (.73, .075, 145), "cyan": (.72, .06, 210), "blue": (.71, .07, 240),
            "dark-blue": (.60, .07, 240), "violet": (.71, .075, 295), "magenta": (.70, .075, 340),
            "red": (.68, .10, 18), "orange": (.73, .085, 45), "yellow": (.74, .065, 90), "dark-cyan": (.60, .06, 210),
            "comments": (.60, .03, 200), "doc-comments": (.66, .035, 195), "strings": (.74, .045, 185),
            "diff-added-bg": (.28, .03, 150), "diff-removed-bg": (.28, .035, 20), "diff-changed-bg": (.28, .03, 90),
            "diff-added-refine": (.35, .055, 150), "diff-removed-refine": (.35, .065, 20),
        },
        "light": {
            "bg": (.965, .014, 188), "bg-alt": (.935, .018, 190), "fg": (.33, .025, 215), "fg-alt": (.42, .025, 210),
            "base0": (.99, .004, 195), "base1": (.945, .01, 195), "base2": (.91, .014, 198), "base3": (.86, .016, 200),
            "base4": (.76, .02, 202), "base5": (.62, .025, 205), "base6": (.50, .028, 208), "base7": (.40, .028, 212),
            "base8": (.33, .025, 215), "surface": (.945, .01, 195),
            "teal": (.52, .09, 178), "green": (.52, .09, 145), "cyan": (.51, .075, 220), "blue": (.50, .085, 245),
            "dark-blue": (.42, .085, 245), "violet": (.50, .09, 295), "magenta": (.50, .09, 345),
            "red": (.51, .12, 18), "orange": (.53, .10, 45), "yellow": (.52, .09, 90), "dark-cyan": (.42, .06, 220),
            "comments": (.535, .03, 200), "doc-comments": (.48, .03, 200), "strings": (.52, .05, 190),
            "diff-added-bg": (.93, .03, 150), "diff-removed-bg": (.93, .03, 20), "diff-changed-bg": (.93, .035, 90),
            "diff-added-refine": (.87, .06, 150), "diff-removed-refine": (.87, .06, 20),
        },
        "refs": {
            "grey": "base5", "highlight": "teal", "vertical-bar": "base3", "builtin": "magenta",
            "constants": "orange", "functions": "teal", "keywords": "violet", "methods": "blue",
            "operators": "base6", "type": "cyan", "variables": "fg", "numbers": "orange", "error": "red",
            "warning": "orange", "success": "green", "vc-modified": "yellow", "vc-added": "green",
            "vc-deleted": "red",
        },
        "commentary": {
            "dark": "Lumina Tide, dark variant.\nDeep ocean at night, lit from within by a single bioluminescent glow; sea-glass, kelp, slate blue and jellyfish violet at equal weight, coral and sand as rare warm notes.",
            "light": "Lumina Tide, light variant.\nSea-foam paper under the same bioluminescent glow; deep inks of ocean blue, kelp, violet and coral at equal weight.",
        },
    },
    "oxblood": {
        "dark": {
            "bg": (.215, .035, 8), "bg-alt": (.19, .032, 8), "fg": (.87, .025, 60), "fg-alt": (.74, .03, 40),
            "base0": (.165, .028, 8), "base1": (.235, .036, 8), "base2": (.27, .038, 8), "base3": (.31, .04, 8),
            "base4": (.40, .04, 10), "base5": (.52, .04, 15), "base6": (.63, .035, 30), "base7": (.75, .03, 50),
            "base8": (.87, .025, 60), "surface": (.245, .037, 8),
            "magenta": (.77, .11, 5), "red": (.68, .12, 22), "orange": (.72, .08, 60), "yellow": (.74, .09, 88),
            "green": (.72, .05, 165), "teal": (.71, .045, 190), "cyan": (.71, .04, 215), "blue": (.70, .06, 260),
            "violet": (.69, .07, 320), "dark-blue": (.60, .06, 260), "dark-cyan": (.60, .04, 215),
            "comments": (.60, .035, 15), "doc-comments": (.66, .035, 30), "strings": (.76, .035, 75),
            "diff-added-bg": (.27, .03, 160), "diff-removed-bg": (.27, .045, 25), "diff-changed-bg": (.27, .035, 80),
            "diff-added-refine": (.34, .055, 160), "diff-removed-refine": (.34, .075, 25),
        },
        "light": {
            "bg": (.965, .018, 15), "bg-alt": (.935, .024, 15), "fg": (.33, .035, 0), "fg-alt": (.43, .035, 5),
            "base0": (.99, .008, 15), "base1": (.945, .02, 15), "base2": (.91, .024, 15), "base3": (.86, .026, 15),
            "base4": (.76, .028, 15), "base5": (.62, .03, 10), "base6": (.50, .032, 5), "base7": (.40, .034, 0),
            "base8": (.33, .035, 0), "surface": (.945, .02, 15),
            "magenta": (.50, .14, 5), "red": (.50, .12, 25), "orange": (.53, .10, 55), "yellow": (.53, .09, 85),
            "green": (.51, .06, 165), "teal": (.51, .055, 190), "cyan": (.51, .05, 215), "blue": (.49, .08, 260),
            "violet": (.49, .08, 320), "dark-blue": (.41, .08, 260), "dark-cyan": (.41, .05, 215),
            "comments": (.535, .03, 10), "doc-comments": (.48, .03, 5), "strings": (.50, .045, 60),
            "diff-added-bg": (.93, .03, 160), "diff-removed-bg": (.93, .03, 25), "diff-changed-bg": (.93, .035, 80),
            "diff-added-refine": (.87, .06, 160), "diff-removed-refine": (.87, .06, 25),
        },
        "refs": {
            "grey": "base5", "highlight": "magenta", "vertical-bar": "base3", "builtin": "blue",
            "constants": "orange", "functions": "magenta", "keywords": "violet", "methods": "yellow",
            "operators": "base6", "type": "green", "variables": "fg", "numbers": "orange", "error": "red",
            "warning": "orange", "success": "green", "vc-modified": "yellow", "vc-added": "green",
            "vc-deleted": "red",
        },
        "commentary": {
            "dark": "Lumina Oxblood, dark variant.\nA theatre after the curtain falls: oxblood velvet in shadow, one rose spotlight on the stage. Plum, gilt, brass and sage at equal weight, cream-parchment strings.",
            "light": "Lumina Oxblood, light variant.\nBlush programme paper under the same rose spotlight; deep inks of plum, gilt, brass and sage at equal weight.",
        },
    },
    "canopy": {
        "dark": {
            "bg": (.215, .02, 148), "bg-alt": (.19, .018, 148), "fg": (.86, .025, 120), "fg-alt": (.74, .03, 125),
            "base0": (.165, .016, 148), "base1": (.235, .022, 148), "base2": (.27, .024, 146), "base3": (.31, .026, 145),
            "base4": (.40, .028, 145), "base5": (.52, .03, 140), "base6": (.63, .03, 135), "base7": (.75, .03, 128),
            "base8": (.86, .025, 120), "surface": (.245, .023, 148),
            "yellow": (.81, .12, 106), "green": (.74, .085, 140), "teal": (.71, .06, 175), "cyan": (.71, .05, 205),
            "blue": (.70, .06, 250), "dark-blue": (.60, .06, 250), "violet": (.70, .06, 295), "magenta": (.69, .07, 350),
            "red": (.68, .10, 35), "orange": (.73, .09, 62), "dark-cyan": (.60, .05, 205),
            "comments": (.60, .035, 140), "doc-comments": (.66, .04, 135), "strings": (.74, .04, 70),
            "diff-added-bg": (.28, .045, 145), "diff-removed-bg": (.27, .04, 25), "diff-changed-bg": (.27, .035, 85),
            "diff-added-refine": (.35, .07, 145), "diff-removed-refine": (.34, .07, 25),
        },
        "light": {
            "bg": (.965, .014, 130), "bg-alt": (.935, .018, 132), "fg": (.33, .025, 150), "fg-alt": (.43, .028, 148),
            "base0": (.99, .006, 130), "base1": (.945, .016, 132), "base2": (.91, .02, 134), "base3": (.86, .023, 136),
            "base4": (.76, .026, 140), "base5": (.62, .028, 144), "base6": (.50, .028, 147), "base7": (.40, .027, 150),
            "base8": (.33, .025, 150), "surface": (.945, .016, 132),
            "yellow": (.53, .11, 100), "green": (.51, .09, 145), "teal": (.51, .07, 175), "cyan": (.51, .06, 210),
            "blue": (.49, .08, 250), "dark-blue": (.41, .08, 250), "violet": (.49, .08, 295), "magenta": (.49, .09, 350),
            "red": (.50, .11, 35), "orange": (.53, .10, 60), "dark-cyan": (.41, .05, 210),
            "comments": (.535, .03, 140), "doc-comments": (.48, .03, 140), "strings": (.50, .045, 65),
            "diff-added-bg": (.92, .045, 145), "diff-removed-bg": (.93, .03, 25), "diff-changed-bg": (.93, .035, 85),
            "diff-added-refine": (.86, .07, 145), "diff-removed-refine": (.87, .06, 25),
        },
        "refs": {
            "grey": "base5", "highlight": "yellow", "vertical-bar": "base3", "builtin": "violet",
            "constants": "red", "functions": "yellow", "keywords": "green", "methods": "cyan",
            "operators": "base6", "type": "orange", "variables": "fg", "numbers": "red", "error": "red",
            "warning": "orange", "success": "green", "vc-modified": "yellow", "vc-added": "green",
            "vc-deleted": "red",
        },
        "commentary": {
            "dark": "Lumina Canopy, dark variant.\nA pine forest at noon: a single shaft of leaf-filtered sun, chartreuse gold, pierces the canopy. Chlorophyll, pine, russet and heather at equal weight in the shade, bark-brown strings.",
            "light": "Lumina Canopy, light variant.\nLeaf-tinted paper under the same shaft of sun; deep inks of chlorophyll, pine, russet and heather at equal weight.",
        },
    },
    "slate": {
        "dark": {
            "bg": (.215, .009, 256), "bg-alt": (.19, .009, 258), "fg": (.86, .008, 260), "fg-alt": (.74, .014, 260),
            "base0": (.165, .008, 258), "base1": (.235, .01, 256), "base2": (.27, .011, 256), "base3": (.31, .012, 256),
            "base4": (.40, .014, 258), "base5": (.52, .016, 258), "base6": (.63, .017, 260), "base7": (.75, .016, 260),
            "base8": (.86, .008, 260), "surface": (.245, .01, 256),
            "blue": (.76, .09, 245), "teal": (.71, .05, 195), "cyan": (.71, .05, 215), "green": (.72, .055, 155),
            "violet": (.70, .05, 285), "magenta": (.70, .055, 340), "red": (.67, .09, 22), "orange": (.72, .07, 62),
            "yellow": (.74, .06, 92), "dark-blue": (.62, .07, 245), "dark-cyan": (.60, .045, 215),
            "comments": (.60, .018, 258), "doc-comments": (.66, .02, 258), "strings": (.76, .015, 250),
            "variables": (.81, .01, 262),
            "diff-added-bg": (.27, .03, 150), "diff-removed-bg": (.27, .035, 20), "diff-changed-bg": (.27, .03, 85),
            "diff-added-refine": (.34, .055, 150), "diff-removed-refine": (.34, .065, 20),
        },
        "light": {
            "bg": (.96, .006, 255), "bg-alt": (.93, .008, 258), "fg": (.33, .015, 258), "fg-alt": (.43, .016, 260),
            "base0": (.99, .003, 255), "base1": (.94, .007, 256), "base2": (.905, .009, 258), "base3": (.855, .011, 258),
            "base4": (.76, .013, 260), "base5": (.62, .015, 260), "base6": (.50, .016, 260), "base7": (.40, .016, 258),
            "base8": (.33, .015, 258), "surface": (.94, .007, 256),
            "blue": (.50, .11, 250), "teal": (.51, .06, 195), "cyan": (.51, .06, 220), "green": (.51, .07, 155),
            "violet": (.50, .07, 285), "magenta": (.50, .08, 340), "red": (.50, .11, 22), "orange": (.53, .09, 58),
            "yellow": (.52, .08, 90), "dark-blue": (.42, .10, 250), "dark-cyan": (.42, .05, 220),
            "comments": (.535, .015, 258), "doc-comments": (.48, .015, 258), "strings": (.47, .012, 258),
            "variables": (.39, .015, 258),
            "diff-added-bg": (.93, .03, 150), "diff-removed-bg": (.93, .03, 20), "diff-changed-bg": (.93, .035, 85),
            "diff-added-refine": (.87, .06, 150), "diff-removed-refine": (.87, .06, 20),
        },
        "refs": {
            "grey": "base5", "highlight": "blue", "vertical-bar": "base3", "builtin": "cyan",
            "constants": "magenta", "functions": "blue", "keywords": "cyan", "methods": "teal",
            "operators": "base6", "type": "violet", "numbers": "orange", "error": "red",
            "warning": "orange", "success": "green", "vc-modified": "yellow", "vc-added": "green",
            "vc-deleted": "red",
        },
        "commentary": {
            "dark": "Lumina Slate, dark variant.\nCold graphite ground; near-achromatic text and strings, one steel-blue lamp, steel cyan, muted violet, teal and sage at equal weight, a single warm note of brass in numbers.",
            "light": "Lumina Slate, light variant.\nCool grey paper under the same steel-blue lamp; near-achromatic inks with steel cyan, muted violet, teal and sage at equal weight.",
        },
    },
}


def field(dark, h, c, bg=None, fg=None, fgh=None):
    """Ground, greys and text of a flavor from one hue and one chroma."""
    fgh = h if fgh is None else fgh
    if dark:
        b = bg or .21
        steps = {"bg": b, "bg-alt": b - .025, "base0": b - .05, "base1": b + .02, "surface": b + .03,
                 "base2": b + .06, "base3": b + .10, "base4": .40, "base5": .52, "base6": .63, "base7": .76}
        out = {k: (L, c * (1.1 if L > b else .9), h) for k, L in steps.items()}
        out["base7"] = (.76, c * .7, fgh)
        f = fg or .88
    else:
        b = bg or .968
        steps = {"bg": b, "bg-alt": b - .03, "base0": min(b + .025, 1), "base1": b - .02, "surface": b - .02,
                 "base2": b - .055, "base3": b - .105, "base4": .76, "base5": .62, "base6": .50, "base7": .40}
        out = {k: (L, c * (1.4 if L < b else .5), h) for k, L in steps.items()}
        f = fg or .31
    out["fg"] = out["base8"] = (f, c * (.45 if dark else 1.4), fgh)
    out["fg-alt"] = ((f - .13) if dark else (f + .11), c * (.9 if dark else 1.3), fgh)
    return out


def diffs(dark, add=150, rem=22, chg=92):
    if dark:
        return {"diff-added-bg": (.28, .04, add), "diff-removed-bg": (.28, .05, rem), "diff-changed-bg": (.28, .04, chg),
                "diff-added-refine": (.36, .07, add), "diff-removed-refine": (.36, .085, rem)}
    return {"diff-added-bg": (.93, .035, add), "diff-removed-bg": (.93, .035, rem), "diff-changed-bg": (.93, .04, chg),
            "diff-added-refine": (.87, .07, add), "diff-removed-refine": (.87, .07, rem)}


VIVID = {
    "nocturne": {
        "dark": {**field(True, 268, .038), **diffs(True),
                 "orange": (.78, .15, 58), "red": (.71, .16, 22), "yellow": (.77, .13, 95), "green": (.76, .15, 150),
                 "teal": (.75, .11, 185), "cyan": (.75, .12, 215), "blue": (.72, .15, 258), "violet": (.72, .15, 295),
                 "magenta": (.72, .16, 345), "dark-blue": (.60, .13, 258), "dark-cyan": (.62, .10, 215),
                 "comments": (.60, .04, 265), "doc-comments": (.66, .045, 265)},
        "light": {**field(False, 265, .012), **diffs(False),
                  "orange": (.545, .16, 50), "red": (.51, .17, 22), "yellow": (.53, .12, 90), "green": (.52, .14, 150),
                  "teal": (.52, .10, 185), "cyan": (.51, .11, 220), "blue": (.48, .17, 262), "violet": (.49, .17, 295),
                  "magenta": (.50, .18, 345), "dark-blue": (.40, .15, 262), "dark-cyan": (.42, .09, 220),
                  "comments": (.535, .035, 265), "doc-comments": (.48, .04, 265)},
        "refs": {"grey": "base5", "highlight": "orange", "vertical-bar": "base3", "builtin": "cyan",
                 "constants": "magenta", "functions": "orange", "keywords": "violet", "methods": "blue",
                 "operators": "base6", "type": "teal", "variables": "fg", "numbers": "red", "strings": "green",
                 "error": "red", "warning": "yellow", "success": "green", "vc-modified": "yellow",
                 "vc-added": "green", "vc-deleted": "red"},
        "commentary": {
            "dark": "Lumina Nocturne, dark variant.\nA city at night under a deep indigo sky, lit by one sodium streetlamp; neon violet, cobalt, jade and rose at equal weight.",
            "light": "Lumina Nocturne, light variant.\nMoonlit blue-white paper under the same sodium lamp; vivid inks of violet, cobalt, jade and rose at equal weight.",
        },
    },
    "amethyst": {
        "dark": {**field(True, 305, .05), **diffs(True),
                 "yellow": (.85, .13, 98), "magenta": (.74, .16, 350), "red": (.70, .16, 20), "orange": (.76, .13, 55),
                 "green": (.78, .14, 160), "teal": (.77, .11, 185), "cyan": (.76, .11, 215), "blue": (.73, .13, 265),
                 "violet": (.72, .14, 300), "dark-blue": (.62, .12, 265), "dark-cyan": (.62, .09, 215),
                 "comments": (.61, .05, 300), "doc-comments": (.67, .055, 300)},
        "light": {**field(False, 305, .024), **diffs(False),
                  "yellow": (.53, .125, 103), "magenta": (.50, .17, 350), "red": (.51, .17, 22), "orange": (.53, .13, 50),
                  "green": (.52, .12, 160), "teal": (.52, .09, 185), "cyan": (.51, .10, 220), "blue": (.48, .15, 265),
                  "violet": (.48, .16, 300), "dark-blue": (.40, .13, 265), "dark-cyan": (.42, .08, 220),
                  "comments": (.535, .04, 305), "doc-comments": (.48, .045, 305)},
        "refs": {"grey": "base5", "highlight": "yellow", "vertical-bar": "base3", "builtin": "blue",
                 "constants": "violet", "functions": "yellow", "keywords": "magenta", "methods": "cyan",
                 "operators": "base6", "type": "cyan", "variables": "fg", "numbers": "orange", "strings": "green",
                 "error": "red", "warning": "orange", "success": "green", "vc-modified": "orange",
                 "vc-added": "green", "vc-deleted": "red"},
        "commentary": {
            "dark": "Lumina Amethyst, dark variant.\nInside a split amethyst geode, one shard of citrine catching the light; orchid, mint, ice blue and lilac at equal weight.",
            "light": "Lumina Amethyst, light variant.\nLilac paper under the same citrine light; vivid inks of orchid, mint, ice blue and lilac at equal weight.",
        },
    },
    "obsidian": {
        "dark": {**field(True, 285, .008, bg=.165), **diffs(True),
                 "orange": (.72, .19, 34), "red": (.70, .18, 8), "yellow": (.78, .13, 92), "green": (.77, .16, 148),
                 "teal": (.76, .12, 185), "cyan": (.76, .12, 215), "blue": (.72, .15, 262), "violet": (.72, .15, 300),
                 "magenta": (.72, .17, 345), "dark-blue": (.60, .13, 262), "dark-cyan": (.62, .10, 215),
                 "comments": (.60, .015, 285), "doc-comments": (.66, .018, 285)},
        "light": {**field(False, 285, .004, bg=.985, fg=.30), **diffs(False),
                  "orange": (.53, .19, 33), "red": (.50, .19, 8), "yellow": (.52, .12, 85), "green": (.51, .15, 148),
                  "teal": (.51, .10, 185), "cyan": (.50, .11, 220), "blue": (.47, .17, 262), "violet": (.47, .17, 300),
                  "magenta": (.49, .19, 345), "dark-blue": (.40, .15, 262), "dark-cyan": (.41, .09, 220),
                  "comments": (.53, .012, 285), "doc-comments": (.47, .014, 285)},
        "refs": {"grey": "base5", "highlight": "orange", "vertical-bar": "base3", "builtin": "violet",
                 "constants": "magenta", "functions": "orange", "keywords": "teal", "methods": "cyan",
                 "operators": "base6", "type": "blue", "variables": "fg", "numbers": "yellow", "strings": "green",
                 "error": "red", "warning": "yellow", "success": "green", "vc-modified": "yellow",
                 "vc-added": "green", "vc-deleted": "red"},
        "commentary": {
            "dark": "Lumina Obsidian, dark variant.\nVolcanic glass, near-black, split by a single seam of molten lava; glacier teal, cobalt, jade and magenta at equal weight.",
            "light": "Lumina Obsidian, light variant.\nWhite marble veined with the same lava; vivid inks of glacier teal, cobalt, jade and magenta at equal weight.",
        },
    },
    "prisma": {
        "dark": {**field(True, 275, .014, bg=.22), **diffs(True),
                 "spark": (.97, .015, 95), "red": (.71, .16, 25), "orange": (.75, .15, 58), "yellow": (.78, .14, 98),
                 "green": (.76, .16, 148), "teal": (.76, .12, 185), "cyan": (.75, .12, 218), "blue": (.72, .15, 258),
                 "violet": (.71, .16, 298), "magenta": (.72, .17, 340), "dark-blue": (.62, .13, 258),
                 "dark-cyan": (.62, .10, 218), "comments": (.60, .02, 275), "doc-comments": (.66, .025, 275)},
        "light": {**field(False, 275, .005, bg=.985, fg=.32), **diffs(False),
                  "spark": (.26, .03, 280), "red": (.51, .18, 25), "orange": (.53, .14, 55), "yellow": (.53, .12, 90),
                  "green": (.51, .15, 148), "teal": (.51, .10, 185), "cyan": (.50, .11, 220), "blue": (.47, .17, 260),
                  "violet": (.47, .18, 298), "magenta": (.49, .19, 340), "dark-blue": (.40, .15, 260),
                  "dark-cyan": (.41, .09, 220), "comments": (.53, .015, 275), "doc-comments": (.47, .018, 275)},
        "refs": {"grey": "base5", "highlight": "spark", "vertical-bar": "base3", "builtin": "magenta",
                 "constants": "orange", "functions": "blue", "keywords": "violet", "methods": "cyan",
                 "operators": "base6", "type": "yellow", "variables": "fg", "numbers": "red", "strings": "green",
                 "error": "red", "warning": "orange", "success": "green", "vc-modified": "yellow",
                 "vc-added": "green", "vc-deleted": "red"},
        "commentary": {
            "dark": "Lumina Prisma, dark variant.\nA single white ray enters a glass prism: the ray is the lamp, the code is its spectrum, every hue at equal weight.",
            "light": "Lumina Prisma, light variant.\nWhite paper and one stroke of ink; the code is a full spectrum of vivid inks at equal weight.",
        },
    },
}
PALETTES.update(VIVID)


ACCENT_KEYS = ["red", "orange", "yellow", "green", "teal", "cyan", "blue", "violet", "magenta"]
ANSI = {"red": "red", "orange": "brightred", "yellow": "yellow", "green": "green", "teal": "brightgreen",
        "cyan": "cyan", "blue": "blue", "violet": "brightmagenta", "magenta": "magenta",
        "dark-blue": "brightblue", "dark-cyan": "brightcyan", "fg": "white", "bg": "black"}


def _lab(c):
    L, C, h = c
    return L, C * math.cos(math.radians(h)), C * math.sin(math.radians(h))


def _lch(L, a, b):
    return L, math.hypot(a, b), math.degrees(math.atan2(b, a)) % 360


def mix(c1, c2, t):
    """Mix two OKLCH colours in OKLab; t = share of c2."""
    a, b = _lab(c1), _lab(c2)
    return _lch(*[x + (y - x) * t for x, y in zip(a, b)])


def lift(c, bg, target, step):
    """Move lightness of c (by step per iteration) until contrast with bg >= target."""
    L, C, h = c
    while contrast(to_hex(L, C, h), to_hex(*bg)) < target and 0 < L < 1:
        L += step
    return min(max(L, 0), 1)


def signature(pal, lead, dark):
    """Lumina light signature: the lamp tints the current line, the selection and jumps."""
    bg, lamp = pal["bg"], pal[lead]
    out = dict(pal)
    out["halo"] = mix(bg, lamp, .075 if dark else .10)
    out["halo2"] = mix(bg, lamp, .14 if dark else .17)
    out["region"] = out["selection"] = mix(bg, lamp, .24 if dark else .26)
    out["glow"] = mix(bg, lamp, .42 if dark else .40)
    L, C, h = bg
    out["dim"] = (L - .03, C * .8, h) if dark else (L - .025, C * 1.2, h)
    return out


def high_contrast(pal, lead, dark):
    """Derive the -contrast variant: fg >= 15:1, comments >= 6:1, accents >= 7:1 (AAA)."""
    q = dict(pal)
    if dark:
        for k, L in {"bg": .165, "bg-alt": .14, "base0": .12, "base1": .19, "surface": .20,
                     "base2": .235, "base3": .29, "base4": .42, "base5": .58, "base6": .70,
                     "base7": .82, "fg": .95, "fg-alt": .86, "base8": .95}.items():
            q[k] = (L, q[k][1], q[k][2])
    else:
        for k, L in {"bg": .995, "bg-alt": .965, "base0": 1.0, "base1": .975, "surface": .975,
                     "base2": .94, "base3": .89, "base4": .74, "base5": .55, "base6": .42,
                     "base7": .31, "fg": .17, "fg-alt": .29, "base8": .17}.items():
            q[k] = (L, q[k][1], q[k][2])
    bg, step = q["bg"], (.005 if dark else -.005)
    accents = [k for k in ACCENT_KEYS if k != lead]
    Lacc = max(lift(q[k], bg, 7.2, step) for k in accents) if dark else \
        min(lift(q[k], bg, 7.2, step) for k in accents)
    for k in accents:
        q[k] = (Lacc, q[k][1], q[k][2])
    if lead in q:
        q[lead] = (lift(q[lead], bg, 8.5, step), q[lead][1], q[lead][2])
    for k, target in (("comments", 6.2), ("doc-comments", 6.8), ("strings", 7.2),
                      ("variables", 12.0), ("dark-blue", 4.5), ("dark-cyan", 4.5)):
        if k in q:
            q[k] = (lift(q[k], bg, target, step), q[k][1], q[k][2])
    for k in ("diff-added-bg", "diff-removed-bg", "diff-changed-bg",
              "diff-added-refine", "diff-removed-refine"):
        if k in q:
            L, C, h = q[k]
            q[k] = ((L - .05, C * 1.2, h) if dark else (L + .02, C * 1.2, h))
    return q


def write(flavors):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from lumina_gen import SCHEMAS
    spec = json.loads(SPEC.read_text())
    for flavor in flavors:
        pal = PALETTES[flavor]
        lead = SCHEMAS[flavor]["lead"]
        modes = spec["flavors"].setdefault(flavor, {})
        for mode in ("dark", "light"):
            dark = mode == "dark"
            base = pal[mode]
            variants = {mode: signature(base, lead, dark),
                        f"{mode}-contrast": signature(high_contrast(base, lead, dark), lead, dark)}
            for vname, vpal in variants.items():
                t = modes.setdefault(vname, {})
                old = t.get("colors", {})
                colors = {}
                for k, v in vpal.items():
                    h = to_hex(*v)
                    ansi = old[k][2] if isinstance(old.get(k), list) else ANSI.get(k, "black" if dark else "white")
                    colors[k] = [h, h.lower(), ansi]
                for k, r in pal["refs"].items():
                    if k not in vpal:
                        colors[k] = {"ref": r}
                t["theme"] = f"lumina-{flavor}-{vname}"
                t["background"] = mode
                t["schema"] = flavor
                t["colors"] = colors
                text = pal["commentary"][mode]
                if vname.endswith("contrast"):
                    first, rest = text.split("\n", 1)
                    text = first.replace("variant.", "variant, high contrast.") + "\n" + rest
                t["commentary"] = text
                bg = colors["bg"][0]
                print(f"{flavor}-{vname}: " + " ".join(
                    f"{k} {contrast(colors[k][0], bg):.1f}" for k in
                    ["fg", "comments", lead] + [a for a in ACCENT_KEYS if a != lead]))
        spec["flavors"][flavor] = {k: modes[k] for k in ("dark", "light", "dark-contrast", "light-contrast")}
    SPEC.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    write(sys.argv[1:] or list(PALETTES))
