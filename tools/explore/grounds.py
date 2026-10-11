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


if __name__ == "__main__":
    main()
