"""Build docs/gallery.html and assets/screens/*.svg from rendered theme dumps."""
import html, json, re, sys
from pathlib import Path

GAL, ROOT = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(ROOT / "generators"))
import lumina_gen as g

SPEC = json.loads(g.SPEC.read_text())["flavors"]
RANGES = {"Feutrés": ["dawn", "oxblood", "tide", "canopy", "slate"],
          "Vifs": ["nocturne", "amethyst", "obsidian", "prisma"]}
LINES = slice(13, 32)
SPAN = re.compile(r'<span style="([^"]*)">(.*?)</span>', re.S)


def load(t):
    return json.loads((GAL / f"{t}.json").read_text())


def face(d, f, k):
    return (d["faces"].get(f) or {}).get(k)


def card_html(t):
    d = load(t)
    bg, fg = face(d, "default", "bg"), face(d, "default", "fg")
    hl, cur = face(d, "hl-line", "bg") or bg, face(d, "cursor", "bg") or fg
    rows = []
    for i, (h, lbg) in enumerate(d["py"][LINES], 1):
        is_cur = i == 15
        nf = "line-number-current-line" if is_cur else "line-number"
        num = f'<span style="color:{face(d, nf, "fg") or fg}">{i:>2} </span>'
        if is_cur:
            h = h.replace('<span style="">    ', f'<span style="">    </span><span style="background:{cur};color:{bg}">&nbsp;</span><span style="">', 1)
        rows.append(f'<div class="r" style="{"background:" + (lbg or hl) if (lbg or is_cur) else ""}">{num}{h or "&nbsp;"}</div>')
    ml = d["faces"].get("mode-line") or {}
    bar = face(d, "doom-modeline-bar", "bg") or cur
    name = t.replace("lumina-", "")
    return (f'<figure><div class="code" style="background:{bg};color:{fg}">{"".join(rows)}</div>'
            f'<div class="ml" style="{ml.get("style", "")}"><span class="bar" style="background:{bar}"></span>'
            f'<b>{name}</b></div></figure>')


def card_svg(t):
    d = load(t)
    bg, fg = face(d, "default", "bg"), face(d, "default", "fg")
    hl, cur = face(d, "hl-line", "bg") or bg, face(d, "cursor", "bg") or fg
    lh, cw, pad, n = 21, 8.43, 14, len(d["py"][LINES])
    w, h = 760, pad * 2 + n * lh + 34
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
           f'font-family="JetBrains Mono, Menlo, Consolas, monospace" font-size="14">',
           f'<rect width="{w}" height="{h}" rx="10" fill="{bg}"/>']
    for i, (row, lbg) in enumerate(d["py"][LINES], 1):
        y = pad + (i - 1) * lh
        if lbg or i == 15:
            out.append(f'<rect x="0" y="{y}" width="{w}" height="{lh}" fill="{lbg or hl}"/>')
        nf = "line-number-current-line" if i == 15 else "line-number"
        out.append(f'<text x="{pad}" y="{y + 15}" fill="{face(d, nf, "fg") or fg}">{i:>2}</text>')
        x, spans = pad + 3.5 * cw, []
        for style, txt in SPAN.findall(row):
            txt = html.unescape(txt)
            col = re.search(r"(?<!-)color:([^;]+)", style)
            attrs = f' fill="{col.group(1) if col else fg}"'
            if "font-style:italic" in style:
                attrs += ' font-style="italic"'
            if re.search(r"font-weight:(6|7|8)00", style):
                attrs += ' font-weight="600"'
            spans.append(f'<tspan{attrs}>{html.escape(txt)}</tspan>')
        if i == 15:
            out.append(f'<rect x="{x + 4 * cw}" y="{y + 2}" width="{cw}" height="{lh - 4}" fill="{cur}"/>')
        out.append(f'<text x="{x}" y="{y + 15}" xml:space="preserve" fill="{fg}">{"".join(spans)}</text>')
    my = h - 30
    mlbg = face(d, "mode-line", "bg") or bg
    bar = face(d, "doom-modeline-bar", "bg") or cur
    out += [f'<rect x="0" y="{my}" width="{w}" height="30" fill="{mlbg}"/>',
            f'<rect x="0" y="{my}" width="4" height="30" fill="{bar}"/>',
            f'<text x="{pad + 4}" y="{my + 20}" fill="{face(d, "mode-line", "fg") or fg}" font-weight="600">'
            f'{t}</text></svg>']
    return "\n".join(out)


sections = []
for rng, flavors in RANGES.items():
    for fl in flavors:
        modes = SPEC[fl]
        desc = modes["dark"]["commentary"].split("\n", 1)[1]
        cards = "".join(card_html(d["theme"]) for d in modes.values())
        sections.append(f'<section><h2>{fl.capitalize()} <small>{rng}</small></h2><p>{html.escape(desc)}</p>'
                        f'<div class="grid">{cards}</div></section>')
page = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Lumina Gallery</title><style>
body{{margin:0;padding:28px 16px;background:#1b1b1d;color:#ddd;font:15px/1.45 -apple-system,system-ui,sans-serif}}
h1{{font-weight:600;margin:0}} h2{{font-weight:500;margin:34px 0 2px}} h2 small{{color:#888;font-size:13px;margin-left:8px}}
section p{{color:#aaa;margin:0 0 12px;max-width:90ch}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(440px,1fr));gap:14px}}
figure{{margin:0;border-radius:10px;overflow:hidden}}
.code{{font:12.5px/1.55 "Zed Mono","JetBrains Mono",Menlo,monospace;padding:8px 0;overflow:hidden}}
.r{{white-space:pre;padding:0 10px}} .ml{{display:flex;gap:8px;align-items:center;font:12px "Zed Mono",Menlo,monospace;padding:6px 10px 6px 0}}
.bar{{width:3px;align-self:stretch}}
@media (max-width:500px){{.grid{{grid-template-columns:1fr}} .code{{overflow-x:auto}}}}
</style></head><body><h1>Lumina</h1><p>Neuf saveurs, chacune en sombre, clair et contraste élevé ; Prisma a aussi un clair noir et blanc. Rendu exporté depuis GNU Emacs 30.2.</p>
{"".join(sections)}</body></html>"""
(ROOT / "docs" / "gallery.html").write_text(page)
shots = ROOT / "assets" / "screens"
shots.mkdir(parents=True, exist_ok=True)
for fl in sum(RANGES.values(), []):
    for m in [k for k in SPEC[fl] if not k.endswith("contrast")]:
        t = SPEC[fl][m]["theme"]
        (shots / f"{t}.svg").write_text(card_svg(t))
print("gallery ok,", len(list(shots.glob("*.svg"))), "svg")
