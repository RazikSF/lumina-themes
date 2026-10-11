"""The 34 reference themes the user chose, rendered on the same code and ordered from warm to cold.

Warmth = chroma-weighted mean of cos(hue - 50) over text and the seven syntax roles, blended with the tint of ground and text.

Usage: python3 tools/explore/refs.py  -> docs/refs.html
"""
import math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "generators")); sys.path.insert(0, str(ROOT / "tools/explore"))
from oklch import from_hex, contrast
import explore, measure

REFS = ["doom-Iosvkem", "doom-bluloco-dark", "doom-badger", "catppuccin", "doom-dracula", "doom-gruvbox", "doom-henna", "doom-horizon", "doom-laserwave",
        "doom-manegarm", "doom-miramare", "doom-nord-aurora", "doom-oksolar-dark", "doom-old-hope", "doom-one", "doom-outrun-electric", "doom-palenight",
        "doom-peacock", "doom-pine", "doom-rouge", "doom-snazzy", "doom-solarized-dark-high-contrast", "doom-tokyo-night", "doom-tomorrow-night",
        "doom-winter-is-coming-dark-blue", "jetbrains-darcula", "jazz", "tao-yin", "doom-flexoki", "doom-gotham", "doom-indigo", "posimacs-dark", "uwu", "seti"]


def warmth(data):
    d = data["faces"]
    bg = d["default"]["bg"]; fg = d["default"]["fg"]
    cols = [fg] + [(d.get(f) or {}).get("fg") for f in measure.ROLES.values()]
    cols = [c for c in cols if c and c.startswith("#")]
    num = den = 0.0
    for c in cols:
        L, C, h = from_hex(c)
        if C < .03:
            continue
        num += C * math.cos(math.radians(h - 50)); den += C
    acc = num / den if den else 0.0
    bL, bC, bh = from_hex(bg); fL, fC, fh = from_hex(fg)
    tint = (bC * 4 * math.cos(math.radians(bh - 50)) if bC > .004 else 0.0) + (fC * 3 * math.cos(math.radians(fh - 50)) if fC > .01 else 0.0)
    return .7 * acc + .3 * max(-1, min(1, tint)), fh if fC > .01 else None, contrast(fg, bg)


def main():
    rows = []
    for name in REFS:
        data = measure.render(name)
        if not data:
            continue
        w, fh, k = warmth(data)
        tag = "chaud" if w > .25 else "froid" if w < -.25 else "neutre"
        txt = f"texte {'chaud' if fh is not None and (fh < 110 or fh > 330) else 'froid' if fh is not None else 'gris'} {k:.1f}:1"
        rows.append((w, name, explore.card(f"{name} · {tag} ({w:+.2f}) · {txt}", data)))
        print(f"{w:+.2f} {name} {txt}")
    rows.sort(key=lambda r: -r[0])
    page = ("""<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Références</title><style>
body{margin:0;padding:20px 14px;background:#2a2a2a;color:#ddd;font:14px/1.4 -apple-system,system-ui,sans-serif} h1{font-weight:600;margin:0 0 4px} p{color:#aaa;margin:0 0 14px;max-width:90ch}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(560px,1fr));gap:14px}
figure{margin:0} .code{font:12.5px/1.5 "JetBrains Mono",Menlo,monospace;padding:6px 0;border-radius:6px 6px 0 0;overflow:hidden} .r{white-space:pre;padding:0 8px;min-height:1.5em}
.ml{display:flex;align-items:center;gap:8px;font:11.5px Menlo,monospace;padding:5px 8px 5px 0;border-radius:0 0 6px 6px} .bar{width:3px;align-self:stretch}
</style></head><body><h1>Tes 34 références, du plus chaud au plus froid</h1><p>Chaleur mesurée sur le texte et les sept rôles de syntaxe (pondérée par la saturation), puis par la teinte du fond et du texte. Nomme les chaudes que tu aimes, hors Jazz : leur structure commune guidera le pôle chaud.</p><div class="grid">"""
            + "".join(c for _, _, c in rows) + "</div></body></html>")
    (ROOT / "docs/refs.html").write_text(page); print("ok", len(rows), "-> docs/refs.html")


if __name__ == "__main__":
    main()
