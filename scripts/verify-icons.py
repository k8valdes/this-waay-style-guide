#!/usr/bin/env python3
"""
verify-icons.py — the pass/fail gate for the icon concept-naming manifest (Phase 2R
follow-up). Standard library only. Checks assets/icons/icon-manifest.json against the
304 files on disk. Prints PASS/FAIL per check + a summary; exits 0 only if all pass.

    python3 scripts/verify-icons.py
"""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ICONS_DIR = REPO / "product-design-studio" / "assets" / "icons"
MANIFEST = ICONS_DIR / "icon-manifest.json"
EXPECTED_COUNT = 304
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

results = []
def check(name, passed, details=None):
    results.append((name, bool(passed), details or []))


def main():
    if not MANIFEST.exists():
        check("1. manifest file exists", False, [str(MANIFEST)])
        report()
        sys.exit(1)

    try:
        doc = json.loads(MANIFEST.read_text())
    except Exception as e:
        check("1. manifest is valid JSON", False, [str(e)])
        report()
        sys.exit(1)

    icons = doc.get("icons", [])

    # 1. exactly 304 entries, one per icon-NNN.png on disk, zero missing / zero extra
    on_disk = {f"icon-{i:03d}.png" for i in range(1, EXPECTED_COUNT + 1)}
    in_manifest = {e.get("file") for e in icons}
    missing_from_manifest = sorted(on_disk - in_manifest)
    extra_in_manifest = sorted(in_manifest - on_disk)
    c1 = (len(icons) == EXPECTED_COUNT) and not missing_from_manifest and not extra_in_manifest
    check(f"1. {EXPECTED_COUNT}/{EXPECTED_COUNT} icons present in manifest, zero missing/extra",
          c1,
          ([] if len(icons) == EXPECTED_COUNT else [f"manifest has {len(icons)} entries, expected {EXPECTED_COUNT}"])
          + [f"missing: {m}" for m in missing_from_manifest[:10]]
          + [f"unexpected: {e}" for e in extra_in_manifest[:10]])

    # 2. every entry has the required fields, correctly typed; naming convention enforced
    v2 = []
    for e in icons:
        f = e.get("file", "<no file>")
        for field in ("file", "concept", "category", "aliases"):
            if field not in e:
                v2.append(f"{f}: missing field '{field}'")
        concept = e.get("concept")
        if concept and not NAME_RE.match(concept):
            v2.append(f"{f}: concept '{concept}' violates hyphenated-lowercase convention")
        aliases = e.get("aliases")
        if aliases is not None and not isinstance(aliases, list):
            v2.append(f"{f}: aliases must be a list or omitted, got {type(aliases).__name__}")
        elif isinstance(aliases, list) and not (1 <= len(aliases) <= 4):
            v2.append(f"{f}: aliases must have 1-4 entries, got {len(aliases)}")
        if "notes" in e and e["notes"] is not None and not isinstance(e["notes"], str):
            v2.append(f"{f}: notes must be null or a string")
    check("2. every entry has file/concept/category/aliases; concept is hyphenated-lowercase",
          not v2, v2[:15])

    # 3. every file value resolves to a real, existing SVG/PNG on disk
    v3 = []
    for e in icons:
        f = e.get("file")
        if f and not (ICONS_DIR / f).exists():
            v3.append(f"{f}: does not exist on disk at {ICONS_DIR}")
    check("3. every manifest 'file' value resolves to a real file on disk", not v3, v3[:15])

    # 4. zero unresolved concept collisions — a concept may repeat only when every
    #    occurrence carries a qualifier suffix distinguishing it from its siblings
    #    (heuristic: if a bare concept appears 2+ times, that IS the collision — the
    #    fix is for none of them to share the identical bare string).
    from collections import Counter
    concept_counts = Counter(e.get("concept") for e in icons if e.get("concept"))
    unresolved = sorted(c for c, n in concept_counts.items() if n > 1)
    v4 = [f"'{c}' used identically by {concept_counts[c]} icons — needs a qualifier suffix" for c in unresolved]
    check("4. zero unresolved concept collisions (duplicates all carry distinguishing qualifiers)",
          not v4, v4[:15])

    # 5. category values are drawn from a small fixed set (informational: report the set seen)
    categories = sorted(set(e.get("category") for e in icons if e.get("category")))
    check("5. categories used (informational)", True, [", ".join(categories)])

    report()
    sys.exit(0 if all(p for _, p, _ in results) else 1)


def report():
    print(f"verify-icons.py — {MANIFEST}")
    print("-" * 72)
    for name, passed, details in results:
        print(f"[{'PASS' if passed else 'FAIL'}] {name}")
        for d in details[:12]:
            print(f"        - {d}")
        if len(details) > 12:
            print(f"        … and {len(details) - 12} more")
    print("-" * 72)
    n = sum(1 for _, p, _ in results if p)
    print(f"{n}/{len(results)} checks passed — {'ALL PASS' if n == len(results) else 'FAILURES PRESENT'}")


if __name__ == "__main__":
    main()
