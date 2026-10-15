"""Gemini's drafts beside their Lumina flavors, dark and light. Usage: gemini_sheet.py OUT.html"""
import html, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "generators")); sys.path.insert(0, str(ROOT / "tools/explore"))
import lumina_gen as g
from slide_langs import tokens
from gemini_import import G
ROLES = [("keywords", "mots-clés"), ("functions", "fonctions"), ("type", "types"), ("strings", "chaînes"), ("constants", "constantes"), ("builtin", "builtins")]
RO = {"fn": "functions", "kw": "keywords", "ty": "type", "st": "strings", "co": "constants", "bi": "builtin"}
GEMINI_LIGHT = {  # Gemini's light drafts: four inks only
    "borealis": dict(keywords="#6B5FA3", strings="#2D7E63", functions="#1D7A6B", type="#9E7B2A"),
    "cashmere": dict(keywords="#BD5D63", strings="#597A45", functions="#B37A2E", type="#C4683D"),
    "aethelgard": dict(keywords="#8A39C4", strings="#1D8A78", functions="#0A8A73", type="#B38600"),
    "sakura": dict(keywords="#834FA2", strings="#2D7E58", functions="#C75D81", type="#B86A2E"),
    "obsidian": dict(keywords="#A85C20", strings="#2E7D32", functions="#9C7A1E", type="#1E6BB8"),
}
spec = json.loads(g.SPEC.read_text())["flavors"]
code = tokens("ex.py")[:60]


def block(label, bg, fg, cm, cols):
    cols = {r: cols.get(r, fg) for r, _ in ROLES}
    sw = "".join(f'<div><span style="background:{cols[r]}"></span><b style="color:{cols[r]}">{n}</b></div>' for r, n in ROLES)
    body = "".join(f'<span style="color:{fg if r == "fg" else cm if r == "cm" else cols[RO[r]]}{";font-style:italic" if r == "cm" else ""}">{html.escape(v)}</span>' for r, v in code)
    return f'<div class="b" style="background:{bg};color:{fg}"><em>{label}</em><div class="sw">{sw}</div><pre>{body}</pre></div>'


rows = []
for f, d in G.items():
    cells = [block("Gemini, sombre", d["bg"], d["fg"], d["comment"], d["inks"])]
    for mode, lab in (("dark", "Lumina, sombre"), ("light", "Lumina, clair")):
        c = spec[f][mode]["colors"]; sch = g.SCHEMAS[f]
        cells.append(block(lab, g.C(c, "bg"), g.C(c, "fg"), g.C(c, "comments"), {r: g.resolve_ref(r, c, sch) for r, _ in ROLES}))
    l = d["light"]
    cells.insert(2, block("Gemini, clair (quatre encres)" if f in GEMINI_LIGHT else "Gemini, clair : aucun", l["bg"], l["fg"], l["comment"], GEMINI_LIGHT.get(f, {})))
    rows.append(f'<h2>{f}</h2><div class="pair">{"".join(cells)}</div>')
Path(sys.argv[1]).write_text(f"""<!doctype html><meta charset="utf-8"><title>Saveurs de Gemini</title><style>
body{{margin:0;padding:14px;background:#777;font:13px -apple-system,sans-serif}} h2{{margin:16px 0 4px;font-size:14px;color:#111}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:8px}} .b{{border-radius:7px;padding:8px 10px}} .b em{{font-style:normal;font-size:11px;opacity:.7}}
.sw{{display:flex;gap:6px;margin:6px 0}} .sw div{{flex:1;text-align:center}} .sw span{{display:block;height:22px;border-radius:4px}} .sw b{{font:600 11px Menlo,monospace}}
pre{{margin:0;font:12px/1.45 Menlo,monospace;white-space:pre;overflow:hidden}}
</style>{"".join(rows)}""")
print("ok", len(rows))
