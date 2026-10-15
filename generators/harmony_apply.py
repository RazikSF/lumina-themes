"""Six-ink harmony (generators/harmony.json) applied to the flavor definitions and schemas.

Each flavor in harmony.json carries one ink per code role, dark and light, in OKLCH. An ink goes to the
colour slot that matches its hue (red stays reserved for errors); the role map and the schema slots that
follow the roles (lead, preprocessor, escape, rainbow, outline, orderless, magit, org) are rebuilt from it.
"""
import json
from pathlib import Path

HARMONY = json.loads((Path(__file__).resolve().parent / "harmony.json").read_text())
ROLES = ["keywords", "strings", "type", "builtin", "constants", "functions"]
SECTORS = [("magenta", 330, 15), ("orange", 15, 60), ("yellow", 60, 100), ("green", 100, 160), ("teal", 160, 195),
           ("cyan", 195, 235), ("blue", 235, 275), ("violet", 275, 330)]
ORDER = [s for s, _, _ in SECTORS]


def _in(h, a, b):
    return (a <= h < b) if a < b else (h >= a or h < b)


def _centre(a, b):
    return ((a + ((b - a) % 360) / 2) % 360)


def slots(flavor):
    """Role -> slot, unique, by hue; a clash moves the ink to the nearest free neighbouring slot."""
    inks = HARMONY[flavor]["dark"]
    taken, out = set(), {}
    for r in sorted(ROLES, key=lambda r: inks[r][2]):
        h = inks[r][2]
        ranked = sorted(SECTORS, key=lambda s: 0 if _in(h, s[1], s[2]) else min(abs((h - _centre(s[1], s[2]) + 180) % 360 - 180), 360))
        for name, _, _ in ranked:
            if name not in taken:
                out[r] = name; taken.add(name); break
    if flavor == "prisma":
        out["functions"] = "spark"
    return out


def flavor_overrides(flavor):
    """roles, lamp and the per-mode slot overrides for compose()."""
    sl = slots(flavor)
    extra = {mode: {sl[r]: tuple(HARMONY[flavor][mode][r]) for r in ROLES} for mode in ("dark", "light") if mode in HARMONY[flavor]}
    for mode, red in HARMONY[flavor].get("red", {}).items():
        extra.setdefault(mode, {})["red"] = tuple(red)
    roles = {"functions": sl["functions"], "keywords": sl["keywords"], "type": sl["type"], "strings": sl["strings"],
             "constants": sl["constants"], "builtin": sl["builtin"], "methods": "fg"}
    return roles, sl["functions"], extra


def schema_overrides(flavor):
    sl = slots(flavor)
    by_hue = [sl[r] for r in sorted(ROLES, key=lambda r: HARMONY[flavor]["dark"][r][2])]
    return {"lead": sl["functions"], "function_call": "fg", "property": "fg", "preprocessor": sl["keywords"],
            "escape": sl["constants"], "rainbow": by_hue, "outline": [sl["functions"], sl["keywords"], sl["type"], sl["strings"]],
            "orderless": [sl["keywords"], sl["functions"], sl["constants"]], "magit_branch_local": sl["keywords"],
            "magit_branch_remote": sl["strings"], "org_todo": sl["functions"], "org_done": sl["strings"],
            "role_inks": True}


SEMIBOLD = {f: {"weight": "semi-bold"} for f in ("font-lock-keyword-face", "font-lock-type-face", "font-lock-function-name-face")}


def gemini_design(flavor):
    """Gemini's face design: calls in the function ink, properties and escapes in the builtin ink, the
    preprocessor in the keyword ink, grey brackets, semi-bold keywords, types and definitions."""
    sl = slots(flavor)
    return {"function_call": sl["functions"], "property": sl["builtin"], "preprocessor": sl["keywords"], "escape": sl["builtin"],
            "rainbow": ["base6"] * 6, "faces": {"dark": SEMIBOLD, "light": SEMIBOLD}}


AS_DRAWN = {"fg_max": {"dark": 17, "light": 12.5}, "comments_min": {"dark": 3.8, "light": 4.3}}  # Gemini's drafts: brighter text, softer comments


NAMES = [(20, "rose"), (45, "salmon"), (65, "apricot"), (92, "gold"), (115, "straw"), (138, "lime"), (160, "sage"),
         (200, "mint"), (250, "sky"), (275, "periwinkle"), (305, "lilac"), (335, "orchid"), (361, "pink")]


def hue_name(h, light=False):
    for limit, name in NAMES:
        if h < limit:
            if light:
                return {"gold": "amber", "straw": "amber", "apricot": "rust", "salmon": "brick", "mint": "teal", "sage": "jade",
                        "sky": "blue", "periwinkle": "indigo", "lilac": "violet", "orchid": "plum", "pink": "crimson"}.get(name, name)
            return name
    return "pink"


SCENES = {
    "dawn": ("Warm sepia room", "Warm paper"), "oxblood": ("A theatre after the curtain falls, oxblood velvet", "Blush programme paper"),
    "tide": ("Deep ocean at night", "Sea-washed paper"), "canopy": ("Pine forest at noon", "Moss-white paper"),
    "slate": ("Cold graphite", "Cold white paper"), "nocturne": ("A city at night under an indigo sky", "Moonlit blue-white paper"),
    "amethyst": ("Inside a split amethyst geode", "Lilac paper"), "prisma": ("Neutral night, the full spectrum", "White paper, the full spectrum"),
    "indigo": ("Indigo night", "Lavender-white paper"), "azur": ("Blue slate under a clear sky, vivid", "Cool paper, vivid inks"),
    "sirocco": ("Desert wind at dusk over terracotta", "Sand paper"), "celadon": ("Glazed jade porcelain", "Pale celadon paper"),
    "sumi": ("Ink-black ground", "Rice paper"), "aquarelle": ("The slide palette rearranged, slate night", "Cool paper, the same inks"),
    "jardin": ("The slide palette with mint keywords, slate night", "Cool paper, the same inks"), "pivoine": ("A soft dusk of peony petals, lighter than the night grounds", "Blush paper"),
    "neon-cyber": ("Urban night in neon, every ink at full voltage", "Cool white paper, the same neon as deep inks"),
    "borealis": ("Misty pine forest under the aurora", "Frosted white paper"),
    "cashmere": ("Espresso velvet, warm pastels", "Warm linen paper"),
    "aethelgard": ("Midnight velvet and astral gold", "Cool marble paper"),
    "sakura": ("Twilight plum night under cherry blossom", "Blossom-white paper"),
}


def commentary(flavor, old):
    """Scene of the flavor, then its six inks by role."""
    out = {}
    for mode in ("dark", "light"):
        title, _, rest = old.get(mode, "").partition("\n")
        scene = SCENES[flavor][0 if mode == "dark" else 1]
        inks = HARMONY[flavor][mode]
        part = ", ".join(f"{hue_name(inks[r][2], mode == 'light')} {n}" for r, n in
                         (("keywords", "keywords"), ("functions", "functions"), ("type", "types"), ("strings", "strings"),
                          ("constants", "constants"), ("builtin", "builtins")))
        out[mode] = f"{title}\n{scene}; {part}: six inks of one weight."
    for k, v in old.items():
        if k not in out:
            out[k] = v
    return out
