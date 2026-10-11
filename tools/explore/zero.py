"""Dark from scratch: two poles rendered beside the references the user named.

  froid  Open Color gray-9 ground, light grey text, vivid mid accents (Dracula register)
  chaud  warm stone ground, cream text, earthy saturated accents (Gruvbox register)

Usage: python3 tools/explore/zero.py  -> docs/zero.html, prototypes lumina-froid0-dark / lumina-chaud0-dark in Doom
"""
import json, os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "generators")); sys.path.insert(0, str(ROOT / "tools/explore"))
from oklch import from_hex, to_hex, contrast
import v2_palettes as vp
import lumina_gen as g
import explore

OC = json.loads((ROOT / "tools/explore/sources.json").read_text())["open-color"]
DOOM = Path.home() / ".config/emacs/.local/straight/build-30.2/doom-themes"


def oc(name, step):
    return from_hex(OC[name][step])


def tw(n, s):
    import re
    v = json.loads((ROOT / "tools/explore/sources.json").read_text())["tailwind"][n][str(s)]
    L, C, h = re.match(r"oklch\(([\d.]+)% ([\d.]+) ([\d.]+|none)\)", v).groups()
    return (float(L) / 100, float(C), 0.0 if h == "none" else float(h))


def mute(c, C):
    return (c[0], min(c[1], C), c[2])


# Recipe measured on the 34 references: ground L .24, text L .88 (11:1) above every accent,
# accents staged .66-.84 with keywords the most saturated and types the lightest, comments ~3.5:1.
# Hue vocabulary measured on the references, role by role (median L, C, h):
#   strings green-yellow (.77, .12, 128), types gold (.83, .13, 86), functions blue (.72, .13, 260),
#   constants orange (.74, .14, 51), keywords the most saturated role, purple-magenta (.72, .15, 318),
#   builtin orange like constants, error red deeper (.64, .20, 25); five hues, text .88 above them all.
# Soft-text sub-group of the references (One 7.8, Tokyo Night 8.1, Darcula 6.9, Jazz 7.9): text ~8.5:1
# and every accent darker than the text, deep and calm (L .62-.78, C .10-.15); hue vocabulary of vesper5.
ACC = {"blue": (.68, .13, 258), "magenta": (.68, .15, 318), "green": (.72, .11, 128), "yellow": (.78, .12, 88), "orange": (.70, .13, 52),
       "red": (.62, .18, 25), "violet": (.68, .11, 300), "teal": (.72, .09, 175), "cyan": (.72, .10, 212)}
ROLES6 = dict(functions="blue", keywords="magenta", type="yellow", strings="green", constants="orange", builtin="orange", methods="blue")
def shift(acc, dL=0.0, dC=0.0):
    return {k: ((v[0] + dL, v[1] + dC, v[2]) if k in ACC else v) for k, v in acc.items()}


G = (265, .025, .004, .24, .985); CM = {"comments": (.52, .02, 265), "doc-comments": (.57, .02, 265)}
LAV = {"fg": (.83, .03, 285), "base8": (.83, .03, 285), "fg-alt": (.73, .03, 285)}
CAT = {"fg": (.86, .03, 280), "base8": (.86, .03, 280), "fg-alt": (.76, .03, 280)}
# Lesson: the plain text (variables) must be TINTED, never grey-white: Jazz #c6a57b (L .74, C .07), Catppuccin #cdd6f4 (C .03).
# Warm pole, measured on the five warm references the user likes (Rouge, Manegarm, Miramare, uwu, Tomorrow Night):
# near-neutral ground L .20-.27, accents L .63-.85 and C .07-.19, vocabulary coral-red 16-28, apricot 45-58, gold 83-89,
# olive-sage 113-152, mauve 307-348, one teal 219-244; three of the five colour variables coral-red.  Round 9 (L .60-.72) was "too dark":
# round 10 lifts every accent to L .68-.80 and the sand text to L .80 so that it stays above the accents.
WARM_UI = {"red": (.64, .18, 15), "orange": (.74, .14, 52), "yellow": (.80, .11, 84), "green": (.74, .10, 120), "teal": (.70, .09, 190),
           "cyan": (.70, .09, 215), "blue": (.68, .08, 250), "violet": (.68, .10, 300), "magenta": (.70, .11, 330),
           "fg": (.80, .045, 70), "base8": (.80, .045, 70), "fg-alt": (.70, .04, 70), "comments": (.48, .015, 60), "doc-comments": (.53, .02, 65)}
