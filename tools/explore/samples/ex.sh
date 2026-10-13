#!/bin/bash
# Compile chaque fiche et nettoie les fichiers auxiliaires
set -euo pipefail
DOSSIER="${1:-fiches}"

for f in "$DOSSIER"/*.tex; do
  if lualatex -interaction=nonstopmode "$f" > /dev/null; then
    echo "ok : $(basename "$f" .tex)"
  else
    echo "échec : $f" >&2; exit 1
  fi
done
rm -f "$DOSSIER"/*.{aux,log,out}
