"""Accent character lab for dark grounds: the same flavor with accents taken at different
steps of the public scales.  A = Tailwind 300 (current pastel), B = Tailwind 400 (deeper,
more saturated), C = Radix dark 11 (designed low-contrast text), D = Tailwind 400 desaturated.

Usage: python3 tools/explore/steps.py  -> docs/steps.html, twins lumina-<flavor><B|C|D>-dark in Doom
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "generators")); sys.path.insert(0, str(ROOT / "tools/explore"))
from oklch import from_hex, to_hex
import v2_palettes as vp
import lumina_gen as g
import explore

SRC = json.loads((ROOT / "tools/explore/sources.json").read_text())


def tw_table(step):
    out = {}
    for n in vp.TW300:
        v = SRC["tailwind"][n][str(step)]; L, C, h = re.match(r"oklch\(([\d.]+)% ([\d.]+) ([\d.]+|none)\)", v).groups()
        out[n] = (round(float(L) / 100, 3), round(float(C), 3), 0.0 if h == "none" else round(float(h), 1))
    return out


def radix_dark_table(step):
    out = {}
    for n in vp.TW300:
        name = {"emerald": "jade", "fuchsia": "plum", "rose": "crimson", "amber": "amber"}.get(n, n)
        scale = SRC["radix-dark"].get(name + "Dark")
        if not scale:
            continue
        hx = scale.get(name + str(step)) or list(scale.values())[step - 1]; L, C, h = from_hex(hx)
        out[n] = (round(L, 3), round(C, 3), round(h, 1))
    return out


def oc_table(step):
    out = {}
    for n in vp.TW300:
        name = {"emerald": "green", "fuchsia": "grape", "rose": "pink", "amber": "yellow", "sky": "cyan", "purple": "grape"}.get(n, n)
        if name in SRC["open-color"]:
            L, C, h = from_hex(SRC["open-color"][name][step]); out[n] = (round(L, 3), round(C, 3), round(h, 1))
    return out


FREE = ((.60, .95), (.50, .53))
VARIANTS = {
    "A": ("Tailwind 300, pastel (actuel)", vp.TW300, ((.79, .85), (.50, .53)), (.13, .16)),
    "E": ("Tailwind 400 brut : chroma libre, clarté libre", tw_table(400), FREE, (.30, .16)),
    "F": ("clartés mêlées, à la Dracula : mots-clés et constantes 400, chaînes et types 300", {**tw_table(400), **{k: vp.TW300[k] for k in ("emerald", "lime", "green", "sky", "cyan", "amber", "yellow")}}, FREE, (.30, .16)),
    "G": ("Open Color 5 brut, le plus vif", oc_table(5), FREE, (.30, .16)),
}


def main(install_dir=Path.home() / ".doom.d/themes"):
    faces = g._load_decl("faces.json"); variables = g._load_decl("variables.json"); rows = []
    for flavor in ["vesper", "dawn", "nocturne", "oxblood"]:
        spec = vp.FLAVORS[flavor]; sch = g.SCHEMAS[flavor]; cells = []
        for key, (label, table, band, cap) in VARIANTS.items():
            saved = vp.TW300; vp.TW300 = {**saved, **table}
            try:
                pal = vp.compose(**{**spec, "band": band, "cap": cap if key != "A" else spec.get("cap", cap)})
            finally:
                vp.TW300 = saved
            if key != "A":
                hues = {**vp.DEFAULT_HUES, **spec.get("hues", {})}; twn = hues[spec["lamp"]][0]
                L, C, h = table.get(twn) or vp.TW300[twn]; pal["dark"][spec["lamp"]] = (L, C, h)
            sig = vp.signature(pal["dark"], spec["lamp"], True, pal["sig"])
            colors = {k: [to_hex(*v), to_hex(*v).lower(), "black"] for k, v in sig.items()}
            for k, r in pal["refs"].items():
                colors.setdefault(k, {"ref": r})
            theme = f"lumina-{flavor}-dark" if key == "A" else f"lumina-{flavor}{key}-dark"
            body = "\n".join(g.emit_face(n, g.spec_to_attrs(fs, colors, sch)) for n, fs in faces.items())
            vars_ = f"\n\n(custom-theme-set-variables\n '{theme}\n" + "\n".join(g.emit_variable(n, v, colors, sch) for n, v in variables.items()) + ")"
            text = (g.ELISP_FILE_HEADER.format(file=f"{theme}-theme.el", short=theme, theme=theme, docstring=f"{flavor}, {label}", commentary=f";; {flavor}, {label}")
                    + body + g.ELISP_FILE_FOOTER.format(file=f"{theme}-theme.el", theme=theme, variables=vars_))
            (explore.THEMES / f"{theme}-theme.el").write_text(text)
            if key != "A":
                (install_dir / f"{theme}-theme.el").write_text(text)
            cells.append(explore.card(f"{theme} : {label}", explore.render(theme, False)))
        rows.append(f'<h2>{flavor}</h2><div class="grid">' + "".join(cells) + "</div>")
    page = ("""<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Accents sombres</title><style>
body{margin:0;padding:20px 14px;background:#2a2a2a;color:#ddd;font:14px/1.4 -apple-system,system-ui,sans-serif} h1{font-weight:600;margin:0 0 4px} p{color:#aaa;margin:0 0 14px;max-width:90ch}
h2{font-weight:500;color:#bbb;margin:22px 0 8px;text-transform:capitalize} .grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
figure{margin:0} .code{font:12.5px/1.5 "JetBrains Mono",Menlo,monospace;padding:6px 0;border-radius:6px 6px 0 0;overflow:hidden} .r{white-space:pre;padding:0 8px;min-height:1.5em}
.ml{display:flex;align-items:center;gap:8px;font:11.5px Menlo,monospace;padding:5px 8px 5px 0;border-radius:0 0 6px 6px} .bar{width:3px;align-self:stretch}
@media (max-width:1150px){.grid{grid-template-columns:1fr}}
</style></head><body><h1>Sombre : quatre caractères d'accents</h1><p>Même fond, mêmes rôles ; seules changent la profondeur et la saturation des accents. A pastel Tailwind 300 (actuel) ; E Tailwind 400 brut, chroma et clarté libres ; F clartés mêlées à la Dracula ; G Open Color 5 brut, le plus vif. E, F, G installés sous lumina-&lt;saveur&gt;E/F/G-dark. Rendu par Emacs.</p>"""
            + "".join(rows) + "</body></html>")
    (ROOT / "docs/steps.html").write_text(page); print("ok -> docs/steps.html; twins installed in", install_dir)


if __name__ == "__main__":
    main()