WARM_G = (40, .006, .010, .21, .975)
COLD = {
    "vesper8": dict(base="vesper", ground=(265, .028, .004, .22, .985), text=(.76, .40),
                    accents={**ACC, "fg": (.76, .045, 272), "base8": (.76, .045, 272), "fg-alt": (.66, .04, 272), "comments": (.50, .02, 265), "doc-comments": (.55, .02, 265)},
                    roles={**ROLES6, "builtin": "cyan", "methods": "cyan"}, label="constantes orange #DD854C, builtins ciel sourd #4BB5C9"),
}
PROTOS = {
    "rouge10": dict(base="dawn", ground=WARM_G, text=(.80, .40),
                    accents={**WARM_UI, "salmon": (.80, .10, 32), "coral": (.70, .14, 18), "rose": (.70, .14, 358), "mauve": (.70, .10, 326), "sage": (.76, .07, 135)},
                    roles=dict(functions="salmon", keywords="mauve", type="coral", strings="sage", constants="coral", builtin="rose", methods="salmon"),
                    label="chaud A, registre Rouge, plus clair : fonctions saumon, types et constantes corail, builtins rose, chaînes sauge, mots-clés mauve"),
    "sienne10": dict(base="dawn", ground=WARM_G, text=(.80, .40),
                     accents={**WARM_UI, "coral": (.72, .15, 28), "mauve": (.70, .11, 322), "gold": (.80, .11, 84), "olive": (.76, .11, 112), "apricot": (.74, .14, 54), "teal": (.70, .09, 205)},
                     roles=dict(functions="coral", keywords="mauve", type="gold", strings="olive", constants="apricot", builtin="teal", methods="coral"),
                     label="chaud B, six teintes, plus clair : fonctions corail, mots-clés mauve, types or, chaînes olive, constantes abricot, builtins sarcelle"),
    "sienne10v": dict(base="dawn", ground=WARM_G, text=(.80, .40),
                      accents={**WARM_UI, "coral": (.68, .15, 22), "sage": (.76, .09, 150), "mauve": (.70, .11, 322), "gold": (.80, .11, 84), "olive": (.76, .11, 112), "apricot": (.74, .14, 54), "teal": (.70, .09, 205)},
                      roles=dict(functions="sage", keywords="mauve", type="gold", strings="olive", constants="apricot", builtin="teal", methods="sage", variables="coral"),
                      label="chaud B', variables corail comme Rouge, uwu et Tomorrow : fonctions sauge, mots-clés mauve, types or, chaînes olive, constantes abricot, builtins sarcelle"),
    "ocre10": dict(base="dawn", ground=WARM_G, text=(.80, .40),
                   accents={**WARM_UI, "apricot": (.76, .16, 50), "coral": (.68, .17, 28), "chartreuse": (.74, .14, 125), "gold": (.80, .11, 86), "mauve": (.70, .11, 330), "teal": (.70, .09, 205)},
                   roles=dict(functions="apricot", keywords="coral", type="chartreuse", strings="gold", constants="mauve", builtin="teal", methods="apricot"),
                   label="chaud C, registre Manegarm, plus clair : lampe abricot, mots-clés corail, types chartreuse, chaînes or, constantes mauve, builtins sarcelle"),
}
# Round 11: the user keeps the sienne10 colour set but rejects its role assignment and the warm near-black ground.
# Same six colours, four assignments (lamp gold / teal / apricot / mauve) on a neutral ground, and the teal-lamp assignment on three grounds
# measured on the references: neutral (Jazz, Tomorrow Night), slate (Rouge), blue-grey mist (uwu).
SIENNE = {"coral": (.72, .15, 28), "mauve": (.70, .11, 322), "gold": (.80, .11, 84), "olive": (.76, .11, 112), "apricot": (.74, .14, 54), "teal": (.70, .09, 205)}
G_NEUTRE = (0, .002, .010, .22, .975); G_ARDOISE = (262, .030, .010, .24, .975); G_BRUME = (240, .010, .010, .22, .975)
def sienne(ground, roles, label, cm=60):
    acc = {**WARM_UI, **SIENNE, "comments": (.50, .015, cm), "doc-comments": (.55, .02, cm)}
    return dict(base="dawn", ground=ground, text=(.80, .40), accents=acc, roles=roles, label=label)
A_OR = dict(functions="gold", keywords="coral", type="teal", strings="olive", constants="apricot", builtin="mauve", methods="gold")
A_SARCELLE = dict(functions="teal", keywords="mauve", type="gold", strings="olive", constants="coral", builtin="apricot", methods="teal")
A_ABRICOT = dict(functions="apricot", keywords="mauve", type="teal", strings="olive", constants="coral", builtin="gold", methods="apricot")
A_MAUVE = dict(functions="mauve", keywords="coral", type="gold", strings="olive", constants="teal", builtin="apricot", methods="mauve")
SIENNE11 = {
    "sienne11-or": sienne(G_NEUTRE, A_OR, "affectation 1, fond neutre : fonctions or, mots-clés corail, types sarcelle, chaînes olive, constantes abricot, builtins mauve"),
    "sienne11-neutre": sienne(G_NEUTRE, A_SARCELLE, "affectation 2, fond neutre 0,22 : fonctions sarcelle, mots-clés mauve, types or, chaînes olive, constantes corail, builtins abricot"),
    "sienne11-abricot": sienne(G_NEUTRE, A_ABRICOT, "affectation 3, fond neutre : fonctions abricot, mots-clés mauve, types sarcelle, chaînes olive, constantes corail, builtins or"),
    "sienne11-mauve": sienne(G_NEUTRE, A_MAUVE, "affectation 4, fond neutre : fonctions mauve, mots-clés corail, types or, chaînes olive, constantes sarcelle, builtins abricot"),
    "sienne11-ardoise": sienne(G_ARDOISE, A_SARCELLE, "affectation 2, fond ardoise 0,24 (comme Rouge)", cm=262),
    "sienne11-brume": sienne(G_BRUME, A_SARCELLE, "affectation 2, fond gris-bleu 0,22 (comme uwu, Tomorrow Night)", cm=240),
}
# Round 12: assignment 2 (teal lamp) on the slate and mist grounds; the sand text (#D1B99F, C .045) reads yellowish on a cool ground,
# so three quieter text tones: muted beige (C .025), warm grey (C .012), rosy beige (C .028, hue 45).
TEXTES = {"beige": (.80, .025, 70), "gris": (.80, .012, 60), "rose": (.80, .028, 45)}
def sienne12(ground, cm, tk):
    pr = sienne(ground, A_SARCELLE, "", cm=cm)
    L, C, h = TEXTES[tk]
    pr["accents"] = {**pr["accents"], "fg": (L, C, h), "base8": (L, C, h), "fg-alt": (L - .10, C * .9, h)}
    pr["label"] = f"fond {'ardoise' if ground is G_ARDOISE else 'gris-bleu'}, texte {dict(beige='beige discret', gris='gris chaud', rose='beige rosé')[tk]} (chroma {C:.3f})"
    return pr
