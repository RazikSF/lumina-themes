"""Every role assignment of a fixed five-colour palette, rendered on code, in one comparison page.

Usage: python3 tools/explore/slide_palette.py OUT.html
Palette: the "Les couleurs des pages web" slide (ground #1C2030, gold, salmon, mint, sky, blue swatch).
"""
import html, itertools, json, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "generators"))
from oklch import contrast, fit_chroma, from_hex, to_hex

GROUND, TEXT, GREY = "#1D2130", "#E8E9E7", "#A3A7B7"
INKS = {"or": "#F7C054", "saumon": "#EC907E", "menthe": "#87C3AB", "ciel": "#77B8E7"}
BLUE = INKS["ciel"]
PAPER = "#F6F7FA"


def lab(h):
    L, C, hh = from_hex(h); return L, C * math.cos(math.radians(hh)), C * math.sin(math.radians(hh))


def de(a, b): return 100 * math.dist(lab(a), lab(b))


def mix(a, b, t):
    A, B = lab(a), lab(b); L, x, y = [p + (q - p) * t for p, q in zip(A, B)]
    return to_hex(L, math.hypot(x, y), math.degrees(math.atan2(y, x)) % 360)


def with_L(h, L, cscale=1.0):
    _, C, hh = from_hex(h); return to_hex(L, fit_chroma(L, C * cscale, hh), hh)


def text_at(target, bg, light):
    """Neutral text of the ground's hue reaching `target` contrast."""
    _, C, hh = from_hex(TEXT)
    L = 0.30 if light else 0.95
    step = 0.002 if light else -0.002
    while (contrast(to_hex(L, C, hh), bg) > target) and 0.2 < L < 0.99:
        L += step
    return to_hex(L, C, hh)


def light_inks():
    out = {k: with_L(v, .50, 1.35) for k, v in INKS.items()}
    out["or"] = to_hex(.53, fit_chroma(.53, .16, 66), 66)
    return out


SAMPLE = [
    [("cm", "# Seau à jetons : débit limité par seconde")],
    [("cm", "@"), ("bi", "dataclass")],
    [("kw", "class "), ("ty", "TokenBucket"), ("fg", ":")],
    [("fg", "    capacity: "), ("ty", "float"), ("fg", " = "), ("co", "10.0")],
    [("fg", "    label: "), ("ty", "str"), ("fg", " = "), ("st", '"api"')],
    [],
    [("kw", "    def "), ("fn", "try_consume"), ("fg", "(self, n: "), ("ty", "int"), ("fg", " = "), ("co", "1"), ("fg", ") -> "), ("ty", "bool"), ("fg", ":")],
    [("fg", "        self."), ("fn", "_refill"), ("fg", "()")],
    [("kw", "        if "), ("fg", "self.tokens < n "), ("kw", "or "), ("fg", "n <= "), ("co", "0"), ("fg", ":")],
    [("fg", "            log."), ("fn", "debug"), ("fg", "("), ("st", 'f"vide : {self.tokens}"'), ("fg", ")")],
    [("kw", "            return "), ("co", "False")],
    [("fg", "        self.tokens -= n")],
    [("kw", "        return "), ("co", "True"), ("cm", "  # jeton accordé")],
]
ROLE_NAMES = {"fn": "fonctions", "kw": "mots-clés", "ty": "types", "st": "chaînes", "co": "constantes", "bi": "builtins"}


def combos():
    for fn, kw, ty, st in itertools.permutations(list(INKS), 4):
        for co in (fn, kw, ty, st):
            yield {"fn": fn, "kw": kw, "ty": ty, "st": st, "co": co, "bi": ty}


def score(c):
    used = {c[r] for r in ("fn", "kw", "ty", "st", "co")}
    cols = [INKS[n] for n in used]
    inner = min(de(a, b) for a, b in itertools.combinations(cols, 2))
    lamp = INKS[c["fn"]]
    sal = min(de(lamp, INKS[n]) for n in used if n != c["fn"])
    shared = c["co"] in (c["kw"], c["ty"], c["st"], c["fn"])
    warm = sum(1 for r in ("kw", "ty", "st") if c[r] in ("or", "saumon"))
    return inner, sal, shared, warm


cs = []
for c in combos():
    inner, sal, shared, warm = score(c)
    rank = inner + (2 if c["co"] in (c["kw"], c["fn"]) else 0) - 3 * max(0, warm - 1)
    cs.append({**c, "inner": round(inner, 1), "sal": round(sal, 1), "warm": warm, "rank": round(rank, 1)})
cs.sort(key=lambda x: -x["rank"])
by_kw = {}
for c in cs:
    by_kw.setdefault(c["kw"], []).append(c)
cs = [c for group in itertools.zip_longest(*by_kw.values()) for c in group if c]

