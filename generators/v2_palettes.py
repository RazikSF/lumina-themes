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

from oklch import contrast, to_hex, fit_chroma

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
    s.update({k: (v[0] if dark else v[1]) if isinstance(v, tuple) else v for k, v in (sig or {}).items()})
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
        ld = SCHEMAS[flavor]["lead"]
        modes = spec["flavors"].setdefault(flavor, {})
        extra = {name: (src, {**pal[src], **over}) for name, (src, over) in pal.get("variants", {}).items()}
        for mode, (src, base) in {"dark": ("dark", pal["dark"]), "light": ("light", pal["light"]), **extra}.items():
            dark = src == "dark"
            lead = ld[src] if isinstance(ld, dict) else ld
            refs = pal.get("refs_dark", pal["refs"]) if dark else pal["refs"]
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
                for k, r in refs.items():
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
DEFAULT_HUES = {"red": ("rose", "crimson"), "orange": ("orange", "orange"), "yellow": ("amber", "amber"), "green": ("emerald", "grass"),
                "teal": ("teal", "teal"), "cyan": ("sky", "sky"), "blue": ("indigo", "indigo"), "violet": ("violet", "violet"),
                "magenta": ("fuchsia", "crimson")}
SIG = {"halo": (.10, .12), "halo2": (.16, .18), "region": .26, "glow": .45, "overlay": (.05, .04)}


def compose(ground, lamp, roles, hues=None, text=(.78, .40), cap=(.13, .16), band=((.79, .85), (.50, .53)),
            commentary=None, variants=None, extra=None, paper=None, roles_dark=None, sig=None):
    """Build a flavor from public scales.

    ground   (hue, chroma dark, chroma light, L dark, L light)
    lamp     the slot that carries the lamp: one step lighter and more saturated than the band
    red      reserved for errors: crimson, one step darker and more saturated than the band
    roles    {"functions", "keywords", "type", "strings", "constants", "builtin", "methods"} -> slot
    hues     slot -> (Tailwind hue, Radix hue); defaults in DEFAULT_HUES; may add "spark"
    paper    (hue, chroma, L) of the light paper when it differs from the ground (Radix light step 2)
    lamp     may be a (dark, light) pair; roles_dark overrides roles for the dark side; sig overrides SIG per flavor
    """
    lamp_d, lamp_l = lamp if isinstance(lamp, tuple) else (lamp, lamp)
    roles_d = roles_dark or roles
    h, cd, cl, Ld, Ll = ground
    hl, cl, Ll = paper or (h, cl, Ll)
    hues = {**DEFAULT_HUES, **(hues or {})}
    dark = {**field(True, h, cd, bg=Ld, fg=text[0]), **diffs(True)}
    light = {**field(False, hl, cl, bg=Ll, fg=text[1]), **diffs(False)}
    for k in ("bg-alt", "base1", "base2", "base3", "surface"):
        L_, C_, h_ = light[k]; light[k] = (L_, min(C_, .02), h_)
    for slot, (twn, rxn) in hues.items():
        for pal, table, i in ((dark, TW300, 0), (light, RX11, 1)):
            L, C, hh = table[twn if i == 0 else rxn]
            if slot == (lamp_d, lamp_l)[i]:
                L, C = (max(L, band[0][1] + .02), max(C, cap[0] + .01)) if i == 0 else (min(L, band[1][0] - .02), max(C, cap[1] + .02))
            elif slot == "red":
                L, C = (band[0][0] - .01, cap[0] + .02) if i == 0 else (band[1][0] - .02, cap[1] + .03)
            else:
                L = min(max(L, band[i][0]), band[i][1]); C = min(C, cap[i])
            pal[slot] = (L, fit_chroma(L, C, hh), hh)
    dark["comments"] = (.61, min(cd * 1.1, .05), h); dark["doc-comments"] = (.67, min(cd * 1.1, .05), h)
    light["comments"] = (.54, max(cl * 2, .012), hl); light["doc-comments"] = (.47, max(cl * 2, .014), hl)
    for pal, over in ((dark, (extra or {}).get("dark", {})), (light, (extra or {}).get("light", {}))):
        pal.update(over)
    dark["dark-blue"] = (dark["blue"][0] - .14, dark["blue"][1], dark["blue"][2]); dark["dark-cyan"] = (dark["cyan"][0] - .14, dark["cyan"][1], dark["cyan"][2])
    light["dark-blue"] = (light["blue"][0] - .10, light["blue"][1], light["blue"][2]); light["dark-cyan"] = (light["cyan"][0] - .10, light["cyan"][1], light["cyan"][2])
    def mkrefs(lp, rl):
        return {"grey": "base5", "highlight": lp, "vertical-bar": "base3", "operators": "base6", "variables": "fg",
                "error": "red", "warning": "orange", "success": "green", "vc-modified": "yellow", "vc-added": "green", "vc-deleted": "red",
                "numbers": rl["constants"], **rl}
    out = {"dark": dark, "light": light, "sig": {**SIG, **(sig or {})}, "refs": mkrefs(lamp_l, roles), "refs_dark": mkrefs(lamp_d, roles_d),
           "commentary": commentary or {}}
    if variants:
        out["variants"] = variants
    return out


