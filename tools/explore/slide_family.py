"""A family of role assignments of the slide palette on the same code: fixed keywords and functions,
both orders of the two remaining inks on types and strings, four- and six-ink variants.
Usage: python3 tools/explore/slide_family.py OUT.html KW FN   (e.g. menthe saumon)"""
import html, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "tools/explore"))
from slide_langs import tokens, INKS, GROUND, TEXT, GREY

out, kw, fn = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
rest = [c for c in ("or", "saumon", "menthe", "ciel") if c not in (kw, fn)]
code = tokens("ex.py") + [["fg", "\n\n"]] + tokens("ex.js") + [["fg", "\n\n"]] + tokens("ex.sql")
RN = dict(fn="fonctions", kw="mots-clés", ty="types", st="chaînes", co="constantes", bi="builtins")
cards = []
for ty, st in ((rest[0], rest[1]), (rest[1], rest[0])):
    base = dict(kw=kw, fn=fn, ty=ty, st=st)
    tag = f"types {ty}, chaînes {st}"
    for name, co, bi in ((f"4 couleurs, constantes {kw}", kw, ty), (f"4 couleurs, constantes {fn}", fn, ty),
                         ("6 couleurs : constantes lilas, builtins rose", "lilas", "rose"), ("6 couleurs : constantes rose, builtins lilas", "rose", "lilas")):
        c = {**base, "co": co, "bi": bi}
        col = lambda r: TEXT if r == "fg" else GREY if r == "cm" else INKS[c[r]]
        body = "".join(f'<span style="color:{col(r)}{";font-style:italic" if r == "cm" else ""}">{html.escape(v)}</span>' for r, v in code)
        leg = " ".join(f'<span style="color:{INKS[c[r]]}">{RN[r]} : {c[r]}</span>' for r in ("ty", "st", "co", "bi"))
        cards.append(f'<div class="card"><div class="t"><b>{len(cards) + 1}. {tag} · {name}</b></div><div class="t">{leg}</div><pre>{body}</pre></div>')
out.write_text(f"""<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mots-clés {kw}, fonctions {fn}</title><style>
body{{margin:0;padding:16px;background:#15161a;color:#ddd;font:14px -apple-system,sans-serif}} h1{{font-size:18px;margin:0 0 4px}} p{{color:#999;margin:0 0 12px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(520px,1fr));gap:12px}}
.card{{background:{GROUND};border-radius:9px;overflow:hidden}} .t{{padding:6px 12px 0;font-size:12.5px;display:flex;gap:12px;flex-wrap:wrap}} .t b{{color:#fff}}
pre{{margin:0;padding:8px 12px 12px;font:12.5px/1.5 Menlo,monospace;white-space:pre;overflow:hidden}}
</style><h1>Mots-clés {kw}, fonctions {fn}</h1><p>Les deux encres restantes ({rest[0]} et {rest[1]}) sur les types et les chaînes, dans les deux sens ; puis constantes et builtins à quatre ou six couleurs.</p>
<div class="grid">{"".join(cards)}</div>""")
print("ok", len(cards), "cartes")
