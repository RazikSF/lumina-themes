"""Build docs/showcase.html: one full-interface mock per theme, every colour read from
the faces Emacs computed (tools/preview/render.el).  Layout only is drawn here."""
import html, json, sys
from pathlib import Path

GAL, ROOT = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(ROOT / "generators"))
import lumina_gen as g

SPEC = json.loads(g.SPEC.read_text())["flavors"]
ORDER = ["vesper", "dawn", "oxblood", "tide", "canopy", "slate", "nocturne", "amethyst", "prisma"]
MODES = ["dark", "light", "dark-ink", "light-ink"]


def load(t):
    return json.loads((GAL / f"{t}.json").read_text())


class T:
    def __init__(self, d):
        self.d = d
    def st(self, f):
        return (self.d["faces"].get(f) or {}).get("style") or ""
    def fg(self, f, dflt=None):
        return (self.d["faces"].get(f) or {}).get("fg") or dflt
    def bg(self, f, dflt=None):
        return (self.d["faces"].get(f) or {}).get("bg") or dflt
    def span(self, f, text, extra=""):
        return f'<span style="{self.st(f)}{extra}">{html.escape(text)}</span>'


def code_window(t, lines, cur, numbers=True, dim=False, diffmarks=()):
    bg, fg = t.bg("default"), t.fg("default")
    if dim:
        bg = t.bg("auto-dim-other-buffers-face", bg)
    hl = t.bg("hl-line", bg); cb = t.bg("cursor", fg)
    out = [f'<div class="win" style="background:{bg};color:{fg}">']
    for i, (h, lbg) in enumerate(lines, 1):
        is_cur = i == cur
        rowbg = lbg or (hl if is_cur and not dim else None)
        mark = ""
        if i in diffmarks:
            face = {1: "diff-hl-insert", 2: "diff-hl-change", 3: "diff-hl-delete"}[diffmarks[i]]
            mark = f'<span class="dh" style="background:{t.fg(face)}"></span>'
        num = ""
        if numbers:
            nf = "line-number-current-line" if is_cur else "line-number"
            num = f'<span class="ln" style="{t.st(nf)}">{i:>3}</span>'
        if is_cur:
            h = h.replace('<span style="">    ', f'<span style="">    </span><span style="background:{cb};color:{bg}">&nbsp;</span><span style="">', 1)
        if i == cur + 1:
            h += t.span("eglot-inlay-hint-face", "  : float")
        if i == cur + 3 and h:
            h = h.replace('</span>', f'</span>', 1)
            h += f'<span style="{t.st("flycheck-warning").replace("text-decoration","text-decoration")}"> </span>'
        out.append(f'<div class="row" style="{"background:"+rowbg if rowbg else ""}"><span class="fr">{mark}</span>{num}'
                   f'<span class="txt">{h or "&nbsp;"}</span></div>')
    out.append('</div>')
    return "".join(out)


def modeline(t, active, name, mode, meow="normal", modified=False):
    f = "mode-line" if active else "mode-line-inactive"
    bar = t.bg("doom-modeline-bar") if active else t.bg("mode-line-inactive", t.bg("default"))
    st = t.st(f)
    parts = [f'<span class="bar" style="background:{bar}"></span>']
    if active:
        parts.append(t.span(f"meow-{meow}-indicator", {"normal": "NORMAL", "insert": "INSERT", "keypad": "KEYPAD", "motion": "MOTION", "beacon": "BEACON"}[meow]))
        parts.append(t.span("doom-modeline-buffer-path", "lumina/") + t.span("doom-modeline-buffer-file", name))
        if modified:
            parts.append(t.span("doom-modeline-buffer-modified", "●"))
    else:
        parts.append(f"<span>{html.escape(name)}</span>")
    parts.append('<span class="sp"></span>')
    if active:
        parts.append(t.span("doom-modeline-lsp-success", "LSP ✓"))
        parts.append(t.span("doom-modeline-info", "✔ 0") + " " + t.span("doom-modeline-warning", "⚠ 2"))
    parts.append(t.span("doom-modeline-buffer-major-mode", mode))
    parts.append("<span>12:4</span>")
    return f'<div class="ml" style="{st}">{"".join(parts)}</div>'


def tabbar(t):
    return (f'<div class="tb" style="{t.st("tab-bar")}">'
            + t.span("tab-bar-tab-inactive", " main ") + t.span("tab-bar-tab", " limiter.py ")
            + t.span("tab-bar-tab-inactive", " carnet.org ") + t.span("tab-bar-tab-inactive", " *magit* ") + '</div>')


