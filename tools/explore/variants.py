"""Tuning variants of Vesper, installed as lumina-vesperN-{dark,light} for testing inside Emacs.

Usage: python3 tools/explore/variants.py [install-dir]   (default ~/.doom.d/themes)
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "generators"))
from oklch import to_hex, contrast
import v2_palettes as vp
import lumina_gen as g

BASE = vp.PALETTES["vesper"]
SIG = dict(BASE["sig"])
VARIANTS = {
    "vesper1": ("référence : texte 9,6:1 sombre et 10:1 clair, lampe sarcelle moyenne, halo 10 %", {}, {}, {}),
    "vesper2": ("texte adouci à 8:1 (Tokyo Night), commentaires un cran plus bas",
                {"fg": (.76, .019, 255), "fg-alt": (.66, .02, 255), "base8": (.76, .019, 255), "doc-comments": (.64, .045, 257)},
                {"fg": (.40, .02, 258), "fg-alt": (.50, .02, 258), "base8": (.40, .02, 258), "comments": (.54, .014, 264)}, {}),
    "vesper3": ("lampe discrète : sarcelle moins saturée, halos à 7 %",
                {"teal": (.83, .10, 181)}, {"teal": (.52, .08, 179)}, {"halo": .07, "halo2": .13, "region": .22, "glow": .38}),
    "vesper4": ("lampe franche : sarcelle plus saturée, halos à 14 %",
                {"teal": (.87, .155, 181)}, {"teal": (.50, .12, 179)}, {"halo": .14, "halo2": .22, "region": .30, "glow": .50}),
    "vesper5": ("fond neutre zinc au lieu de l'ardoise marine, texte 8,5:1",
                {**vp.field(True, 286, .006, bg=.21, fg=.78, fgh=286)}, {**vp.field(False, 286, .003, bg=.985, fg=.38)}, {}),
    "vesper7": ("recommandée : texte 9:1 sombre et 8,8:1 clair, lampe et halos de la référence, ardoise marine",
                {"fg": (.78, .019, 255), "fg-alt": (.68, .02, 255), "base8": (.78, .019, 255)},
                {"fg": (.40, .02, 258), "fg-alt": (.50, .02, 258), "base8": (.40, .02, 258), "comments": (.54, .014, 264)}, {}),
    "vesper6": ("fond plus profond (ardoise 950), texte 8,5:1",
                {**vp.field(True, 265, .042, bg=.165, fg=.78, fgh=255)}, {"fg": (.34, .02, 258), "fg-alt": (.44, .02, 258), "base8": (.34, .02, 258)}, {}),
}


def colors_for(pal, mode):
    dark = mode == "dark"
    sig = vp.signature(pal, "teal", dark, pal.pop("_sig"))
    colors = {k: [to_hex(*v), to_hex(*v).lower(), "black"] for k, v in sig.items()}
    for k, r in BASE["refs"].items():
        colors.setdefault(k, {"ref": r})
    return colors


def main():
    out = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else Path.home() / ".doom.d/themes"
    out.mkdir(parents=True, exist_ok=True)
    faces = g._load_decl("faces.json"); variables = g._load_decl("variables.json"); sch = g.SCHEMAS["vesper"]
    for name, (desc, over_d, over_l, sig) in VARIANTS.items():
        for mode, over in (("dark", over_d), ("light", over_l)):
            pal = {**BASE[mode], **over, "_sig": {**SIG, **sig}}
            colors = colors_for(pal, mode); theme = f"lumina-{name}-{mode}"
            body = "\n".join(g.emit_face(n, g.spec_to_attrs(fs, colors, sch)) for n, fs in faces.items())
            vars_ = (f"\n\n(custom-theme-set-variables\n '{theme}\n" + "\n".join(g.emit_variable(n, v, colors, sch) for n, v in variables.items()) + ")")
            text = (g.ELISP_FILE_HEADER.format(file=f"{theme}-theme.el", short=theme, theme=theme, docstring=f"Vesper variant: {desc}", commentary=f";; Vesper variant: {desc}")
                    + body + g.ELISP_FILE_FOOTER.format(file=f"{theme}-theme.el", theme=theme, variables=vars_))
            (out / f"{theme}-theme.el").write_text(text)
            bg = colors["bg"][0]
            print(f"{theme:26s} fg {contrast(colors['fg'][0], bg):4.1f}  comments {contrast(colors['comments'][0], bg):3.1f}  lamp {contrast(colors['teal'][0], bg):4.1f}  bg {bg}  fg {colors['fg'][0]}  teal {colors['teal'][0]}")
    print(f"{len(VARIANTS) * 2} themes -> {out}")


if __name__ == "__main__" and "--sheet" not in sys.argv:
    main()


def sheet(install_dir):
    """Render every variant through Emacs into docs/variants.html."""
    import os, subprocess
    import explore
    cards = {"dark": [], "light": []}
    for name, (desc, *_rest) in VARIANTS.items():
        for mode in ("dark", "light"):
            theme = f"lumina-{name}-{mode}"
            env = dict(os.environ, R_THEME=theme, R_OUT=str(explore.OUT / f"{theme}.json"), R_PATH=str(install_dir),
                       R_DIR=str(ROOT / "tools/preview"), R_PY=str(ROOT / "docs/sample.py"))
            env.pop("R_LIGHT", None)
            if mode == "light":
                env["R_LIGHT"] = "1"
            subprocess.run(["emacs", "-Q", "--batch", "-l", str(ROOT / "tools/preview/render.el")], env=env, capture_output=True)
            d = json.loads((explore.OUT / f"{theme}.json").read_text())
            cards[mode].append(explore.card(f"{theme} : {desc}", d))
    page = """<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Vesper variants</title><style>
body{margin:0;padding:20px 14px;background:#2a2a2a;color:#ddd;font:14px/1.4 -apple-system,system-ui,sans-serif} h1{font-weight:600;margin:0 0 4px} p{color:#aaa;margin:0 0 14px;max-width:90ch}
h2{font-weight:500;color:#bbb;margin:22px 0 8px} .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(560px,1fr));gap:14px}
figure{margin:0} .code{font:12.5px/1.5 "JetBrains Mono",Menlo,monospace;padding:6px 0;border-radius:6px 6px 0 0;overflow:hidden} .r{white-space:pre;padding:0 8px;min-height:1.5em}
.ml{display:flex;align-items:center;gap:8px;font:11.5px Menlo,monospace;padding:5px 8px 5px 0;border-radius:0 0 6px 6px} .bar{width:3px;align-self:stretch}
</style></head><body><h1>Vesper : variantes de réglage</h1><p>Rendu par Emacs. vesper1 référence ; vesper2 texte 8:1 ; vesper3 lampe discrète ; vesper4 lampe franche ; vesper5 fond zinc neutre ; vesper6 fond plus profond ; vesper7 composite recommandé.</p>"""
    for mode in ("dark", "light"):
        page += f'<h2>{"Sombre" if mode == "dark" else "Clair"}</h2><div class="grid">' + "".join(cards[mode]) + "</div>"
    (ROOT / "docs/variants.html").write_text(page + "</body></html>")
    print("sheet -> docs/variants.html")


if __name__ == "__main__" and "--sheet" in sys.argv:
    sheet(Path.home() / ".doom.d/themes")