SIENNE12 = {f"sienne12-{g}-{t}": sienne12(gr, cm, t) for g, gr, cm in (("ardoise", G_ARDOISE, 262), ("brume", G_BRUME, 240)) for t in TEXTES}
# Vesper strings: on real NSI Python the olive green (.72, .11, 128) "does not fit"; four replacements in the free arcs of the wheel
# (blue 258, purple 318, gold 88, coral 34, turquoise 172 are taken): bright lime, mint, pale sky, grey sage.
VESPER = vp.FLAVORS["vesper"]
def vesper_strings(name, green, label):
    return dict(base="vesper", ground=VESPER["ground"], text=VESPER["text"], accents={**VESPER["extra"]["dark"], "green": green}, roles=VESPER["roles"], label=label)
STRINGS = {
    "vesper-lime": vesper_strings("vesper-lime", (.82, .13, 118), "chaînes lime clair (comme Gruvbox, Tokyo Night)"),
    "vesper-menthe": vesper_strings("vesper-menthe", (.78, .09, 155), "chaînes menthe"),
    "vesper-ciel": vesper_strings("vesper-ciel", (.80, .08, 228), "chaînes ciel pâle"),
    "vesper-sauge": vesper_strings("vesper-sauge", (.78, .05, 140), "chaînes sauge grise, discrètes"),
}
# Three further palette types, each more restrained than Vesper (six hues): Indigo (three hues on an indigo ground, Monoink's
# ink tones for the rest), Encre (one amber accent on neutral charcoal, Monoink register), Opale (four hues, Horizon register,
# plum-charcoal ground).  Measured: doom-indigo bg (278, .030) L .21, keywords periwinkle 270, strings orange 54; doom-monoink bg (268, .010)
# L .20, one azure 253, strings/types grey L .68-.71, constants light L .88; doom-horizon bg (277, .021) L .27, purple 313, sky 226, peach 48, salmon 30.
UI_COOL = {"red": (.64, .17, 15), "green": (.72, .08, 150), "teal": (.72, .08, 185), "cyan": (.74, .08, 220), "blue": (.70, .10, 255), "violet": (.72, .09, 300), "magenta": (.72, .11, 320), "yellow": (.82, .08, 85), "orange": (.78, .09, 52)}
TROIS = {
    "indigo": dict(base="vesper", ground=(278, .030, .010, .21, .98), text=(.80, .40), lead="blue",
                   accents={**UI_COOL, "blue": (.72, .14, 255), "violet": (.76, .10, 300), "orange": (.80, .08, 52),
                            "fg": (.80, .03, 278), "base8": (.80, .03, 278), "fg-alt": (.70, .03, 278), "comments": (.56, .03, 278), "doc-comments": (.60, .03, 278),
                            "ink-light": (.88, .04, 280), "ink-dim": (.70, .04, 278)},
                   roles=dict(functions="blue", keywords="violet", type="ink-light", strings="orange", constants="ink-dim", builtin="ink-dim", methods="blue"),
                   label="Indigo, trois teintes : fonctions azur, mots-clés lilas, chaînes pêche ; types, constantes et builtins en tons d'encre lavande"),
    "encre": dict(base="slate", ground=(268, .010, .006, .20, .98), text=(.84, .40), lead="yellow",
                  accents={**UI_COOL, "yellow": (.80, .12, 78),
                           "fg": (.84, .012, 268), "base8": (.84, .012, 268), "fg-alt": (.74, .012, 268), "comments": (.54, .012, 268), "doc-comments": (.58, .012, 268),
                           "ink-light": (.92, .01, 268), "ink-mid": (.76, .014, 268), "ink-dim": (.70, .012, 268)},
                  roles=dict(functions="ink-light", keywords="yellow", type="ink-mid", strings="ink-dim", constants="ink-light", builtin="ink-mid", methods="ink-light"),
                  label="Encre, une teinte : mots-clés ambre, tout le reste en encres grises (fonctions et constantes claires, chaînes sombres)"),
    "opale": dict(base="nocturne", ground=(300, .015, .010, .23, .98), text=(.80, .40), lead="cyan",
                  accents={**UI_COOL, "magenta": (.72, .13, 330), "cyan": (.78, .10, 215), "orange": (.80, .10, 60), "red": (.62, .18, 12),
                           "coral": (.72, .14, 30), "aqua-dim": (.66, .10, 215),
                           "fg": (.80, .015, 300), "base8": (.80, .015, 300), "fg-alt": (.70, .015, 300), "comments": (.54, .02, 300), "doc-comments": (.58, .02, 300)},
                  roles=dict(functions="cyan", keywords="magenta", type="aqua-dim", strings="orange", constants="coral", builtin="aqua-dim", methods="cyan"),
                  label="Opale, quatre teintes : fonctions aigue-marine, mots-clés orchidée, chaînes abricot, constantes corail ; types et builtins en aigue-marine sombre"),
}
# Indigo, second round: the Monoink azure must be the keyword colour (def, return, for), everything else in ink tones.
INDIGO_INK = {**UI_COOL, "blue": (.72, .14, 255),
              "fg": (.80, .03, 278), "base8": (.80, .03, 278), "fg-alt": (.70, .03, 278), "comments": (.56, .03, 278), "doc-comments": (.60, .03, 278),
              "ink-light": (.90, .03, 280), "ink-mid": (.74, .035, 278), "ink-dim": (.68, .035, 278)}
