#!/bin/bash
# Usage: tools/preview/gallery.sh  -> docs/gallery.html + assets/screens/*.svg
set -e
P=$(cd "$(dirname "$0")" && pwd); R=$(cd "$P/../.." && pwd)
mkdir -p "$P/gal"; rm -f "$P/gal/"*.json
for f in "$R"/emacs/themes/lumina-*-theme.el; do
  t=$(basename "$f" -theme.el)
  case "$t" in *-light*) export R_LIGHT=1 ;; *) unset R_LIGHT ;; esac
  R_THEME=$t R_OUT=$P/gal/$t.json R_PATH=$R/emacs/themes R_DIR=$P R_PY=$R/docs/sample.py \
    emacs -Q --batch -l "$P/render.el" 2>&1 | grep -v LANG | head -2 || true
done
python3 "$P/gallery.py" "$P/gal" "$R"
