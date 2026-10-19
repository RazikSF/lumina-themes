# Lumina

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Colour themes for **Emacs**, **Neovim**, **VS Code**, **WezTerm** and your
terminal: fourteen flavors, each with a dark and a light version, plus a
high-contrast pair for low vision.

Each flavor starts from a scene, a sky at dusk, a lagoon, a café, a
library, and takes its colours from it. The colours are calm and of even
strength: none shouts louder than the others, so your eyes can rest
anywhere on the screen. Rayleigh is the default flavor.

- **Easy on the eyes.** Soft text, tinted by the background.
- **Readable by everyone.** Every colour stays legible and distinct,
  colour-blind readers included.
- **The same everywhere.** One design in every editor, and in over 150
  Emacs packages.

<img src="assets/screens/lumina-rayleigh-dark.svg" width="49%"> <img src="assets/screens/lumina-rayleigh-light.svg" width="49%">

*Rayleigh, the default flavor: the blue hour by night, a clear noon by day.*

## Flavors

<!-- flavors -->
| | Flavor | Dark | Light |
|---|---|---|---|
| <img src="assets/swatches/lumina-rayleigh.svg" width="240"> | **Rayleigh** | Twilight after sunset: the blue hour, the Belt of Venus and the last gold | A clear sky at noon: zenith blue ink on cloud white |
| <img src="assets/swatches/lumina-cherenkov.svg" width="240"> | **Cherenkov** | The blue-violet glow of a reactor pool, uranium-glass green | The same glow printed in cobalt |
| <img src="assets/swatches/lumina-quartz.svg" width="240"> | **Quartz** | Violet quartz on a neutral grey night | Amethyst ink on white paper |
| <img src="assets/swatches/lumina-olive.svg" width="240"> | **Olive** | Provence at dusk: an olive grove, lavender rows, rosé, ochre cliffs, blue shutters, terracotta roofs | Limestone paper, lavender ink |
| <img src="assets/swatches/lumina-dusk.svg" width="240"> | **Dusk** | A warm evening on a mid-dark plum ground: orchid, honey and coral | Lilac paper, aubergine ink |
| <img src="assets/swatches/lumina-oxblood.svg" width="240"> | **Oxblood** | A wine cellar by candlelight: rose and candle gold on wine | Powdered paper, wine and gold inks |
| <img src="assets/swatches/lumina-lagoon.svg" width="240"> | **Lagoon** | A lagoon at dusk on a mid-dark blue-green ground: coral, golden sand, clear water | Pale lagoon paper, coral ink |
| <img src="assets/swatches/lumina-ember.svg" width="240"> | **Ember** | A desk lamp on warm graphite: apricot and butter | Ivory paper, printer's inks |
| <img src="assets/swatches/lumina-canopy.svg" width="240"> | **Canopy** | The sun above a forest at night | Old gold on celadon paper |
| <img src="assets/swatches/lumina-harbor.svg" width="240"> | **Harbor** | Harbour lights on navy water: lemon, amber, sea glass | A nautical chart: teal ink on pale blue paper |
| <img src="assets/swatches/lumina-espresso.svg" width="240"> | **Espresso** | A café at night: espresso, crema, pistachio, cinnamon and a blue enamel cup | Latte paper, roasted inks |
| <img src="assets/swatches/lumina-aurora.svg" width="240"> | **Aurora** | Green curtains over a violet polar night: star gold, the red flash of oxygen | Snow paper under the aurora, emerald ink |
| <img src="assets/swatches/lumina-parchment.svg" width="240"> | **Parchment** | A reading room at night: tobacco leather, a brass lamp, teal bindings | Parchment, teal and madder inks |
| <img src="assets/swatches/lumina-nebula.svg" width="240"> | **Nebula** | An emission nebula in deep space: oxygen cyan, sulphur gold, hydrogen rose | The nebula printed in an atlas: peacock ink on clean white |

The swatches show the six code colours in role order: keywords, functions,
types, strings, constants, builtins; dark variant on the left, light on the right.

### Gallery

**Rayleigh**

