"""Palette lab: render candidate palettes x role assignments through Emacs into one contact sheet.

Sources (tools/explore/sources.json, downloaded from the official repositories), public
colour systems composed here, never a ready-made editor theme:
  Radix Colors   step 11 of each hue on the mauve or slate ground (equal text contrast by design)
  Tailwind v4    -300 on slate/zinc-900 (dark), -700 on -50 (light); OKLCH-defined
  Open Color     step 3 on gray-9 (dark), step 8 on gray-0 (light); public domain

Usage: python3 tools/explore/explore.py  -> docs/explore.html + tools/explore/out/*.svg
"""
import json, math, os, re, subprocess, sys, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "generators"))
from oklch import from_hex, to_hex
import v2_palettes as vp
import lumina_gen as g

SRC = json.loads((ROOT / "tools/explore/sources.json").read_text())
OUT = ROOT / "tools/explore/out"; THEMES = OUT / "themes"; THEMES.mkdir(parents=True, exist_ok=True)


def tw(name, step):
    v = SRC["tailwind"][name][str(step)]
    if v.startswith("#"):
        return v
    L, C, h = re.match(r"oklch\(([\d.]+)% ([\d.]+) ([\d.]+|none)\)", v).groups()
    return to_hex(float(L) / 100, float(C), 0.0 if h == "none" else float(h))


def radix(mode, name, step):
    key = name + ("Dark" if mode == "dark" else "")
    return SRC["radix-" + mode][key][key + str(step)] if (key + str(step)) in SRC["radix-" + mode][key] else list(SRC["radix-" + mode][key].values())[step - 1]


def oc(name, step):
    return SRC["open-color"][name][step]


ACC = ["red", "orange", "yellow", "green", "teal", "cyan", "blue", "violet", "magenta"]


def candidates():
    """Public colour systems only, composed here: no ready-made editor theme or brand palette."""
    c = {}
    hues = {"red": "red", "orange": "orange", "yellow": "amber", "green": "grass", "teal": "teal", "cyan": "sky", "blue": "indigo", "violet": "violet", "magenta": "crimson"}
    for ground in ["mauve", "slate"]:
        c[f"radix-{ground}"] = {m: {"bg": radix(m, ground, 1), "fg": radix(m, ground, 12), "comments": radix(m, ground, 11),
                                    **{k: radix(m, v, 11) for k, v in hues.items()}} for m in ["dark", "light"]}
    hues = {"red": "rose", "orange": "orange", "yellow": "amber", "green": "emerald", "teal": "teal", "cyan": "sky", "blue": "indigo", "violet": "violet", "magenta": "fuchsia"}
    for ground in ["slate", "zinc"]:
        c[f"tailwind-{ground}"] = {"dark": {"bg": tw(ground, 900), "fg": tw(ground, 200), "comments": tw(ground, 500), **{k: tw(v, 300) for k, v in hues.items()}},
                                   "light": {"bg": tw(ground, 50), "fg": tw(ground, 800), "comments": tw(ground, 500), **{k: tw(v, 700) for k, v in hues.items()}}}
    hues = {"red": "red", "orange": "orange", "yellow": "yellow", "green": "green", "teal": "teal", "cyan": "cyan", "blue": "indigo", "violet": "violet", "magenta": "pink"}
    c["open-color"] = {"dark": {"bg": oc("gray", 9), "fg": oc("gray", 3), "comments": oc("gray", 6), **{k: oc(v, 3) for k, v in hues.items()}},
                       "light": {"bg": oc("gray", 0), "fg": oc("gray", 8), "comments": oc("gray", 6), **{k: oc(v, 8) for k, v in hues.items()}}}
    return c


MAPPINGS = {
    "indigo": dict(lead="blue", functions="blue", keywords="violet", strings="green", type="cyan", constants="orange", builtin="teal",
                   function_call="cyan", property="teal", preprocessor="violet", escape="orange"),
    "gold": dict(lead="yellow", functions="yellow", keywords="blue", strings="green", type="violet", constants="orange", builtin="teal",
                 function_call="cyan", property="teal", preprocessor="blue", escape="orange"),
    "teal": dict(lead="teal", functions="teal", keywords="violet", strings="green", type="blue", constants="orange", builtin="cyan",
                 function_call="cyan", property="blue", preprocessor="violet", escape="orange"),
}


