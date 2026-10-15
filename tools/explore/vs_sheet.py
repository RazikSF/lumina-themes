"""Current flavors vs the Vesper/Sienne-profile proposal, swatches and code. Usage: vs_sheet.py OUT.html [dark|light]"""
import html, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "generators")); sys.path.insert(0, str(ROOT / "tools/explore"))
from oklch import to_hex
import lumina_gen as g
from slide_langs import tokens
ROLES = [("keywords", "mots-clés"), ("functions", "fonctions"), ("type", "types"), ("strings", "chaînes"), ("constants", "constantes"), ("builtin", "builtins")]
RO = {"fn": "functions", "kw": "keywords", "ty": "type", "st": "strings", "co": "constants", "bi": "builtin"}
out, mode = Path(sys.argv[1]), (sys.argv[2] if len(sys.argv) > 2 else "dark")
spec = json.loads(g.SPEC.read_text())["flavors"]
prop = json.loads((ROOT / "tools/explore/out/harmony-proposal.json").read_text())
code = tokens("ex.py")[:60]


def block(label, bg, fg, cm, cols):
    sw = "".join(f'<div><span style="background:{cols[r]}"></span><b style="color:{cols[r]}">{n}</b></div>' for r, n in ROLES)
    body = "".join(f'<span style="color:{fg if r == "fg" else cm if r == "cm" else cols[RO[r]]}{";font-style:italic" if r == "cm" else ""}">{html.escape(v)}</span>' for r, v in code)
    return f'<div class="b" style="background:{bg};color:{fg}"><em>{label}</em><div class="sw">{sw}</div><pre>{body}</pre></div>'


rows = []
for f in ["vesper", "sienne"] + [k for k in prop if k in spec and k not in ("vesper", "sienne", "nuancier")]:
    c = spec[f][mode]["colors"]; sch = g.SCHEMAS[f]
    bg, fg, cm = g.C(c, "bg"), g.C(c, "fg"), g.C(c, "comments")
    cur = {r: g.resolve_ref(r, c, sch) for r, _ in ROLES}
    if f in ("vesper", "sienne"):
        rows.append(f'<h2>{f} (référence)</h2><div class="pair">{block("référence", bg, fg, cm, cur)}</div>')
    else:
        new = {r: to_hex(*v) for r, v in prop[f][mode].items()}
        rows.append(f'<h2>{f}</h2><div class="pair">{block("actuel", bg, fg, cm, cur)}{block("méthode Vesper et Sienne", bg, fg, cm, new)}</div>')
out.write_text(f"""<!doctype html><meta charset="utf-8"><title>Méthode Vesper et Sienne</title><style>
body{{margin:0;padding:14px;background:#777;font:13px -apple-system,sans-serif}} h2{{margin:14px 0 4px;font-size:13px;color:#111}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:8px}} .b{{border-radius:7px;padding:8px 10px}} .b em{{font-style:normal;font-size:11px;opacity:.7}}
.sw{{display:flex;gap:6px;margin:6px 0}} .sw div{{flex:1;text-align:center}} .sw span{{display:block;height:22px;border-radius:4px}} .sw b{{font:600 11px Menlo,monospace}}
pre{{margin:0;font:12px/1.45 Menlo,monospace;white-space:pre;overflow:hidden}}
</style>{"".join(rows)}""")
print("ok", len(rows))