<img src="assets/screens/lumina-rayleigh-dark.svg" width="49%"> <img src="assets/screens/lumina-rayleigh-light.svg" width="49%">

**Cherenkov**

<img src="assets/screens/lumina-cherenkov-dark.svg" width="49%"> <img src="assets/screens/lumina-cherenkov-light.svg" width="49%">

**Quartz**

<img src="assets/screens/lumina-quartz-dark.svg" width="49%"> <img src="assets/screens/lumina-quartz-light.svg" width="49%">

**Olive**

<img src="assets/screens/lumina-olive-dark.svg" width="49%"> <img src="assets/screens/lumina-olive-light.svg" width="49%">

**Dusk**

<img src="assets/screens/lumina-dusk-dark.svg" width="49%"> <img src="assets/screens/lumina-dusk-light.svg" width="49%">

**Oxblood**

<img src="assets/screens/lumina-oxblood-dark.svg" width="49%"> <img src="assets/screens/lumina-oxblood-light.svg" width="49%">

**Lagoon**

<img src="assets/screens/lumina-lagoon-dark.svg" width="49%"> <img src="assets/screens/lumina-lagoon-light.svg" width="49%">

**Ember**

<img src="assets/screens/lumina-ember-dark.svg" width="49%"> <img src="assets/screens/lumina-ember-light.svg" width="49%">

**Canopy**

<img src="assets/screens/lumina-canopy-dark.svg" width="49%"> <img src="assets/screens/lumina-canopy-light.svg" width="49%">

**Harbor**

<img src="assets/screens/lumina-harbor-dark.svg" width="49%"> <img src="assets/screens/lumina-harbor-light.svg" width="49%">

**Espresso**

<img src="assets/screens/lumina-espresso-dark.svg" width="49%"> <img src="assets/screens/lumina-espresso-light.svg" width="49%">

**Aurora**

<img src="assets/screens/lumina-aurora-dark.svg" width="49%"> <img src="assets/screens/lumina-aurora-light.svg" width="49%">

**Parchment**

<img src="assets/screens/lumina-parchment-dark.svg" width="49%"> <img src="assets/screens/lumina-parchment-light.svg" width="49%">

**Nebula**

<img src="assets/screens/lumina-nebula-dark.svg" width="49%"> <img src="assets/screens/lumina-nebula-light.svg" width="49%">
<!-- /flavors -->

## Install

### Emacs

Requires Emacs 27.1 or later. The package is `lumina-themes`.

**Emacs 30, `use-package` with `:vc`**:
```elisp
(use-package lumina-themes
  :vc (:url "https://github.com/RazikSF/lumina-themes" :lisp-dir "emacs")
  :config (load-theme 'lumina-rayleigh-dark t))
```

**Doom Emacs**, in `packages.el`:
```elisp
(package! lumina-themes
  :recipe (:host github :repo "RazikSF/lumina-themes"
           :files ("emacs/*.el" "emacs/themes/*.el")))
```
then in `config.el`:
```elisp
(setq doom-theme 'lumina-rayleigh-dark)
```

**straight.el**:
```elisp
(straight-use-package
 '(lumina-themes :type git :host github :repo "RazikSF/lumina-themes"
                 :files ("emacs/*.el" "emacs/themes/*.el")))
(load-theme 'lumina-rayleigh-dark t)
```

**elpaca**:
```elisp
(elpaca (lumina-themes :host github :repo "RazikSF/lumina-themes"
                       :files ("emacs/*.el" "emacs/themes/*.el")))
```

**By hand**: clone the repository, then
```elisp
(add-to-list 'load-path "/path/to/lumina-themes/emacs")
(add-to-list 'custom-theme-load-path "/path/to/lumina-themes/emacs/themes")
(load-theme 'lumina-rayleigh-dark t)
```

The themes are plain `deftheme` files with no dependency. Each one sets
about 3 000 faces: the core interface, built-in modes and over 150
packages (org and org-modern, magit, vertico, corfu, company, consult,
marginalia, embark, treemacs, dirvish, lsp-mode, eglot, tree-sitter,
flycheck, flymake, meow, evil, vterm, mu4e, elfeed, markdown, web-mode,
doom-modeline, transient, which-key, avy and more). Faces of packages
you do not use are simply ignored.

