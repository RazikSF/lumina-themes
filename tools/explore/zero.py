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
SHEETS = {
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


def render_doom(theme):
    import glob as _g
    hits = _g.glob(str(DOOM.parent / f"*/{theme}-theme.el")) + _g.glob(str(Path.home() / f".doom.d/themes/{theme}-theme.el"))
    d = Path(hits[0]).parent if hits else DOOM
    env = dict(os.environ, R_THEME=theme, R_OUT=str(explore.OUT / f"{theme}.json"), R_PATH=f"{d}:{d.parent}:{DOOM}:{DOOM}/themes", R_DIR=str(ROOT / "tools/preview"), R_PY=str(ROOT / "docs/sample.py"))
    if theme.startswith("doom-"):
        env["R_DOOM"] = "1"
    env.pop("R_LIGHT", None)
    subprocess.run(["emacs", "-Q", "--batch", "-l", str(ROOT / "tools/preview/render.el")], env=env, capture_output=True)
    return json.loads((explore.OUT / f"{theme}.json").read_text())


def main(sheet="warm", install_dir=Path.home() / ".doom.d/themes"):
    import measure
    sh = SHEETS[sheet]
    faces = g._load_decl("faces.json"); variables = g._load_decl("variables.json"); cards = []
    for ref in sh["refs"]:
        cards.append(explore.card(f"{ref} (référence)", render_doom(ref)))
    for name, pr in sh["protos"].items():
        sch = {**g.schema_for(pr["base"], "dark"), "lead": pr["roles"]["functions"], "function_call": pr["roles"]["methods"], "property": pr["roles"]["builtin"]}
        roles = {k: v for k, v in pr["roles"].items() if k != "variables"}
        pal = vp.compose(ground=pr["ground"], lamp=roles["functions"], roles=roles, text=pr["text"], band=((.55, .95), (.50, .53)), cap=(.40, .16),
                         extra={"dark": pr["accents"]})
        if "variables" in pr["roles"]:
            pal["refs_dark"]["variables"] = pr["roles"]["variables"]
        sig = vp.signature(pal["dark"], roles["functions"], True, {"halo": .07, "halo2": .14, "region": .24, "glow": .42, "overlay": .05})
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
        cards.append(explore.card(f"{theme} : {pr['label']}", explore.render(theme, False)))
    for theme in sh["themes"]:
        cards.append(explore.card(theme, measure.render(theme)))
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
