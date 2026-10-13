"""Before / after sheet for the six-ink harmonisation. Usage: python3 tools/explore/harmony_sheet.py OUT.html"""
import html, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "generators")); sys.path.insert(0, str(ROOT / "tools/explore"))
from oklch import to_hex
import lumina_gen as g
from slide_langs import tokens

ROLE_OF = {"fn": "functions", "kw": "keywords", "ty": "type", "st": "strings", "co": "constants", "bi": "builtin"}
spec = json.loads(g.SPEC.read_text())["flavors"]
prop = json.loads((ROOT / "tools/explore/out/harmony-proposal.json").read_text())
code = tokens("ex.py")


def card(title, bg, fg, cm, col):
    body = "".join(f'<span style="color:{fg if r == "fg" else cm if r == "cm" else col[ROLE_OF[r]]}{";font-style:italic" if r == "cm" else ""}">{html.escape(v)}</span>' for r, v in code)
    sw = "".join(f'<i style="background:{col[ROLE_OF[k]]}" title="{ROLE_OF[k]}"></i>' for k in ("kw", "st", "ty", "bi", "co", "fn"))
    return f'<div class="card" style="background:{bg};color:{fg}"><div class="t" style="color:{cm}">{title}<span class="sw">{sw}</span></div><pre>{body}</pre></div>'


rows = []
for f in prop:
    for mode in ("dark", "light"):
        if f not in spec:
            continue
        c = spec[f][mode]["colors"]; sch = g.SCHEMAS[f]
        bg, fg, cm = g.C(c, "bg"), g.C(c, "fg"), g.C(c, "comments")
        before = {r: g.resolve_ref(r, c, sch) for r in ROLE_OF.values()}
        if mode not in prop[f]:
            continue
        after = {r: to_hex(*v) for r, v in prop[f][mode].items()}
        rows.append(f'<h2>{f} · {"sombre" if mode == "dark" else "clair"}</h2><div class="pair">{card("actuel", bg, fg, cm, before)}{card("proposé", bg, fg, cm, after)}</div>')
page = f"""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Harmonie six encres</title><style>
body{{margin:0;padding:16px;background:#141518;color:#ddd;font:14px -apple-system,sans-serif}} h2{{font-size:14px;margin:18px 0 6px}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:10px}} .card{{border-radius:8px;overflow:hidden}}
.t{{font-size:12px;padding:6px 10px 0;display:flex;justify-content:space-between}} .sw i{{display:inline-block;width:16px;height:12px;margin-left:3px;border-radius:2px}}
pre{{margin:0;padding:6px 10px 10px;font:14px/1.5 Menlo,monospace;white-space:pre;overflow:hidden}}
</style><h1>Six encres : actuel et proposé</h1>{"".join(rows)}"""
Path(sys.argv[1]).write_text(page); print("ok", len(rows), "paires")
