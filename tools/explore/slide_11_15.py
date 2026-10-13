"""Combos 11 and 15 of the slide palette and every five- and six-ink variant, on the same code.
Usage: python3 tools/explore/slide_11_15.py OUT.html"""
import html, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "tools/explore"))
from slide_langs import tokens, INKS, GROUND, TEXT, GREY

BASE = dict(fn="or", kw="ciel", ty="menthe", st="saumon")
VARIANTS = [("n° 11", "or", "menthe"), ("n° 15", "ciel", "menthe"), ("11 + rose", "or", "rose"), ("11 + lilas", "or", "lilas"),
            ("15 + rose", "ciel", "rose"), ("15 + lilas", "ciel", "lilas"), ("6 couleurs A", "lilas", "rose"), ("6 couleurs B", "rose", "lilas")]
code = tokens("ex.py") + [["fg", "\n\n"]] + tokens("ex.js") + [["fg", "\n\n"]] + tokens("ex.sql")
RN = dict(fn="fonctions", kw="mots-clés", ty="types", st="chaînes", co="constantes", bi="builtins")


def card(name, co, bi):
    c = {**BASE, "co": co, "bi": bi}
    col = lambda r: TEXT if r == "fg" else GREY if r == "cm" else INKS[c[r]]
    body = "".join(f'<span style="color:{col(r)}{";font-style:italic" if r == "cm" else ""}">{html.escape(v)}</span>' for r, v in code)
    leg = " ".join(f'<span style="color:{INKS[c[r]]}">{RN[r]} : {c[r]}</span>' for r in ("co", "bi"))
    return f'<div class="card"><div class="t"><b>{name}</b> {leg}</div><pre>{body}</pre></div>'


Path(sys.argv[1]).write_text(f"""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>11 et 15</title><style>
body{{margin:0;padding:16px;background:#15161a;color:#ddd;font:14px -apple-system,sans-serif}} h1{{font-size:18px;margin:0 0 4px}} p{{color:#999;margin:0 0 12px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(520px,1fr));gap:12px}}
.card{{background:{GROUND};border-radius:9px;overflow:hidden}} .t{{padding:8px 12px 0;font-size:12.5px;display:flex;gap:12px;flex-wrap:wrap}} .t b{{color:#fff}}
pre{{margin:0;padding:8px 12px 12px;font:12.5px/1.5 Menlo,monospace;white-space:pre;overflow:hidden}}
</style><h1>Famille des n° 11 et 15</h1><p>Base commune : mots-clés ciel, fonctions or, types menthe, chaînes saumon. Seules changent les constantes et les builtins.</p>
<div class="grid">{"".join(card(*v) for v in VARIANTS)}</div>""")
print("ok")
