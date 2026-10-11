#!/usr/bin/env python3
"""Lumina 3 palettes: composed from public colour scales (Tailwind v4 step 300 on dark
grounds, Radix Colors step 11 on light paper), written to spec/lumina.json.

Each flavor = one ground hue, one lamp slot, one hue per accent slot, one role map.
Non-lamp accents are clamped to a common lightness band and a chroma cap so the
lamp alone stands out; text sits near 9:1, never white nor black.

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


SIGNATURE = {"halo": (.075, .10), "halo2": (.14, .17), "region": (.24, .26), "glow": (.42, .40), "overlay": (.045, .03)}


def signature(pal, lead, dark, sig=None):
    """Lumina light signature: the lamp tints the current line, the selection and jumps.
    Also derives the popup ground (overlay) and one tinted ground per accent (<accent>-bg).
    SIG overrides the mix strengths per flavor: {"halo": x, "halo2": x, "region": x, "glow": x, "overlay": x}."""
    bg, lamp = pal["bg"], pal[lead]
    s = {k: (v[0] if dark else v[1]) for k, v in SIGNATURE.items()}
    s.update(sig or {})
    out = dict(pal)
    out["halo"] = mix(bg, lamp, s["halo"])
    out["halo2"] = mix(bg, lamp, s["halo2"])
    out["region"] = out["selection"] = mix(bg, lamp, s["region"])
    out["glow"] = mix(bg, lamp, s["glow"])
    L, C, h = bg
    out["dim"] = (L - .03, C * .8, h) if dark else (L - .025, C * 1.2, h)
    out["overlay"] = mix((L + s["overlay"], C * 1.1, h) if dark else (L - s["overlay"], C * 1.3, h), lamp, .04)
    for k in (*ACCENT_KEYS, "spark"):
        if k in pal:
            out[f"{k}-bg"] = mix(bg, pal[k], .16 if dark else .09)
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
        extra = {name: (src, {**pal[src], **over}) for name, (src, over) in pal.get("variants", {}).items()}
        for mode, (src, base) in {"dark": ("dark", pal["dark"]), "light": ("light", pal["light"]), **extra}.items():
            dark = src == "dark"
            sig = pal.get("sig")
            variants = {mode: signature(base, lead, dark, sig),
                        f"{mode}-contrast": signature(high_contrast(base, lead, dark), lead, dark, sig)}
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
                t["background"] = src
                t["schema"] = flavor
                t["colors"] = colors
                text = pal["commentary"].get(mode, pal["commentary"][src])
                if vname.endswith("contrast"):
                    first, rest = text.split("\n", 1)
                    text = first.replace("variant.", "variant, high contrast.") + "\n" + rest
                t["commentary"] = text
                bg = colors["bg"][0]
                print(f"{flavor}-{vname}: " + " ".join(
                    f"{k} {contrast(colors[k][0], bg):.1f}" for k in
                    ["fg", "comments", lead] + [a for a in ACCENT_KEYS if a != lead]))
        order = ["dark", "light", *extra, "dark-contrast", "light-contrast", *(f"{e}-contrast" for e in extra)]
        spec["flavors"][flavor] = {k: modes[k] for k in order}
    SPEC.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")


# Public colour scales, OKLCH (L, C, h), baked from the official sources (tools/explore/sources.json).
TW300 = {  # Tailwind v4, step 300: pastel accents for dark grounds
    "red": (0.808, 0.114, 19.6),
    "orange": (0.837, 0.128, 66.3),
    "amber": (0.879, 0.169, 91.6),
    "yellow": (0.905, 0.182, 98.1),
    "lime": (0.897, 0.196, 126.7),
    "green": (0.871, 0.15, 154.4),
    "emerald": (0.845, 0.143, 165.0),
    "teal": (0.855, 0.138, 181.1),
    "cyan": (0.865, 0.127, 207.1),
    "sky": (0.828, 0.111, 230.3),
    "blue": (0.809, 0.105, 251.8),
    "indigo": (0.785, 0.115, 274.7),
    "violet": (0.811, 0.111, 293.6),
    "purple": (0.827, 0.119, 306.4),
    "fuchsia": (0.833, 0.145, 321.4),
    "pink": (0.823, 0.12, 346.0),
    "rose": (0.81, 0.117, 11.6),
}
RX11 = {  # Radix Colors light, step 11: ink accents for light paper
    "red": (0.557, 0.197, 25.2),
    "tomato": (0.566, 0.198, 32.7),
    "orange": (0.585, 0.174, 42.7),
    "amber": (0.571, 0.129, 63.9),
    "yellow": (0.569, 0.119, 76.8),
    "lime": (0.544, 0.111, 128.6),
    "grass": (0.526, 0.129, 147.2),
    "green": (0.543, 0.112, 159.5),
    "jade": (0.547, 0.098, 170.0),
    "teal": (0.552, 0.101, 178.8),
    "cyan": (0.547, 0.097, 220.8),
    "sky": (0.525, 0.108, 232.5),
    "blue": (0.556, 0.162, 252.2),
    "indigo": (0.509, 0.172, 267.2),
    "iris": (0.511, 0.174, 279.8),
    "violet": (0.508, 0.159, 288.6),
    "purple": (0.517, 0.173, 305.9),
    "plum": (0.522, 0.173, 321.9),
    "pink": (0.558, 0.207, 347.3),
    "crimson": (0.552, 0.207, 4.5),
    "ruby": (0.549, 0.199, 13.9),
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


SLOTS = ["red", "orange", "yellow", "green", "teal", "cyan", "blue", "violet", "magenta"]
DEFAULT_HUES = {"red": ("red", "red"), "orange": ("orange", "orange"), "yellow": ("amber", "amber"), "green": ("emerald", "grass"),
                "teal": ("teal", "teal"), "cyan": ("sky", "sky"), "blue": ("indigo", "indigo"), "violet": ("violet", "violet"),
                "magenta": ("fuchsia", "crimson")}
SIG = {"halo": .10, "halo2": .16, "region": .26, "glow": .45, "overlay": .05}


def compose(ground, lamp, roles, hues=None, text=(.78, .40), cap=(.13, .16), band=((.79, .85), (.50, .53)),
            commentary=None, variants=None, extra=None):
    """Build a flavor from public scales.

    ground   (hue, chroma dark, chroma light, L dark, L light)
    lamp     the slot that carries the lamp (kept at its scale value, never clamped)
    roles    {"functions", "keywords", "type", "strings", "constants", "builtin", "methods"} -> slot
    hues     slot -> (Tailwind hue, Radix hue); defaults in DEFAULT_HUES; may add "spark"
    """
    h, cd, cl, Ld, Ll = ground
    hues = {**DEFAULT_HUES, **(hues or {})}
    dark = {**field(True, h, cd, bg=Ld, fg=text[0]), **diffs(True)}
    light = {**field(False, h, cl, bg=Ll, fg=text[1]), **diffs(False)}
    for slot, (twn, rxn) in hues.items():
        for pal, table, i in ((dark, TW300, 0), (light, RX11, 1)):
            L, C, hh = table[twn if i == 0 else rxn]
            if slot != lamp:
                L = min(max(L, band[i][0]), band[i][1]); C = min(C, cap[i])
            elif i == 1:
                L = min(L, .54)
            pal[slot] = (L, C, hh)
    dark["dark-blue"] = (dark["blue"][0] - .14, dark["blue"][1], dark["blue"][2]); dark["dark-cyan"] = (dark["cyan"][0] - .14, dark["cyan"][1], dark["cyan"][2])
    light["dark-blue"] = (light["blue"][0] - .10, light["blue"][1], light["blue"][2]); light["dark-cyan"] = (light["cyan"][0] - .10, light["cyan"][1], light["cyan"][2])
    dark["comments"] = (.61, min(cd * 1.1, .05), h); dark["doc-comments"] = (.67, min(cd * 1.1, .05), h)
    light["comments"] = (.54, max(cl * 2, .012), h); light["doc-comments"] = (.47, max(cl * 2, .014), h)
    for pal, over in ((dark, (extra or {}).get("dark", {})), (light, (extra or {}).get("light", {}))):
        pal.update(over)
    refs = {"grey": "base5", "highlight": lamp, "vertical-bar": "base3", "operators": "base6", "variables": "fg",
            "error": "red", "warning": "orange", "success": "green", "vc-modified": "yellow", "vc-added": "green", "vc-deleted": "red",
            "numbers": roles["constants"], **roles}
    out = {"dark": dark, "light": light, "sig": dict(SIG), "refs": refs, "commentary": commentary or {}}
    if variants:
        out["variants"] = variants
    return out


FLAVORS = {
    "vesper": dict(ground=(265, .042, .004, .208, .985), lamp="teal",
                      roles=dict(functions="teal", keywords="violet", type="blue", strings="green", constants="orange", builtin="cyan", methods="cyan"),
                      hues={"red": ("rose", "red")},
                      commentary={"dark": "Lumina Vesper, dark variant.\nNavy slate at dusk; the lamp is a mint-teal star, violet keywords and indigo types beside it, soft text, one apricot note.",
                                  "light": "Lumina Vesper, light variant.\nCool white paper; the same teal star as a deep ink, violet keywords and indigo types beside it, soft text, one apricot note."}),
    "dawn": dict(ground=(56.0, 0.006, .010, 0.216, .975), lamp="yellow",
                    roles=dict(functions="yellow", keywords="orange", type="teal", strings="green", constants="magenta", builtin="blue", methods="cyan"),
                    hues={"green": ("lime", "lime"), "red": ("red", "tomato"), "magenta": ("rose", "crimson")},
                    commentary={"dark": "Lumina Dawn, dark variant.\nWarm sepia room lit by one amber lamp; terracotta keywords, teal types, lime strings, rose constants, soft text.",
                                "light": "Lumina Dawn, light variant.\nWarm paper under the same amber lamp; terracotta, teal, lime and crimson inks, soft text."}),
    "oxblood": dict(ground=(3.6, 0.015, .012, 0.208, .975), lamp="magenta",
                       roles=dict(functions="magenta", keywords="violet", type="yellow", strings="green", constants="orange", builtin="cyan", methods="cyan"),
                       hues={"magenta": ("rose", "crimson")},
                       commentary={"dark": "Lumina Oxblood, dark variant.\nA theatre after the curtain falls; a rose spotlight on oxblood velvet, violet keywords, amber types, soft text.",
                                   "light": "Lumina Oxblood, light variant.\nBlush paper under the same rose spotlight; crimson, violet and amber inks, soft text."}),
    "tide": dict(ground=(257.5, 0.029, .006, 0.216, .985), lamp="cyan",
                    roles=dict(functions="cyan", keywords="teal", type="blue", strings="green", constants="yellow", builtin="violet", methods="blue"),
                    hues={"red": ("rose", "red")},
                    commentary={"dark": "Lumina Tide, dark variant.\nDeep ocean at night; a sky-blue lamp lit from within, teal keywords, indigo types, soft text, one amber note.",
                                "light": "Lumina Tide, light variant.\nSea-washed paper; the same sky lamp as a deep ink, teal and indigo beside it, one amber note."}),
    "canopy": dict(ground=(149.9, 0.013, .006, 0.21, .98), lamp="green",
                      roles=dict(functions="green", keywords="teal", type="yellow", strings="cyan", constants="orange", builtin="violet", methods="blue"),
                      hues={"green": ("green", "grass")},
                      commentary={"dark": "Lumina Canopy, dark variant.\nPine forest at noon; the lamp is leaf-filtered sun, teal keywords, amber types, sky strings, soft text.",
                                  "light": "Lumina Canopy, light variant.\nMoss-white paper; the same green light as a deep ink, teal, amber and sky inks, soft text."}),
    "slate": dict(ground=(285.9, 0.006, .003, 0.21, .985), lamp="blue",
                     roles=dict(functions="blue", keywords="cyan", type="violet", strings="green", constants="orange", builtin="teal", methods="cyan"),
                     cap=(.09, .12),
                     commentary={"dark": "Lumina Slate, dark variant.\nCold graphite; one steel-blue lamp, every other accent held back to a whisper, soft text.",
                                 "light": "Lumina Slate, light variant.\nCold white paper; the same steel-blue ink, every other accent held back, soft text."}),
    "nocturne": dict(ground=(266.4, 0.042, .008, 0.208, .98), lamp="orange",
                        roles=dict(functions="orange", keywords="violet", type="cyan", strings="green", constants="yellow", builtin="blue", methods="cyan"),
                        hues={"red": ("rose", "red")},
                        commentary={"dark": "Lumina Nocturne, dark variant.\nA city at night under an indigo sky; one sodium streetlamp, neon violet keywords, sky types, soft text.",
                                    "light": "Lumina Nocturne, light variant.\nMoonlit blue-white paper under the same sodium lamp; violet, sky and jade inks, soft text."}),
    "amethyst": dict(ground=(326.6, 0.032, .010, 0.21, .98), lamp="yellow",
                        roles=dict(functions="yellow", keywords="magenta", type="cyan", strings="green", constants="orange", builtin="violet", methods="cyan"),
                        hues={"magenta": ("fuchsia", "plum"), "red": ("rose", "red")},
                        commentary={"dark": "Lumina Amethyst, dark variant.\nInside a split amethyst geode; one shard of citrine catching the light, orchid keywords, ice-blue types, soft text.",
                                    "light": "Lumina Amethyst, light variant.\nLilac paper under the same citrine light; plum, sky and jade inks, soft text."}),
    "obsidian": dict(ground=(89.9, 0.0, .003, 0.213, .99), lamp="red",
                        roles=dict(functions="red", keywords="teal", type="cyan", strings="green", constants="yellow", builtin="violet", methods="blue"),
                        hues={"red": ("red", "tomato")},
                        commentary={"dark": "Lumina Obsidian, dark variant.\nVolcanic glass, near-black, split by one seam of molten lava; glacier teal keywords, sky types, soft text.",
                                    "light": "Lumina Obsidian, light variant.\nWhite marble veined with the same lava; teal, sky and jade inks, soft text."}),
    "prisma": dict(ground=(286.6, 0.029, .005, 0.209, .985), lamp="spark",
                      roles=dict(functions="spark", keywords="violet", type="yellow", strings="green", constants="orange", builtin="magenta", methods="cyan"),
                      hues={"spark": ("purple", "purple")},
                      commentary={"dark": "Lumina Prisma, dark variant.\nBlack light: the lamp is ultraviolet, the definitions fluoresce in it, and the code is a full spectrum at equal weight.",
                                  "dark-ink": "Lumina Prisma, dark ink variant.\nBlack and white: a single white ray enters a glass prism; the ray is the lamp, the code is its spectrum.",
                                  "light": "Lumina Prisma, light variant.\nWhite paper in daylight; the lamp turns ultraviolet and the code is a full spectrum of vivid inks.",
                                  "light-ink": "Lumina Prisma, light ink variant.\nBlack and white: white paper, one lamp of black ink, and the code as a full spectrum of inks."},
                      variants={"dark-ink": ("dark", {"spark": (.97, .015, 95)}), "light-ink": ("light", {"spark": (.26, .03, 280)})}),
}
PALETTES = {k: compose(**v) for k, v in FLAVORS.items()}


if __name__ == "__main__":
    write(sys.argv[1:] or list(PALETTES))
