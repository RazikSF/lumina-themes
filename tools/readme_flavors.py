#!/usr/bin/env python3
"""Rewrite the Flavors table and gallery of README.md from spec/lumina.json.

Usage: python3 tools/readme_flavors.py
"""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "generators")); sys.path.insert(0, str(ROOT / "tools/preview"))
import lumina_gen as g
from oklch import from_hex
from harmony_apply import hue_name, SCENES

RANGES = {"Signature": ["encre", "nuancier", "aquarelle", "jardin", "sienne", "vesper", "indigo"],
          "Muted": ["dawn", "oxblood", "tide", "slate", "brume"], "Vivid": ["nocturne", "prisma", "neon-cyber", "synthwave"],
          "Materials": ["sirocco", "celadon", "sumi", "pivoine", "cafe", "petrole"],
          "Gemini's drafts": ["borealis", "cashmere", "aethelgard"], "For every eye": ["lucide"]}
ROLES = [("keywords", "Keywords"), ("functions", "Functions"), ("type", "Types"), ("strings", "Strings"),
         ("constants", "Constants"), ("builtin", "Builtins")]
TITLE = {"cafe": "Café", "petrole": "Pétrole", "neon-cyber": "Neon Cyber"}


def main():
    spec = json.loads(g.SPEC.read_text())["flavors"]
    listed = [f for fs in RANGES.values() for f in fs]
    missing = set(spec) - set(listed)
    if missing:
        sys.exit(f"flavors missing from RANGES: {sorted(missing)}")
    title = lambda f: TITLE.get(f, f.capitalize())
    rows = ["| Flavor | Scene | " + " | ".join(n for _, n in ROLES) + " |", "|---" * 8 + "|"]
    gallery = []
    for rng, fs in RANGES.items():
        gallery.append(f"#### {rng}\n")
        for f in fs:
            c = spec[f]["dark"]["colors"]; sch = g.schema_for(f, "dark")
            inks = [hue_name(from_hex(g.resolve_ref(r, c, sch))[2]) for r, _ in ROLES]
            scene = SCENES.get(f, ("", ""))[0]
            rows.append(f"| **{title(f)}** | {scene} | " + " | ".join(inks) + " |")
            gallery.append(f"**{title(f)}**\n\n<img src=\"assets/screens/lumina-{f}-dark.svg\" width=\"49%\"> "
                           f"<img src=\"assets/screens/lumina-{f}-light.svg\" width=\"49%\">\n")
            if f == "prisma":
                gallery.append("**Prisma ink** (black and white)\n\n<img src=\"assets/screens/lumina-prisma-dark-ink.svg\" width=\"49%\"> "
                               "<img src=\"assets/screens/lumina-prisma-light-ink.svg\" width=\"49%\">\n")
    intro = ("Each flavor sets one scene, a ground and six inks, one per role, drawn from a family of hues\n"
             "that suits the scene. The inks are tuned by colour-design theory: the Ou and Luo (2006)\n"
             "harmony model over every pair, Matsuda's hue templates and an even chroma, while staying\n"
             "legible (4.6:1 or more) and apart from one another (`tools/explore/theorie.py`, scored by\n"
             "`tools/explore/beaute.py`). Ink names below are those of the dark variant.\n")
    body = "## Flavors\n\n" + intro + "\n" + "\n".join(rows) + "\n\n### Gallery\n\n" + "\n".join(gallery) + "\n"
    path = ROOT / "README.md"
    text = path.read_text()
    text = re.sub(r"## Flavors\n.*?(?=### Names)", lambda m: body, text, flags=re.S)
    path.write_text(text)
    print(len(rows) - 2, "flavors")


if __name__ == "__main__":
    main()
