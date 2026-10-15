#!/usr/bin/env python3
"""Lumina theme generator (palette-first, declarative).

Three layers of source of truth:

  spec/lumina.json           palette + helpers + commentary per flavor/mode
  SCHEMAS (this file)        per-flavor face design (lead, rainbow/outline/
                             orderless sequences, modeline_bg, vertico_bg,
                             function-call/property/preprocessor/escape,
                             magit/org/modeline-modified) shared dark/light
  spec/faces.json            face name -> {fg, bg, weight, slant, ...}  (Emacs)
                             written by generators/faces_src.py
  spec/variables.json        theme variables: hl-todo, vc-annotate, ... (Emacs)
  spec/nvim_highlights.json  highlight group -> {fg, bg, sp, link, ...} (Nvim)
  spec/vscode.json           workbench colors + tokenColors + semantic     (VS Code)

The generator is a thin resolver: each face/group/color slot in the
declarative specs references a palette name ("blue", "comments"), a
schema slot ("schema.lead", "schema.modeline_bg"), or a schema array
slot ("schema.rainbow[2]"), optionally with an alpha suffix ("yellow@55").
`resolve_ref` turns any of these into a literal "#rrggbb" (or "#rrggbbaa")
per flavor.  All three emitters are tiny iterators over their declarative
spec; adjusting any face is one JSON edit propagated to the 14 themes.

Usage:
    python3 generators/lumina_gen.py extract   # bootstrap palette spec from .el
    python3 generators/lumina_gen.py build      # spec -> all targets
    python3 generators/lumina_gen.py all        # extract then build
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
SPEC = ROOT / "spec" / "lumina.json"
DOOM_THEMES = Path.home() / ".doom.d" / "themes"

FLAVORS = ["dawn", "oxblood", "tide", "canopy", "slate"]

# ---------------------------------------------------------------------------
# Per-flavour syntax schema (face design intent, shared dark/light).
# ---------------------------------------------------------------------------
SCHEMAS = {
    "vesper": {"v2": True, "lead": "blue", "fg_min": {"dark": 7.5, "light": 8}, "comments_min": {"dark": 2.8, "light": 4.3}, "accent_bg_min": {"dark": 3.3, "light": 4.0}, "spread": {"dark": .22, "light": .13},
               "modeline_bg": "bg-alt", "vertico_bg": "halo2", "function_call": "blue", "property": "rose", "preprocessor": "violet", "escape": "orange", "modeline_modified": "orange",
               "rainbow": ["blue", "magenta", "cyan", "orange", "yellow", "violet"], "outline": ["blue", "magenta", "cyan", "yellow"], "orderless": ["blue", "magenta", "orange"],
               "magit_branch_local": "cyan", "magit_branch_remote": "violet", "org_todo": "orange", "org_done": "green"},
    "sienne": {"v2": True, "lead": "teal", "warm_family": True, "fg_min": 8, "comments_min": {"dark": 2.8, "light": 4.3}, "accent_min": {"dark": 3.6, "light": 4.5}, "accent_bg_min": {"dark": 3.3, "light": 4.0}, "spread": {"dark": .21, "light": .14},
               "modeline_bg": "bg-alt", "vertico_bg": "halo2", "function_call": "teal", "property": "orange", "preprocessor": "magenta", "escape": "orange", "modeline_modified": "orange",
               "rainbow": ["teal", "magenta", "yellow", "orange", "green", "violet"], "outline": ["teal", "magenta", "yellow", "green"], "orderless": ["teal", "magenta", "orange"],
               "magit_branch_local": "cyan", "magit_branch_remote": "violet", "org_todo": "orange", "org_done": "green"},
    "dawn": {"v2": True, "lead": "yellow", "fg_min": 8, "modeline_bg": "bg-alt", "vertico_bg": "halo2", "function_call": "blue", "property": "blue", "preprocessor": "teal", "escape": "magenta", "modeline_modified": "orange", "rainbow": ["yellow", "teal", "blue", "magenta", "cyan", "violet"], "outline": ["yellow", "teal", "blue", "cyan"], "orderless": ["yellow", "teal", "magenta"], "magit_branch_local": "blue", "magit_branch_remote": "teal", "org_todo": "orange", "org_done": "green"},
    "oxblood": {"v2": True, "lead": "magenta", "fg_min": 8, "modeline_bg": "bg-alt", "vertico_bg": "halo2", "function_call": "cyan", "property": "cyan", "preprocessor": "blue", "escape": "teal", "modeline_modified": "orange", "rainbow": ["magenta", "blue", "orange", "teal", "green", "cyan"], "outline": ["magenta", "blue", "orange", "green"], "orderless": ["magenta", "blue", "teal"], "magit_branch_local": "blue", "magit_branch_remote": "teal", "org_todo": "orange", "org_done": "green"},
    "tide": {"v2": True, "lead": "cyan", "fg_min": 8, "modeline_bg": "bg-alt", "vertico_bg": "halo2", "function_call": "violet", "property": "violet", "preprocessor": "teal", "escape": "orange", "modeline_modified": "orange", "rainbow": ["cyan", "teal", "violet", "orange", "green", "magenta"], "outline": ["cyan", "teal", "violet", "green"], "orderless": ["cyan", "teal", "orange"], "magit_branch_local": "blue", "magit_branch_remote": "teal", "org_todo": "orange", "org_done": "green"},
    "canopy": {"v2": True, "lead": "green", "fg_min": 8, "modeline_bg": "bg-alt", "vertico_bg": "halo2", "function_call": "yellow", "property": "yellow", "preprocessor": "blue", "escape": "magenta", "modeline_modified": "orange", "rainbow": ["green", "blue", "yellow", "magenta", "cyan", "violet"], "outline": ["green", "blue", "yellow", "cyan"], "orderless": ["green", "blue", "magenta"], "magit_branch_local": "blue", "magit_branch_remote": "teal", "org_todo": "orange", "org_done": "green"},
    "slate": {"v2": True, "lead": "blue", "fg_min": 8, "modeline_bg": "bg-alt", "vertico_bg": "halo2", "function_call": "yellow", "property": "cyan", "preprocessor": "cyan", "escape": "magenta", "modeline_modified": "orange", "rainbow": ["blue", "cyan", "yellow", "magenta", "green", "violet"], "outline": ["blue", "cyan", "yellow", "green"], "orderless": ["blue", "cyan", "magenta"], "magit_branch_local": "cyan", "magit_branch_remote": "teal", "org_todo": "orange", "org_done": "green"},
    "indigo": {"v2": True, "lead": "blue", "fg_min": 8, "warm_family": True,
               "modeline_bg": "bg-alt", "vertico_bg": "halo2", "function_call": "ink-light", "property": "ink-mid", "preprocessor": "violet", "escape": "orange", "modeline_modified": "orange",
               "rainbow": ["blue", "orange", "violet", "cyan", "yellow", "magenta"], "outline": ["blue", "violet", "cyan", "orange"], "orderless": ["blue", "orange", "violet"],
               "magit_branch_local": "cyan", "magit_branch_remote": "violet", "org_todo": "orange", "org_done": "green"},
    "azur": {"v2": True, "lead": "blue", "fg_min": 8, "warm_family": True,
             "modeline_bg": "bg-alt", "vertico_bg": "halo2", "function_call": "orange", "property": "violet", "preprocessor": "violet", "escape": "yellow", "modeline_modified": "orange",
             "rainbow": ["blue", "orange", "violet", "yellow", "teal", "green"], "outline": ["blue", "orange", "violet", "teal"], "orderless": ["blue", "orange", "yellow"],
             "magit_branch_local": "cyan", "magit_branch_remote": "violet", "org_todo": "orange", "org_done": "green"},
    "nocturne": {"v2": True, "lead": "orange", "fg_min": 8, "modeline_bg": "bg-alt", "vertico_bg": "halo2", "function_call": "cyan", "property": "cyan", "preprocessor": "blue", "escape": "magenta", "modeline_modified": "yellow", "rainbow": ["orange", "blue", "cyan", "magenta", "green", "violet"], "outline": ["orange", "blue", "cyan", "green"], "orderless": ["orange", "blue", "magenta"], "magit_branch_local": "blue", "magit_branch_remote": "teal", "org_todo": "yellow", "org_done": "green"},
    "amethyst": {"v2": True, "lead": "yellow", "fg_min": 8, "modeline_bg": "bg-alt", "vertico_bg": "halo2", "function_call": "cyan", "property": "green", "preprocessor": "magenta", "escape": "blue", "modeline_modified": "orange", "rainbow": ["yellow", "magenta", "cyan", "blue", "green", "violet"], "outline": ["yellow", "magenta", "green", "cyan"], "orderless": ["yellow", "magenta", "cyan"], "magit_branch_local": "blue", "magit_branch_remote": "teal", "org_todo": "orange", "org_done": "green"},
    "prisma": {"v2": True, "lead": "spark", "fg_min": 8, "modeline_bg": "bg-alt", "vertico_bg": "halo2", "function_call": "teal", "property": "cyan", "preprocessor": "green", "escape": "orange", "modeline_modified": "orange", "rainbow": ["red", "orange", "yellow", "green", "blue", "violet"], "outline": ["spark", "green", "teal", "cyan"], "orderless": ["spark", "green", "orange"], "magit_branch_local": "blue", "magit_branch_remote": "teal", "org_todo": "orange", "org_done": "green"},
    "sirocco": {"v2": True, "lead": "cyan", "fg_min": 8, "warm_family": True, "modeline_bg": "bg-alt", "vertico_bg": "halo2", "function_call": "green", "property": "blue", "preprocessor": "orange", "escape": "cyan", "modeline_modified": "orange", "rainbow": ["cyan", "orange", "green", "magenta", "blue", "yellow"], "outline": ["cyan", "orange", "green", "magenta"], "orderless": ["cyan", "orange", "magenta"], "magit_branch_local": "cyan", "magit_branch_remote": "green", "org_todo": "orange", "org_done": "green"},
    "celadon": {"v2": True, "lead": "orange", "fg_min": 8, "modeline_bg": "bg-alt", "vertico_bg": "halo2", "function_call": "green", "property": "blue", "preprocessor": "cyan", "escape": "orange", "modeline_modified": "orange", "rainbow": ["orange", "cyan", "green", "magenta", "blue", "violet"], "outline": ["orange", "cyan", "green", "magenta"], "orderless": ["orange", "cyan", "magenta"], "magit_branch_local": "blue", "magit_branch_remote": "green", "org_todo": "orange", "org_done": "green"},
    "sumi": {"v2": True, "lead": "green", "fg_min": 8, "modeline_bg": "bg-alt", "vertico_bg": "halo2", "function_call": "magenta", "property": "cyan", "preprocessor": "orange", "escape": "orange", "modeline_modified": "yellow", "rainbow": ["green", "orange", "magenta", "cyan", "blue", "violet"], "outline": ["green", "orange", "cyan", "magenta"], "orderless": ["green", "orange", "cyan"], "magit_branch_local": "blue", "magit_branch_remote": "green", "org_todo": "orange", "org_done": "green"},
    "pivoine": {"v2": True, "lead": "teal", "fg_min": 8, "modeline_bg": "bg-alt", "vertico_bg": "halo2", "function_call": "blue", "property": "cyan", "preprocessor": "magenta", "escape": "orange", "modeline_modified": "orange", "rainbow": ["teal", "magenta", "blue", "cyan", "orange", "violet"], "outline": ["teal", "magenta", "blue", "cyan"], "orderless": ["teal", "magenta", "blue"], "magit_branch_local": "blue", "magit_branch_remote": "teal", "org_todo": "orange", "org_done": "teal"},
}


# ---------------------------------------------------------------------------
# Bootstrap: read palette + commentary from the original def-doom-theme files
# in ~/.doom.d/themes/doom-lumina-*-theme.el .  Only used for `extract`.
# ---------------------------------------------------------------------------
def el_name(flavor: str, mode: str) -> str:
    return f"lumina-{flavor}-{mode}"


def old_el_path(flavor: str, mode: str) -> Path:
    if flavor == "dawn":
        sym = "doom-lumina-dawn-dark" if mode == "dark" else "doom-lumina-dawn"
    else:
        suffix = "dark" if mode == "dark" else "light"
        sym = f"doom-lumina-{flavor}-{suffix}"
    return DOOM_THEMES / f"{sym}-theme.el"


TRIPLET = re.compile(
    r'^\s*\((\S+)\s+\'\("(#[0-9A-Fa-f]{6})"\s+"([^"]+)"\s+"([^"]+)"\s*\)\)\s*$'
)
SYMREF = re.compile(r'^\s*\((\S+)\s+([A-Za-z][A-Za-z0-9-]*)\)\s*$')

PALETTE_KEYS = [
    "bg", "fg", "bg-alt", "fg-alt",
    "base0", "base1", "base2", "base3", "base4",
    "base5", "base6", "base7", "base8",
    "grey",
    "red", "orange", "green", "teal", "yellow", "blue",
    "dark-blue", "magenta", "violet", "cyan", "dark-cyan",
]
HELPER_KEYS = [
    "highlight", "vertical-bar", "selection", "builtin", "comments",
    "doc-comments", "constants", "functions", "keywords", "methods",
    "operators", "type", "strings", "variables", "numbers", "region",
    "error", "warning", "success", "vc-modified", "vc-added", "vc-deleted",
]


def lift_commentary(text: str) -> str:
    lines = text.split("\n")
    try:
        start = next(i for i, ln in enumerate(lines) if ln.startswith(";;; Commentary:"))
        end = next(i for i, ln in enumerate(lines) if ln.startswith(";;; Code:"))
    except StopIteration:
        return ""
    body = []
    for ln in lines[start + 1:end]:
        s_ = ln.strip()
        if not s_ or s_ == ";;":
            continue
        body.append(s_[3:] if s_.startswith(";; ") else s_.lstrip(";").lstrip())
    return "\n".join(body).strip()


def extract():
    out = {"family": "lumina", "flavors": {}}
    for flavor in FLAVORS:
        out["flavors"][flavor] = {}
        for mode in ("dark", "light"):
            p = old_el_path(flavor, mode)
            text = p.read_text()
            lines = text.split("\n")
            start = next(i for i, ln in enumerate(lines) if "((bg" in ln)
            close = next(
                i for i in range(start, len(lines))
                if "-modeline-pad" in lines[i] and ")))" in lines[i + 2]
            ) + 2
            colors = {}
            for ln in lines[start:close + 1]:
                if "-modeline-pad" in ln:
                    continue
                probe = ln.replace("((", "(", 1) if "((bg" in ln else ln
                m = TRIPLET.match(probe)
                if m:
                    colors[m.group(1)] = [m.group(2), m.group(3), m.group(4)]
                    continue
                m = SYMREF.match(probe)
                if m and m.group(1) in PALETTE_KEYS + HELPER_KEYS:
                    colors[m.group(1)] = {"ref": m.group(2)}
            out["flavors"][flavor][mode] = {
                "theme": el_name(flavor, mode),
                "background": "dark" if mode == "dark" else "light",
                "schema": flavor,
                "colors": colors,
                "commentary": lift_commentary(text),
            }
    SPEC.parent.mkdir(parents=True, exist_ok=True)
    SPEC.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"extracted -> {SPEC.relative_to(ROOT)}  ({len(FLAVORS)} flavors x2)")


# ---------------------------------------------------------------------------
# Resolution: turn a string ref into a literal hex against a flavour's
# colours + schema.  This is the heart of the generator.
# ---------------------------------------------------------------------------
def C(colors, key, default="#000000"):
    v = colors.get(key)
    if isinstance(v, list):
        return v[0]
    if isinstance(v, dict):
        return C(colors, v["ref"], default)
    return default


SCHEMAS["nuancier"] = {"v2": True, "lead": "orange", "fg_min": 8, "fg_max": 12.5, "modeline_bg": "bg-alt", "vertico_bg": "halo2",
                       "modeline_modified": "orange"}
SCHEMAS["aquarelle"] = dict(SCHEMAS["nuancier"])
SCHEMAS["jardin"] = dict(SCHEMAS["nuancier"])
sys.path.insert(0, str(Path(__file__).resolve().parent))
from harmony_apply import HARMONY as _HARMONY, schema_overrides as _schema_overrides
for _f in _HARMONY:
    SCHEMAS[_f].update(_schema_overrides(_f))


def schema_for(flavor: str, mode: str) -> dict:
    """The flavor's schema resolved for one mode: a {"dark": x, "light": y} value picks the mode's side."""
    return {k: (v.get(mode, v.get("dark")) if isinstance(v, dict) else v) for k, v in SCHEMAS[flavor].items()}


def resolve_ref(ref, colors, schema):
    """Resolve a string ref to a literal '#rrggbb' (optionally + alpha).

    Forms accepted:
      'bg', 'base1', 'blue', 'comments', 'region'   - palette/helper lookup
      'schema.lead', 'schema.modeline_bg'           - schema scalar slot
      'schema.rainbow[2]', 'schema.outline[0]'      - schema array slot
      '#aabbcc'                                     - literal pass-through
      Any of the above with '@AA' suffix            - append 8-digit alpha
    Non-string values are returned as-is.
    """
    if not isinstance(ref, str):
        return ref
    alpha = ""
    if "@" in ref:
        ref, alpha = ref.rsplit("@", 1)
    if ref.startswith("#"):
        return ref + alpha
    if ref.startswith("schema."):
        path = ref[len("schema."):]
        if "[" in path:
            name, rest = path.split("[", 1)
            idx = int(rest.rstrip("]"))
            target = schema[name][idx]
        else:
            target = schema[path]
        return resolve_ref(target, colors, schema) + alpha
    return C(colors, ref) + alpha


# ---------------------------------------------------------------------------
# Emacs deftheme emitter (declarative, fed by spec/faces.json).
# ---------------------------------------------------------------------------
def pretty(theme: str) -> str:
    """lumina-dawn-dark-contrast -> Lumina Dawn Dark Contrast."""
    return " ".join(w.capitalize() for w in theme.split("-"))


def emit_face(name: str, attrs: list) -> str:
    body = " ".join(f"{k} {v}" for k, v in attrs)
    return f" '({name} ((t ({body}))))"


def _color(ref, colors, schema):
    return "unspecified" if ref == "unspecified" else f'"{resolve_ref(ref, colors, schema)}"'


def spec_to_attrs(fspec: dict, colors: dict, schema: dict) -> list:
    """Turn a face spec dict (from faces.json) into emit_face's attrs list.
    Canonical order: fg, bg, weight, slant, box, underline, overline,
    strike-through, inverse, extend, inherit, height."""
    attrs = []
    if "fg" in fspec:
        attrs.append((":foreground", _color(fspec["fg"], colors, schema)))
    if "bg" in fspec:
        attrs.append((":background", _color(fspec["bg"], colors, schema)))
    if "weight" in fspec:
        attrs.append((":weight", str(fspec["weight"])))
    elif fspec.get("bold"):
        attrs.append((":weight", "bold"))
    if "slant" in fspec:
        attrs.append((":slant", str(fspec["slant"])))
    elif fspec.get("italic"):
        attrs.append((":slant", "italic"))
    if "box" in fspec:
        b = fspec["box"]
        if b is True:
            attrs.append((":box", "t"))
        else:
            w = b["width"]
            w = f"({w[0]} . {w[1]})" if isinstance(w, list) else str(w)
            s = f' :style {b["style"]}' if b.get("style") else ""
            attrs.append((":box", f'(:line-width {w} :color {_color(b["color"], colors, schema)}{s})'))
    u = fspec.get("underline")
    if u is True:
        attrs.append((":underline", "t"))
    elif isinstance(u, str):
        attrs.append((":underline", _color(u, colors, schema)))
    elif isinstance(u, dict):
        attrs.append((":underline", f'(:color {_color(u["color"], colors, schema)}'
                                    f' :style {u.get("style", "line")})'))
    if "overline" in fspec:
        attrs.append((":overline", _color(fspec["overline"], colors, schema)))
    s = fspec.get("strike-through")
    if s is True:
        attrs.append((":strike-through", "t"))
    elif isinstance(s, str):
        attrs.append((":strike-through", _color(s, colors, schema)))
    if fspec.get("inverse"):
        attrs.append((":inverse-video", "t"))
    if fspec.get("extend"):
        attrs.append((":extend", "t"))
    if "inherit" in fspec:
        inh = str(fspec["inherit"])
        attrs.append((":inherit", f"({inh})" if " " in inh else inh))
    if "height" in fspec:
        attrs.append((":height", str(fspec["height"])))
    return attrs


def emit_variable(name: str, vspec, colors: dict, schema: dict) -> str:
    """One `custom-theme-set-variables' entry.  Value forms: a color ref,
    a number, {lit}, {cons: [a, b]}, {vector: [...]}, {list: [...]},
    {alist: {key: ref}} and {pairs: [[k, ref], ...]}."""
    def lit(v):
        if isinstance(v, str):
            return f'"{resolve_ref(v, colors, schema)}"'
        if isinstance(v, (int, float)):
            return str(v)
        if isinstance(v, dict):
            if "lit" in v:
                return v["lit"]
            if "cons" in v:
                a, b = v["cons"]
                return f"({lit(a)} . {lit(b)})"
            if "vector" in v:
                return "[" + " ".join(lit(x) for x in v["vector"]) + "]"
            if "list" in v:
                return "(" + " ".join(lit(x) for x in v["list"]) + ")"
            if "alist" in v:
                return "(" + " ".join(f'("{k}" . {lit(x)})' for k, x in v["alist"].items()) + ")"
            if "pairs" in v:
                return "(" + " ".join(f"({lit(k)} . {lit(x)})" for k, x in v["pairs"]) + ")"
        raise ValueError(f"bad variable spec for {name}: {vspec!r}")
    value = lit(vspec)
    if value.startswith("("):
        value = "'" + value
    return f" '({name} {value})"


ELISP_FILE_HEADER = '''\
;;; {file} --- {short} -*- lexical-binding: t; -*-
;;
;; Author: razik <https://github.com/RazikSF>
;; Maintainer: razik <https://github.com/RazikSF>
;; URL: https://github.com/RazikSF/lumina-themes
;; Version: 2.1.0
;; Package-Requires: ((emacs "26.1"))
;; Keywords: faces, themes
;;
;;; Commentary:
;;
{commentary}
;;
;;; Code:

(deftheme {theme}
  "{docstring}")

(custom-theme-set-faces
 '{theme}
'''
ELISP_FILE_FOOTER = ''' ){variables}

;;;###autoload
(when load-file-name
  (add-to-list 'custom-theme-load-path
               (file-name-as-directory (file-name-directory load-file-name))))

(provide-theme '{theme})

;;; {file} ends here
'''


def _load_decl(name):
    """Load a declarative spec file, stripping the leading _schema doc key."""
    d = json.loads((ROOT / "spec" / name).read_text())
    return {k: v for k, v in d.items() if not k.startswith("_")}


def build_emacs(spec: dict):
    outdir = ROOT / "emacs" / "themes"
    outdir.mkdir(parents=True, exist_ok=True)
    face_map = _load_decl("faces.json")
    var_map = _load_decl("variables.json")
    n = 0
    for flavor, modes in spec["flavors"].items():
        for d in modes.values():
            c = d["colors"]
            theme = d["theme"]
            mode = d["background"]
            sch = schema_for(flavor, mode)
            short = pretty(theme)
            commentary = "\n".join(f";; {ln}" if ln else ";;"
                                   for ln in d["commentary"].split("\n"))
            docstring = (commentary.split("\n")[0].lstrip("; ").strip()
                         or short).replace('"', '\\"')
            faces = [emit_face(name, spec_to_attrs(fs, c, sch))
                     for name, fs in face_map.items()]
            variables = ""
            if var_map:
                variables = (f"\n\n(custom-theme-set-variables\n '{theme}\n"
                             + "\n".join(emit_variable(n, v, c, sch) for n, v in var_map.items())
                             + ")")
            file_name = f"{theme}-theme.el"
            text = (
                ELISP_FILE_HEADER.format(
                    file=file_name, short=short, theme=theme,
                    docstring=docstring, commentary=commentary,
                )
                + "\n".join(faces)
                + ELISP_FILE_FOOTER.format(file=file_name, theme=theme, variables=variables)
            )
            (outdir / file_name).write_text(text)
            n += 1
    print(f"emacs   -> {n} files in emacs/themes/  ({len(face_map)} faces, {len(var_map)} variables each)")


# ---------------------------------------------------------------------------
# WezTerm + base24 emitters (the mappings here are short and uniform; kept
# inline rather than hoisted into a declarative spec).
# ---------------------------------------------------------------------------
def build_wezterm(spec: dict):
    outdir = ROOT / "wezterm"
    outdir.mkdir(parents=True, exist_ok=True)
    n = 0
    for flavor, modes in spec["flavors"].items():
        for d in modes.values():
            c = d["colors"]
            name = d["theme"]
            lead = resolve_ref("schema.lead", c, schema_for(flavor, d["background"]))
            ansi = [C(c, k) for k in
                    ("base1", "red", "green", "yellow", "blue",
                     "magenta", "cyan", "base7")]
            brights = [C(c, k) for k in
                       ("base5", "orange", "teal", "yellow", "dark-blue",
                        "violet", "cyan", "base8")]
            toml = f'''# {name} -- Lumina ({flavor}, {d["background"]})
# Generated from spec/lumina.json. Do not edit by hand.
[colors]
foreground   = "{C(c,'fg')}"
background   = "{C(c,'bg')}"
cursor_bg    = "{C(c,'fg')}"
cursor_fg    = "{C(c,'bg')}"
cursor_border = "{C(c,'fg')}"
selection_bg = "{C(c,'selection')}"
selection_fg = "{C(c,'fg')}"
scrollbar_thumb = "{C(c,'base4')}"
split = "{C(c,'base3')}"
compose_cursor = "{lead}"
visual_bell = "{C(c,'glow')}"
copy_mode_active_highlight_bg = {{ Color = "{lead}" }}
copy_mode_active_highlight_fg = {{ Color = "{C(c,'bg')}" }}
copy_mode_inactive_highlight_bg = {{ Color = "{C(c,'halo2')}" }}
copy_mode_inactive_highlight_fg = {{ Color = "{C(c,'fg')}" }}
quick_select_label_bg = {{ Color = "{C(c,'orange')}" }}
quick_select_label_fg = {{ Color = "{C(c,'bg')}" }}
quick_select_match_bg = {{ Color = "{C(c,'halo2')}" }}
quick_select_match_fg = {{ Color = "{C(c,'fg')}" }}
ansi = [{", ".join(f'"{x}"' for x in ansi)}]
brights = [{", ".join(f'"{x}"' for x in brights)}]

[colors.indexed]
16 = "{C(c,'orange')}"
17 = "{C(c,'teal')}"
18 = "{C(c,'violet')}"
19 = "{C(c,'dark-blue')}"

[colors.tab_bar]
background = "{C(c,'bg-alt')}"
inactive_tab_edge = "{C(c,'base2')}"
[colors.tab_bar.active_tab]
bg_color = "{C(c,'bg')}"
fg_color = "{C(c,'fg')}"
intensity = "Bold"
[colors.tab_bar.inactive_tab]
bg_color = "{C(c,'bg-alt')}"
fg_color = "{C(c,'base6')}"
[colors.tab_bar.inactive_tab_hover]
bg_color = "{C(c,'halo')}"
fg_color = "{C(c,'fg')}"
[colors.tab_bar.new_tab]
bg_color = "{C(c,'bg-alt')}"
fg_color = "{C(c,'base5')}"
[colors.tab_bar.new_tab_hover]
bg_color = "{C(c,'halo2')}"
fg_color = "{lead}"

[metadata]
name = "{name}"
'''
            (outdir / f"{name}.toml").write_text(toml)
            n += 1
    print(f"wezterm -> {n} files in wezterm/")


def build_base24(spec: dict):
    outdir = ROOT / "base24"
    outdir.mkdir(parents=True, exist_ok=True)
    n = 0
    for flavor, modes in spec["flavors"].items():
        for d in modes.values():
            c = d["colors"]
            name = d["theme"]
            slots = {
                "base00": C(c, "bg"),     "base01": C(c, "base1"),
                "base02": C(c, "base2"),  "base03": C(c, "base3"),
                "base04": C(c, "base5"),  "base05": C(c, "fg"),
                "base06": C(c, "base7"),  "base07": C(c, "base8"),
                "base08": C(c, "red"),    "base09": C(c, "orange"),
                "base0A": C(c, "yellow"), "base0B": C(c, "green"),
                "base0C": C(c, "cyan"),   "base0D": C(c, "blue"),
                "base0E": C(c, "violet"), "base0F": C(c, "magenta"),
                "base10": C(c, "base0"),  "base11": C(c, "bg-alt"),
                "base12": C(c, "red"),    "base13": C(c, "yellow"),
                "base14": C(c, "green"),  "base15": C(c, "cyan"),
                "base16": C(c, "blue"),   "base17": C(c, "magenta"),
            }
            body = "\n".join(f'  {k}: "{v.lstrip("#")}"' for k, v in slots.items())
            sysmode = d["background"]
            yaml = (
                f'system: "base24"\n'
                f'name: "{pretty(name)}"\n'
                f'author: "razik (https://github.com/RazikSF)"\n'
                f'variant: "{sysmode}"\n'
                f'palette:\n{body}\n'
            )
            (outdir / f"{name}.yaml").write_text(yaml)
            n += 1
    print(f"base24  -> {n} files in base24/")


# ---------------------------------------------------------------------------
# VS Code emitter (declarative, fed by spec/vscode.json).
# ---------------------------------------------------------------------------
def build_vscode(spec: dict):
    outdir = ROOT / "vscode"
    themes_dir = outdir / "themes"
    themes_dir.mkdir(parents=True, exist_ok=True)
    vmap = json.loads((ROOT / "spec" / "vscode.json").read_text())
    workbench_spec = vmap["colors"]
    token_rules = vmap["tokenColors"]
    semantic_spec = vmap["semanticTokenColors"]
    n = 0
    for flavor, modes in spec["flavors"].items():
        for d in modes.values():
            c = d["colors"]
            theme = d["theme"]
            mode = d["background"]
            sch = schema_for(flavor, mode)
            workbench = {k: resolve_ref(v, c, sch)
                         for k, v in workbench_spec.items()}
            token_colors = []
            for rule in token_rules:
                settings = {}
                if "fg" in rule:
                    settings["foreground"] = resolve_ref(rule["fg"], c, sch)
                if "fontStyle" in rule:
                    settings["fontStyle"] = rule["fontStyle"]
                token_colors.append({"scope": rule["scope"], "settings": settings})
            semantic = {}
            for role, rspec in semantic_spec.items():
                entry = {}
                if "fg" in rspec:
                    entry["foreground"] = resolve_ref(rspec["fg"], c, sch)
                if "fontStyle" in rspec:
                    entry["fontStyle"] = rspec["fontStyle"]
                semantic[role] = entry
            theme_obj = {
                "name": pretty(theme),
                "type": mode,
                "semanticHighlighting": True,
                "colors": workbench,
                "tokenColors": token_colors,
                "semanticTokenColors": semantic,
            }
            (themes_dir / f"{theme}-color-theme.json").write_text(
                json.dumps(theme_obj, indent=2) + "\n"
            )
            n += 1
    pkg = {
        "name": "lumina-themes",
        "displayName": "Lumina",
        "description":
            "A curated palette-first theme family — one light governs each "
            "field. Sixteen flavors in dark, light and high contrast.",
        "version": "2.1.0",
        "publisher": "RazikSF",
        "license": "MIT",
        "engines": {"vscode": "^1.74.0"},
        "categories": ["Themes"],
        "keywords": ["theme", "color-theme", "dark", "light", "lumina"],
        "repository": {"type": "git",
                       "url": "https://github.com/RazikSF/lumina-themes.git"},
        "contributes": {
            "themes": [
                {"label": pretty(d["theme"]),
                 "uiTheme": "vs-dark" if d["background"] == "dark" else "vs",
                 "path": f"./themes/{d['theme']}-color-theme.json"}
                for modes in spec["flavors"].values() for d in modes.values()
            ]
        },
    }
    (outdir / "package.json").write_text(json.dumps(pkg, indent=2) + "\n")
    (outdir / ".vscodeignore").write_text(
        "**/.git/**\n**/.DS_Store\n**/*.vsix\n"
    )
    print(f"vscode  -> {n} themes + package.json in vscode/")


# ---------------------------------------------------------------------------
# Neovim emitter (declarative, fed by spec/nvim_highlights.json).
# ---------------------------------------------------------------------------
def _nv_line(name: str, hspec: dict, colors: dict, schema: dict) -> str:
    if "link" in hspec:
        return f"set(0, '{name}', {{ link = '{hspec['link']}' }})"
    parts = []
    if "fg" in hspec:
        parts.append(f"fg = '{resolve_ref(hspec['fg'], colors, schema)}'")
    if "bg" in hspec:
        parts.append(f"bg = '{resolve_ref(hspec['bg'], colors, schema)}'")
    if "sp" in hspec:
        parts.append(f"sp = '{resolve_ref(hspec['sp'], colors, schema)}'")
    for k in ("bold", "italic", "underline", "undercurl", "strikethrough"):
        if hspec.get(k):
            parts.append(f"{k} = true")
    return f"set(0, '{name}', {{ {', '.join(parts)} }})"


def build_nvim(spec: dict):
    outdir = ROOT / "nvim" / "colors"
    outdir.mkdir(parents=True, exist_ok=True)
    hl_map = _load_decl("nvim_highlights.json")
    n = 0
    for flavor, modes in spec["flavors"].items():
        for d in modes.values():
            c = d["colors"]
            theme = d["theme"]
            mode = d["background"]
            sch = schema_for(flavor, mode)
            lines = [
                f"-- {theme} -- Lumina ({flavor}, {mode})",
                "-- Generated from spec/lumina.json + spec/nvim_highlights.json.",
                "",
                "vim.cmd('highlight clear')",
                "if vim.fn.exists('syntax_on') == 1 then vim.cmd('syntax reset') end",
                f"vim.o.background = '{mode}'",
                f"vim.g.colors_name = '{theme}'",
                "",
                "local set = vim.api.nvim_set_hl",
                "",
            ]
            lines += [_nv_line(name, hspec, c, sch)
                      for name, hspec in hl_map.items()]
            term = [C(c, k) for k in ("base0", "red", "green", "yellow", "blue", "magenta", "cyan", "base8",
                                      "base5", "red", "green", "yellow", "blue", "magenta", "cyan", "fg")]
            lines += [""] + [f"vim.g.terminal_color_{i} = '{col}'" for i, col in enumerate(term)]
            (outdir / f"{theme}.lua").write_text("\n".join(lines) + "\n")
            _nv_lualine(theme, flavor, mode, c, sch)
            n += 1
    print(f"nvim    -> {n} files in nvim/colors/ + lualine themes in nvim/lua/lualine/themes/")


def _nv_lualine(theme, flavor, mode, c, sch):
    """Emit nvim/lua/lualine/themes/<theme>.lua: lamp for normal, teal insert,
    violet visual, red replace, orange command; b/c sections on the chrome."""
    lead = resolve_ref("schema.lead", c, sch)
    bg, bg_alt, fg_alt, base1, base5 = C(c, "bg"), C(c, "bg-alt"), C(c, "fg-alt"), C(c, "base1"), C(c, "base5")
    modes = {"normal": lead, "insert": C(c, "teal"), "visual": C(c, "violet"), "replace": C(c, "red"),
             "command": C(c, "orange"), "terminal": C(c, "green")}
    body = []
    for m, col in modes.items():
        body.append(f"  {m} = {{ a = {{ fg = '{bg}', bg = '{col}', gui = 'bold' }}, "
                    f"b = {{ fg = '{fg_alt}', bg = '{base1}' }}, c = {{ fg = '{fg_alt}', bg = '{bg_alt}' }} }},")
    body.append(f"  inactive = {{ a = {{ fg = '{base5}', bg = '{bg_alt}' }}, "
                f"b = {{ fg = '{base5}', bg = '{bg_alt}' }}, c = {{ fg = '{base5}', bg = '{bg}' }} }},")
    out = ROOT / "nvim" / "lua" / "lualine" / "themes"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{theme}.lua").write_text(
        f"-- {theme} -- Lumina lualine theme ({flavor}, {mode}). Generated; do not edit.\n"
        "return {\n" + "\n".join(body) + "\n}\n")


ACCENTS = ["red", "orange", "yellow", "green", "teal",
           "cyan", "blue", "violet", "magenta"]


def check(spec: dict) -> bool:
    """Lumina 2 legibility gate, applied to flavors whose schema sets v2.

    Standard variants: fg 8-12.5:1 (fg_min/fg_max per schema), comments >= 4.3,
    accents >= 4.5.  -contrast variants: fg >= 15, comments >= 6, accents >= 7.
    Both: non-lead accents within 0.08 OKLCH lightness, every accent >= 4.0
    on its own tinted ground, fg >= 9 on the popup ground, lamp >= 3.5 on halo2
    (short highlighted tokens only: paren match, current search hit).
    """
    from oklch import contrast, from_hex
    ok = True
    for flavor, modes in spec["flavors"].items():
        if not SCHEMAS[flavor].get("v2"):
            continue
        for d in modes.values():
            sch = schema_for(flavor, d["background"])
            c = d["colors"]
            bg = C(c, "bg")
            hc = d["theme"].endswith("-contrast")
            fails = []
            fg = contrast(C(c, "fg"), bg)
            lo, hi = (15, 21) if hc else (sch.get("fg_min", 10), sch.get("fg_max", 12.5))
            if not lo <= fg <= hi:
                fails.append(f"fg {fg:.1f} outside {lo}-{hi}")
            for k in ("comments", "doc-comments"):
                if contrast(C(c, k), bg) < (6 if hc else sch.get("comments_min", 4.3)):
                    fails.append(f"{k} {contrast(C(c, k), bg):.1f}")
            for k in ACCENTS:
                if contrast(C(c, k), bg) < (7 if hc else sch.get("accent_min", 4.5)):
                    fails.append(f"{k} {contrast(C(c, k), bg):.1f}")
            lead = sch["lead"]
            for k in ACCENTS + ["spark"]:
                if k in c and f"{k}-bg" in c and contrast(C(c, k), C(c, f"{k}-bg")) < sch.get("accent_bg_min", 4.0):
                    fails.append(f"{k} on {k}-bg {contrast(C(c, k), C(c, f'{k}-bg')):.1f}")
            if "overlay" in c and contrast(C(c, "fg"), C(c, "overlay")) < sch.get("fg_min", 10) - 1:
                fails.append(f"fg on overlay {contrast(C(c, 'fg'), C(c, 'overlay')):.1f}")
            if "halo2" in c and contrast(C(c, lead), C(c, "halo2")) < 3.5:
                fails.append(f"lead on halo2 {contrast(C(c, lead), C(c, 'halo2')):.1f}")
            if sch.get("role_inks"):
                ls = [from_hex(resolve_ref(r, c, sch))[0] for r in ("functions", "keywords", "type", "strings", "constants", "builtin")]
                ls = [from_hex(resolve_ref(r, c, sch))[0] for r in ("functions", "keywords", "type", "strings", "constants", "builtin")
                      if from_hex(resolve_ref(r, c, sch))[1] > .05]
            else:
                ls = [from_hex(C(c, k))[0] for k in ACCENTS + (["spark"] if "spark" in c and from_hex(C(c, "spark"))[1] > .05 else [])]
            if max(ls) - min(ls) > sch.get("spread", .16 if sch.get("role_inks") else .0805):
                fails.append(f"accent lightness spread {max(ls) - min(ls):.2f} > {sch.get('spread', .16 if sch.get('role_inks') else .0805):.2f}")
            print(f"{'FAIL' if fails else 'OK  '} {d['theme']}"
                  + (": " + "; ".join(fails) if fails else ""))
            ok = ok and not fails
    return ok


def build():
    spec = json.loads(SPEC.read_text())
    build_emacs(spec)
    build_wezterm(spec)
    build_base24(spec)
    build_vscode(spec)
    build_nvim(spec)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd in ("extract", "all"):
        extract()
    if cmd in ("build", "all"):
        build()
    if cmd == "check":
        sys.exit(0 if check(json.loads(SPEC.read_text())) else 1)