dark = {"bg": GROUND, "grey": GREY, "inks": INKS, "blue": BLUE,
        "text": {"orig": TEXT, "soft": text_at(9.0, GROUND, False)}}
li = light_inks()
light = {"bg": PAPER, "grey": with_L(GREY, .55), "inks": li, "blue": with_L(BLUE, .50, 1.1),
         "text": {"orig": "#1E2230", "soft": text_at(9.0, PAPER, True)}}
def equalise(inks, L, cap):
    out = {}
    for k, v in inks.items():
        _, C, hh = from_hex(v)
        c = min(C, cap * (.78 if 70 <= hh <= 115 else 1))
        out[k] = to_hex(L, fit_chroma(L, c, hh), hh)
    return out


dark["inks_eq"] = equalise(INKS, .77, .105)
light["inks_eq"] = equalise(li, .51, .14)
for m in (dark, light):
    m["inks_orig"] = m["inks"]
    m["halo"] = {k: mix(m["bg"], v, .10) for k, v in m["inks"].items()}
    m["halo_eq"] = {k: mix(m["bg"], v, .10) for k, v in m["inks_eq"].items()}
    m["contrast_eq"] = {k: round(contrast(v, m["bg"]), 1) for k, v in m["inks_eq"].items()}
    m["region"] = mix(m["bg"], m["blue"], .30)
    m["ln"] = mix(m["bg"], m["grey"], .45)
    m["contrast"] = {k: round(contrast(v, m["bg"]), 1) for k, v in m["inks"].items()}
    m["tcontrast"] = {k: round(contrast(v, m["bg"]), 1) for k, v in m["text"].items()}

