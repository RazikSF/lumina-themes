"""Ground lab: for each flavor, render four dark grounds with the flavor's own accents.

  current        the ground in generators/v2_palettes.py
  radix 2        Radix Colors <hue>Dark step 2, the "app background" of that hue
  radix 1        Radix Colors <hue>Dark step 1, the deeper one
  tailwind       the nearest Tailwind neutral -900 (stone, zinc, neutral, gray, slate)

Usage: python3 tools/explore/grounds.py  -> docs/grounds.html
"""
import json, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "generators")); sys.path.insert(0, str(ROOT / "tools/explore"))
from oklch import from_hex, to_hex
import v2_palettes as vp
import lumina_gen as g
import explore

SRC = json.loads((ROOT / "tools/explore/sources.json").read_text())
RADIX_HUE = {"dawn": "amber", "oxblood": "ruby", "tide": "sky", "canopy": "grass", "slate": "slate", "nocturne": "indigo",
             "amethyst": "plum", "obsidian": "gray", "prisma": "iris", "vesper": "indigo"}
TW_NEUTRAL = {"dawn": "stone", "oxblood": "stone", "tide": "slate", "canopy": "zinc", "slate": "zinc", "nocturne": "slate",
              "amethyst": "zinc", "obsidian": "neutral", "prisma": "zinc", "vesper": "slate"}


def radix_dark(hue, step):
    scale = SRC["radix-dark"][hue + "Dark"]; L, C, h = from_hex(scale.get(hue + str(step)) or list(scale.values())[step - 1])
    return (round(L, 3), round(C, 3), round(h, 1))


def tw900(name):
    return explore.tw(name, 900) and from_hex(explore.tw(name, 900))


def ground_variants(flavor):
    h, cd, cl, Ld, Ll = vp.FLAVORS[flavor]["ground"]
    r2 = radix_dark(RADIX_HUE[flavor], 2); r1 = radix_dark(RADIX_HUE[flavor], 1); tw = tw900(TW_NEUTRAL[flavor])
    return {"current": (h, cd, cl, Ld, Ll), f"radix {RADIX_HUE[flavor]} 2": (r2[2], r2[1], cl, r2[0], Ll),
            f"radix {RADIX_HUE[flavor]} 1": (r1[2], r1[1], cl, r1[0], Ll), f"tailwind {TW_NEUTRAL[flavor]}-900": (tw[2], tw[1], cl, tw[0], Ll)}


def main():
    cards = []
    faces = g._load_decl("faces.json")
    for flavor in [f for f in vp.FLAVORS if f != "vesper"]:
        spec = vp.FLAVORS[flavor]; sch = g.SCHEMAS[flavor]
        for label, ground in ground_variants(flavor).items():
            pal = vp.compose(**{**spec, "ground": ground})
            sig = vp.signature(pal["dark"], spec["lamp"], True, pal["sig"])
            colors = {k: [to_hex(*v), to_hex(*v).lower(), "black"] for k, v in sig.items()}
            for k, r in pal["refs"].items():
                colors.setdefault(k, {"ref": r})
            theme = f"ground-{flavor}-{re.sub(r'[^a-z0-9]+', '-', label)}"
            body = "\n".join(g.emit_face(n, g.spec_to_attrs(fs, colors, sch)) for n, fs in faces.items())
            (explore.THEMES / f"{theme}-theme.el").write_text(
                g.ELISP_FILE_HEADER.format(file=f"{theme}-theme.el", short=theme, theme=theme, docstring=theme, commentary=";; lab")
                + body + g.ELISP_FILE_FOOTER.format(file=f"{theme}-theme.el", theme=theme, variables=""))
            bg = colors["bg"][0]
            cards.append(explore.card(f"{flavor} : {label} {bg}", explore.render(theme, False)))
    page = ("""<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Lumina grounds</title><style>
body{margin:0;padding:20px 14px;background:#2a2a2a;color:#ddd;font:14px/1.4 -apple-system,system-ui,sans-serif} h1{font-weight:600;margin:0 0 4px} p{color:#aaa;margin:0 0 14px;max-width:90ch}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(560px,1fr));gap:14px}
figure{margin:0} .code{font:12.5px/1.5 "JetBrains Mono",Menlo,monospace;padding:6px 0;border-radius:6px 6px 0 0;overflow:hidden} .r{white-space:pre;padding:0 8px;min-height:1.5em}
.ml{display:flex;align-items:center;gap:8px;font:11.5px Menlo,monospace;padding:5px 8px 5px 0;border-radius:0 0 6px 6px} .bar{width:3px;align-self:stretch}
</style></head><body><h1>Lumina : fonds sombres candidats</h1><p>Par saveur, quatre fonds avec les accents de la saveur : actuel ; Radix pas 2 (fond d'application de la teinte) ; Radix pas 1 (plus profond) ; neutre Tailwind 900 le plus proche. Rendu par Emacs.</p><div class="grid">"""
            + "".join(cards) + "</div></body></html>")
    (ROOT / "docs/grounds.html").write_text(page)
    print("ok", len(cards), "cards -> docs/grounds.html")


