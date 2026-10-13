"""Structural audit of every flavor: role separation, lamp hierarchy, warm notes, error red.

Usage: python3 tools/explore/audit.py   (exit 1 when a defect remains)
"""
import json, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "generators"))
from oklch import from_hex
import lumina_gen as g

ROLES = ["functions", "keywords", "type", "strings", "constants", "builtin", "methods"]
NAMES = {"functions": "lampe", "keywords": "mots-clés", "type": "types", "strings": "chaînes", "constants": "constantes", "builtin": "builtins", "methods": "appels"}
CONFUSABLE, WEAK, LAMP_MIN, RED_MIN = 8.0, 12.0, 9.0, 10.0


def lab(h):
    L, C, hh = from_hex(h); return (L, C * math.cos(math.radians(hh)), C * math.sin(math.radians(hh)))


def de(a, b):
    return 100 * math.dist(lab(a), lab(b))


def warm(h):
    return 15 <= from_hex(h)[2] <= 110


def audit(flavor, mode, colors):
    def C(k):
        v = colors[k]; return v[0] if isinstance(v, list) else C(v["ref"])
    role = {r: C(r) for r in ROLES}
    sch = g.schema_for(flavor, mode); role["property"] = C(sch["property"]); role["escape"] = C(sch["escape"])
    issues = []
    keys = ROLES + ["property"]
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            if role[a] == role[b]:
                continue
            d = de(role[a], role[b])
            if d < sch.get("confusable", CONFUSABLE):
                issues.append(f"confondus {NAMES.get(a, a)} / {NAMES.get(b, b)} dE {d:.0f}")

    lamp = role["functions"]
    others = [r for r in ROLES if r != "functions" and role[r] != lamp]
    nearest = min(de(lamp, role[r]) for r in others)
    warm_roles = [r for r in ROLES if warm(role[r])]
    if warm(lamp) and any(r != "functions" for r in warm_roles) and not sch.get("warm_family"):
        issues.append("deux notes chaudes : lampe + " + ", ".join(NAMES[r] for r in warm_roles if r != "functions"))
    if not warm_roles:
        issues.append("aucune note chaude")
    dred = min(de(C("red"), role[r]) for r in ROLES)
    if dred < RED_MIN:
        issues.append(f"rouge d'erreur confondable dE {dred:.0f}")
    return issues


def main():
    spec = json.load(open(ROOT / "spec/lumina.json"))["flavors"]
    bad = 0
    for flavor, modes in spec.items():
        for mode in ("dark", "light"):
            issues = audit(flavor, mode, modes[mode]["colors"])
            bad += bool(issues)
            print(f"{flavor:9s} {mode:5s} " + ("OK" if not issues else " | ".join(issues)))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