INDIGO_ROLES = dict(functions="ink-light", keywords="blue", type="ink-mid", strings="ink-dim", constants="ink-light", builtin="ink-mid", methods="ink-light")
INDIGO2 = {
    "indigo2": dict(base="vesper", ground=(278, .030, .010, .21, .98), text=(.80, .40), lead="blue", accents=INDIGO_INK, roles=INDIGO_ROLES,
                    label="Indigo, une teinte : mots-clés azur (def, return, for), tout le reste en encres lavande, structure d'Encre sur le fond de doom-indigo"),
    "indigo2b": dict(base="vesper", ground=(278, .030, .010, .21, .98), text=(.80, .40), lead="blue", accents={**INDIGO_INK, "orange": (.80, .07, 52)}, roles={**INDIGO_ROLES, "strings": "orange"},
                     label="Indigo, variante à une note chaude : idem, chaînes pêche sourd"),
}
# Third round: no more near-white inks; every tone is a tint or shade of the theme's one hue (monochromatic scheme).
def mono(ground, hue, accent_slot, accent, text, light, mid, dim, cm, extra=None, label=""):
    acc = {**UI_COOL, accent_slot: accent, "fg": text, "base8": text, "fg-alt": (text[0] - .10, text[1], text[2]),
           "comments": cm, "doc-comments": (cm[0] + .04, cm[1], cm[2]), "ink-light": light, "ink-mid": mid, "ink-dim": dim, **(extra or {})}
    roles = dict(functions="ink-light", keywords=accent_slot, type="ink-mid", strings="ink-dim", constants="ink-light", builtin="ink-mid", methods="ink-light")
    return dict(base="vesper", ground=ground, text=(text[0], .40), lead=accent_slot, accents=acc, roles=roles, label=label)
