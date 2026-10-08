#!/bin/bash
S=$(cd "$(dirname "$0")" && pwd); N=$HOME/Dropbox/code/lumina-themes/emacs/themes; DT=$HOME/.config/emacs/.local/straight/build-30.2/doom-themes
r(){ export R_LIGHT; if [ -n "$4" ]; then export R_DOOM=1; else unset R_DOOM; fi
  R_THEME=$1 R_OUT=$S/out/$2.json R_PATH=$3 R_DIR=$S R_PY=$HOME/Dropbox/code/lumina-themes/docs/sample.py emacs -Q --batch -l $S/render.el 2>&1 | grep -v LANG | head -2; }
r lumina-dawn-dark old-dark $S/old; R_LIGHT=1 r lumina-dawn-light old-light $S/old
r lumina-dawn-dark new-dark $N; R_LIGHT=1 r lumina-dawn-light new-light $N
r doom-gruvbox gruvbox-dark "$DT:$DT/themes" D; r doom-gruvbox-light gruvbox-light "$DT:$DT/themes" D
