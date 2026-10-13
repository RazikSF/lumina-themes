"""Six big swatches per flavor on its ground, before and after, Nuancier first. Usage: ... OUT.html [dark|light]"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "generators"))
from oklch import to_hex
import lumina_gen as g
ROLES = [("keywords", "mots-clés"), ("strings", "chaînes"), ("type", "types"), ("builtin", "builtins"), ("constants", "constantes"), ("functions", "fonctions")]
out, mode = Path(sys.argv[1]), (sys.argv[2] if len(sys.argv) > 2 else "dark")
spec = json.loads(g.SPEC.read_text())["flavors"]
origin = json.loads((ROOT / "tools/explore/out/lumina-before-harmony.json").read_text())["flavors"]


OLD_SCHEMAS = None


def _resolve(colors, role):
    """Resolve a role in an old palette: roles are refs to slots in the palette itself."""
    v = colors[role]
    while isinstance(v, dict):
        v = colors[v["ref"]]
    return v[0]


def row(label, bg, fg, cols):
    sw = "".join(f'<div><span style="background:{cols[r]}"></span><b style="color:{cols[r]}">{n}</b></div>' for r, n in ROLES)
    return f'<div class="row" style="background:{bg};color:{fg}"><em>{label}</em>{sw}</div>'


blocks = []
nu = {"keywords": "#77B8E7", "strings": "#87C3AB", "type": "#F7C054", "builtin": "#E297BA", "constants": "#B5A4EA", "functions": "#EC907E"}
if mode == "dark":
    blocks.append(f'<h2>étalon : Nuancier</h2>{row("diapo", "#1D2130", "#E8E9E7", nu)}')
for f in spec:
    c = spec[f][mode]["colors"]; sch = g.SCHEMAS[f]
    bg, fg = g.C(c, "bg"), g.C(c, "fg")
    after = {r: g.resolve_ref(r, c, sch) for r, _ in ROLES}
    rows_ = row("après", bg, fg, after)
    if f in origin:
        oc = origin[f][mode]["colors"]
        before = {r: g.resolve_ref(r, oc, sch) if False else None for r, _ in ROLES}
        import lumina_gen as _g
        before = {}
        for r, _ in ROLES:
            v = oc[r] if r in oc else None
            before[r] = _resolve(oc, r)
        rows_ = row("avant", g.C(oc, "bg"), g.C(oc, "fg"), before) + rows_
    blocks.append(f'<h2>{f}</h2>{rows_}')
out.write_text(f"""<!doctype html><meta charset="utf-8"><title>Six encres</title><style>
body{{margin:0;padding:14px;background:#777;font:13px -apple-system,sans-serif}} h2{{margin:12px 0 4px;font-size:13px;color:#111}}
.row{{display:flex;align-items:center;gap:8px;padding:8px 10px;border-radius:6px;margin-bottom:3px}} .row em{{width:60px;font-style:normal;font-size:11px;opacity:.7}}
.row div{{flex:1;text-align:center}} .row span{{display:block;height:26px;border-radius:4px}} .row b{{font:600 12px Menlo,monospace}}
</style>{"".join(blocks)}""")
print("ok")
