#!/usr/bin/env python3
"""Lumina theme generator (palette-first, declarative).

Three layers of source of truth:

  spec/lumina.json           palette + helpers + commentary per flavor/mode
  SCHEMAS (this file)        per-flavor face design (lead, rainbow/outline/
                             orderless sequences, modeline_bg, vertico_bg,
                             function-call/property/preprocessor/escape,
                             magit/org/modeline-modified) shared dark/light
  spec/faces.json            face name -> {fg, bg, bold/italic/...}  (Emacs)
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
SPEC = ROOT / "spec" / "lumina.json"
DOOM_THEMES = Path.home() / ".doom.d" / "themes"

FLAVORS = ["dawn", "oxblood", "ember", "tide", "indigo", "canopy", "slate"]

# ---------------------------------------------------------------------------
# Per-flavour syntax schema (face design intent, shared dark/light).
# ---------------------------------------------------------------------------
SCHEMAS = {
    "dawn": {
        "lead": "violet",
        "modeline_bg": "base1", "vertico_bg": "base2",
        "function_call": "blue", "property": "cyan",
        "preprocessor": "violet", "escape": "magenta",
        "modeline_modified": "orange",
        "rainbow":   ["violet", "blue", "green", "magenta", "teal", "orange"],
        "outline":   ["violet", "blue", "green", "magenta"],
        "orderless": ["violet", "blue", "green"],
        "magit_branch_local": "blue", "magit_branch_remote": "green",
        "org_todo": "orange", "org_done": "green",
    },
    "oxblood": {
        "lead": "yellow",
        "modeline_bg": "bg-alt", "vertico_bg": "base3",
        "function_call": "magenta", "property": "green",
        "preprocessor": "yellow", "escape": "cyan",
        "modeline_modified": "orange",
        "rainbow":   ["yellow", "magenta", "cyan", "green", "violet", "blue"],
        "outline":   ["yellow", "magenta", "cyan", "green"],
        "orderless": ["yellow", "magenta", "cyan"],
        "magit_branch_local": "magenta", "magit_branch_remote": "teal",
        "org_todo": "orange", "org_done": "green",
    },
    "ember": {
        "lead": "orange",
        "modeline_bg": "bg-alt", "vertico_bg": "base3",
        "function_call": "blue", "property": "teal",
        "preprocessor": "orange", "escape": "magenta",
        "modeline_modified": "red",
        "rainbow":   ["orange", "blue", "teal", "yellow", "magenta", "green"],
        "outline":   ["orange", "blue", "teal", "yellow"],
        "orderless": ["orange", "blue", "teal"],
        "magit_branch_local": "blue", "magit_branch_remote": "teal",
        "org_todo": "red", "org_done": "green",
    },
    "tide": {
        "lead": "green",
        "modeline_bg": "bg-alt", "vertico_bg": "base3",
        "function_call": "green", "property": "cyan",
        "preprocessor": "violet", "escape": "magenta",
        "modeline_modified": "orange",
        "rainbow":   ["green", "teal", "violet", "cyan", "magenta", "yellow"],
        "outline":   ["green", "teal", "violet", "cyan"],
        "orderless": ["green", "violet", "cyan"],
        "magit_branch_local": "teal", "magit_branch_remote": "cyan",
        "org_todo": "orange", "org_done": "green",
    },
    "indigo": {
        "lead": "blue",
        "modeline_bg": "bg-alt", "vertico_bg": "base3",
        "function_call": "teal", "property": "green",
        "preprocessor": "blue", "escape": "orange",
        "modeline_modified": "orange",
        "rainbow":   ["blue", "teal", "orange", "green", "violet", "magenta"],
        "outline":   ["blue", "teal", "orange", "green"],
        "orderless": ["blue", "teal", "orange"],
        "magit_branch_local": "teal", "magit_branch_remote": "green",
        "org_todo": "orange", "org_done": "green",
    },
    "canopy": {
        "lead": "yellow",
        "modeline_bg": "bg-alt", "vertico_bg": "base3",
        "function_call": "teal", "property": "green",
        "preprocessor": "yellow", "escape": "orange",
        "modeline_modified": "orange",
        "rainbow":   ["yellow", "teal", "green", "orange", "violet", "blue"],
        "outline":   ["yellow", "teal", "green", "orange"],
        "orderless": ["yellow", "teal", "green"],
        "magit_branch_local": "teal", "magit_branch_remote": "green",
        "org_todo": "orange", "org_done": "green",
    },
    "slate": {
        "lead": "blue",
        "modeline_bg": "bg-alt", "vertico_bg": "base3",
        "function_call": "teal", "property": "cyan",
        "preprocessor": "blue", "escape": "orange",
        "modeline_modified": "orange",
        "rainbow":   ["blue", "teal", "cyan", "violet", "green", "orange"],
        "outline":   ["blue", "teal", "cyan", "violet"],
        "orderless": ["blue", "teal", "cyan"],
        "magit_branch_local": "teal", "magit_branch_remote": "cyan",
        "org_todo": "orange", "org_done": "green",
    },
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
def emit_face(name: str, attrs: list) -> str:
    body = " ".join(f"{k} {v}" for k, v in attrs)
    return f" '({name} ((t ({body}))))"


def spec_to_attrs(fspec: dict, colors: dict, schema: dict) -> list:
    """Turn a face spec dict (from faces.json) into emit_face's attrs list.
    Canonical order: fg, bg, weight, slant, underline, extend, inherit, height."""
    attrs = []
    if "fg" in fspec:
        attrs.append((":foreground", f'"{resolve_ref(fspec["fg"], colors, schema)}"'))
    if "bg" in fspec:
        attrs.append((":background", f'"{resolve_ref(fspec["bg"], colors, schema)}"'))
    if "weight" in fspec:
        attrs.append((":weight", str(fspec["weight"])))
    elif fspec.get("bold"):
        attrs.append((":weight", "bold"))
    if "slant" in fspec:
        attrs.append((":slant", str(fspec["slant"])))
    elif fspec.get("italic"):
        attrs.append((":slant", "italic"))
    if fspec.get("underline") is True:
        attrs.append((":underline", "t"))
    if fspec.get("extend"):
        attrs.append((":extend", "t"))
    if "inherit" in fspec:
        attrs.append((":inherit", str(fspec["inherit"])))
    if "height" in fspec:
        attrs.append((":height", str(fspec["height"])))
    return attrs


ELISP_FILE_HEADER = '''\
;;; {file} --- {short} -*- lexical-binding: t; -*-
;;
;; Author: razik <https://github.com/RazikSF>
;; Maintainer: razik <https://github.com/RazikSF>
;; URL: https://github.com/RazikSF/lumina-themes
;; Version: 1.0.0
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
ELISP_FILE_FOOTER = ''' )

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
    n = 0
    for flavor, modes in spec["flavors"].items():
        sch = SCHEMAS[flavor]
        for d in modes.values():
            c = d["colors"]
            theme = d["theme"]
            mode = d["background"]
            short = f"Lumina {flavor.capitalize()}, {mode}"
            commentary = "\n".join(f";; {ln}" if ln else ";;"
                                   for ln in d["commentary"].split("\n"))
            docstring = (commentary.split("\n")[0].lstrip("; ").strip()
                         or short).replace('"', '\\"')
            faces = [emit_face(name, spec_to_attrs(fs, c, sch))
                     for name, fs in face_map.items()]
            file_name = f"{theme}-theme.el"
            text = (
                ELISP_FILE_HEADER.format(
                    file=file_name, short=short, theme=theme,
                    docstring=docstring, commentary=commentary,
                )
                + "\n".join(faces)
                + ELISP_FILE_FOOTER.format(file=file_name, theme=theme)
            )
            (outdir / file_name).write_text(text)
            n += 1
    print(f"emacs   -> {n} files in emacs/themes/")


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
ansi = [{", ".join(f'"{x}"' for x in ansi)}]
brights = [{", ".join(f'"{x}"' for x in brights)}]

[colors.tab_bar]
background = "{C(c,'bg-alt')}"
[colors.tab_bar.active_tab]
bg_color = "{C(c,'bg')}"
fg_color = "{C(c,'fg')}"
[colors.tab_bar.inactive_tab]
bg_color = "{C(c,'bg-alt')}"
fg_color = "{C(c,'base6')}"

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
                f'name: "Lumina {flavor.capitalize()} {sysmode.capitalize()}"\n'
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
        sch = SCHEMAS[flavor]
        for d in modes.values():
            c = d["colors"]
            theme = d["theme"]
            mode = d["background"]
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
                "name": f"Lumina {flavor.capitalize()} {mode.capitalize()}",
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
            "field. Seven flavors × dark/light.",
        "version": "1.0.0",
        "publisher": "RazikSF",
        "license": "MIT",
        "engines": {"vscode": "^1.74.0"},
        "categories": ["Themes"],
        "keywords": ["theme", "color-theme", "dark", "light", "lumina"],
        "repository": {"type": "git",
                       "url": "https://github.com/RazikSF/lumina-themes.git"},
        "contributes": {
            "themes": [
                {"label": f"Lumina {f.capitalize()} {m.capitalize()}",
                 "uiTheme": "vs-dark" if m == "dark" else "vs",
                 "path": f"./themes/lumina-{f}-{m}-color-theme.json"}
                for f in FLAVORS for m in ("dark", "light")
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
    for k in ("bold", "italic", "underline", "undercurl"):
        if hspec.get(k):
            parts.append(f"{k} = true")
    return f"set(0, '{name}', {{ {', '.join(parts)} }})"


def build_nvim(spec: dict):
    outdir = ROOT / "nvim" / "colors"
    outdir.mkdir(parents=True, exist_ok=True)
    hl_map = _load_decl("nvim_highlights.json")
    n = 0
    for flavor, modes in spec["flavors"].items():
        sch = SCHEMAS[flavor]
        for d in modes.values():
            c = d["colors"]
            theme = d["theme"]
            mode = d["background"]
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
            (outdir / f"{theme}.lua").write_text("\n".join(lines) + "\n")
            n += 1
    print(f"nvim    -> {n} files in nvim/colors/")


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
