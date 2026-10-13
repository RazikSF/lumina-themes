"""Two role assignments of the slide palette on twelve languages, side by side (tokenised by Pygments).

Usage: python3 tools/explore/slide_langs.py OUT.html
"""
import html, json, math, sys
from pathlib import Path

from pygments import lex
from pygments.lexers import get_lexer_for_filename
from pygments.token import Comment, Keyword, Name, Number, Operator, String, Literal

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "generators"))
from oklch import contrast, fit_chroma, from_hex, to_hex

SAMPLES = ROOT / "tools/explore/samples"
FILES = [("Python", "ex.py"), ("JavaScript", "ex.js"), ("TypeScript", "ex.ts"), ("Rust", "ex.rs"), ("C", "ex.c"),
         ("Java", "Ex.java"), ("SQL", "ex.sql"), ("HTML", "ex.html"), ("CSS", "ex.css"), ("Bash", "ex.sh"),
         ("LaTeX", "ex.tex"), ("Emacs Lisp", "ex.el")]
GROUND, TEXT, GREY = "#1D2130", "#E8E9E7", "#A3A7B7"
INKS = {"or": "#F7C054", "saumon": "#EC907E", "menthe": "#87C3AB", "ciel": "#77B8E7",
        "lilas": "#B5A4EA", "rose": "#E297BA", "vert tendre": "#A2BC75"}
PAPER = "#F6F7FA"
COMBOS = {"n° 19 (4 couleurs)": dict(fn="saumon", kw="ciel", ty="or", st="menthe", co="saumon", bi="or"),
          "n° 23 (4 couleurs)": dict(fn="saumon", kw="ciel", ty="or", st="menthe", co="ciel", bi="or"),
          "6 couleurs : constantes lilas, builtins rose": dict(fn="saumon", kw="ciel", ty="or", st="menthe", co="lilas", bi="rose"),
          "6 couleurs : constantes rose, builtins lilas": dict(fn="saumon", kw="ciel", ty="or", st="menthe", co="rose", bi="lilas"),
          "6 couleurs : constantes lilas, builtins vert tendre": dict(fn="saumon", kw="ciel", ty="or", st="menthe", co="lilas", bi="vert tendre")}


def role(tt):
    if tt in Comment: return "cm"
    if tt in String.Symbol: return "co"
    if tt in String or tt in Literal.String: return "st"
    if tt in Number: return "co"
    if tt in Keyword.Constant or tt in Name.Constant: return "co"
    if tt in Keyword.Type: return "ty"
    if tt in Operator.Word: return "kw"
    if tt in Keyword: return "kw"
    if tt in Name.Function or tt in Name.Function.Magic: return "fn"
    if tt in Name.Class or tt in Name.Attribute or tt in Name.Namespace: return "ty"
    if tt in Name.Builtin.Pseudo: return "fg"
    if tt in Name.Builtin or tt in Name.Decorator: return "bi"
    if tt in Name.Tag or tt in Name.Label: return "kw"
    return "fg"


def tokens(fname):
    src = (SAMPLES / fname).read_text()
    lexer = get_lexer_for_filename(fname)
    out = []
    for tt, val in lex(src, lexer):
        r = role(tt)
        if out and out[-1][0] == r:
            out[-1][1] += val
        else:
            out.append([r, val])
    return out


def with_L(h, L, cs=1.0):
    _, C, hh = from_hex(h); return to_hex(L, fit_chroma(L, C * cs, hh), hh)


def text_at(target, bg, light):
    _, C, hh = from_hex(TEXT); L = .30 if light else .95; step = .002 if light else -.002
    while contrast(to_hex(L, C, hh), bg) > target and .2 < L < .99:
        L += step
    return to_hex(L, C, hh)


light_inks = {k: with_L(v, .50, 1.35) for k, v in INKS.items()}
light_inks["rose"] = with_L(INKS["rose"], .50, 1.5)
light_inks["or"] = to_hex(.53, fit_chroma(.53, .16, 66), 66)
MODES = {"dark": {"bg": GROUND, "grey": GREY, "inks": INKS, "text": {"orig": TEXT, "soft": text_at(9, GROUND, False)}},
         "light": {"bg": PAPER, "grey": with_L(GREY, .55), "inks": light_inks, "text": {"orig": "#1E2230", "soft": text_at(9, PAPER, True)}}}
