# Lumina

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A family of five themes for code editors and terminals.

Each flavor is anchored in a specific material, pigment or scene and
rendered with a single dominant lead across a tightly disciplined
cascade of supporting hues. The light variants are not negatives of the
darks: each is a complete companion in its own register.

## Flavors

Five flavors, each in a dark and a light variant, ten themes in all. Fifteen
earlier flavors are kept, unmaintained, in `archive/`.

| Flavor | Lead | Description |
|---|---|---|
| **Dawn**       | amber lamp      | warm sepia room lit by a single amber lamp; muted inks of rust, olive, sage, slate and plum |
| **Oxblood**    | gilt yellow     | theatre after the curtain falls; oxblood-velvet drape, a single overhead spot on the gilt frame |
| **Tide**       | biolum green    | deep ocean at night, lit from within by a bioluminescent jellyfish |
| **Canopy**     | sun yellow      | pine forest at noon; one shaft of sun through the leaves |
| **Slate**      | steel blue      | cold graphite ground; near-achromatic with one steel-blue voice |

## Supported targets

| Target | Output |
|---|---|
| **Emacs** (vanilla `deftheme`)  | `emacs/themes/*.el` (10) |
| **Neovim** (Lua colorscheme)    | `nvim/colors/*.lua` (10) |
| **VS Code** (extension)         | `vscode/themes/*.json` (10) + `package.json` |
| **WezTerm** (color scheme)      | `wezterm/*.toml` (10) |
| **base24** (tinted-theming)     | `base24/*.yaml` (10) |

The Emacs files require no external dependency: they set a comprehensive
face surface — modeline, completion, syntax, outline, org, magit, diff,
dired, dirvish, vertico, consult, marginalia, corfu, eldoc, flycheck,
flymake, eshell, compilation, tab-bar, tab-line, helpful, which-key,
treemacs — so the look is consistent without requiring any particular
package to be present.

## Install

### Emacs

Requires Emacs 26.1 or later.

**MELPA**:
```elisp
M-x package-install RET lumina-themes RET
M-x load-theme RET lumina-dawn-dark RET
```

**Doom** — `packages.el`:
```elisp
(package! lumina-themes :recipe (:host github :repo "RazikSF/lumina-themes"
                                 :files ("emacs/*.el" "emacs/themes/*.el")))
```
Then `config.el`:
```elisp
(require 'lumina-themes)
(setq doom-theme 'lumina-dawn-dark)
```

**`straight.el`**:
```elisp
(straight-use-package
 '(lumina-themes :type git :host github :repo "RazikSF/lumina-themes"
                 :files ("emacs/*.el" "emacs/themes/*.el")))
(load-theme 'lumina-dawn-dark t)
```

**`elpaca`**:
```elisp
(elpaca (lumina-themes :host github :repo "RazikSF/lumina-themes"
                       :files ("emacs/*.el" "emacs/themes/*.el")))
```

**Manual**: clone the repository and add `emacs/themes/` to
`custom-theme-load-path`:
```elisp
(add-to-list 'custom-theme-load-path "/path/to/lumina-themes/emacs/themes")
(load-theme 'lumina-dawn-dark t)
```

#### Customisation

Six optional variables, set them before loading a theme or call
`M-x lumina-themes-reapply` after toggling them:

```elisp
(setq lumina-themes-brighter-comments  nil)  ; bolder comments
(setq lumina-themes-comment-bg         nil)  ; tinted comment background
(setq lumina-themes-padded-modeline    nil)  ; t, or integer pixel width
(setq lumina-themes-italic-comments    t)    ; italic on comments
(setq lumina-themes-italic-types       t)    ; italic on type names
(setq lumina-themes-bold-keywords      t)    ; bold on keywords
```

`M-x lumina-themes-load-random` loads a random Lumina theme.  Prefix
arg `C-u` restricts to dark, `C-u C-u` to light.

### Neovim

**`lazy.nvim`**:
```lua
{
  "RazikSF/lumina-themes",
  init = function()
    vim.opt.rtp:append(vim.fn.stdpath("data") .. "/lazy/lumina-themes/nvim")
  end,
  config = function() vim.cmd.colorscheme("lumina-dawn-dark") end,
}
```

**`packer.nvim`**:
```lua
use { "RazikSF/lumina-themes", rtp = "nvim" }
```

**`vim-plug`**:
```vim
Plug 'RazikSF/lumina-themes', { 'rtp': 'nvim' }
```

**Manual**: copy `nvim/colors/*.lua` into your Neovim runtime's
`colors/` directory, then `:colorscheme lumina-dawn-dark`.

### VS Code

**Marketplace**:
```
ext install RazikSF.lumina-themes
```
Then `Cmd/Ctrl-K Cmd/Ctrl-T` and pick a Lumina flavor.

**Manual `.vsix`**:
```sh
cd vscode && npx @vscode/vsce package
code --install-extension lumina-themes-1.0.0.vsix
```

### WezTerm

```lua
config.color_scheme_dirs = { "/path/to/lumina-themes/wezterm" }
config.color_scheme = "lumina-dawn-dark"
```

### base24 / tinted-theming

The `base24/` YAML files are standard tinted-theming schemes. Use them
with [tinty](https://github.com/tinted-theming/tinty),
[base16-shell](https://github.com/tinted-theming/base16-shell) or any
community template to theme terminals, `bat`, `fzf`, `btop` and the rest
of the CLI from a single source.

## Architecture

```
spec/lumina.json            single source of truth (palette per flavor/mode)
spec/faces.json             declarative face mapping (~390 faces)
spec/nvim_highlights.json   declarative Neovim highlight mapping
spec/vscode.json            declarative VS Code workbench + tokens
generators/lumina_gen.py    spec -> all targets; embeds per-flavor schemas
emacs/themes/*.el           generated; pure vanilla deftheme
emacs/lumina-themes.el      Emacs package loader
nvim/colors/*.lua           generated
vscode/themes/*.json        generated
vscode/package.json         generated; bundles all flavors
wezterm/*.toml              generated
base24/*.yaml               generated
Makefile                    make build / make verify / make extract
```

Lumina is palette-first. `spec/lumina.json` carries one palette per
(flavor, mode); per-flavor syntax schemas live in
`generators/lumina_gen.py` as Python data (lead accent, rainbow /
outline / orderless sequences, modeline and vertico backgrounds, magit
and org mappings, preprocessor and escape slots — shared between dark
and light). The generator resolves palette references to literal hex
per flavor and emits one file per target per (flavor, mode).

A color edit in `spec/lumina.json` propagates to all five targets on
the next `make build`.

## Develop

Requires Python 3.11+.

```sh
make build       # spec -> all targets
make verify      # rebuild and smoke-test all themes load on vanilla Emacs
make extract     # one-time bootstrap from existing .el files (rarely needed)
```

## Contributing

Issues for color bugs — contrast on a specific UI surface, a face that
lands wrong, a missing package — are welcome.

Pull requests that add a flavor must justify its position on the hue
coverage map (does it fill a real gap, with a specific real-world
referent?), follow the single-lead discipline, and include a
screenshot.

Pull requests that retune existing colors should explain the intent and
include before/after captures.

## License

Licensed under the [MIT License](LICENSE).
