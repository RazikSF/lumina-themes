"""Contact sheet of the six code-role colours per flavor, on their own ground.

Usage: python3 tools/explore/sheet_roles.py OUT.html [flavor ...]
"""
import html, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "generators"))
import lumina_gen as g

ROLES = [("functions", "fonction"), ("keywords", "mot-clé"), ("type", "type"),
         ("strings", "chaîne"), ("constants", "constante"), ("builtin", "builtin")]
CODE = [("keywords", "def "), ("functions", "refill"), ("fg", "(self, "), ("type", "Bucket"), ("fg", ") -> "),
        ("builtin", "float"), ("fg", ":\n    "), ("keywords", "return "), ("builtin", "min"), ("fg", "(self.cap, "),
        ("constants", "None"), ("fg", ", "), ("strings", '"tokens"'), ("fg", ", "), ("constants", "1.0"), ("fg", ")")]


def block(f, mode, spec):
    c = spec[f][mode]["colors"]
    col = lambda r: g.resolve_ref(r, c, g.SCHEMAS[f])
    bg, fg = col("bg"), col("fg")
    sw = "".join(f'<div class="sw"><span style="background:{col(r)}"></span><i style="color:{col(r)}">{n}</i></div>' for r, n in ROLES)
    code = "".join(f'<span style="color:{col(r)}">{html.escape(t)}</span>' for r, t in CODE)
    return f'<div class="card" style="background:{bg};color:{fg}"><b>{f} {mode}</b><div class="row">{sw}</div><pre>{code}</pre></div>'


out = Path(sys.argv[1]); flavors = sys.argv[2:]
spec = json.loads(g.SPEC.read_text())["flavors"]
flavors = flavors or list(spec)
cards = "".join(block(f, m, spec) for m in ("dark", "light") for f in flavors)
out.write_text(f"""<!doctype html><meta charset="utf-8"><title>Lumina roles</title><style>
body{{margin:0;padding:12px;background:#777;font:13px -apple-system,sans-serif}}
.grid{{display:grid;grid-template-columns:repeat({len(flavors)},1fr);gap:8px}}
.card{{padding:10px;border-radius:8px}} .row{{display:flex;gap:6px;margin:8px 0}}
.sw{{flex:1;text-align:center}} .sw span{{display:block;height:34px;border-radius:4px}} .sw i{{font-style:normal;font-size:11px}}
pre{{font:14px/1.5 "Zed Mono",Menlo,monospace;margin:0;white-space:pre-wrap}}
</style><div class="grid">{cards}</div>""")
print("ok", out)