def palette(src, mode, mapping):
    dark = mode == "dark"
    L, C, h = from_hex(src["bg"])
    pal = {**vp.field(dark, h, C, bg=L, fg=from_hex(src["fg"])[0], fgh=from_hex(src["fg"])[2]), **vp.diffs(dark)}
    pal["fg"] = pal["base8"] = from_hex(src["fg"])
    for k in ACC + ["comments"]:
        pal[k] = from_hex(src[k])
    pal["doc-comments"] = (pal["comments"][0] + (.06 if dark else -.06), pal["comments"][1], pal["comments"][2])
    pal["dark-blue"] = (pal["blue"][0] - (.12 if dark else -.1), pal["blue"][1], pal["blue"][2])
    pal["dark-cyan"] = (pal["cyan"][0] - (.12 if dark else -.1), pal["cyan"][1], pal["cyan"][2])
    pal["strings"] = pal[mapping["strings"]]
    pal = vp.signature(pal, mapping["lead"], dark, {"halo": .10, "halo2": .18, "region": .26, "glow": .45, "overlay": .055})
    colors = {k: [to_hex(*v), to_hex(*v).lower(), "black"] for k, v in pal.items()}
    refs = {"grey": "base5", "highlight": mapping["lead"], "vertical-bar": "base3", "builtin": mapping["builtin"], "constants": mapping["constants"],
            "functions": mapping["functions"], "keywords": mapping["keywords"], "methods": mapping["function_call"], "operators": "base6",
            "type": mapping["type"], "variables": "fg", "numbers": mapping["constants"], "error": "red", "warning": "orange", "success": "green",
            "vc-modified": "yellow", "vc-added": "green", "vc-deleted": "red"}
    for k, r in refs.items():
        colors.setdefault(k, {"ref": r})
    return colors


def schema(mapping):
    m = mapping
    return {"v2": True, "lead": m["lead"], "modeline_bg": "bg-alt", "vertico_bg": "halo2", "function_call": m["function_call"],
            "property": m["property"], "preprocessor": m["preprocessor"], "escape": m["escape"], "modeline_modified": "orange",
            "rainbow": [m["lead"], m["keywords"], m["function_call"], "orange", m["builtin"], "magenta"],
            "outline": [m["lead"], m["keywords"], m["function_call"], m["builtin"]], "orderless": [m["lead"], m["keywords"], "orange"],
            "magit_branch_local": "blue", "magit_branch_remote": "teal", "org_todo": "orange", "org_done": "green"}


def emit(theme, colors, sch):
    faces = g._load_decl("faces.json")
    body = "\n".join(g.emit_face(n, g.spec_to_attrs(fs, colors, sch)) for n, fs in faces.items())
    text = (g.ELISP_FILE_HEADER.format(file=f"{theme}-theme.el", short=theme, theme=theme, docstring=theme, commentary=";; lab")
            + body + g.ELISP_FILE_FOOTER.format(file=f"{theme}-theme.el", theme=theme, variables=""))
    (THEMES / f"{theme}-theme.el").write_text(text)


def render(theme, light):
    env = dict(os.environ, R_THEME=theme, R_OUT=str(OUT / f"{theme}.json"), R_PATH=str(THEMES), R_DIR=str(ROOT / "tools/preview"), R_PY=str(ROOT / "docs/sample.py"))
    env.pop("R_LIGHT", None)
    if light:
        env["R_LIGHT"] = "1"
    subprocess.run(["emacs", "-Q", "--batch", "-l", str(ROOT / "tools/preview/render.el")], env=env, capture_output=True)
    return json.loads((OUT / f"{theme}.json").read_text())


