import json, sys, html
S = sys.argv[1]; OUT = sys.argv[2]
def load(n): return json.load(open(f"{S}/out/{n}.json"))
def st(d, f, k="style"): return (d["faces"].get(f) or {}).get(k) or ""
def col(d, f, k, dflt=None): return (d["faces"].get(f) or {}).get(k) or dflt

def window(d, lines, cur=None, numbers=True, active=True, title="", mode=""):
    bg = col(d, "default", "bg"); fg = col(d, "default", "fg")
    hl = col(d, "hl-line", "bg", bg)
    out = [f'<div class="win" style="background:{bg};color:{fg}">']
    for i, (h, lbg) in enumerate(lines, 1):
        is_cur = (i == cur)
        rowbg = lbg or (hl if is_cur else None)
        num = ""
        if numbers:
            nf = "line-number-current-line" if is_cur else "line-number"
            n = 0 if is_cur else abs(i - cur) if cur else i
            n = i if is_cur else n
            num = f'<span class="ln" style="{st(d,"line-number")}{st(d,nf)}">{n:>3} </span>'
        if is_cur:
            cb = col(d, "cursor", "bg", fg)
            h = h.replace('<span style="">    ', f'<span style="">    </span><span style="background:{cb};color:{bg}">s</span><span style="">', 1) if False else h
            h = f'<span style="background:{cb};color:{bg}">&nbsp;</span>' + h if not h.startswith('<span style="">    ') else h.replace('<span style="">    ', f'<span style="">    </span><span style="background:{cb};color:{bg}">&#8203;&nbsp;</span><span style="">', 1)
        out.append(f'<div class="row" style="{"background:"+rowbg if rowbg else ""}">{num}<span class="txt">{h or "&nbsp;"}</span></div>')
    out.append('</div>')
    ml = "mode-line" if active else "mode-line-inactive"
    bar = col(d, "doom-modeline-bar", "bg") if active else None
    name_style = st(d, "doom-modeline-buffer-file") or "font-weight:700;"
    out.append(f'<div class="ml" style="{st(d,ml)}">'
               + (f'<span class="bar" style="background:{bar}"></span>' if bar else '<span class="bar"></span>')
               + (f'<span style="{name_style}">{title}</span>' if active else f'<span>{title}</span>')
               + f'<span class="sp"></span><span>{mode}</span></div>')
    return "\n".join(out)

def mini(d):
    bg = col(d, "default", "bg")
    sol = col(d, "solaire-default-face", "bg") or bg
    pr = st(d, "minibuffer-prompt"); cur = col(d, "vertico-current", "bg") or col(d, "region", "bg") or col(d, "hl-line", "bg") or bg
    m = st(d, "orderless-match-face-0") or st(d, "completions-common-part")
    rows = [("lumi", "na-dawn-dark", True), ("lumi", "na-dawn-light", False), ("lumi", "na-tide-dark", False)]
    s = f'<div class="mini" style="background:{sol};color:{col(d,"default","fg")}"><div><span style="{pr}">Load custom theme: </span>lumi</div>'
    for a, b, c in rows:
        s += f'<div class="row" style="{"background:"+cur if c else ""}"><span style="{m}">{a}</span>{b}</div>'
    return s + "</div>"

def panel(name, d):
    py = [tuple(x) for x in d["py"][13:40]]
    return (f'<section><h3>{html.escape(name)}</h3>'
            + window(d, py, cur=15, title="limiter.py", mode="Python")
            + window(d, [tuple(x) for x in d["org"]], numbers=False, active=False, title="carnet.org", mode="Org")
            + window(d, [tuple(x) for x in d["diff"]], numbers=False, active=False, title="magit-diff", mode="Diff")
            + mini(d) + '</section>')

rows = [("Sombre", [("Dawn 1 (actuel)", "old-dark"), ("Dawn 2 (proposé)", "new-dark"), ("Gruvbox (référence)", "gruvbox-dark")]),
        ("Clair", [("Dawn 1 (actuel)", "old-light"), ("Dawn 2 (proposé)", "new-light"), ("Gruvbox clair (référence)", "gruvbox-light")])]
body = "".join(f'<h2>{t}</h2><div class="grid">' + "".join(panel(n, load(f)) for n, f in p) + "</div>" for t, p in rows)
page = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lumina Dawn 2</title><style>
body{{margin:0;padding:24px 16px;background:#2a2a2a;color:#ddd;font:15px/1.4 -apple-system,system-ui,sans-serif}}
h1{{font-weight:600;margin:0 0 4px}} p.note{{margin:0 0 20px;color:#aaa;max-width:70ch}}
h2{{font-weight:500;margin:28px 0 10px;color:#bbb}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(470px,1fr));gap:18px}}
section h3{{margin:0 0 6px;font-weight:500;font-size:14px;color:#ccc}}
.win,.mini{{font:13.5px/1.5 "Zed Mono","JetBrains Mono",Menlo,monospace;padding:6px 0;overflow:hidden}} .row,.mini div{{white-space:pre}}
.row{{padding-right:8px;min-height:1.5em}} .ln{{display:inline-block;padding:0 8px 0 4px}} .txt{{padding-left:6px}}
.mini{{padding:6px 10px}}
.ml{{display:flex;align-items:center;gap:10px;font:12.5px "Zed Mono",Menlo,monospace;padding:7px 10px 7px 0}}
.bar{{width:3px;align-self:stretch;margin-right:4px}} .sp{{flex:1}}
@media (max-width:520px){{.grid{{grid-template-columns:1fr}} .win{{overflow-x:auto}}}}
</style></head><body><h1>Lumina Dawn 2</h1>
<p class="note">Rendu exporté depuis GNU Emacs 30.2 (emacs -Q, fontification réelle de python-mode, org-mode et diff-mode). Chaque couleur vient des faces calculées par Emacs ; seuls la mise en page, le curseur et la barre d'état sont dessinés à l'identique pour les trois thèmes.</p>
{body}</body></html>"""
open(OUT, "w").write(page)
print("ok", len(page))
