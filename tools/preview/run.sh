#!/bin/bash
# Usage: tools/preview/run.sh FLAVOR [GIT_REF]  -> docs/<flavor>2-preview.html
set -e
P=$(cd "$(dirname "$0")" && pwd); R=$(cd "$P/../.." && pwd)
F=${1:?flavor}; REF=${2:-HEAD}
N=$R/emacs/themes; DT=$HOME/.config/emacs/.local/straight/build-30.2/doom-themes
mkdir -p "$P/out" "$P/old"; rm -f "$P/out/"*.json "$P/old/"*.el
for m in dark light; do git -C "$R" show "$REF:emacs/themes/lumina-$F-$m-theme.el" > "$P/old/lumina-$F-$m-theme.el"; done
r(){ if [ -n "$4" ]; then export R_DOOM=1; else unset R_DOOM; fi
  R_THEME=$1 R_OUT=$P/out/$2.json R_PATH=$3 R_DIR=$P R_PY=$R/docs/sample.py emacs -Q --batch -l "$P/render.el" 2>&1 | grep -v LANG | head -2 || true; }
unset R_LIGHT
r lumina-$F-dark old-dark "$P/old"; r lumina-$F-dark new-dark "$N"; r doom-gruvbox gruvbox-dark "$DT:$DT/themes" D
export R_LIGHT=1
r lumina-$F-light old-light "$P/old"; r lumina-$F-light new-light "$N"; r doom-gruvbox-light gruvbox-light "$DT:$DT/themes" D
python3 "$P/build.py" "$P" "$R/docs/${F}2-preview.html" "$F"
