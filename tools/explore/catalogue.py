"""Catalogue: every installed dark theme rendered on the same code, to pick references by eye.

Usage: python3 tools/explore/catalogue.py  -> docs/catalogue.html
"""
import glob, json, os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "tools/explore"))
import explore

B = Path.home() / ".config/emacs/.local/straight/build-30.2"
SKIP = ("light", "day", "dawn", "latte", "frappe", "operandi", "morning", "spring", "summer", "cyprus", "arbutus", "kassio", "reverie", "frost", "elea-light", "maris-light", "melissa-light", "duo-light", "trio-light", "deuteranopia-light", "tritanopia-light", "eagle", "lumina", "doom-lumina", "celestia", "neoschool", "axiom", "lagoon", "forest", "rhodium", "terra", "leuven", "tango-plus", "alabaster", "parchment", "nano-light", "standard-light", "solarized-light", "gruvbox-light", "nord-light", "one-light", "opera-light", "feather-light", "acario-light", "bluloco-light", "homage-white", "oksolar-light", "flatwhite", "plain", "tomorrow-day", "winter-is-coming-light", "ayu-light", "ef-light", "ef-duo-light")


def main():
    files = sorted(glob.glob(str(B / "*/*-theme.el"))) + sorted(glob.glob(str(Path.home() / ".doom.d/themes/*-theme.el")))
    cards = []; seen = set()
    for f in files:
        name = Path(f).name[:-len("-theme.el")]
        if name in seen or any(s in name for s in SKIP) or name.startswith(("lumina", "doom-celestia", "doom-neoschool", "doom-axiom", "doom-lagoon", "doom-forest", "doom-rhodium", "doom-terra", "doom-frost", "ground-", "lab-")):
            continue
        seen.add(name)
        d = Path(f).parent
        env = dict(os.environ, R_THEME=name, R_OUT=str(explore.OUT / f"cat-{name}.json"), R_PATH=f"{d}:{d.parent}:{B / 'doom-themes'}:{B / 'doom-themes' / 'themes'}",
                   R_DIR=str(ROOT / "tools/preview"), R_PY=str(ROOT / "docs/sample.py"), R_DOOM="1" if name.startswith("doom-") else "")
        env.pop("R_LIGHT", None)
        if not env["R_DOOM"]:
            env.pop("R_DOOM")
        r = subprocess.run(["emacs", "-Q", "--batch", "-l", str(ROOT / "tools/preview/render.el")], env=env, capture_output=True, timeout=60)
        out = explore.OUT / f"cat-{name}.json"
        if not out.exists():
            continue
        try:
            data = json.loads(out.read_text())
        except Exception:
            continue
        bg = (data["faces"].get("default") or {}).get("bg") or ""
        import re as _re
        if not _re.fullmatch(r"#[0-9A-Fa-f]{6}", bg):
            out.unlink(); continue
        L = int(bg[1:3], 16) * .299 + int(bg[3:5], 16) * .587 + int(bg[5:7], 16) * .114
        if L > 110:
            out.unlink(); continue
        cards.append((name, explore.card(name, data))); out.unlink()
    page = ("""<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Catalogue sombre</title><style>
body{margin:0;padding:20px 14px;background:#2a2a2a;color:#ddd;font:14px/1.4 -apple-system,system-ui,sans-serif} h1{font-weight:600;margin:0 0 4px} p{color:#aaa;margin:0 0 14px;max-width:90ch}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(560px,1fr));gap:14px}
figure{margin:0} .code{font:12.5px/1.5 "JetBrains Mono",Menlo,monospace;padding:6px 0;border-radius:6px 6px 0 0;overflow:hidden} .r{white-space:pre;padding:0 8px;min-height:1.5em}
.ml{display:flex;align-items:center;gap:8px;font:11.5px Menlo,monospace;padding:5px 8px 5px 0;border-radius:0 0 6px 6px} .bar{width:3px;align-self:stretch}
</style></head><body><h1>Catalogue : thèmes sombres installés</h1><p>""" + f"{len(cards)} thèmes, même code, même Emacs. Nomme les trois à cinq que tu trouves beaux ; leur structure commune servira de recette." + """</p><div class="grid">"""
            + "".join(c for _, c in cards) + "</div></body></html>")
    (ROOT / "docs/catalogue.html").write_text(page); print("ok", len(cards), "themes -> docs/catalogue.html")


if __name__ == "__main__":
    main()