def card(theme, d):
    f = lambda n, k: (d["faces"].get(n) or {}).get(k)
    bg, fg = f("default", "bg"), f("default", "fg"); hl = f("hl-line", "bg") or bg; cur = f("cursor", "bg") or fg
    rows = []
    for i, (h, lbg) in enumerate(d["py"][13:32], 1):
        is_cur = i == 15
        num = f'<span style="color:{f("line-number-current-line", "fg") if is_cur else f("line-number", "fg")}">{i:>2} </span>'
        if is_cur:
            h = h.replace('<span style="">    ', f'<span style="">    </span><span style="background:{cur};color:{bg}">&nbsp;</span><span style="">', 1)
        rows.append(f'<div class="r" style="{"background:" + (lbg or hl) if (lbg or is_cur) else ""}">{num}{h or "&nbsp;"}</div>')
    ml = (d["faces"].get("mode-line") or {}).get("style", "")
    return (f'<figure><div class="code" style="background:{bg};color:{fg}">{"".join(rows)}</div>'
            f'<div class="ml" style="{ml}"><span class="bar" style="background:{f("doom-modeline-bar", "bg") or cur}"></span><b>{theme}</b></div></figure>')


def main():
    cards = {"dark": [], "light": []}
    for src_name, modes in candidates().items():
        for mode, src in modes.items():
            for map_name, mapping in MAPPINGS.items():
                theme = f"lab-{src_name}-{map_name}-{mode}"
                emit(theme, palette(src, mode, mapping), schema(mapping))
                cards[mode].append(card(theme, render(theme, mode == "light")))
    for mode in ["dark", "light"]:
        env = dict(os.environ, R_THEME=f"lumina-vesper-{mode}", R_OUT=str(OUT / f"ref-{mode}.json"), R_PATH=str(ROOT / "emacs/themes"),
                   R_DIR=str(ROOT / "tools/preview"), R_PY=str(ROOT / "docs/sample.py"))
        env.pop("R_LIGHT", None)
        if mode == "light":
            env["R_LIGHT"] = "1"
        subprocess.run(["emacs", "-Q", "--batch", "-l", str(ROOT / "tools/preview/render.el")], env=env, capture_output=True)
        cards[mode].insert(0, card(f"lumina-vesper-{mode} (actuel)", json.loads((OUT / f"ref-{mode}.json").read_text())))
    page = """<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Lumina palette lab</title><style>
body{margin:0;padding:20px 14px;background:#2a2a2a;color:#ddd;font:14px/1.4 -apple-system,system-ui,sans-serif} h1{font-weight:600;margin:0 0 4px} p{color:#aaa;margin:0 0 14px;max-width:90ch}
h2{font-weight:500;color:#bbb;margin:22px 0 8px} .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(560px,1fr));gap:14px}
figure{margin:0} .code{font:12.5px/1.5 "JetBrains Mono",Menlo,monospace;padding:6px 0;border-radius:6px 6px 0 0;overflow:hidden} .r{white-space:pre;padding:0 8px;min-height:1.5em}
.ml{display:flex;align-items:center;gap:8px;font:11.5px Menlo,monospace;padding:5px 8px 5px 0;border-radius:0 0 6px 6px} .bar{width:3px;align-self:stretch}
</style></head><body><h1>Lumina palette lab</h1><p>Sources publiques composées ici : Radix Colors (pas 11 sur mauve ou slate), Tailwind v4 (300 sur slate ou zinc 900 ; 700 sur 50), Open Color (3 sur gray-9 ; 8 sur gray-0). Affectations : <b>indigo</b> = fonctions indigo, mots-clés violet, types ciel ; <b>gold</b> = fonctions ambre, mots-clés indigo, types violet ; <b>teal</b> = fonctions sarcelle, mots-clés violet, types indigo. Chaînes vertes, constantes orange partout. Rendu par Emacs.</p>"""
    for mode in ["dark", "light"]:
        page += f'<h2>{"Sombre" if mode == "dark" else "Clair"}</h2><div class="grid">' + "".join(cards[mode]) + '</div>'
    (ROOT / "docs/explore.html").write_text(page + "</body></html>")
    print("ok", sum(len(v) for v in cards.values()), "cards -> docs/explore.html")


if __name__ == "__main__":
    main()
