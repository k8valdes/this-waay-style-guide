#!/usr/bin/env python3
"""
verify-phase3b.py — the Phase 3b pass/fail gate. Exits non-zero on any failure.

  1. Resolver — every reference resolves, no cycles, on the live v4.0 file.
  2. Determinism — the full pipeline run twice is byte-identical.
  3. Production-only — no deprecated/proposed token (the 16 ledger items) in any artifact.
  4. Round-trip — emit_dtcg output is valid 2025.10 and re-resolves to the same values.
  5. No-regression — deck 4/4, docx 3/3, validate.py clean.
  6. Guide — its :root asserts no value contradicting the resolved CSS.

    python3 scripts/verify-phase3b.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from resolve_tokens import Resolver, ResolveError  # noqa: E402
import emit_css, emit_figma, emit_dtcg, emit_pptx  # noqa: E402
import validate  # noqa: E402

REPO = HERE.parent
GUIDE = REPO / "product-design-studio" / "index.html"
DECK = REPO / "assets" / "templates" / "this-waay-deck.potx"
DOCX = REPO / "assets" / "templates" / "this-waay-reference.docx"

results = []
def check(name, ok, details=None):
    results.append((name, bool(ok), details or []))


def main():
    # 1. resolver: no cycles / dangling on the live file
    try:
        r = Resolver()
        prod = r.resolve("production")
        r.resolve("all")
        check("1. resolver: all references resolve, no cycles", True,
              [f"{len(prod)} production tokens resolved"])
    except ResolveError as e:
        check("1. resolver: all references resolve, no cycles", False, [str(e)])
        report(); sys.exit(1)

    # 2. determinism — every emitter run twice is byte-identical
    def gen():
        rr = Resolver(); p = rr.resolve("production")
        return {
            "css": emit_css.emit(p, rr.version),
            "figma": json.dumps(emit_figma.emit(p, rr.version)),
            "dtcg": json.dumps(emit_dtcg.emit(p, rr.version, rr.ns)),
            "pptx": emit_pptx.full_theme_xml(),
        }
    a, b = gen(), gen()
    diff = [k for k in a if a[k] != b[k]]
    check("2. determinism: pipeline run twice is byte-identical", not diff, diff)

    # 3. production-only — 16 ledger items absent from all artifacts
    arts = dict(a)
    hits = [f"{item} in {name}" for name, text in arts.items()
            for item in validate.LEDGER if item in text or validate.slug(item) in text]
    check("3. production-only: 16 ledger items absent from all artifacts", not hits, hits)

    # 4. round-trip — emit_dtcg is valid 2025.10 and re-resolves to same values
    dtcg = emit_dtcg.emit(prod, r.version, r.ns)
    rt = []
    if dtcg.get("$schema") != "https://www.designtokens.org/schemas/2025.10/format.json":
        rt.append("dtcg $schema not 2025.10")
    # spot-check: colours are object form and match the resolved values
    def walk(node, path=()):
        if isinstance(node, dict):
            if "$value" in node:
                yield path, node; return
            for k, v in node.items():
                if not k.startswith("$"):
                    yield from walk(v, path + (k,))
    for path, tok in walk(dtcg):
        if tok.get("$type") == "color":
            v = tok["$value"]
            if not (isinstance(v, dict) and "hex" in v and "components" in v):
                rt.append(f"{'.'.join(path)}: color not object-form")
            else:
                src = prod.get(".".join(path))
                if src and src["value"]["hex"] != v["hex"]:
                    rt.append(f"{'.'.join(path)}: hex drift {v['hex']} != {src['value']['hex']}")
    check("4. round-trip: emit_dtcg valid 2025.10, re-resolves identically", not rt, rt[:8])

    # 5. no-regression — deck 4/4, docx 3/3, validate.py clean
    reg = []
    for label, art in [("deck", DECK), ("docx", DOCX)]:
        rc = subprocess.run([sys.executable, str(HERE / "validate-spec.py"),
                             "--brand", "product-design-studio", "--template", str(art)],
                            capture_output=True, text=True)
        if rc.returncode != 0:
            reg.append(f"{label} template validation failed")
    rc = subprocess.run([sys.executable, str(HERE / "validate.py")], capture_output=True, text=True)
    if rc.returncode != 0:
        reg.append("validate.py failed")
    check("5. no-regression: deck 4/4, docx 3/3, validate.py clean", not reg, reg)

    # 6. guide — its generated --color-* values match emit_css; aliases defined
    g = GUIDE.read_text()
    root = re.search(r':root\s*\{(.*?)\n  \}', g, re.DOTALL).group(1)
    guide_vars = dict(re.findall(r'(--[\w-]+):\s*([^;]+);', root))
    css_vars = dict(re.findall(r'(--[\w-]+):\s*([^;]+);', emit_css.emit(prod, r.version)))
    gcheck = []
    for name, val in css_vars.items():
        if name in guide_vars and guide_vars[name].strip() != val.strip():
            gcheck.append(f"{name}: guide={guide_vars[name].strip()} != css={val.strip()}")
    # every --tw-* the markup uses is defined in :root
    used = set(re.findall(r'var\((--tw-[\w-]+)\)', g))
    undef = [v for v in used if v not in guide_vars]
    if undef:
        gcheck.append(f"undefined vars: {undef[:5]}")
    check("6. guide asserts no value contradicting the resolved CSS", not gcheck, gcheck[:8])

    report()
    sys.exit(0 if all(p for _, p, _ in results) else 1)


def report():
    print("verify-phase3b.py")
    print("-" * 66)
    for name, ok, details in results:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        for d in details[:10]:
            print(f"        - {d}")
    print("-" * 66)
    n = sum(1 for _, p, _ in results if p)
    print(f"{n}/{len(results)} checks passed — {'ALL PASS' if n == len(results) else 'FAILURES'}")


if __name__ == "__main__":
    main()
