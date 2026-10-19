-- lumina -- picks the Lumina theme from 'background' and one setting:
--   vim.g.lumina_flavor = "rayleigh"   (any Lumina flavor; Rayleigh if unset)
-- then :colorscheme lumina.

local mode = vim.o.background == "light" and "light" or "dark"
local name = "lumina-" .. (vim.g.lumina_flavor or "rayleigh") .. "-" .. mode
local file = vim.api.nvim_get_runtime_file("colors/" .. name .. ".lua", false)[1]
if file then
  dofile(file) -- a colour scheme cannot call :colorscheme itself; the theme sets its own name
  vim.g.colors_name = "lumina" -- a later change of 'background' (Neovim reads the terminal's) reloads this picker, not one variant
else
  vim.notify("Lumina: no theme " .. name, vim.log.levels.ERROR)
end
