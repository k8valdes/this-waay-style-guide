#!/usr/bin/env python3
"""
verify-phase0.py — the pass/fail gate for the Phase 0 spec reconciliation.

Standard library only. Asserts, against product-design-studio/tokens.json,
that every Phase 0 fix is actually present in the file. Prints a PASS/FAIL
line per check and a one-line summary. Exits 0 only if ALL checks pass;
non-zero on any failure.

This is the artifact that makes "done" checkable. Success on this pass is
this script exiting 0 — not prose. Wire it as the last step of any future
spec change:

    python3 scripts/verify-phase0.py
"""

import json
import sys
from pathlib import Path

TOKENS = Path(__file__).resolve().parent.parent / "product-design-studio" / "tokens.json"

results = []  # (name, passed, detail)


def check(name, passed, detail=""):
    results.append((name, bool(passed), detail))


def dig(obj, *keys):
    """Safe nested lookup; returns None if any key is missing."""
    for k in keys:
        if isinstance(obj, dict) and k in obj:
            obj = obj[k]
        else:
            return None
    return obj


def main():
    raw = TOKENS.read_text()

    # 8. Valid JSON that round-trips — do this first; everything else needs the parse.
    roundtrips = False
    data = None
    try:
        data = json.loads(raw)
        json.dumps(data)  # must re-serialize without error
        roundtrips = True
    except Exception as e:  # noqa: BLE001 — any parse/serialize failure is a fail
        check("8. tokens.json is valid JSON and round-trips", False, str(e))
        # Without a parse, the structural checks can't run — report and bail.
        report()
        sys.exit(1)

    # 1. meta.version == "3.1"
    version = dig(data, "meta", "version")
    check("1. meta.version == \"3.1\"", version == "3.1", f"found: {version!r}")

    # 2. "Navy text, never white" appears nowhere in the file
    absent = "Navy text, never white" not in raw
    n = raw.count("Navy text, never white")
    check("2. 'Navy text, never white' absent from file", absent,
          "not found" if absent else f"still present ({n}x)")

    # 3. accessibility.textOnGreenOrTealFill covers white-on-green and cites 2.42
    tog = dig(data, "accessibility", "textOnGreenOrTealFill")
    tog_blob = json.dumps(tog).lower() if tog is not None else ""
    covers_green_white = ("2.42" in tog_blob) and ("white" in tog_blob) and ("green" in tog_blob)
    check("3. textOnGreenOrTealFill states white-on-green @ 2.42",
          covers_green_white,
          "present" if covers_green_white else "missing '2.42' and/or white-on-green language")

    # 4. "borderline" appears nowhere in color.green
    green = dig(data, "color", "green")
    green_blob = json.dumps(green).lower() if green is not None else ""
    no_borderline = "borderline" not in green_blob
    check("4. 'borderline' absent from color.green", no_borderline,
          "clean" if no_borderline else "still present in color.green")

    # 5. spacing.use["96px"] no longer claims the retired clamp
    ninety_six = dig(data, "spacing", "use", "96px") or ""
    no_dead_clamp = "clamped 56-110px" not in ninety_six
    check("5. spacing.use['96px'] drops 'clamped 56-110px'", no_dead_clamp,
          repr(ninety_six[:60] + ("…" if len(ninety_six) > 60 else "")))

    # 6. weightEquivalents promoted to production
    we_status = dig(data, "typography", "family", "weightEquivalents", "status")
    check("6. typography.family.weightEquivalents.status == \"production\"",
          we_status == "production", f"found: {we_status!r}")

    # 7. every family carries a non-empty familyName
    families = dig(data, "typography", "family", "model", "families")
    if isinstance(families, dict) and families:
        missing = [k for k, v in families.items()
                   if not (isinstance(v, dict) and str(v.get("familyName", "")).strip())]
        check("7. every model.families entry has a familyName",
              not missing,
              "all present" if not missing else f"missing on: {', '.join(missing)}")
    else:
        check("7. every model.families entry has a familyName", False,
              "typography.family.model.families not found or empty")

    # 8. (announced last, already computed)
    check("8. tokens.json is valid JSON and round-trips", roundtrips, "ok")

    report()
    sys.exit(0 if all(p for _, p, _ in results) else 1)


def report():
    # keep declared numeric order (1..8) regardless of append order
    ordered = sorted(results, key=lambda r: int(r[0].split(".", 1)[0]))
    print(f"verify-phase0.py — {TOKENS}")
    print("-" * 68)
    for name, passed, detail in ordered:
        tag = "PASS" if passed else "FAIL"
        line = f"[{tag}] {name}"
        if detail:
            line += f"  — {detail}"
        print(line)
    print("-" * 68)
    passed_n = sum(1 for _, p, _ in ordered if p)
    total = len(ordered)
    verdict = "ALL CHECKS PASS" if passed_n == total else "FAILURES PRESENT"
    print(f"{passed_n}/{total} checks passed — {verdict}")


if __name__ == "__main__":
    main()
