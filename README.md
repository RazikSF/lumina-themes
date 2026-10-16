# Lumina

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Even light.** Lumina is a family of themes for Emacs, Neovim, VS Code,
WezTerm and the terminal, built on a single idea: every colour in the
code carries the same weight. No colour glows brighter than its
neighbours; hues alone tell keywords, functions, types and strings
apart, so the eye can rest on any part of the screen.

Twenty-six flavors, each in dark, light and high contrast, plus Prisma's
black-and-white twins: 108 themes. The reference is **Encre**: two inks
only, blue and amber, on a night ground `#0D1217` with blue-grey text at
12:1. Keywords `#91C1E0`, types `#74A4C2` and builtins `#AFE0FF` are three
lightnesses of one blue; functions `#B3A27C`, constants `#CFC098` and
strings `#EDDDB4` three lightnesses of one amber. It scores highest on
colour-design theory, and every other flavor is tuned to the same standard.

<img src="assets/screens/lumina-encre-dark.svg" width="49%"> <img src="assets/screens/lumina-encre-light.svg" width="49%">

## What makes it different

- **Harmony by colour theory.** Each flavor draws its six inks from a
  family of hues set by its scene (a warm room, the ocean, a city at
  night), then tunes them by published models: Ou and Luo's two-colour
  harmony, Matsuda's hue templates, and an even chroma. No ink is lit
  above the others: lightness stays within 0.15 across the six.
- **Distinct, even for colour-blind eyes.** Every pair of inks stays
  apart (OKLab distance 9 at night, 8 on paper). **Lucide** goes further:
  its inks stay apart under simulated deuteranopia and protanopia.
- **A clear face design.** Function calls take the function ink,
  properties the builtin ink; keywords, types and definitions are
  semi-bold; brackets and operators stay grey; line numbers fade into the
  ground.
- **Tinted text.** Body text is a light grey with a reflection of the
  flavor's hue at 12:1, never pure white.