if __name__ == "__main__" and "--pair" not in sys.argv:
    main()


def pair(install_dir=Path.home() / ".doom.d/themes"):
    """Two columns per flavor, Radix app background (left) and Tailwind neutral -900 (right);
    the non-current one is installed as lumina-<flavor>2-dark for testing in Emacs."""
    faces = g._load_decl("faces.json"); variables = g._load_decl("variables.json"); rows = []
    for flavor, spec in vp.FLAVORS.items():
        sch = g.SCHEMAS[flavor]; cl, Ll = spec["ground"][2], spec["ground"][4]
        hue = RADIX_HUE[flavor]; step = 2
        r = radix_dark(hue, step); tw = tw900(TW_NEUTRAL[flavor])
        grounds = {"radix": (f"Radix {hue} {step}", (r[2], r[1], cl, r[0], Ll)), "tailwind": (f"Tailwind {TW_NEUTRAL[flavor]}-900", (tw[2], tw[1], cl, tw[0], Ll))}
        current = "tailwind" if flavor == "vesper" else "radix"
        cells = []
        for key, (label, ground) in grounds.items():
            pal = vp.compose(**{**spec, "ground": ground}); sig = vp.signature(pal["dark"], spec["lamp"], True, pal["sig"])
            colors = {k: [to_hex(*v), to_hex(*v).lower(), "black"] for k, v in sig.items()}
            for k, ref in pal["refs"].items():
                colors.setdefault(k, {"ref": ref})
            theme = f"lumina-{flavor}-dark" if key == current else f"lumina-{flavor}2-dark"
            body = "\n".join(g.emit_face(n, g.spec_to_attrs(fs, colors, sch)) for n, fs in faces.items())
            vars_ = f"\n\n(custom-theme-set-variables\n '{theme}\n" + "\n".join(g.emit_variable(n, v, colors, sch) for n, v in variables.items()) + ")"
            text = (g.ELISP_FILE_HEADER.format(file=f"{theme}-theme.el", short=theme, theme=theme, docstring=f"{flavor}, {label}", commentary=f";; {flavor}, {label}")
                    + body + g.ELISP_FILE_FOOTER.format(file=f"{theme}-theme.el", theme=theme, variables=vars_))
            (explore.THEMES / f"{theme}-theme.el").write_text(text)
            if key != current:
                (install_dir / f"{theme}-theme.el").write_text(text)
            cells.append(explore.card(f"{theme} : {label} {colors['bg'][0]}" + ("  (actuel)" if key == current else ""), explore.render(theme, False)))
        rows.append(f'<h2>{flavor}</h2><div class="grid">' + "".join(cells) + "</div>")
    page = ("""<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Radix / Tailwind</title><style>
body{margin:0;padding:20px 14px;background:#2a2a2a;color:#ddd;font:14px/1.4 -apple-system,system-ui,sans-serif} h1{font-weight:600;margin:0 0 4px} p{color:#aaa;margin:0 0 14px;max-width:90ch}
h2{font-weight:500;color:#bbb;margin:22px 0 8px;text-transform:capitalize} .grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
figure{margin:0} .code{font:12.5px/1.5 "JetBrains Mono",Menlo,monospace;padding:6px 0;border-radius:6px 6px 0 0;overflow:hidden} .r{white-space:pre;padding:0 8px;min-height:1.5em}
.ml{display:flex;align-items:center;gap:8px;font:11.5px Menlo,monospace;padding:5px 8px 5px 0;border-radius:0 0 6px 6px} .bar{width:3px;align-self:stretch}
@media (max-width:1150px){.grid{grid-template-columns:1fr}}
</style></head><body><h1>Fonds sombres : Radix (gauche) et Tailwind (droite)</h1><p>Par saveur, le fond d'application Radix pas 2 de la teinte et le neutre Tailwind 900 le plus proche, avec les accents de la saveur. La version non retenue est installée sous lumina-&lt;saveur&gt;2-dark. Rendu par Emacs.</p>"""
            + "".join(rows) + "</body></html>")
    (ROOT / "docs/grounds-pair.html").write_text(page)
    print("ok", len(rows), "flavors -> docs/grounds-pair.html; variants installed in", install_dir)


if __name__ == "__main__" and "--pair" in sys.argv:
    pair()
