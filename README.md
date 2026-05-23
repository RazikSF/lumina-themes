# Lumina

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> A curated theme family built on one principle:
> **a single light governs the whole field.**

Each flavor is a monochrome ground — *one* temperature, no contamination —
carrying a bespoke set of accents tuned **to that ground**. Lumina starts
from a hand-tuned reference (Dawn) and rotates only the field hue, holding
the rest of the discipline constant.

## Flavors

Seven lights, each in dark and light — 14 themes total.

| Flavor | The light · the field |
|---|---|
| **Dawn**    | warm sepia-neutral — the reference, the daily driver |
| **Oxblood** | deep oxblood velvet, gilt catching one stage light |
| **Ember**   | cold iron under one incandescent forge-glow |
| **Tide**    | oceanic teal lit from within by a single bioluminescence |
| **Indigo**  | a deep indigo dye vat, copper and verdigris of oxidation |
| **Canopy**  | pine ground, one shaft of sun through the leaves |
| **Slate**   | near-achromatic cold graphite, one steel-blue voice |

**Dawn** is the reference. Tune everything else against it. It is also the
flavor that *almost no one gets right*: a warm-modern paper just tinted
enough not to be screen-light, deep hand-mixed inks varied across the
spectrum. The other six are variations of mood — the *field* changes, the
*method* doesn't.

The coverage is deliberate and considered complete: warm-neutral,
red/wine, orange/forge, teal, blue/indigo, green, cold-neutral — one
position per design axis. Lumina deliberately omits violet (sits between
Oxblood and Indigo) and yellow grounds (not a beautiful field — gimmick
risk). Adding them would be padding, not range.

## Supported targets

| Target | Status | Output |
|---|---|---|
| **Emacs** (vanilla `deftheme`)  | ✓ MELPA-ready | `emacs/themes/*.el` (14) |
| **Neovim** (Lua colorscheme)    | ✓ ready       | `nvim/colors/*.lua` (14) |
| **VS Code** (extension)         | ✓ ready       | `vscode/themes/*.json` (14) + `package.json` |
| **WezTerm** (color scheme dir)  | ✓ ready       | `wezterm/*.toml` (14) |
| **base24** (tinted-theming)     | ✓ ready       | `base24/*.yaml` (14) — multiplier for ~hundreds of CLI apps |

The Emacs files are **pure vanilla** — zero external dependency. They set
a comprehensive face surface (modeline, completion, syntax, outline, org,
diff, dired) explicitly, so the look is polished without depending on any
particular package being present.

## Install

### Emacs

Requires Emacs 26.1 or later.

**MELPA** *(once accepted)*:
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

**Vanilla / `straight.el` / `elpaca`**:
```elisp
;; straight.el
(straight-use-package
 '(lumina-themes :type git :host github :repo "RazikSF/lumina-themes"
                 :files ("emacs/*.el" "emacs/themes/*.el")))
(load-theme 'lumina-dawn-dark t)

;; elpaca
(elpaca (lumina-themes :host github :repo "RazikSF/lumina-themes"
                       :files ("emacs/*.el" "emacs/themes/*.el")))
```

**Manual**: clone the repo and add `emacs/themes/` to
`custom-theme-load-path`:
```elisp
(add-to-list 'custom-theme-load-path "/path/to/lumina-themes/emacs/themes")
(load-theme 'lumina-dawn-dark t)
```

### Neovim

**`lazy.nvim`**:
```lua
{
  "RazikSF/lumina-themes",
  config = function()
    vim.cmd.colorscheme("lumina-dawn-dark")
  end,
}
```
With explicit subdirectory if needed (the schemes live in `nvim/colors/`):
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

**Manual**: copy `nvim/colors/*.lua` into your Neovim runtime's `colors/`
directory, then `:colorscheme lumina-dawn-dark`.

### VS Code

