#!/usr/bin/env python3
"""Lumina 2 palettes, defined in OKLCH (L, C, h) and written to spec/lumina.json.

Usage:
    python3 generators/v2_palettes.py [flavor ...]   # default: every flavor below
"""
import json
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
            "region": (.32, .035, 70), "selection": (.32, .035, 70),
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
            "region": (.89, .04, 80), "selection": (.89, .04, 80),
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
            "region": (.34, .045, 215), "selection": (.34, .045, 215),
            "diff-added-bg": (.28, .03, 150), "diff-removed-bg": (.28, .035, 20), "diff-changed-bg": (.28, .03, 90),
            "diff-added-refine": (.35, .055, 150), "diff-removed-refine": (.35, .065, 20),
        },
        "light": {
            "bg": (.965, .008, 195), "bg-alt": (.935, .012, 195), "fg": (.33, .025, 215), "fg-alt": (.42, .025, 210),
            "base0": (.99, .004, 195), "base1": (.945, .01, 195), "base2": (.91, .014, 198), "base3": (.86, .016, 200),
            "base4": (.76, .02, 202), "base5": (.62, .025, 205), "base6": (.50, .028, 208), "base7": (.40, .028, 212),
            "base8": (.33, .025, 215), "surface": (.945, .01, 195),
            "teal": (.52, .09, 178), "green": (.52, .09, 145), "cyan": (.51, .075, 220), "blue": (.50, .085, 245),
            "dark-blue": (.42, .085, 245), "violet": (.50, .09, 295), "magenta": (.50, .09, 345),
            "red": (.51, .12, 18), "orange": (.53, .10, 45), "yellow": (.52, .09, 90), "dark-cyan": (.42, .06, 220),
            "comments": (.535, .03, 200), "doc-comments": (.48, .03, 200), "strings": (.52, .05, 190),
            "region": (.89, .035, 200), "selection": (.89, .035, 200),
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
            "bg": (.215, .025, 355), "bg-alt": (.19, .024, 355), "fg": (.86, .035, 80), "fg-alt": (.74, .035, 70),
            "base0": (.165, .02, 355), "base1": (.235, .027, 355), "base2": (.27, .029, 355), "base3": (.31, .031, 355),
            "base4": (.40, .033, 0), "base5": (.52, .035, 10), "base6": (.63, .035, 25), "base7": (.75, .035, 55),
            "base8": (.86, .035, 80), "surface": (.245, .028, 355),
            "yellow": (.78, .11, 82), "orange": (.72, .09, 58), "red": (.67, .11, 15), "magenta": (.69, .08, 355),
            "violet": (.69, .06, 325), "green": (.72, .05, 170), "teal": (.71, .045, 185), "cyan": (.72, .04, 200),
            "blue": (.70, .06, 255), "dark-blue": (.60, .06, 255), "dark-cyan": (.60, .04, 200),
            "comments": (.60, .03, 15), "doc-comments": (.66, .035, 30), "strings": (.75, .04, 80),
            "region": (.33, .045, 0), "selection": (.33, .045, 0),
            "diff-added-bg": (.27, .03, 160), "diff-removed-bg": (.27, .04, 20), "diff-changed-bg": (.27, .035, 75),
            "diff-added-refine": (.34, .055, 160), "diff-removed-refine": (.34, .07, 20),
        },
        "light": {
            "bg": (.965, .015, 75), "bg-alt": (.935, .02, 72), "fg": (.33, .03, 0), "fg-alt": (.43, .03, 5),
            "base0": (.99, .008, 80), "base1": (.945, .018, 72), "base2": (.91, .022, 70), "base3": (.86, .025, 65),
            "base4": (.76, .028, 50), "base5": (.62, .03, 30), "base6": (.50, .032, 10), "base7": (.40, .032, 5),
            "base8": (.33, .03, 0), "surface": (.945, .018, 72),
            "yellow": (.53, .10, 72), "orange": (.53, .10, 55), "red": (.49, .13, 15), "magenta": (.49, .10, 355),
            "violet": (.49, .07, 325), "green": (.51, .06, 170), "teal": (.51, .055, 185), "cyan": (.51, .05, 205),
            "blue": (.49, .08, 255), "dark-blue": (.41, .08, 255), "dark-cyan": (.41, .05, 205),
            "comments": (.535, .03, 25), "doc-comments": (.48, .03, 20), "strings": (.50, .05, 70),
            "region": (.89, .035, 30), "selection": (.89, .035, 30),
            "diff-added-bg": (.93, .03, 160), "diff-removed-bg": (.93, .03, 20), "diff-changed-bg": (.93, .035, 80),
            "diff-added-refine": (.87, .06, 160), "diff-removed-refine": (.87, .06, 20),
        },
        "refs": {
            "grey": "base5", "highlight": "yellow", "vertical-bar": "base3", "builtin": "violet",
            "constants": "red", "functions": "yellow", "keywords": "magenta", "methods": "orange",
            "operators": "base6", "type": "green", "variables": "fg", "numbers": "red", "error": "red",
            "warning": "orange", "success": "green", "vc-modified": "yellow", "vc-added": "green",
            "vc-deleted": "red",
        },
        "commentary": {
            "dark": "Lumina Oxblood, dark variant.\nA theatre after the curtain falls: oxblood-velvet drape in shadow, a single overhead spot on the gilt frame. Velvet rose, brass and wine at equal weight, sage relief, cream-parchment strings.",
            "light": "Lumina Oxblood, light variant.\nWarm programme paper under the same gilt spot; deep inks of velvet rose, brass, wine and sage at equal weight.",
        },
    },
}


def write(flavors):
    spec = json.loads(SPEC.read_text())
    for flavor in flavors:
        pal = PALETTES[flavor]
        for mode in ("dark", "light"):
            t = spec["flavors"][flavor][mode]
            old = t["colors"]
            colors = {}
            for k, v in pal[mode].items():
                h = to_hex(*v)
                ansi = old[k][2] if isinstance(old.get(k), list) else ("black" if mode == "dark" else "white")
                colors[k] = [h, h.lower(), ansi]
            for k, r in pal["refs"].items():
                colors[k] = {"ref": r}
            t["colors"] = colors
            t["commentary"] = pal["commentary"][mode]
            bg = colors["bg"][0]
            print(f"{flavor}-{mode}: " + " ".join(
                f"{k} {contrast(colors[k][0], bg):.1f}" for k in
                ("fg", "comments", "red", "orange", "yellow", "green", "teal",
                 "cyan", "blue", "violet", "magenta")))
    SPEC.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    write(sys.argv[1:] or list(PALETTES))