MONO = {
    "indigo3": mono((278, .030, .010, .21, .98), 265, "blue", (.72, .14, 255), text=(.80, .045, 272), light=(.88, .07, 262), mid=(.76, .08, 268), dim=(.68, .07, 262), cm=(.56, .04, 270),
                    label="Indigo, nuances d'indigo : mots-clés azur, fonctions et constantes pervenche clair, types et builtins bleu-lavande, chaînes bleu ardoise, texte lavande"),
    "encre3": mono((75, .006, .006, .20, .98), 78, "yellow", (.80, .12, 78), text=(.84, .025, 80), light=(.90, .05, 85), mid=(.76, .05, 80), dim=(.68, .05, 75), cm=(.54, .02, 78),
                   label="Encre, nuances d'ambre : mots-clés ambre, fonctions et constantes crème, types et builtins sable, chaînes tan, texte beige clair"),
    "encre3b": mono((268, .010, .006, .20, .98), 268, "yellow", (.80, .12, 78), text=(.84, .02, 268), light=(.90, .035, 268), mid=(.76, .04, 268), dim=(.68, .04, 268), cm=(.54, .02, 268),
                    label="Encre, nuances du fond : mots-clés ambre, encres bleu-ardoise claires, moyennes et sombres, texte gris-bleu"),
}
# Fourth round: the ink tones are tints and shades of a COMPANION hue that pairs with the accent (two-hue scheme).
# Azure's companions: sand/peach (complement, Jazz's warm text on cold accents) or mauve (analogous-violet).
# Amber's companions: plum (triad side) or teal-blue 210 (cool complement, kept away from green); slate 268 is already encre3b.
DUO = {
    "indigo4a": mono((278, .030, .010, .21, .98), 265, "blue", (.72, .14, 255), text=(.80, .045, 75), light=(.88, .06, 72), mid=(.76, .065, 70), dim=(.68, .06, 65), cm=(.56, .03, 270),
                     label="Indigo + sable : mots-clés azur, fonctions et constantes crème, types et builtins sable, chaînes tan, texte sable clair"),
    "indigo4b": mono((278, .030, .010, .21, .98), 265, "blue", (.72, .14, 255), text=(.80, .04, 305), light=(.88, .06, 310), mid=(.76, .07, 310), dim=(.68, .07, 312), cm=(.56, .035, 290),
                     label="Indigo + mauve : mots-clés azur, fonctions et constantes mauve clair, types et builtins mauve, chaînes prune, texte lilas gris"),
    "encre4a": mono((300, .010, .006, .20, .98), 300, "yellow", (.80, .12, 78), text=(.84, .025, 320), light=(.90, .04, 320), mid=(.76, .05, 320), dim=(.68, .06, 322), cm=(.54, .02, 300),
                    label="Encre + prune : mots-clés ambre, fonctions et constantes rose pâle, types et builtins vieux rose, chaînes prune, texte rose gris"),
    "encre4b": mono((220, .010, .006, .20, .98), 215, "yellow", (.80, .12, 78), text=(.84, .025, 215), light=(.90, .045, 212), mid=(.76, .06, 210), dim=(.68, .06, 208), cm=(.54, .02, 220),
                    label="Encre + bleu sarcelle : mots-clés ambre, fonctions et constantes bleu glacier, types et builtins bleu-gris, chaînes pétrole, texte bleu pâle"),
}
# Encre, fifth round: amber rejected with every companion; change the single accent instead and give each its natural companion.
ENCRE5 = {
    "encre5a": mono((268, .010, .006, .20, .98), 268, "orange", (.72, .15, 22), text=(.84, .02, 268), light=(.90, .035, 268), mid=(.76, .04, 268), dim=(.68, .04, 268), cm=(.54, .02, 268),
                    label="Encre corail : mots-clés corail, encres bleu-ardoise claires, moyennes et sombres, texte gris-bleu, charbon froid"),
    "encre5b": mono((300, .008, .006, .20, .98), 250, "magenta", (.70, .14, 335), text=(.84, .02, 250), light=(.90, .035, 250), mid=(.76, .04, 250), dim=(.68, .045, 250), cm=(.54, .02, 280),
                    label="Encre orchidée : mots-clés orchidée, encres bleu acier, texte gris-bleu, charbon prune"),
    "encre5c": mono((60, .005, .006, .20, .98), 72, "teal", (.74, .11, 195), text=(.84, .035, 75), light=(.90, .05, 78), mid=(.76, .055, 72), dim=(.68, .055, 68), cm=(.54, .015, 70),
                    label="Encre sarcelle : mots-clés sarcelle, encres crème, sable et tan (le mariage de Jazz), charbon neutre"),
}
# Azur: Monoink's blue (#5BA8FF, .72/.15/253) as the keyword colour on Monoink's charcoal; the companions are its complement family,
# a warm gradient from cream to coral: cream functions, sand types and builtins, peach strings, coral constants, sand text.  Four hues.
AZUR = {
    "azur": dict(base="vesper", ground=(268, .010, .006, .20, .98), text=(.82, .40), lead="blue",
                 accents={**UI_COOL, "blue": (.72, .15, 253), "orange": (.80, .09, 48), "coral": (.72, .14, 24),
                          "fg": (.82, .04, 75), "base8": (.82, .04, 75), "fg-alt": (.72, .04, 75), "comments": (.54, .015, 268), "doc-comments": (.58, .015, 268),
                          "cream": (.90, .05, 82), "sand": (.76, .055, 72)},
                 roles=dict(functions="cream", keywords="blue", type="sand", strings="orange", constants="coral", builtin="sand", methods="cream"),
                 label="Azur : mots-clés bleu Monoink, fonctions crème, types et builtins sable, chaînes pêche, constantes corail, texte sable, charbon de Monoink"),
}
# Azur, full palette: Monoink's blue on the keywords, five companions around it (gold, peach, lilac, coral, aqua), tinted text, Monoink's charcoal.
AZUR6_ACC = {**UI_COOL, "blue": (.72, .15, 253), "yellow": (.84, .11, 88), "orange": (.78, .11, 45), "violet": (.78, .11, 300), "coral": (.72, .15, 22), "cyan": (.78, .09, 205),
             "fg": (.82, .03, 262), "base8": (.82, .03, 262), "fg-alt": (.72, .03, 262), "comments": (.54, .015, 268), "doc-comments": (.58, .015, 268)}
AZUR6 = {
    "azur6a": dict(base="vesper", ground=(268, .010, .006, .20, .98), text=(.82, .40), lead="blue", accents=AZUR6_ACC,
                   roles=dict(functions="yellow", keywords="blue", type="violet", strings="orange", constants="coral", builtin="cyan", methods="yellow"),
                   label="Azur A : mots-clés bleu Monoink, fonctions or, types lilas, chaînes pêche, constantes corail, builtins aigue-marine, texte gris-bleu"),
    "azur6b": dict(base="vesper", ground=(268, .010, .006, .20, .98), text=(.82, .40), lead="blue", accents=AZUR6_ACC,
                   roles=dict(functions="violet", keywords="blue", type="yellow", strings="orange", constants="coral", builtin="cyan", methods="violet"),
                   label="Azur B : mêmes couleurs, fonctions lilas et types or"),
}
# Azur A ground: the Monoink charcoal (268, .010, L .20) is near-black and flat; three blue-tinted grounds, each with comments in the same hue.
AZUR_ROLES = dict(functions="yellow", keywords="blue", type="violet", strings="orange", constants="coral", builtin="cyan", methods="yellow")
def azur_ground(name, ground, label):
    h = ground[0]
    acc = {**AZUR6_ACC, "fg": (.82, .03, h), "base8": (.82, .03, h), "fg-alt": (.72, .03, h), "comments": (.55, .02, h), "doc-comments": (.59, .02, h)}
    return dict(base="vesper", ground=ground, text=(.82, .40), lead="blue", accents=acc, roles=AZUR_ROLES, label=label)