data = {"combos": cs, "dark": dark, "light": light, "sample": SAMPLE, "roles": ROLE_NAMES}
page = """<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Palette diapo</title><style>
:root{--ink:#e6e7ea;--mute:#9a9ca3;--panel:#2a2c31;--page:#1d1e22}
@media (prefers-color-scheme: light){:root:not([data-theme="dark"]){--ink:#22242a;--mute:#5d606a;--panel:#e9eaee;--page:#f4f4f6}}
:root[data-theme="light"]{--ink:#22242a;--mute:#5d606a;--panel:#e9eaee;--page:#f4f4f6}
body{margin:0;padding:20px 16px 40px;background:var(--page);color:var(--ink);font:15px/1.45 -apple-system,system-ui,sans-serif}
h1{font-weight:600;margin:0 0 4px} p.lead{color:var(--mute);margin:0 0 16px;max-width:80ch}
.bar{display:flex;flex-wrap:wrap;gap:14px;align-items:center;margin:0 0 16px;padding:10px 12px;background:var(--panel);border-radius:8px}
.bar label{color:var(--mute);font-size:13px} .bar select,.bar button{font:inherit;font-size:13px;padding:3px 8px;border-radius:6px;border:1px solid #8884;background:transparent;color:var(--ink)}
.bar button.on{background:#8883}
.sw{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 18px}
.sw div{font-size:12px;color:var(--mute)} .sw span{display:block;width:92px;height:40px;border-radius:6px;margin-bottom:4px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(430px,1fr));gap:14px}
.card{border-radius:10px;overflow:hidden}
.head{display:flex;justify-content:space-between;gap:8px;padding:8px 12px 0;font:12px -apple-system,sans-serif}
.legend{display:flex;flex-wrap:wrap;gap:4px 10px;padding:4px 12px 6px;font:11px -apple-system,sans-serif}
pre{margin:0;padding:6px 0 10px;font:12.5px/1.55 "Zed Mono","JetBrains Mono",Menlo,monospace;overflow-x:auto}
.ln{display:inline-block;width:2.4em;text-align:right;padding-right:10px;user-select:none}
.row{display:block;padding-right:10px}
.cur{display:inline-block;width:.6em}
.ml{display:flex;align-items:center;gap:8px;font:11.5px Menlo,monospace;padding:5px 10px 5px 0}
.ml i{width:3px;align-self:stretch}
.best{font-weight:600}
@media (max-width:480px){.grid{grid-template-columns:1fr}}
</style></head><body>
<h1>Palette de la diapositive : toutes les combinaisons</h1>
<p class="lead">Fond, texte, gris et quatre couleurs relevés au pixel sur la diapositive (médiane exacte, sans arrondi) : l'or du titre, le saumon, la menthe et le ciel des trois mots, le texte et le gris. Les quatre encres se répartissent entre fonctions, mots-clés, types et chaînes ; les constantes reprennent l'une d'elles. La sélection et la barre d'état prennent une teinte tirée du ciel. Le bouton « même intensité » ramène les quatre encres à une clarté et une saturation communes (l'or, plus vif sur la diapo, est le plus touché).</p>
<div class="sw" id="sw"></div>
<div class="bar">
  <label>Mode <button id="mDark" class="on">sombre</button><button id="mLight">clair</button></label>
  <label>Texte <button id="tOrig" class="on">diapo (12,9:1)</button><button id="tSoft">adouci (9:1)</button></label>
  <label>Encres <button id="iOrig" class="on">diapo</button><button id="iEq">même intensité</button></label>
  <label>Fonctions <select id="lamp"><option value="">toutes</option><option>or</option><option>saumon</option><option>menthe</option><option>ciel</option></select></label>
  <label>Mots-clés <select id="kwf"><option value="">tous</option><option>or</option><option>saumon</option><option>menthe</option><option>ciel</option></select></label>
  <label>Afficher <select id="n"><option value="12">les 12 premières</option><option value="24">24</option><option value="96">les 96</option></select></label>
</div>
<div class="grid" id="grid"></div>
<script>
const D=__DATA__;
let mode="dark", text="orig", ink="orig";
function M(){const m=D[mode];return {...m,inks:ink=="eq"?m.inks_eq:m.inks_orig,halo:ink=="eq"?m.halo_eq:m.halo,contrast:ink=="eq"?m.contrast_eq:m.contrast}}
const $=id=>document.getElementById(id);
function esc(s){return s.replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]))}
function swatches(){const m=M();$("sw").innerHTML=
  [["fond",m.bg],["texte",m.text[text]],["gris",m.grey],...Object.entries(m.inks),["sélection",m.region]].map(([k,v])=>
  `<div><span style="background:${v};outline:1px solid #8884"></span>${k} ${v}${m.contrast[k]?` · ${m.contrast[k]}:1`:""}${k=="texte"?` · ${m.tcontrast[text]}:1`:""}</div>`).join("")}
function card(c,i){const m=M(), fg=m.text[text], col=r=>r=="fg"?fg:r=="cm"?m.grey:m.inks[c[r]];
  const lamp=m.inks[c.fn];
  const rows=D.sample.map((line,j)=>{const n=j+1, cur=n==7;
    let body=line.map(([r,t])=>`<span style="color:${col(r)}${r=="cm"?";font-style:italic":""}">${esc(t)}</span>`).join("")||"&nbsp;";
    if(n==11) body=body.replace("False",`<span style="background:${m.region}">False</span>`).replace(`<span style="background:${m.region}">False</span>`,`<span style="background:${m.region};color:${m.inks[c.co]}">False</span>`);
    const ln=`<span class="ln" style="color:${cur?lamp:m.ln}">${n}</span>`;
    const cursor=cur?`<span class="cur" style="background:${lamp}">&nbsp;</span>`:"";
    return `<span class="row" style="${cur?"background:"+m.halo[c.fn]:""}">${ln}${cursor}${body}</span>`}).join("");
  const leg=Object.entries(D.roles).map(([r,nm])=>`<span style="color:${m.inks[c[r]]}">${nm} : ${c[r]}</span>`).join("");
  return `<div class="card" style="background:${m.bg};color:${fg}">
   <div class="head"><span>n° ${i+1} · mots-clés ${c.kw}</span><span style="color:${m.grey}">séparation des encres ${c.inner}</span></div>
   <div class="legend">${leg}</div><pre>${rows}</pre>
   <div class="ml" style="background:${mode=="dark"?"#151827":"#e4e6ec"};color:${m.grey}"><i style="background:${m.blue}"></i><b style="color:${fg}">limiter.py</b><span style="flex:1"></span>Python</div></div>`}
function render(){swatches();const lamp=$("lamp").value, kwf=$("kwf").value, n=+$("n").value;
  const list=D.combos.map((c,i)=>[c,i]).filter(([c])=>(!lamp||c.fn==lamp)&&(!kwf||c.kw==kwf)).slice(0,n);
  $("grid").innerHTML=list.map(([c,i])=>card(c,i)).join("")}
function tog(a,b,set){$(a).onclick=()=>{set();$(a).classList.add("on");$(b).classList.remove("on");render()}}
tog("mDark","mLight",()=>mode="dark");tog("mLight","mDark",()=>mode="light");
tog("tOrig","tSoft",()=>text="orig");tog("tSoft","tOrig",()=>text="soft");
tog("iOrig","iEq",()=>ink="orig");tog("iEq","iOrig",()=>ink="eq");
$("lamp").onchange=render;$("kwf").onchange=render;$("n").onchange=render;render();
</script></body></html>"""
Path(sys.argv[1]).write_text(page.replace("__DATA__", json.dumps(data, ensure_ascii=False)))
print("ok", len(cs), "combinaisons ; texte adouci", dark["text"]["soft"], dark["tcontrast"]["soft"], "; clair", light["contrast"])
for c in cs[:6]:
    print(c["rank"], "lampe", c["fn"], "| mots-clés", c["kw"], "types", c["ty"], "chaînes", c["st"], "constantes", c["co"], "| lampe", c["sal"], "encres", c["inner"])