def headerline(t):
    sep = t.span("lsp-headerline-breadcrumb-separator-face", " › ")
    return (f'<div class="hl" style="{t.st("header-line")}">' + t.span("lsp-headerline-breadcrumb-project-prefix-face", "lumina")
            + sep + t.span("lsp-headerline-breadcrumb-path-face", "src") + sep + t.span("lsp-headerline-breadcrumb-path-face", "limiter.py")
            + sep + t.span("lsp-headerline-breadcrumb-symbols-face", "TokenBucket") + sep
            + t.span("lsp-headerline-breadcrumb-symbols-face", "try_consume") + '</div>')


def treemacs(t, dim):
    bg = t.bg("auto-dim-other-buffers-face", t.bg("default")) if dim else t.bg("default")
    rows = [t.span("treemacs-root-face", "▾ lumina"),
            "  " + t.span("treemacs-directory-face", "▾ src"),
            "      " + t.span("treemacs-file-face", "limiter.py"),
            "      " + t.span("treemacs-git-modified-face", "bucket.py"),
            "      " + t.span("treemacs-git-untracked-face", "scratch.py"),
            "  " + t.span("treemacs-directory-face", "▸ docs"),
            "  " + t.span("treemacs-git-added-face", "README.md"),
            "  " + t.span("treemacs-file-face", "Makefile")]
    return f'<div class="tree" style="background:{bg};color:{t.fg("default")}">' + "".join(f'<div>{r}</div>' for r in rows) + '</div>'


def minibuffer(t):
    bg = t.bg("solaire-default-face") or t.bg("default")
    o = [t.st("orderless-match-face-0"), t.st("orderless-match-face-1")]
    rows = [("group", t.span("vertico-group-title", "Buffers") + f'<span style="{t.st("vertico-group-separator")}"> ────────────────────────────</span>'),
            ("cur", f'<span style="{o[0]}">lim</span>iter.py <span style="{o[1]}">tok</span>en' + t.span("marginalia-mode", "   Python") + t.span("marginalia-file-name", "  ~/lumina/src/limiter.py")),
            ("", f'<span style="{o[0]}">lim</span>its.org  <span style="{o[1]}">tok</span>ens' + t.span("marginalia-mode", "   Org") + t.span("marginalia-date", "  2 min ago")),
            ("group", t.span("vertico-group-title", "Files") + f'<span style="{t.st("vertico-group-separator")}"> ──────────────────────────────</span>'),
            ("", f'<span style="{o[0]}">lim</span>e/<span style="{o[1]}">tok</span>enizer.py' + t.span("marginalia-documentation", "   Split a stream into tokens")),
            ("", f'README.<span style="{o[0]}">lim</span>' + t.span("marginalia-documentation", "   Rate limiter notes")),
            ]
    s = f'<div class="mini" style="background:{bg};color:{t.fg("default")}"><div>' + t.span("minibuffer-prompt", "Switch to buffer: ") + 'lim tok' + f'<span style="background:{t.bg("cursor")}">&nbsp;</span></div>'
    for kind, r in rows:
        style = f'background:{t.bg("vertico-current")};' if kind == "cur" else ""
        s += f'<div class="row" style="{style}">{r}</div>'
    return s + "</div>"


def corfu(t):
    rows = [("", "tokens", "float"), ("cur", "try_consume", "method"), ("", "refill_rate", "float"), ("", "capacity", "float"), ("", "last_refill", "float")]
    s = f'<div class="corfu" style="background:{t.bg("corfu-default")};color:{t.fg("corfu-default", t.fg("default"))};border:1px solid {t.bg("corfu-border")}">'
    for kind, a, b in rows:
        style = f'background:{t.bg("corfu-current")};' if kind == "cur" else ""
        s += f'<div class="row" style="{style}"><span style="{t.st("completions-common-part")}">t</span>{html.escape(a[1:])}' + t.span("corfu-annotations", f"  {b}") + '</div>'
    s += f'<div class="cbar" style="background:{t.bg("corfu-bar")}"></div></div>'
    return s


def whichkey(t):
    bg = t.bg("solaire-default-face") or t.bg("default")
    k = lambda key, desc, grp=False: (t.span("which-key-key-face", key) + t.span("which-key-separator-face", " → ")
                                       + (t.span("which-key-group-description-face", "+" + desc) if grp else t.span("which-key-command-description-face", desc)))
    cells = [k("b", "buffer", True), k("f", "file", True), k("g", "git", True), k("s", "search", True),
             k("SPC", "find file"), k(":", "M-x"), k("w", "window", True), k("q", "quit", True)]
    return f'<div class="wk" style="background:{bg};color:{t.fg("default")}">' + "".join(f'<span class="cell">{c}</span>' for c in cells) + '</div>'