**Commands** (after `(require 'lumina-themes)`):

| Command | Effect |
|---|---|
| `lumina-themes-select` | pick a Lumina theme with completion |
| `lumina-themes-toggle` | switch between the dark and light variant of the current flavor |
| `lumina-themes-load-random` | load a random Lumina theme (`C-u`: dark only, `C-u C-u`: light only) |
| `lumina-themes-reapply` | re-apply the options below after changing them |

**Options**, set before loading a theme:

```elisp
(setq lumina-themes-italic-comments    t)    ; italic comments (default)
(setq lumina-themes-italic-types       nil)  ; italic type names
(setq lumina-themes-bold-keywords      nil)  ; bold instead of semi-bold keywords
(setq lumina-themes-brighter-comments  nil)  ; comments at the docstring contrast
(setq lumina-themes-comment-bg         nil)  ; tinted background behind comments
(setq lumina-themes-padded-modeline    nil)  ; t, or a padding width in pixels
```

### Neovim

Requires Neovim 0.8 or later with true colours (`termguicolors`, on by
default since Neovim 0.10 in terminals that support it). The
colorschemes are written in Lua; Vim is not supported.

**lazy.nvim**:
```lua
{
  "RazikSF/lumina-themes",
  lazy = false,
  priority = 1000,
  config = function()
    vim.cmd.colorscheme("lumina-rayleigh-dark")
  end,
}
```

**vim-plug**: `Plug 'RazikSF/lumina-themes'`, then
`colorscheme lumina-rayleigh-dark`.

`:colorscheme lumina` picks the flavor named by `vim.g.lumina_flavor`
(Rayleigh when it is unset), dark or light after `background`.

Each colorscheme sets about 1 600 highlight groups: the interface,
tree-sitter captures, LSP semantic tokens, diagnostics, the terminal
colours and some 40 plugins (telescope, fzf-lua, snacks, nvim-tree,
neo-tree, oil, nvim-cmp, blink.cmp, gitsigns, neogit, diffview, flash,
leap, noice, which-key, trouble, lazy, mason, dap-ui, neotest,
render-markdown, mini, bufferline, aerial and more). A lualine theme of
the same name ships with each one:

```lua
require("lualine").setup({ options = { theme = "lumina-rayleigh-dark" } })
```

### VS Code

Build the extension from the `vscode/` folder and install it:

```sh
cd vscode && npx @vscode/vsce package --no-dependencies
code --install-extension lumina-themes-1.0.0.vsix
```

Then open the theme picker (`Ctrl+K Ctrl+T`, `Cmd+K Cmd+T` on macOS) and
choose a Lumina flavor: 30 entries. Each
theme sets 568 workbench colours, 94 token rules and 54 semantic token
rules; the Quartz contrast pair registers as a high-contrast theme.

### WezTerm

```lua
config.color_scheme_dirs = { "/path/to/lumina-themes/wezterm" }
config.color_scheme = "lumina-rayleigh-dark"
```

### Terminals and other tools: base24

The `base24/` files are standard [tinted-theming](https://github.com/tinted-theming/home)
schemes. Use them with [tinty](https://github.com/tinted-theming/tinty) or
any tinted-theming template to colour your terminal, `bat`, `fzf`, `btop`
and the rest of your tools.

## Names

`lumina-<flavor>-<dark|light>`, for example `lumina-rayleigh-dark` or
`lumina-aurora-light`, in every editor. Quartz adds
`lumina-quartz-dark-contrast` and `lumina-quartz-light-contrast`: text
above 16:1, comments above 6:1, every code colour at 7:1 or more (WCAG
AAA).

## Contributing

The theme files are generated: please do not edit them by hand. Open an
issue for a colour that lands wrong, an unreadable surface or a missing
package; name the face or highlight group and attach a screenshot.

## License

[MIT](LICENSE).