VESPER_DARK = {"blue": (.68, .13, 258), "magenta": (.68, .15, 318), "cyan": (.76, .10, 215), "yellow": (.84, .10, 95), "orange": (.71, .15, 34), "rose": (.74, .12, 350),
               "red": (.63, .19, 14), "violet": (.68, .11, 300), "green": (.72, .08, 150), "teal": (.72, .08, 185),
               "fg": (.76, .045, 272), "base8": (.76, .045, 272), "fg-alt": (.66, .04, 272), "comments": (.50, .02, 265), "doc-comments": (.55, .02, 265)}
VESPER_LIGHT = {"blue": (.50, .15, 258), "magenta": (.50, .16, 318), "cyan": (.50, .11, 215), "yellow": (.54, .13, 72), "orange": (.54, .16, 34), "rose": (.52, .16, 350),
                "red": (.42, .19, 10), "violet": (.50, .13, 300), "green": (.50, .12, 150), "teal": (.50, .10, 185)}
SIENNE_DARK = {"teal": (.70, .09, 205), "magenta": (.70, .11, 322), "yellow": (.82, .11, 88), "green": (.74, .11, 116), "coral": (.72, .15, 28), "orange": (.77, .15, 62),
               "red": (.62, .20, 12), "cyan": (.72, .08, 230), "blue": (.68, .08, 250), "violet": (.68, .10, 300),
               "fg": (.80, .025, 70), "base8": (.80, .025, 70), "fg-alt": (.70, .0225, 70), "comments": (.51, .015, 262), "doc-comments": (.56, .02, 262)}
SIENNE_LIGHT = {"teal": (.50, .11, 205), "magenta": (.50, .14, 322), "yellow": (.47, .12, 80), "green": (.52, .11, 118), "coral": (.50, .17, 34), "orange": (.55, .14, 64),
                "red": (.42, .19, 0), "cyan": (.50, .10, 230), "blue": (.50, .12, 250), "violet": (.50, .13, 300)}

UI_COOL = {"red": (.64, .17, 15), "green": (.72, .08, 150), "teal": (.72, .08, 185), "cyan": (.74, .08, 220), "blue": (.70, .10, 255), "violet": (.72, .09, 300), "magenta": (.72, .11, 320), "yellow": (.82, .08, 85), "orange": (.78, .09, 52)}
INDIGO_DARK = {**UI_COOL, "blue": (.72, .14, 255),
               "fg": (.80, .045, 75), "base8": (.80, .045, 75), "fg-alt": (.70, .045, 75), "comments": (.56, .03, 270), "doc-comments": (.60, .03, 270),
               "ink-light": (.88, .06, 72), "ink-mid": (.76, .065, 70), "ink-dim": (.66, .06, 62)}
INDIGO_LIGHT = {"blue": (.50, .16, 255), "fg": (.40, .02, 75), "base8": (.40, .02, 75), "fg-alt": (.51, .02, 75),
                "ink-light": (.30, .06, 72), "ink-mid": (.46, .05, 70), "ink-dim": (.55, .05, 62)}
AZUR_DARK = {**UI_COOL, "red": (.62, .19, 10), "blue": (.72, .15, 253), "yellow": (.83, .08, 92), "orange": (.78, .11, 45), "violet": (.78, .11, 300), "coral": (.72, .15, 22), "cyan": (.78, .09, 205),
             "fg": (.82, .03, 255), "base8": (.82, .03, 255), "fg-alt": (.72, .03, 255), "comments": (.55, .02, 255), "doc-comments": (.59, .02, 255)}
AZUR_LIGHT = {"blue": (.50, .16, 253), "yellow": (.46, .12, 80), "orange": (.52, .13, 48), "violet": (.50, .14, 300), "coral": (.46, .17, 22), "cyan": (.48, .10, 205),
              "red": (.38, .20, 350), "green": (.50, .12, 150), "teal": (.48, .10, 185), "magenta": (.50, .14, 330)}