def magit(t):
    bg = t.bg("default")
    rows = [t.span("magit-section-heading", "Head:     ") + t.span("magit-branch-current", " main ") + "  " + t.span("git-commit-summary", "Lumina: full interface coverage"),
            t.span("magit-section-heading", "Merge:    ") + t.span("magit-branch-remote", "origin/main") + "  " + t.span("magit-tag", "v2.1") + "  " + t.span("magit-hash", "1f31347") + " " + t.span("magit-log-author", "razik") + " " + t.span("magit-log-date", "2 days ago"),
            "", t.span("magit-section-heading", "Unstaged changes (1)")]
    s = f'<div class="mg" style="background:{bg};color:{t.fg("default")}">' + "".join(f'<div class="row">{r or "&nbsp;"}</div>' for r in rows)
    for h, lbg in t.d["diff"][:12]:
        s += f'<div class="row" style="{"background:"+lbg if lbg else ""}">{h or "&nbsp;"}</div>'
    return s + "</div>"


def strips(t):
    bg = t.bg("default")
    org = (t.span("org-modern-todo", " TODO ") + " " + t.span("org-level-2", "Relire le chapitre") + " " + t.span("org-modern-priority", " A ") + "  "
           + t.span("org-modern-tag", " maths ") + " " + t.span("org-modern-date-active", " 2026-10-12 lun ") + "    "
           + t.span("org-modern-done", " DONE ") + " " + t.span("org-headline-done", "Corriger les copies") + "   "
           + t.span("org-code", "~code~") + " " + t.span("org-verbatim", "=verb=") + " " + t.span("org-checkbox", "[X]"))
    tr = (t.span("transient-heading", "Arguments") + "  " + t.span("transient-key", "-f") + " " + t.span("transient-argument", "--force-with-lease")
          + "  " + t.span("transient-key", "-u") + " " + t.span("transient-inactive-value", "--set-upstream") + "   "
          + t.span("transient-heading", "Push to") + "  " + t.span("transient-key", "p") + " " + t.span("transient-value", "origin/main")
          + "  " + t.span("transient-key-exit", "q") + " quit")
    ansi = "".join(f'<span class="sw" style="background:{t.fg(f"ansi-color-{c}")}"></span>' for c in ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"])
    sh = (t.span("eshell-prompt", "~/lumina λ ") + "make verify  " + ansi + "   " + t.span("compilation-info", "OK") + " "
          + t.span("compilation-warning", "warning") + " " + t.span("compilation-error", "error") + "   " + t.span("hl-todo", "TODO") + " "
          + t.span("help-key-binding", " C-c C-c ") + " " + t.span("avy-lead-face", " a ") + t.span("avy-lead-face-0", " s "))
    dired = ("".join(t.span(f, x) for f, x in [("diredfl-dir-priv", "d"), ("diredfl-read-priv", "r"), ("diredfl-write-priv", "w"), ("diredfl-exec-priv", "x"), ("diredfl-read-priv", "r"), ("diredfl-no-priv", "-"), ("diredfl-exec-priv", "x")])
             + "  " + t.span("diredfl-number", "4096") + " " + t.span("diredfl-date-time", "Oct 11 09:12") + "  " + t.span("dired-directory", "src/")
             + "      " + t.span("diredfl-file-name", "limiter") + t.span("diredfl-file-suffix", ".py") + "   " + t.span("nerd-icons-blue", "") + " "
             + t.span("nerd-icons-green", "") + " " + t.span("nerd-icons-yellow", "") + " " + t.span("nerd-icons-red", "") + " " + t.span("nerd-icons-purple", "") + " " + t.span("nerd-icons-cyan", ""))
    mail = (f'<span style="{t.st("mu4e-header-highlight-face")}">' + t.span("mu4e-unread-face", "  Conseil de classe   ") + t.span("mu4e-header-face", "M. Dupont   lun 10:12  ") + '</span>'
            + "  " + t.span("elfeed-search-date-face", "2026-10-11") + " " + t.span("elfeed-search-unread-title-face", "Emacs 30.2 released") + " "
            + t.span("elfeed-search-feed-face", "emacs-news") + " " + t.span("elfeed-search-tag-face", "(emacs)"))
    return f'<div class="strips" style="background:{bg};color:{t.fg("default")}">' + "".join(f'<div class="row">{r}</div>' for r in [org, tr, sh, dired, mail]) + '</div>'


def card(theme):
    t = T(load(theme))
    py = [tuple(x) for x in t.d["py"][13:31]]
    org = [tuple(x) for x in t.d["org"]]
    return (f'<section id="{theme}"><h3>{theme}</h3><div class="frame">'
            + tabbar(t) + headerline(t)
            + '<div class="cols">' + treemacs(t, True)
            + '<div class="col">' + '<div class="rel">' + code_window(t, py, 15, diffmarks={3: 2, 7: 1, 8: 1, 12: 3}) + corfu(t) + '</div>'
            + modeline(t, True, "limiter.py", "Python", "normal", True) + '</div>'
            + '<div class="col">' + code_window(t, org, 0, numbers=False, dim=True) + modeline(t, False, "carnet.org", "Org") + '</div>'
            + '</div>' + magit(t) + strips(t) + whichkey(t) + minibuffer(t) + '</div></section>')


themes = [f"lumina-{fl}-{m}" for fl in ORDER for m in MODES if (GAL / f"lumina-{fl}-{m}.json").exists()]
body = "".join(card(th) for th in themes)
nav = " · ".join(f'<a href="#{th}">{th.replace("lumina-", "")}</a>' for th in themes)
page = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lumina showcase</title><style>
body{{margin:0;padding:24px 16px;background:#202020;color:#ddd;font:15px/1.4 -apple-system,system-ui,sans-serif}}
h1{{font-weight:600;margin:0 0 4px}} p.note{{margin:0 0 14px;color:#aaa;max-width:80ch}} nav{{font-size:13px;color:#888;margin-bottom:22px}} nav a{{color:#bbb;text-decoration:none}}
section h3{{margin:26px 0 6px;font-weight:500;font-size:14px;color:#ccc}}
.frame{{max-width:1180px;font:13px/1.55 "Zed Mono","JetBrains Mono",Menlo,monospace;overflow:hidden;border-radius:6px}}
.tb,.hl,.ml,.wk{{display:flex;align-items:center;gap:8px;padding:3px 8px;white-space:pre}} .tb span{{padding:2px 6px}}
.cols{{display:grid;grid-template-columns:150px 1fr 1fr}} .col{{display:flex;flex-direction:column;min-width:0}} .rel{{position:relative;flex:1;display:flex;flex-direction:column}}
.win{{padding:4px 0;overflow:hidden;flex:1}} .row{{white-space:pre;min-height:1.55em;padding-right:6px;display:flex}} .fr{{display:inline-block;width:8px;position:relative}}
.dh{{position:absolute;left:1px;top:2px;bottom:2px;width:3px}} .ln{{display:inline-block;padding:0 8px 0 4px;min-width:28px;text-align:right}} .txt{{padding-left:6px}}
.tree{{padding:6px 8px;white-space:pre;font-size:12.5px}} .tree div{{min-height:1.55em}}
.ml{{font-size:12px;padding:5px 8px 5px 0}} .bar{{width:3px;align-self:stretch;margin-right:4px}} .sp{{flex:1}}
.corfu{{position:absolute;left:190px;top:175px;width:300px;font-size:12.5px;box-shadow:0 2px 10px rgba(0,0,0,.25)}} .corfu .row{{padding:0 8px}} .cbar{{position:absolute;right:0;top:4px;width:3px;height:40%}}
.mg,.strips,.mini{{padding:6px 10px}} .mg .row,.strips .row,.mini .row,.mini div{{white-space:pre;display:block}} .mini .row{{padding:0 6px}}
.wk{{flex-wrap:wrap;gap:4px 22px;padding:6px 12px;font-size:12.5px}} .sw{{display:inline-block;width:14px;height:14px;vertical-align:middle;margin-right:2px}}
@media (max-width:900px){{.cols{{grid-template-columns:1fr}} .tree{{display:none}} .corfu{{left:40px}}}}
</style></head><body><h1>Lumina showcase</h1>
<p class="note">Maquette d'interface complète par thème : chaque couleur et attribut provient des faces calculées par GNU Emacs 30.2 (emacs -Q, thème chargé, fontification réelle de python-mode, org-mode et diff-mode). Seule la mise en page est dessinée ici.</p>
<nav>{nav}</nav>{body}</body></html>"""
(ROOT / "docs" / "showcase.html").write_text(page)
print("ok", len(themes), "themes ->", ROOT / "docs" / "showcase.html")