data = {"langs": [[name, tokens(f)] for name, f in FILES], "modes": MODES, "combos": COMBOS}
page = """<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Quatre ou six couleurs</title><style>
:root{--ink:#e6e7ea;--mute:#9a9ca3;--panel:#2a2c31;--page:#16171b}
@media (prefers-color-scheme: light){:root:not([data-theme="dark"]){--ink:#22242a;--mute:#5d606a;--panel:#e6e7eb;--page:#f1f1f3}}
:root[data-theme="light"]{--ink:#22242a;--mute:#5d606a;--panel:#e6e7eb;--page:#f1f1f3}
body{margin:0;padding:20px 16px 40px;background:var(--page);color:var(--ink);font:15px/1.45 -apple-system,system-ui,sans-serif}
h1{font-weight:600;margin:0 0 4px} .lead{color:var(--mute);margin:0 0 14px;max-width:85ch}
.bar{position:sticky;top:0;z-index:2;display:flex;flex-wrap:wrap;gap:14px;align-items:center;margin:0 0 16px;padding:10px 12px;background:var(--panel);border-radius:8px}
.bar label{color:var(--mute);font-size:13px} .bar button{font:inherit;font-size:13px;padding:3px 8px;border-radius:6px;border:1px solid #8884;background:transparent;color:var(--ink)}
.bar button.on{background:#8883}
.key{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin-bottom:10px}
.key div{font-size:13px;color:var(--mute)} .key select{font:inherit;font-size:13px;padding:3px 6px;border-radius:6px;background:transparent;color:var(--ink);border:1px solid #8884;margin-bottom:6px}
.sw{display:inline-flex;gap:6px;flex-wrap:wrap} .sw span{display:inline-block;padding:2px 7px;border-radius:5px;font-size:12px}
h2{font-size:15px;font-weight:600;margin:22px 0 8px}
.pair{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.card{border-radius:10px;overflow:hidden}
.card .t{font:12px -apple-system,sans-serif;padding:8px 12px 0}
pre{margin:0;padding:8px 12px 12px;font:12.5px/1.55 "Zed Mono","JetBrains Mono",Menlo,monospace;overflow-x:auto;white-space:pre}
@media (max-width:760px){.pair,.key{grid-template-columns:1fr}}
</style></head><body>
<h1>Quatre ou six couleurs, sur douze langages</h1>
<p class="lead">Base commune : mots-clés ciel, fonctions saumon, types or, chaînes menthe (encres de la diapositive). Les versions à six couleurs donnent aux constantes et aux builtins deux encres fabriquées à la même clarté et à la même saturation que celles de la diapo : lilas, rose ou vert tendre. Choisir une version à gauche et à droite. Coloration par Pygments.</p>
<div class="bar"><label>Mode <button id="mDark" class="on">sombre</button><button id="mLight">clair</button></label>
<label>Texte <button id="tOrig" class="on">diapo</button><button id="tSoft">adouci (9:1)</button></label></div>
<div class="key"><div><select id="left"></select><div id="kl"></div></div><div><select id="right"></select><div id="kr"></div></div></div>
<div id="out"></div>
<script>
const D=__DATA__; let mode="dark", text="orig";
const esc=s=>s.replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));
function card(toks,n){const m=D.modes[mode], c=D.combos[n], fg=m.text[text];
  const col=r=>r=="fg"?fg:r=="cm"?m.grey:m.inks[c[r]];
  return `<div class="card" style="background:${m.bg};color:${fg}"><div class="t" style="color:${m.grey}">${n}</div><pre>${toks.map(([r,v])=>`<span style="color:${col(r)}${r=="cm"?";font-style:italic":""}">${esc(v)}</span>`).join("")}</pre></div>`}
const names=Object.keys(D.combos), L=document.getElementById("left"), R=document.getElementById("right");
for(const s of [L,R]) s.innerHTML=names.map(n=>`<option>${n}</option>`).join("");
L.value=names[0]; R.value=names[2];
const RN={fn:"fonctions",kw:"mots-clés",ty:"types",st:"chaînes",co:"constantes",bi:"builtins"};
function legend(n){const m=D.modes[mode],c=D.combos[n];return `<div class="sw">${Object.entries(RN).map(([r,t])=>`<span style="background:${m.bg};color:${m.inks[c[r]]}">${t} : ${c[r]}</span>`).join("")}</div>`}
function render(){document.getElementById("kl").innerHTML=legend(L.value);document.getElementById("kr").innerHTML=legend(R.value);
  document.getElementById("out").innerHTML=D.langs.map(([name,toks])=>`<h2>${name}</h2><div class="pair">${card(toks,L.value)}${card(toks,R.value)}</div>`).join("")}
L.onchange=render; R.onchange=render;
function tog(a,b,f){document.getElementById(a).onclick=()=>{f();document.getElementById(a).classList.add("on");document.getElementById(b).classList.remove("on");render()}}
tog("mDark","mLight",()=>mode="dark");tog("mLight","mDark",()=>mode="light");tog("tOrig","tSoft",()=>text="orig");tog("tSoft","tOrig",()=>text="soft");render();
</script></body></html>"""
Path(sys.argv[1]).write_text(page.replace("__DATA__", json.dumps(data, ensure_ascii=False)))
from collections import Counter
cnt = Counter(r for _, toks in data["langs"] for r, v in toks if v.strip())
print("ok ; segments par rôle :", dict(cnt))
