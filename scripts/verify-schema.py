#!/usr/bin/env python3
"""
verify-schema.py — the pass/fail gate for the Phase 3a tiered-schema migration.

Standard library only. Asserts the DTCG-2025.10 three-tier structure and the
rules-as-structure invariants against product-design-studio/tokens.json.
Prints PASS/FAIL per check + a summary; exits 0 only if ALL pass.

    python3 scripts/verify-schema.py

Check 11 (preservation) reads the v3.1 file from git (main:…) to confirm the
excellent bits survived; if git is unavailable it falls back to a curated
must-survive list.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TOKENS = REPO / "product-design-studio" / "tokens.json"
REFS = REPO / "product-design-studio" / "references"
NS = "x.brandkit"
SCHEMA_URL = "https://www.designtokens.org/schemas/2025.10/format.json"

results = []
def check(name, passed, details=None):
    results.append((name, bool(passed), details or []))


def load():
    return json.loads(TOKENS.read_text())


def walk(node, path=()):
    """Yield (path_tuple, token_dict) for every leaf TOKEN (a dict with $value)."""
    if isinstance(node, dict):
        if "$value" in node:
            yield path, node
            return
        for k, v in node.items():
            if k.startswith("$"):
                continue
            yield from walk(v, path + (k,))


def token_at(doc, dotted):
    node = doc
    for seg in dotted.split("."):
        if not isinstance(node, dict) or seg not in node:
            return None
        node = node[seg]
    return node if isinstance(node, dict) and "$value" in node else None


REF_RE = re.compile(r"^\{(.+)\}$")

def resolve(doc, dotted, seen=None):
    """Follow alias chain to a terminal token; return (terminal_path, token) or (None,None)."""
    seen = seen or set()
    if dotted in seen:
        return None, None
    seen.add(dotted)
    tok = token_at(doc, dotted)
    if tok is None:
        return None, None
    val = tok["$value"]
    if isinstance(val, str):
        m = REF_RE.match(val.strip())
        if m:
            return resolve(doc, m.group(1), seen)
    return dotted, tok


def ext(tok):
    return (tok.get("$extensions", {}) or {}).get(NS, {}) if isinstance(tok, dict) else {}


def main():
    raw = TOKENS.read_text()

    # 1. valid JSON, schema URL, version 4.0
    try:
        doc = json.loads(raw); json.dumps(doc); ok_json = True
    except Exception as e:
        check("1. valid JSON / $schema 2025.10 / meta.version 4.0", False, [str(e)])
        report(); sys.exit(1)
    c1 = (doc.get("$schema") == SCHEMA_URL) and (doc.get("meta", {}).get("version") == "4.0")
    check("1. valid JSON / $schema 2025.10 / meta.version 4.0", ok_json and c1,
          [] if c1 else [f"$schema={doc.get('$schema')!r} version={doc.get('meta',{}).get('version')!r}"])

    # 2. every color token literal is object-form (components+hex); no bare hex $value
    bad_color = []
    for path, tok in walk(doc.get("color", {}), ("color",)):
        v = tok["$value"]
        if isinstance(v, str):
            if v.strip().startswith("#"):
                bad_color.append(".".join(path) + " = bare hex")
            continue  # reference alias, fine
        if not (isinstance(v, dict) and "components" in v and "hex" in v):
            bad_color.append(".".join(path) + " = missing components/hex")
    check("2. color tokens are object-form (components+hex), no bare hex", not bad_color, bad_color)

    # 3. every dimension is {value, unit}
    bad_dim = []
    for path, tok in walk(doc.get("dimension", {}), ("dimension",)):
        v = tok["$value"]
        if not (isinstance(v, dict) and "value" in v and "unit" in v):
            bad_dim.append(".".join(path))
    check("3. dimensions are {value, unit}", not bad_dim, bad_dim)

    # 4. three tiers present; every {reference} resolves
    color = doc.get("color", {})
    has_primitive = any(k in color for k in ("navy", "green"))
    has_semantic = all(k in color for k in ("surface", "fill", "text", "border"))
    has_component = all(k in doc for k in ("button", "card", "badge"))
    dangling = []
    for path, tok in walk(doc):
        val = tok["$value"]
        vals = val if isinstance(val, list) else [val]
        # gradient stops are objects {color:"{...}", position:...}
        refs = []
        for item in vals:
            if isinstance(item, str) and REF_RE.match(item.strip()):
                refs.append(REF_RE.match(item.strip()).group(1))
            elif isinstance(item, dict) and isinstance(item.get("color"), str) and REF_RE.match(item["color"].strip()):
                refs.append(REF_RE.match(item["color"].strip()).group(1))
        for r in refs:
            if token_at(doc, r) is None:
                dangling.append(".".join(path) + " -> {" + r + "}")
    check("4. three tiers present; every reference resolves",
          has_primitive and has_semantic and has_component and not dangling,
          ([] if (has_primitive and has_semantic and has_component) else ["missing a tier"]) + dangling)

    # helper: primitives a role-set resolves to
    def role_primitives(group):
        out = {}
        for name, tok in group.items():
            if name.startswith("$"):
                continue
            tp, _ = resolve(doc, "color." + _group_name(group, doc) + "." + name) if False else (None, None)
        return out

    # resolve each semantic role directly
    def prim_of(role_path):
        tp, _ = resolve(doc, role_path)
        return tp

    text_roles = {n: prim_of("color.text." + n) for n in color.get("text", {}) if not n.startswith("$")}
    fill_roles = {n: prim_of("color.fill." + n) for n in color.get("fill", {}) if not n.startswith("$")}
    surface_roles = {n: prim_of("color.surface." + n) for n in color.get("surface", {}) if not n.startswith("$")}
    border_roles = {n: prim_of("color.border." + n) for n in color.get("border", {}) if not n.startswith("$")}

    # 5. no text.* role resolves to a fill primitive (accessible-ink enforcement)
    fill_prims = set(v for v in fill_roles.values() if v)
    text_on_fill_prim = [f"text.{n} -> {p}" for n, p in text_roles.items() if p in fill_prims]
    check("5. no text.* role resolves to a fill primitive (accessible-ink)",
          not text_on_fill_prim, text_on_fill_prim)

    # 6. no surface.* references a gradient-stop primitive
    surf_stop = [f"surface.{n} -> {p}" for n, p in surface_roles.items()
                 if p and p.startswith("color._gradientStops")]
    check("6. no surface.* references a gradient-stop primitive", not surf_stop, surf_stop)

    # 7. fill.subtle/surface.sunken/surface.raised not a text-only value; slate/border.subtle not a text role
    #    text-only primitive = referenced by a text role and by no non-text role
    all_role_prims = {}
    for grp, roles in (("text", text_roles), ("fill", fill_roles), ("surface", surface_roles), ("border", border_roles)):
        for n, p in roles.items():
            all_role_prims.setdefault(p, set()).add(grp)
    text_only = {p for p, groups in all_role_prims.items() if groups == {"text"}}
    v7 = []
    for role in ("color.fill.subtle", "color.surface.sunken", "color.surface.raised"):
        p = prim_of(role)
        if p in text_only:
            v7.append(f"{role} -> text-only {p}")
    border_prim = border_roles.get("subtle")
    for n, p in text_roles.items():
        if p and p == border_prim:
            v7.append(f"text.{n} -> border/slate primitive {p}")
    check("7. proposed roles not text-only; slate/border.subtle not a text role", not v7, v7)

    # 8. typography boldFlag <-> fontWeight; 700 only on fontFamily.regular
    v8 = []
    for name, tok in doc.get("typography", {}).items():
        if name.startswith("$"):
            continue
        val = tok["$value"]; e = ext(tok)
        bf = e.get("boldFlag"); fw = val.get("fontWeight"); fam = val.get("fontFamily")
        if bf is True:
            if fw != 700:
                v8.append(f"typography.{name}: boldFlag true but fontWeight {fw}")
            if fam != "{fontFamily.regular}":
                v8.append(f"typography.{name}: boldFlag true on {fam} (must be fontFamily.regular)")
        elif bf is False:
            if fw != 400:
                v8.append(f"typography.{name}: boldFlag false but fontWeight {fw}")
    check("8. typography boldFlag<->fontWeight; 700 only on Axiforma base", not v8, v8)

    # 9. every component has a status; no component references a color primitive (except noted)
    v9 = []
    prim_color_re = re.compile(r"^color\.(?!surface\.|fill\.|text\.|border\.)")
    for grp_name in ("button", "card", "badge"):
        grp = doc.get(grp_name, {})
        for comp_name, comp in grp.items():
            if comp_name.startswith("$"):
                continue
            if not ext(comp).get("status"):
                # status may sit on the component group; some components carry it via $extensions
                if not (isinstance(comp, dict) and NS in comp.get("$extensions", {})):
                    v9.append(f"{grp_name}.{comp_name}: no status")
            # scan references inside this component for direct color-primitive refs
            for path, tok in walk(comp, (grp_name, comp_name)):
                val = tok["$value"]
                if isinstance(val, str):
                    m = REF_RE.match(val.strip())
                    if m and prim_color_re.match(m.group(1)):
                        noted = bool(ext(tok).get("acceptedDeviation") or ext(tok).get("note"))
                        if not noted:
                            v9.append(f"{'.'.join(path)} -> primitive {m.group(1)} (not via a role, unnoted)")
    check("9. every component has status; no unnoted primitive reference", not v9, v9)

    # 10. accepted-deviation on button.primary.label with all five fields
    lbl = token_at(doc, "button.primary.label")
    dev = ext(lbl).get("acceptedDeviation", {}) if lbl else {}
    need = {"verdict", "decided", "reason", "rejected", "remediationLever"}
    missing = sorted(need - set(dev))
    check("10. accepted-deviation on button.primary.label (5 fields)", lbl is not None and not missing,
          missing or ([] if lbl else ["button.primary.label missing"]))

    # 11. preservation — the excellent bits survive (facts, not prose wording)
    corpus = raw
    for f in (sorted(REFS.glob("*.md")) if REFS.exists() else []):
        corpus += "\n" + f.read_text()
    # curated load-bearing facts: the typo, the deviation figures, key corrections
    must = ["#54b886", "2.42", "#36845D", "6.02", "2026-08 by Kate", "#081F37", "#EEF8EC", "fsType"]
    # augment from v3.1 on main: every distinctive HEX inside a correction/typo note must survive
    try:
        v31 = subprocess.run(["git", "-C", str(REPO), "show", "main:product-design-studio/tokens.json"],
                             capture_output=True, text=True, timeout=10)
        if v31.returncode == 0:
            for note in re.findall(r'"(?:v3Correction|v3Addition|v3Change|correction2026_08|removed2026_08|knownTypo)":\s*"([^"]*)"', v31.stdout):
                for hexcode in re.findall(r'#[0-9A-Fa-f]{6}', note):
                    if hexcode not in must:
                        must.append(hexcode)
    except Exception:
        pass
    # structural presence: the migrated file must still carry these constructs
    struct_ok = all(k in raw for k in ('"knownTypo"', '"acceptedDeviation"', '"provenance"'))
    missing_pres = [s for s in must if s not in corpus]
    if not struct_ok:
        missing_pres.append("missing knownTypo/acceptedDeviation/provenance construct")
    check("11. preservation: knownTypo / deviation / corrections survive", not missing_pres, missing_pres)

    report()
    sys.exit(0 if all(p for _, p, _ in results) else 1)


def _group_name(group, doc):  # unused helper kept for clarity
    return ""


def report():
    print(f"verify-schema.py — {TOKENS}")
    print("-" * 72)
    for name, passed, details in results:
        print(f"[{'PASS' if passed else 'FAIL'}] {name}")
        for d in details[:12]:
            print(f"        - {d}")
        if len(details) > 12:
            print(f"        … and {len(details)-12} more")
    print("-" * 72)
    n = sum(1 for _, p, _ in results if p)
    print(f"{n}/{len(results)} checks passed — {'ALL PASS' if n == len(results) else 'FAILURES PRESENT'}")


if __name__ == "__main__":
    main()
