#!/usr/bin/env python3
"""Gemini's dark drafts, face by face, as palette and schema overrides: generators/gemini_drawn.json.

Reads tools/explore/out/drawn-<file>.json (the faces of each draft, dumped from Emacs) and records, for
the plain dark variant, the greys and grounds of the draft (text, selection, current line, line numbers,
mode line, operators, comments, org blocks; a doc face left to the strings is skipped) so the Lumina flavor renders as the draft does.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gemini_import import G

ROOT = Path(__file__).resolve().parents[2]
FILES = {"neon-cyber": "neon-cyber", "borealis": "borealis", "cashmere": "cashmere", "aethelgard": "aethelgard"}
TAKE = {  # palette key <- (face, attribute: 0 fg, 1 bg)
    "fg": ("default", 0), "base8": ("default", 0), "halo": ("hl-line", 1), "region": ("region", 1), "selection": ("region", 1),
    "base4": ("line-number", 0), "fg-alt": ("mode-line", 0), "bg-alt": ("mode-line", 1), "base5": ("mode-line-inactive", 0),
    "base6": ("font-lock-operator-face", 0), "comments": ("font-lock-comment-face", 0), "doc-comments": ("font-lock-doc-face", 0),
    "surface": ("org-block", 1), "halo2": ("show-paren-match", 1), "base2": ("vertical-border", 0),
}


def main():
    out = {}
    for flavor, name in FILES.items():
        faces = json.loads((ROOT / f"tools/explore/out/drawn-{name}.json").read_text())
        pal, inks = {}, {c.upper() for c in G[flavor]["inks"].values()}
        for key, (face, i) in TAKE.items():
            v = faces.get(face, [None, None])[i]
            if v and v.startswith("#") and not (key == "doc-comments" and v.upper() in inks):
                pal[key] = v
        out[flavor] = {"dark": pal}
    (ROOT / "generators/gemini_drawn.json").write_text(json.dumps(out, indent=1) + "\n")
    for f, d in out.items():
        print(f, len(d["dark"]), sorted(set(TAKE) - set(d["dark"])))


if __name__ == "__main__":
    main()