- **Light that follows you.** The lead colour tints the current line, the
  selection and the completion candidate, and flashes on every jump.
  With [auto-dim-other-buffers](https://github.com/mina86/auto-dim-other-buffers.el)
  the windows you are not working in fall into shade.
- **Measured, not guessed.** Comments sit at 4.3:1 or more, every accent
  at 4.5:1 or more, on its own tinted ground at 4:1 or more. `make check`
  refuses a palette that drifts, and `tools/explore/audit.py` refuses two
  code roles closer than 7.5 dE or an error red closer than 9.
- **High contrast built in.** Every theme ships a `-contrast` twin:
  text 15:1 or more, comments 6:1, every accent 7:1 (WCAG AAA), same
  hues at one weight.
- **Readable diffs.** Added, removed and changed lines sit on tinted
  grounds in magit, diff, smerge and ediff.
- **Complete coverage.** Close to 3 000 faces per theme, written against
  the real `defface` names of Emacs 30 and of the installed packages:
  org and org-modern, magit and forge, vertico, corfu, company, consult,
  marginalia, embark, ivy and helm, treemacs and dirvish, lsp-mode,
  lsp-ui, dap and eglot, tree-sitter, flycheck and flymake, meow and
  evil, vterm, eat and term, mu4e, gnus and notmuch, elfeed and erc,
  markdown, LaTeX and web-mode, doom-modeline and nano-modeline,
  transient, which-key, avy, and more. Popups sit on their own ground,
  every state has a tinted ground, and `hl-todo`, `vc-annotate`,
  `pdf-tools` and `rustic` variables follow the palette.

## Flavors

Each flavor sets one scene, a ground and six inks, one per role, drawn from a family of hues
that suits the scene. The inks are tuned by colour-design theory: the Ou and Luo (2006)
harmony model over every pair, Matsuda's hue templates and an even chroma, while staying
legible (4.6:1 or more) and apart from one another (`tools/explore/theorie.py`, scored by
`tools/explore/beaute.py`). Ink names below are those of the dark variant.

| Flavor | Scene | Keywords | Functions | Types | Strings | Constants | Builtins |
|---|---|---|---|---|---|---|---|
| **Encre** | Two inks only, blue and amber, on night paper | sky | gold | sky | gold | gold | sky |
| **Nuancier** | The palette of a slide on web colours, slate night | sky | gold | gold | sage | lilac | lilac |
| **Aquarelle** | The slide palette rearranged, slate night | sky | gold | sage | gold | lilac | orchid |
| **Jardin** | The slide palette with mint keywords, slate night | sage | apricot | gold | periwinkle | lilac | orchid |
| **Sienne** | Slate night under warm inks | periwinkle | sky | gold | lime | gold | apricot |
| **Vesper** | Deep navy at night | lilac | periwinkle | sky | gold | pink | orchid |
| **Indigo** | Indigo night | periwinkle | straw | apricot | lilac | salmon | gold |
| **Dawn** | Warm sepia room | salmon | gold | salmon | sage | gold | straw |
| **Oxblood** | A theatre after the curtain falls, oxblood velvet | lilac | orchid | straw | mint | orchid | periwinkle |
| **Tide** | Deep ocean at night | mint | sky | lilac | mint | salmon | sky |
| **Slate** | Cold graphite | sky | periwinkle | lilac | sky | orchid | mint |
| **Brume** | Morning mist on a lake, a mid-dark ground | sky | sky | sky | mint | orchid | lilac |
| **Nocturne** | A city at night under an indigo sky | lilac | gold | sky | periwinkle | orchid | sky |
| **Prisma** | Neutral night, the full spectrum | lime | periwinkle | sky | lilac | gold | gold |
| **Neon Cyber** | Urban night in neon, every ink at full voltage | pink | mint | straw | sage | gold | pink |
| **Synthwave** | Violet night of an eighties sunset, neon | periwinkle | orchid | gold | sky | gold | lilac |
| **Sirocco** | Desert wind at dusk over terracotta | gold | sky | gold | pink | pink | sky |
| **Celadon** | Glazed jade porcelain | sky | gold | mint | mint | sky | sage |
| **Sumi** | Ink-black ground | salmon | mint | orchid | sky | apricot | orchid |
| **Pivoine** | A soft dusk of peony petals, lighter than the night grounds | orchid | sky | orchid | salmon | salmon | lilac |
| **Café** | Espresso brown, crema and cinnamon | sky | gold | mint | gold | sky | pink |
| **Pétrole** | Deep petrol blue under brass lamps | sky | gold | gold | sky | pink | sky |
| **Borealis** | Misty pine forest under the aurora | periwinkle | sky | straw | sky | salmon | gold |
| **Cashmere** | Espresso velvet, warm pastels | rose | straw | apricot | straw | gold | apricot |
| **Aethelgard** | Midnight velvet and astral gold | pink | sky | gold | mint | apricot | gold |
| **Lucide** | Neutral night, inks told apart with any colour vision | sky | gold | straw | mint | orchid | apricot |

### Gallery

#### Signature

**Encre**

<img src="assets/screens/lumina-encre-dark.svg" width="49%"> <img src="assets/screens/lumina-encre-light.svg" width="49%">

**Nuancier**

<img src="assets/screens/lumina-nuancier-dark.svg" width="49%"> <img src="assets/screens/lumina-nuancier-light.svg" width="49%">

**Aquarelle**

<img src="assets/screens/lumina-aquarelle-dark.svg" width="49%"> <img src="assets/screens/lumina-aquarelle-light.svg" width="49%">

**Jardin**

<img src="assets/screens/lumina-jardin-dark.svg" width="49%"> <img src="assets/screens/lumina-jardin-light.svg" width="49%">

**Sienne**

<img src="assets/screens/lumina-sienne-dark.svg" width="49%"> <img src="assets/screens/lumina-sienne-light.svg" width="49%">

**Vesper**

<img src="assets/screens/lumina-vesper-dark.svg" width="49%"> <img src="assets/screens/lumina-vesper-light.svg" width="49%">

**Indigo**

<img src="assets/screens/lumina-indigo-dark.svg" width="49%"> <img src="assets/screens/lumina-indigo-light.svg" width="49%">

#### Muted

**Dawn**

<img src="assets/screens/lumina-dawn-dark.svg" width="49%"> <img src="assets/screens/lumina-dawn-light.svg" width="49%">

**Oxblood**

<img src="assets/screens/lumina-oxblood-dark.svg" width="49%"> <img src="assets/screens/lumina-oxblood-light.svg" width="49%">

**Tide**

<img src="assets/screens/lumina-tide-dark.svg" width="49%"> <img src="assets/screens/lumina-tide-light.svg" width="49%">

**Slate**

<img src="assets/screens/lumina-slate-dark.svg" width="49%"> <img src="assets/screens/lumina-slate-light.svg" width="49%">

**Brume**

<img src="assets/screens/lumina-brume-dark.svg" width="49%"> <img src="assets/screens/lumina-brume-light.svg" width="49%">

#### Vivid

**Nocturne**

<img src="assets/screens/lumina-nocturne-dark.svg" width="49%"> <img src="assets/screens/lumina-nocturne-light.svg" width="49%">

**Prisma**

<img src="assets/screens/lumina-prisma-dark.svg" width="49%"> <img src="assets/screens/lumina-prisma-light.svg" width="49%">

**Prisma ink** (black and white)

<img src="assets/screens/lumina-prisma-dark-ink.svg" width="49%"> <img src="assets/screens/lumina-prisma-light-ink.svg" width="49%">

**Neon Cyber**

<img src="assets/screens/lumina-neon-cyber-dark.svg" width="49%"> <img src="assets/screens/lumina-neon-cyber-light.svg" width="49%">

**Synthwave**

<img src="assets/screens/lumina-synthwave-dark.svg" width="49%"> <img src="assets/screens/lumina-synthwave-light.svg" width="49%">

#### Materials

**Sirocco**

<img src="assets/screens/lumina-sirocco-dark.svg" width="49%"> <img src="assets/screens/lumina-sirocco-light.svg" width="49%">

**Celadon**

<img src="assets/screens/lumina-celadon-dark.svg" width="49%"> <img src="assets/screens/lumina-celadon-light.svg" width="49%">

**Sumi**

<img src="assets/screens/lumina-sumi-dark.svg" width="49%"> <img src="assets/screens/lumina-sumi-light.svg" width="49%">

**Pivoine**

<img src="assets/screens/lumina-pivoine-dark.svg" width="49%"> <img src="assets/screens/lumina-pivoine-light.svg" width="49%">

**Café**

<img src="assets/screens/lumina-cafe-dark.svg" width="49%"> <img src="assets/screens/lumina-cafe-light.svg" width="49%">

**Pétrole**

<img src="assets/screens/lumina-petrole-dark.svg" width="49%"> <img src="assets/screens/lumina-petrole-light.svg" width="49%">

#### Gemini's drafts

**Borealis**

<img src="assets/screens/lumina-borealis-dark.svg" width="49%"> <img src="assets/screens/lumina-borealis-light.svg" width="49%">

**Cashmere**

<img src="assets/screens/lumina-cashmere-dark.svg" width="49%"> <img src="assets/screens/lumina-cashmere-light.svg" width="49%">

**Aethelgard**

<img src="assets/screens/lumina-aethelgard-dark.svg" width="49%"> <img src="assets/screens/lumina-aethelgard-light.svg" width="49%">

#### For every eye

**Lucide**

<img src="assets/screens/lumina-lucide-dark.svg" width="49%"> <img src="assets/screens/lumina-lucide-light.svg" width="49%">

### Names

`lumina-<flavor>-<dark|light>` and `lumina-<flavor>-<dark|light>-contrast`,
for example `lumina-vesper-dark` or `lumina-dawn-light-contrast`.
Prisma adds black-and-white twins: `lumina-prisma-dark-ink`,
`lumina-prisma-light-ink` and their `-contrast` versions.

## Supported targets

| Target | Output |
|---|---|
| **Emacs** (vanilla `deftheme`)  | `emacs/themes/*.el` (80), close to 3 000 faces each |
| **Neovim** (Lua colorscheme)    | `nvim/colors/*.lua` (80), over 1 600 groups each, plus `nvim/lua/lualine/themes/*.lua` |
| **VS Code** (extension)         | `vscode/themes/*.json` (124): 565 workbench colours, 80 token scopes, 47 semantic tokens |
| **WezTerm** (color scheme)      | `wezterm/*.toml` (80): ANSI, indexed, tab bar states, copy and quick-select modes |
| **base24** (tinted-theming)     | `base24/*.yaml` (80) |

The Emacs files require no external dependency and load on a bare
`emacs -Q` in about ten milliseconds. Each one styles close to 3 000
faces across the core UI, built-in modes and some 180 packages (see
`generators/faces_src.py` for the full list, grouped by section); faces
of packages you do not use are simply ignored. `docs/showcase.html`,
built by `tools/preview/showcase.sh`, shows every theme on a full
interface mock whose colours are read back from Emacs.

## Install

### Emacs

Requires Emacs 26.1 or later.

**MELPA**:
```elisp
M-x package-install RET lumina-themes RET
M-x load-theme RET lumina-vesper-dark RET
```

**Doom** — `packages.el`:
```elisp
(package! lumina-themes :recipe (:host github :repo "RazikSF/lumina-themes"
                                 :files ("emacs/*.el" "emacs/themes/*.el")))
```
Then `config.el`:
```elisp
(require 'lumina-themes)
(setq doom-theme 'lumina-vesper-dark)
```

**`straight.el`**:
```elisp
(straight-use-package
 '(lumina-themes :type git :host github :repo "RazikSF/lumina-themes"
                 :files ("emacs/*.el" "emacs/themes/*.el")))
(load-theme 'lumina-vesper-dark t)
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
(load-theme 'lumina-vesper-dark t)
```

#### Customisation

Six optional variables, set them before loading a theme or call
`M-x lumina-themes-reapply` after toggling them:

```elisp
(setq lumina-themes-brighter-comments  nil)  ; bolder comments
(setq lumina-themes-comment-bg         nil)  ; tinted comment background
(setq lumina-themes-padded-modeline    nil)  ; t, or integer pixel width
(setq lumina-themes-italic-comments    t)    ; italic on comments
(setq lumina-themes-italic-types       nil)  ; italic on type names
(setq lumina-themes-bold-keywords      nil)  ; bold on keywords
```

`M-x lumina-themes-select` picks a Lumina theme with completion,
`M-x lumina-themes-toggle` switches between the dark and light twin of
the current one, and `M-x lumina-themes-load-random` loads a random
theme (prefix arg `C-u` restricts to dark, `C-u C-u` to light).

### Neovim

**`lazy.nvim`**:
```lua
{
  "RazikSF/lumina-themes",
  init = function()
    vim.opt.rtp:append(vim.fn.stdpath("data") .. "/lazy/lumina-themes/nvim")
  end,
  config = function() vim.cmd.colorscheme("lumina-vesper-dark") end,
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
`colors/` directory, then `:colorscheme lumina-vesper-dark`.

Every colorscheme sets `vim.g.terminal_color_0..15` and covers the
core UI, tree-sitter captures, LSP semantic tokens, diagnostics and
some 70 plugins (telescope, fzf-lua, snacks, nvim-tree, neo-tree, oil,
nvim-cmp, blink.cmp, gitsigns, neogit, diffview, fugitive, flash, leap,
noice, notify, which-key, trouble, lazy, mason, dap-ui, neotest,
render-markdown, orgmode, mini.*, bufferline, barbar, lspsaga, navic and
more). A matching lualine theme ships for each flavor:

```lua
require("lualine").setup({ options = { theme = "lumina-vesper-dark" } })
```

### VS Code

**Marketplace**:
```
ext install RazikSF.lumina-themes
```
Then `Cmd/Ctrl-K Cmd/Ctrl-T` and pick a Lumina flavor.

**Manual `.vsix`**:
```sh
cd vscode && npx @vscode/vsce package
code --install-extension lumina-themes-2.1.0.vsix
```

### WezTerm

```lua
config.color_scheme_dirs = { "/path/to/lumina-themes/wezterm" }
config.color_scheme = "lumina-vesper-dark"
```

### base24 / tinted-theming

The `base24/` YAML files are standard tinted-theming schemes. Use them
with [tinty](https://github.com/tinted-theming/tinty),
[base16-shell](https://github.com/tinted-theming/base16-shell) or any
community template to theme terminals, `bat`, `fzf`, `btop` and the rest
of the CLI from a single source.

## Architecture

```
generators/v2_palettes.py   flavors composed from public scales (compose); signature, -contrast
tools/explore/              palette lab: sources.json, explore.py contact sheet, variants.py
spec/lumina.json            generated palettes (one per flavor/variant)
generators/faces_src.py     face design, grouped by package (edit this)
spec/faces.json             generated face mapping (~3 000 faces)
spec/variables.json         theme variables (hl-todo, vc-annotate, pdf-tools)
generators/nvim_src.py      Neovim highlight design, grouped by plugin (edit this)
spec/nvim_highlights.json   generated Neovim highlight mapping
spec/vscode.json            declarative VS Code workbench + tokens
generators/lumina_gen.py    spec -> all targets; embeds per-flavor schemas
emacs/themes/*.el           generated; pure vanilla deftheme
emacs/lumina-themes.el      Emacs package loader
nvim/colors/*.lua           generated, with nvim/lua/lualine/themes/*.lua
vscode/themes/*.json        generated
vscode/package.json         generated; bundles all flavors
wezterm/*.toml              generated
base24/*.yaml               generated
tools/preview/              Emacs batch renderer, gallery, showcase
tools/distance.py           perceptual distance between flavors
archive/                    fifteen retired flavors, restorable
Makefile                    make build / make check / make verify
```

Lumina is palette-first. `spec/lumina.json` carries one palette per
(flavor, mode); per-flavor syntax schemas live in
`generators/lumina_gen.py` as Python data (lead accent, rainbow /
outline / orderless sequences, modeline and vertico backgrounds, magit
and org mappings, preprocessor and escape slots — shared between dark
and light). The generator resolves palette references to literal hex
per flavor and emits one file per target per (flavor, mode).

A flavor is one `compose(...)` call in `generators/v2_palettes.py`:
ground, lead slot, role map, optional hue overrides. It propagates to
all five targets on the next `make build`; a face edit in
`generators/faces_src.py` propagates to the 124 Emacs themes, one in
`generators/nvim_src.py` to the 52 Neovim colorschemes.

## Develop

Requires Python 3.11+.

```sh
make build       # spec -> all targets
python3 generators/v2_palettes.py   # OKLCH -> spec/lumina.json
make check       # contrast and lightness gate
make verify      # rebuild, check, and smoke-test every theme on vanilla Emacs
tools/preview/gallery.sh            # re-render assets/screens/*.svg
tools/preview/showcase.sh           # docs/showcase.html, full UI mock per theme
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