AZUR7 = {
    "azur7-nuit": azur_ground("nuit", (262, .028, .006, .22, .98), "fond nuit (262, .028) clarté 0,22, comme Vesper"),
    "azur7-ardoise": azur_ground("ardoise", (255, .022, .006, .235, .98), "fond ardoise (255, .022) clarté 0,235"),
    "azur7-acier": azur_ground("acier", (240, .016, .006, .25, .98), "fond acier (240, .016) clarté 0,25, le plus clair"),
}
# Azur, straw and peach swapped: peach functions, straw strings.
AZ = vp.FLAVORS["azur"]
AZUR_SWAP = {
    "azur-swap": dict(base="azur", ground=AZ["ground"], text=AZ["text"], lead="blue", accents=AZ["extra"]["dark"],
                      roles={**AZ["roles"], "functions": "orange", "methods": "orange", "strings": "yellow"},
                      label="Azur, paille et pêche inversés : fonctions pêche, chaînes paille"),
}
# Azur, functions in the numbers' coral; the numbers move to a compatible rose.
AZUR_ROSE = {
    "azur-rose": dict(base="azur", ground=AZ["ground"], text=AZ["text"], lead="blue", accents={**AZ["extra"]["dark"], "rose": (.76, .11, 345)},
                      roles={**AZ["roles"], "functions": "coral", "methods": "coral", "strings": "yellow", "constants": "rose"},
                      label="Azur : fonctions corail (l'ancien orange des nombres), nombres et constantes rose, chaînes paille"),
}
# Azur, blue and coral swapped on the rose version: azure functions, coral keywords.
AZUR_INV = {
    "azur-inv": dict(base="azur", ground=AZ["ground"], text=AZ["text"], lead="blue", accents={**AZ["extra"]["dark"], "rose": (.76, .11, 345)},
                     roles={**AZ["roles"], "functions": "blue", "methods": "blue", "keywords": "coral", "strings": "yellow", "constants": "rose"},
                     label="Azur : fonctions bleu Monoink, mots-clés corail, nombres rose, chaînes paille"),
}
SHEETS = {
    "inv": dict(refs=[], protos=AZUR_INV, themes=["lumina-azur-rose-dark"], out="inv.html",
                title="Azur : bleu et corail inversés",
                intro="À gauche fonctions bleu et mots-clés corail ; à droite la version précédente (mots-clés bleu, fonctions corail). Installé sous lumina-azur-inv-dark."),
    "rose": dict(refs=[], protos=AZUR_ROSE, themes=["lumina-azur-swap-dark", "lumina-azur-dark"], out="rose.html",
                 title="Azur : le corail aux fonctions, un rose pour les nombres",
                 intro="Première carte : fonctions corail, constantes et nombres rose, chaînes paille. Puis l'inversion précédente et Azur figé. Installé sous lumina-azur-rose-dark."),
    "swap": dict(refs=[], protos=AZUR_SWAP, themes=["lumina-azur-dark"], out="swap.html",
                 title="Azur : paille et pêche inversés",
                 intro="À gauche l'inversion (fonctions pêche, chaînes paille), à droite Azur tel que figé. Installé sous lumina-azur-swap-dark."),
    "azur7": dict(refs=[], protos=AZUR7, themes=["lumina-azur6a-dark"], out="azur7.html",
                  title="Azur A : trois fonds teintés de bleu",
                  intro="Mêmes couleurs de code qu'Azur A ; seul le fond change, avec le texte et les commentaires accordés à sa teinte. Dernière carte : le charbon Monoink actuel. Installés sous lumina-azur7-nuit, -ardoise, -acier (suffixe -dark) ; azur6b retiré."),
    "azur6": dict(refs=["doom-indigo"], protos=AZUR6, themes=[], out="azur6.html",
                  title="Azur : le bleu de Monoink et cinq compagnes",
                  intro="Un vrai thème : six teintes de code autour du bleu de Monoink, sur son charbon ; texte gris-bleu teinté 10:1 au-dessus des accents. Deux affectations des mêmes couleurs. Installés sous lumina-azur6a-dark et lumina-azur6b-dark ; lumina-azur-dark retiré."),
    "azur": dict(refs=["doom-monoink"], protos=AZUR, themes=["lumina-indigo4a-dark"], out="azur.html",
                 title="Azur : le bleu de Monoink et sa famille complémentaire",
                 intro="Le bleu de Monoink reste seul côté froid ; tout le reste est un dégradé chaud, de la crème au corail, sur le charbon de Monoink. Indigo + sable en dernière carte. Installé sous lumina-azur-dark ; encre5a, 5b, 5c retirés."),
    "encre5": dict(refs=[], protos=ENCRE5, themes=["lumina-indigo4a-dark"], out="encre5.html",
                   title="Encre : trois autres accents, chacun avec sa couleur compagne",
                   intro="L'ambre ne prenait avec aucune compagne ; l'accent change. Corail sur encres bleu-ardoise, orchidée sur encres bleu acier, sarcelle sur encres sable comme Jazz. Indigo + sable en dernière carte pour comparer. Installés sous lumina-encre5a, -encre5b, -encre5c (suffixe -dark) ; encre3b, encre4a, encre4b et indigo4b retirés."),
    "duo": dict(refs=[], protos=DUO, themes=["lumina-encre3b-dark"], out="duo.html",
                title="Indigo et Encre : nuances d'une couleur compagne",
                intro="L'accent reste seul (azur pour Indigo, ambre pour Encre) ; les encres sont des teintes et ombres d'une couleur qui se marie avec lui : sable ou mauve pour l'azur, prune ou bleu sarcelle pour l'ambre, et l'ardoise déjà vue (encre3b). Installés sous lumina-indigo4a, -indigo4b, -encre4a, -encre4b (suffixe -dark) ; indigo3 et encre3 retirés."),
    "mono": dict(refs=["doom-monoink"], protos=MONO, themes=[], out="mono.html",
                 title="Indigo et Encre : nuances de la couleur principale, plus de blanc",
                 intro="Chaque ton est une teinte ou une ombre de la couleur du thème : pervenche, bleu-lavande et bleu ardoise pour Indigo ; crème, sable et tan pour Encre ; une variante d'Encre garde l'ambre seul avec des encres bleu-ardoise. Installés sous lumina-indigo3-dark, lumina-encre3-dark, lumina-encre3b-dark ; indigo2, indigo2b et encre retirés."),
    "indigo2": dict(refs=["doom-monoink"], protos=INDIGO2, themes=["lumina-encre-dark"], out="indigo2.html",
                    title="Indigo, deuxième tour : l'azur de Monoink aux mots-clés",
                    intro="Monoink en référence, puis Indigo à une teinte (azur sur mots-clés, encres lavande ailleurs), la variante avec chaînes pêche, et Encre pour comparer. Installés sous lumina-indigo2-dark et lumina-indigo2b-dark ; lumina-indigo-dark et lumina-opale-dark retirés."),
    "trois": dict(refs=["doom-indigo", "doom-monoink", "doom-horizon"], protos=TROIS, themes=[], out="trois.html",
                  title="Trois autres types de palettes, de plus en plus retenues",
                  intro="Indigo (trois teintes, fond indigo, encres de Monoink), Encre (une seule teinte, charbon neutre), Opale (quatre teintes, registre Horizon). Texte teinté 9:1 partout. Références en tête. Installés sous lumina-indigo-dark, lumina-encre-dark, lumina-opale-dark."),
    "strings": dict(refs=[], protos=STRINGS, themes=["lumina-vesper-dark"], out="strings.html",
                    title="Vesper sombre : la couleur des chaînes, sur du code Python NSI",
                    intro="Première carte : Vesper tel que figé (chaînes vert olive #91B265). Puis quatre remplacements, tout le reste identique. Installés sous lumina-vesper-lime, -menthe, -ciel, -sauge (suffixe -dark)."),
    "final": dict(refs=[], protos={}, themes=["lumina-indigo-dark", "lumina-indigo-light", "lumina-azur-dark", "lumina-azur-light", "lumina-vesper-dark", "lumina-sienne-dark"], out="final.html",
                  title="Indigo et Azur tels que figés dans la spec, Vesper et Sienne pour mémoire",
                  intro="Vesper : fonctions bleu, mots-clés pourpre, types ciel, chaînes paille, constantes corail, builtins rose ; aucun vert dans le code. Sienne : fonctions sarcelle, mots-clés mauve, types or, chaînes olive, constantes corail, builtins abricot. Les clairs reprennent les mêmes teintes en encres (clarté 0,46 à 0,55)."),
    "sienne12": dict(refs=["jazz"], protos=SIENNE12, themes=[], out="sienne12.html",
                     title="Sienne : affectation 2 sur ardoise et gris-bleu, trois tons de texte plus discrets",
                     intro="Le texte sable (#D1B99F) tirait sur le jaune ; ici trois tons plus neutres, toujours teintés : beige discret, gris chaud, beige rosé. Fonctions sarcelle, mots-clés mauve, types or, chaînes olive, constantes corail, builtins abricot. Installés sous lumina-sienne12-{ardoise,brume}-{beige,gris,rose}-dark."),
    "sienne": dict(refs=["jazz", "doom-rouge"], protos=SIENNE11, themes=[], out="sienne.html",
                   title="Sienne : mêmes six couleurs, quatre affectations, trois fonds",
                   intro="Les six couleurs de sienne10 (corail, mauve, or, olive, abricot, sarcelle) et le texte sable sont gardés. Quatre cartes changent l'affectation sur un fond neutre ; les deux dernières gardent l'affectation 2 sur un fond ardoise (Rouge) et un fond gris-bleu (uwu, Tomorrow Night). Installés sous lumina-sienne11-or, -neutre, -abricot, -mauve, -ardoise, -brume (suffixe -dark)."),
    "warm": dict(refs=["jazz", "doom-rouge", "doom-miramare", "doom-tomorrow-night"], protos=PROTOS, themes=[], out="zero.html",
                 title="Pôle chaud, série 10 : plus clair, à côté de quatre de tes références",
                 intro="Même fond noir chaud 0,21, texte sable 0,80 (9:1) au-dessus de tous les accents ; accents clarté 0,68 à 0,80, chroma 0,10 à 0,17. B' donne aux variables le corail de Rouge, uwu et Tomorrow Night. Installés sous lumina-rouge10-dark, lumina-sienne10-dark, lumina-sienne10v-dark, lumina-ocre10-dark."),
    "cold": dict(refs=[], protos=COLD, themes=["lumina-vesper-dark"], out="vesper.html",
                 title="Vesper sombre : 8 contre 9a, côte à côte",
                 intro="À gauche lumina-vesper8-dark (constantes orange, builtins ciel sourd), à droite lumina-vesper-dark tel que figé (constantes corail #F07B60, builtins turquoise #60BFA4). Tout le reste est identique. Les deux sont installés dans Doom."),
}