FLAVORS = {
    "vesper": dict(ground=(265, .028, .004, .22, .985), lamp="blue", paper=(271.3, 0.0083, 0.982), text=(.76, .40),
                      roles=dict(functions="blue", keywords="magenta", type="cyan", strings="yellow", constants="orange", builtin="rose", methods="blue"),
                      extra={"dark": VESPER_DARK, "light": VESPER_LIGHT},
                      sig={"halo": (.07, .12), "halo2": (.14, .18), "region": (.24, .26), "glow": (.42, .45)},
                      commentary={"dark": "Lumina Vesper, dark variant.\nDeep navy at night; blue-lavender text at 8:1, deep accents below it: blue functions, purple keywords, sky types, straw strings, coral constants, rose builtins; no green in the code.",
                                  "light": "Lumina Vesper, light variant.\nCool white paper; the same inks as the night, darkened: blue functions, purple keywords, sky types, straw strings, coral constants, rose builtins; no green in the code."}),
    "sienne": dict(ground=(262, .030, .006, .24, .984), lamp="teal", text=(.80, .40),
                      roles=dict(functions="teal", keywords="magenta", type="yellow", strings="green", constants="coral", builtin="orange", methods="teal"),
                      extra={"dark": SIENNE_DARK, "light": SIENNE_LIGHT},
                      sig={"halo": (.07, .12), "halo2": (.14, .18), "region": (.24, .26), "glow": (.42, .45)},
                      commentary={"dark": "Lumina Sienne, dark variant.\nSlate night under warm inks: beige text at 9:1 above every accent, teal functions, mauve keywords, gold types, olive strings, coral constants, apricot builtins.",
                                  "light": "Lumina Sienne, light variant.\nSlate paper; the same hues as inks: teal functions, mauve keywords, amber types, olive strings, coral constants, apricot builtins."}),
    "dawn": dict(ground=(56.0, 0.006, .010, 0.216, .975), lamp="yellow", paper=(99.1, 0.0238, 0.986),
                    roles=dict(functions="yellow", keywords="teal", type="blue", strings="cyan", constants="magenta", builtin="blue", methods="blue"),
                    hues={"magenta": ("fuchsia", "plum")},
                    commentary={"dark": "Lumina Dawn, dark variant.\nWarm sepia room lit by one amber lamp; terracotta keywords, teal types, lime strings, rose constants, soft text.",
                                "light": "Lumina Dawn, light variant.\nWarm paper under the same amber lamp; terracotta, teal, lime and crimson inks, soft text."}),
    "oxblood": dict(ground=(3.6, 0.015, .012, 0.208, .975), lamp="magenta", paper=(8.5, 0.0087, 0.983),
                       roles=dict(functions="magenta", keywords="blue", type="orange", strings="green", constants="teal", builtin="cyan", methods="cyan"),
                       hues={"magenta": ("fuchsia", "plum"), "green": ("lime", "lime")},
                       commentary={"dark": "Lumina Oxblood, dark variant.\nA theatre after the curtain falls; a rose spotlight on oxblood velvet, violet keywords, amber types, soft text.",
                                   "light": "Lumina Oxblood, light variant.\nBlush paper under the same rose spotlight; crimson, violet and amber inks, soft text."}),
    "tide": dict(ground=(257.5, 0.029, .006, 0.216, .985), lamp="cyan", paper=(219.6, 0.0103, 0.979),
                    roles=dict(functions="cyan", keywords="teal", type="violet", strings="green", constants="orange", builtin="violet", methods="violet"),
                    hues={"green": ("lime", "lime")}, cap=(.10, .14), extra={"dark": {"cyan": (.78, .14, 230)}},
                    commentary={"dark": "Lumina Tide, dark variant.\nDeep ocean at night; a sky-blue lamp lit from within, teal keywords, indigo types, soft text, one amber note.",
                                "light": "Lumina Tide, light variant.\nSea-washed paper; the same sky lamp as a deep ink, teal and indigo beside it, one amber note."}),
    "canopy": dict(ground=(149.9, 0.013, .006, 0.21, .98), lamp="green", paper=(145.5, 0.0101, 0.982),
                      roles=dict(functions="green", keywords="blue", type="yellow", strings="cyan", constants="magenta", builtin="yellow", methods="yellow"),
                      hues={"green": ("green", "grass"), "magenta": ("fuchsia", "plum")},
                      commentary={"dark": "Lumina Canopy, dark variant.\nPine forest at noon; the lamp is leaf-filtered sun, teal keywords, amber types, sky strings, soft text.",
                                  "light": "Lumina Canopy, light variant.\nMoss-white paper; the same green light as a deep ink, teal, amber and sky inks, soft text."}),
    "slate": dict(ground=(285.9, 0.006, .003, 0.21, .985), lamp="blue", paper=(286.4, 0.0026, 0.983),
                     roles=dict(functions="blue", keywords="cyan", type="yellow", strings="green", constants="magenta", builtin="cyan", methods="yellow"),
                      hues={"magenta": ("fuchsia", "plum")},
                     cap=(.10, .14), extra={"dark": {"blue": (.78, .13, 275)}},
                     commentary={"dark": "Lumina Slate, dark variant.\nCold graphite; one steel-blue lamp, every other accent held back to a whisper, soft text.",
                                 "light": "Lumina Slate, light variant.\nCold white paper; the same steel-blue ink, every other accent held back, soft text."}),
    "indigo": dict(ground=(278, .030, .008, .21, .984), lamp="blue", text=(.80, .40),
                      roles=dict(functions="ink-light", keywords="blue", type="ink-mid", strings="ink-dim", constants="ink-light", builtin="ink-mid", methods="ink-light"),
                      extra={"dark": INDIGO_DARK, "light": INDIGO_LIGHT},
                      sig={"halo": (.07, .12), "halo2": (.14, .18), "region": (.24, .26), "glow": (.42, .45)},
                      commentary={"dark": "Lumina Indigo, dark variant.\nIndigo night, one azure for the keywords, everything else in tints of sand: cream functions and constants, sand types and builtins, tan strings, sand text.",
                                  "light": "Lumina Indigo, light variant.\nLavender-white paper, the same azure for the keywords, umber inks for the rest."}),
    "azur": dict(ground=(255, .022, .006, .235, .984), lamp="blue", text=(.82, .40),
                    roles=dict(functions="orange", keywords="blue", type="violet", strings="yellow", constants="coral", builtin="cyan", methods="orange"),
                    extra={"dark": AZUR_DARK, "light": AZUR_LIGHT},
                    sig={"halo": (.07, .12), "halo2": (.14, .18), "region": (.24, .26), "glow": (.42, .45)},
                    commentary={"dark": "Lumina Azur, dark variant.\nBlue slate; Monoink's azure on the keywords and five companions: peach functions, straw strings, coral constants, lilac types, aqua builtins, blue-grey text.",
                                "light": "Lumina Azur, light variant.\nCool paper; the same hues as inks: azure keywords, rust functions, amber strings, coral constants, violet types, teal builtins."}),
    "nocturne": dict(ground=(266.4, 0.042, .008, 0.208, .98), lamp="orange", paper=(271.3, 0.0083, 0.982),
                        roles=dict(functions="orange", keywords="blue", type="cyan", strings="green", constants="magenta", builtin="cyan", methods="cyan"),
                        hues={"magenta": ("fuchsia", "plum")},
                        commentary={"dark": "Lumina Nocturne, dark variant.\nA city at night under an indigo sky; one sodium streetlamp, neon violet keywords, sky types, soft text.",
                                    "light": "Lumina Nocturne, light variant.\nMoonlit blue-white paper under the same sodium lamp; violet, sky and jade inks, soft text."}),
    "amethyst": dict(ground=(326.6, 0.032, .010, 0.21, .98), lamp="yellow", paper=(325.7, 0.0101, 0.982),
                        roles=dict(functions="yellow", keywords="magenta", type="cyan", strings="green", constants="blue", builtin="cyan", methods="cyan"),
                        hues={"magenta": ("fuchsia", "plum")},
                        commentary={"dark": "Lumina Amethyst, dark variant.\nInside a split amethyst geode; one shard of citrine catching the light, orchid keywords, ice-blue types, soft text.",
                                    "light": "Lumina Amethyst, light variant.\nLilac paper under the same citrine light; plum, sky and jade inks, soft text."}),
    "prisma": dict(ground=(286.6, 0.029, .005, 0.209, .985), lamp="spark", paper=(286.2, 0.0093, 0.981),
                      roles=dict(functions="spark", keywords="cyan", type="orange", strings="green", constants="teal", builtin="teal", methods="orange"),
                      hues={"spark": ("purple", "purple"), "green": ("lime", "lime")},
                      commentary={"dark": "Lumina Prisma, dark variant.\nBlack light: the lamp is ultraviolet, the definitions fluoresce in it, and the code is a full spectrum at equal weight.",
                                  "dark-ink": "Lumina Prisma, dark ink variant.\nBlack and white: a single white ray enters a glass prism; the ray is the lamp, the code is its spectrum.",
                                  "light": "Lumina Prisma, light variant.\nWhite paper in daylight; the lamp turns ultraviolet and the code is a full spectrum of vivid inks.",
                                  "light-ink": "Lumina Prisma, light ink variant.\nBlack and white: white paper, one lamp of black ink, and the code as a full spectrum of inks."},
                      variants={"dark-ink": ("dark", {"spark": (.97, .015, 95)}), "light-ink": ("light", {"spark": (.26, .03, 280)})}),
}
PALETTES = {k: compose(**v) for k, v in FLAVORS.items()}


if __name__ == "__main__":
    write(sys.argv[1:] or list(PALETTES))