**Marketplace** *(once published)*:
```
ext install RazikSF.lumina-themes
```
Then `Cmd/Ctrl-K Cmd/Ctrl-T` → pick `Lumina Dawn Dark`.

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

The `base24/` YAML files are standard tinted-theming schemes — drop them
into [tinty](https://github.com/tinted-theming/tinty),
[base16-shell](https://github.com/tinted-theming/base16-shell), or any of
the hundreds of community templates to theme terminals, `bat`, `fzf`,
`btop`, and the rest of the CLI from a single source.

## Architecture

```
spec/lumina.json           <- single source of truth (palette per flavor/mode)
generators/lumina_gen.py    <- spec → all targets; embeds the 7 face schemas
emacs/themes/*.el           <- generated; pure vanilla deftheme, no deps
emacs/lumina-themes.el      <- Emacs package loader
nvim/colors/*.lua           <- generated; ~110 highlight groups per scheme
vscode/themes/*.json        <- generated; ~75 colors + 25 tokens + semantic
vscode/package.json         <- generated; bundles all 14 themes
wezterm/*.toml              <- generated
base24/*.yaml               <- generated
melpa/recipes/lumina-themes  <- MELPA submission recipe
MELPA-CHECKLIST.md           <- step-by-step submission per target
Makefile                     <- make build / make verify
```

Lumina is **palette-first**. `spec/lumina.json` carries one palette per
(flavor, mode); seven syntax schemas live in `generators/lumina_gen.py` as
Python data (the per-flavor design: lead accent, rainbow / outline /
orderless sequences, modeline_bg, vertico_bg, magit / org / preprocessor /
escape mappings, shared by dark and light). The generator runs each schema
through a comprehensive face template, resolving palette references to
literal hex per flavor.

**A color edit propagates everywhere.** Open the spec, change `oxblood.dark.colors.red` from `#DE6A66` to your preference, `make build`, and 5 targets re-emit consistently.

## Develop

Requires Python 3.11+ for the generator (uses `tomllib`).

```sh
make build    # spec/lumina.json -> all targets
make verify   # rebuild + pure-vanilla Emacs load-theme smoke test on all 14
```

To retune a color: edit `spec/lumina.json`, `make build`, copy
`emacs/themes/*.el` into your Doom `themes/` directory (or symlink the
directory). Other targets just re-read from their generated files on next
load.

## Add a flavor (the discipline)

A new Lumina flavor must obey four rules. They are what makes Lumina a
coherent *family*:

1. **One field temperature.** The background, all 8 base ramp steps, and
   the foreground share one temperature — no cold contamination of a warm
   field or vice versa.
2. **Bespoke accents accorded to the field.** Do not reuse another
   flavor's accent set. Mix accents tuned for *this* ground — usually
   pulled slightly toward the field's hue, desaturated relative to stock,
   luminance-harmonized so no single accent screams against the field.
3. **A single lead accent that governs the syntax surface.** All visual
   hooks that emphasize the active surface — modeline bar, cursor, primary
   headings, completion match, opening rainbow delimiter, primary outline
   level — share this single accent. That's the "single light".
4. **The light variant is derived from the dark by inverting the field**
   (warm-tinted paper or cool-tinted paper of the same temperature, then
   deep inks of the same family).

Practical steps:
1. Add a new `flavors.<name>` entry under `dark` and `light` in
   `spec/lumina.json` with full palette + helpers + commentary.
2. Add a matching schema in `SCHEMAS` of `generators/lumina_gen.py`.
3. `make build && make verify`.

## Contributing

PRs that add a flavor must justify the new field on the coverage map (does
it fill a hole that isn't padding?), follow the discipline above, and
include a screenshot. PRs that retune existing flavors should explain the
intent and include before/after.

Issues for color bugs (contrast on a specific UI surface, a face that
landed wrong) are welcome — they're how the discipline gets enforced.

## License

Licensed under the [MIT License](LICENSE).