def render_doom(theme, light=False, sample=None):
    import glob as _g
    hits = _g.glob(str(DOOM.parent / f"*/{theme}-theme.el")) + _g.glob(str(Path.home() / f".doom.d/themes/{theme}-theme.el"))
    d = Path(hits[0]).parent if hits else DOOM
    env = dict(os.environ, R_THEME=theme, R_OUT=str(explore.OUT / f"{theme}.json"), R_PATH=f"{d}:{d.parent}:{DOOM}:{DOOM}/themes", R_DIR=str(ROOT / "tools/preview"), R_PY=str(sample or ROOT / "docs/sample.py"))
    if theme.startswith("doom-"):
        env["R_DOOM"] = "1"
    env.pop("R_LIGHT", None)
    if light:
        env["R_LIGHT"] = "1"
    subprocess.run(["emacs", "-Q", "--batch", "-l", str(ROOT / "tools/preview/render.el")], env=env, capture_output=True)
    return json.loads((explore.OUT / f"{theme}.json").read_text())


def main(sheet="warm", install_dir=Path.home() / ".doom.d/themes"):
    import measure
    sh = SHEETS[sheet]
    sample = ROOT / "docs" / sh.get("sample", "sample_nsi.py"); lines = sh.get("lines", slice(0, 34))
    faces = g._load_decl("faces.json"); variables = g._load_decl("variables.json"); cards = []
    for ref in sh["refs"]:
        cards.append(explore.card(f"{ref} (référence)", render_doom(ref, sample=sample), lines))
    for name, pr in sh["protos"].items():
        lead = pr.get("lead", pr["roles"]["functions"])
        sch = {**g.schema_for(pr["base"], "dark"), "lead": lead, "function_call": pr["roles"]["methods"], "property": pr["roles"]["builtin"]}
        roles = {k: v for k, v in pr["roles"].items() if k != "variables"}
        pal = vp.compose(ground=pr["ground"], lamp=lead, roles=roles, text=pr["text"], band=((.55, .95), (.50, .53)), cap=(.40, .16),
                         extra={"dark": pr["accents"]})
        if "variables" in pr["roles"]:
            pal["refs_dark"]["variables"] = pr["roles"]["variables"]
        sig = vp.signature(pal["dark"], lead, True, {"halo": .07, "halo2": .14, "region": .24, "glow": .42, "overlay": .05})
        colors = {k: [to_hex(*v), to_hex(*v).lower(), "black"] for k, v in sig.items()}
        for k, r in pal["refs_dark"].items():
            if k not in pr["accents"]:
                colors[k] = {"ref": r}
            else:
                colors.setdefault(k, {"ref": r})
        theme = f"lumina-{name}-dark"
        body = "\n".join(g.emit_face(n, g.spec_to_attrs(fs, colors, sch)) for n, fs in faces.items())
        vars_ = f"\n\n(custom-theme-set-variables\n '{theme}\n" + "\n".join(g.emit_variable(n, v, colors, sch) for n, v in variables.items()) + ")"
        text = (g.ELISP_FILE_HEADER.format(file=f"{theme}-theme.el", short=theme, theme=theme, docstring=pr["label"], commentary=f";; {pr['label']}")
                + body + g.ELISP_FILE_FOOTER.format(file=f"{theme}-theme.el", theme=theme, variables=vars_))
        (explore.THEMES / f"{theme}-theme.el").write_text(text); (install_dir / f"{theme}-theme.el").write_text(text)
        bg = colors["bg"][0]
        print(f"{theme}: bg {bg} fg {colors['fg'][0]} {contrast(colors['fg'][0], bg):.1f}:1 | " + " ".join(f"{r}={colors[colors[r]['ref']][0]}" for r in ["functions", "keywords", "type", "strings", "constants", "builtin", "variables"]))
        cards.append(explore.card(f"{theme} : {pr['label']}", explore.render(theme, False, sample), lines))
    for theme in sh["themes"]:
        cards.append(explore.card(theme, render_doom(theme, "light" in theme, sample), lines))
    page = ("""<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>""" + sh["title"] + """</title><style>
body{margin:0;padding:20px 14px;background:#2a2a2a;color:#ddd;font:14px/1.4 -apple-system,system-ui,sans-serif} h1{font-weight:600;margin:0 0 4px} p{color:#aaa;margin:0 0 14px;max-width:90ch}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
figure{margin:0} .code{font:12.5px/1.5 "JetBrains Mono",Menlo,monospace;padding:6px 0;border-radius:6px 6px 0 0;overflow:hidden} .r{white-space:pre;padding:0 8px;min-height:1.5em}
.ml{display:flex;align-items:center;gap:8px;font:11.5px Menlo,monospace;padding:5px 8px 5px 0;border-radius:0 0 6px 6px} .bar{width:3px;align-self:stretch}
@media (max-width:1150px){.grid{grid-template-columns:1fr}}
</style></head><body><h1>""" + sh["title"] + "</h1><p>" + sh["intro"] + """</p><div class="grid">"""
            + "".join(cards) + "</div></body></html>")
    (ROOT / "docs" / sh["out"]).write_text(page); print("ok -> docs/" + sh["out"])


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "warm")
