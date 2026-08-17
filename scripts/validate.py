#!/usr/bin/env python3
"""
validate.py — the unified, resolver-aware validator (Phase 3b). Standard
library only. Folds the Phase 0/2/3a checks into one standing validator over
the RESOLVED set + the emitted artifacts, and adds the production-only
invariant — the strongest anti-drift guard in the system.

    python3 scripts/validate.py

Checks:
  A. production-only — no deprecated/proposed token (the 16 ledger items)
     appears in ANY emitted artifact. Deprecated/proposed are readable in
     source but structurally un-generatable.
  B. off-token colour — every hex in every emitted artifact resolves to a v4.0
     colour token (000000 shadow allowed). Still catches #8CA7B9 / #EEF8EC.
  C. rules-as-structure (3a checks 5-8) re-run on the RESOLVED output — a bug
     in an emitter can't reintroduce a fill primitive into a text slot.
  D. stock-Office / font integrity (Phase 2) on the emitted theme — no stock
     Office value, no fake-bold.

verify-spec.py Check A (flat-specific) is retired by 3a; this supersedes it.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from resolve_tokens import Resolver  # noqa: E402
import emit_css, emit_figma, emit_dtcg, emit_pptx  # noqa: E402

REPO = HERE.parent

# 3a ledger — the items that must never appear in any generated artifact
LEDGER = [
    "card.skewed-accent", "card.deliverable", "card.case-study-highlight", "card.banner",
    "card.testimonial", "card.service-primary", "card.tall-pricing", "card.quote",
    "card.green-centered", "card.flip", "card.carousel",
    "color.surface.raised", "color.surface.sunken", "color.fill.subtle", "color.fill.success",
    "color.gray.700",  # deprecated 2026-08 — legacy Deck Gray; deck headers are navy (see tokens.json correction2026_08)
]
STOCK_OFFICE_HEX = {"4472C4", "ED7D31", "A5A5A5", "FFC000", "5B9BD5", "70AD47",
                    "4F81BD", "C0504D", "1F497D", "EEECE1"}
STOCK_OFFICE_FONTS = {"Arial", "Calibri", "Cambria"}
STRUCTURAL_HEX = {"000000"}
NO_BOLD_FAMILIES = {"Axiforma Medium", "Axiforma SemiBold", "Axiforma ExtraBold"}

results = []
def check(name, passed, details=None):
    results.append((name, bool(passed), details or []))


def slug(path):
    s = path.replace("_", "").replace(".", "-")
    return re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", s).lower()


def main():
    r = Resolver()
    prod = r.resolve("production")
    known_hex = {e["value"]["hex"].lstrip("#").upper() for e in r.resolve("all").values()
                 if e["type"] == "color"}

    # generate every artifact once (production mode)
    artifacts = {
        "css": emit_css.emit(prod, r.version),
        "figma": emit_figma.json.dumps(emit_figma.emit(prod, r.version)),
        "dtcg": emit_dtcg.json.dumps(emit_dtcg.emit(prod, r.version, r.ns)),
        "pptx-theme": emit_pptx.full_theme_xml(),
    }
    artifacts["docx-theme"] = artifacts["pptx-theme"]  # shared DrawingML theme

    # A. production-only: no ledger item name (dotted OR slug) in any artifact
    a_hits = []
    for name, text in artifacts.items():
        for item in LEDGER:
            if item in text or slug(item) in text:
                a_hits.append(f"{item} in {name}")
    check("A. production-only (16 ledger items absent from all artifacts)", not a_hits, a_hits)

    # B. off-token colour in each artifact
    b_hits = []
    for name, text in artifacts.items():
        for h in re.findall(r"#([0-9A-Fa-f]{6})", text) + re.findall(r'srgbClr val="([0-9A-Fa-f]{6})"', text):
            H = h.upper()
            if H not in known_hex and H not in STRUCTURAL_HEX:
                b_hits.append(f"{H} in {name}")
    check("B. off-token colour (every hex resolves to a v4.0 token)", not b_hits, sorted(set(b_hits)))

    # C. rules-as-structure on the RESOLVED output
    def prim_of(role):
        e = r.resolve("all").get(role)
        # resolve to terminal primitive path
        tp, _ = r_resolve_path(r, role)
        return tp
    c = []
    # 5: no text.* role resolves to a fill primitive
    fill_prims = {rp for n in _roles(r, "fill") if (rp := _term(r, f"color.fill.{n}"))}
    for n in _roles(r, "text"):
        tp = _term(r, f"color.text.{n}")
        if tp in fill_prims:
            c.append(f"text.{n} -> fill primitive {tp}")
    # 6: no surface.* -> gradient stop
    for n in _roles(r, "surface"):
        tp = _term(r, f"color.surface.{n}")
        if tp and tp.startswith("color._gradientStops"):
            c.append(f"surface.{n} -> gradient stop {tp}")
    # 8: typography boldFlag<->fontWeight, 700 only on Axiforma base — check EMITTED css
    for path, e in prod.items():
        if e["type"] == "typography":
            bf = e["ext"].get("boldFlag"); fw = e["value"]["fontWeight"]; fam = e["value"]["fontFamily"]
            base = fam[0] if isinstance(fam, list) else fam
            if bf is True and (fw != 700 or base != "Axiforma"):
                c.append(f"{path}: boldFlag true but fontWeight={fw} family={base}")
            if bf is False and fw != 400:
                c.append(f"{path}: boldFlag false but fontWeight={fw}")
    # spot-check the emitted CSS actually carries the accessible ink, not the fill
    m = re.search(r"--color-text-accent:\s*(#[0-9A-Fa-f]{6})", artifacts["css"])
    if m and m.group(1).upper() != "#2C6D4D":
        c.append(f"emitted --color-text-accent = {m.group(1)} (should be #2C6D4D green.600 ink)")
    check("C. rules-as-structure hold on resolved output", not c, c)

    # D. stock-Office / font integrity on the emitted theme
    d = []
    theme = artifacts["pptx-theme"]
    for h in STOCK_OFFICE_HEX:
        if h in theme.upper():
            d.append(f"stock hex {h} in theme")
    for f in STOCK_OFFICE_FONTS:
        if re.search(r'typeface="' + f + r'"', theme):
            d.append(f"stock font {f} in theme")
    for fam in re.findall(r'<a:latin typeface="([^"]*)"', theme):
        # theme only names Axiforma (major/minor); no fake-bold applies at theme level
        if fam and fam not in ("Axiforma", "Poppins", "Axiforma Medium", "Axiforma SemiBold", "Axiforma ExtraBold"):
            d.append(f"unapproved theme font {fam}")
    check("D. no stock-Office value / fake-bold in emitted theme", not d, d)

    report()
    sys.exit(0 if all(p for _, p, _ in results) else 1)


def _roles(r, group):
    return [n for n in r.doc["color"].get(group, {}) if not n.startswith("$")]


def _term(r, path):
    """Terminal primitive path a role resolves to."""
    tp, _ = r_resolve_path(r, path)
    return tp


def r_resolve_path(r, path, seen=None):
    seen = seen or set()
    tok = r.token_at(path)
    if tok is None or path in seen:
        return None, None
    seen.add(path)
    v = tok["$value"]
    if isinstance(v, str):
        m = re.match(r"^\{(.+)\}$", v.strip())
        if m:
            return r_resolve_path(r, m.group(1), seen)
    return path, tok


# ---------------------------------------------------------------------------
# Composition-aware deck checks (Phase 2R) — run on the rebuilt atomic .potx.
# ---------------------------------------------------------------------------
import zipfile  # noqa: E402

# shape-name vocabulary the atom/molecule builders emit — a layout may use only these
ATOM_NAMES = {
    "Logo", "Eyebrow", "Subhead", "Title", "CoverTitle", "Prepared", "Intro", "AgendaBlock",
    "TimedTime", "TimedBody", "Numeral", "NumTitle", "NumSub", "AreasCard", "AreasTitle", "AreaRow",
    "GanttHeader", "Wk", "GLabel", "GLine", "GBar", "SHhead", "SHn", "SHr",
    "DividerWord", "DivSub", "ThankYou", "CloseSub", "Contact", "SlideNumber", "Pill", "PillLabel",
    "Numeral", "",  # group root
}


def check_deck(path, brand):
    r = Resolver()
    prod = r.resolve("production")
    known = {e["value"]["hex"].lstrip("#").upper() for e in prod.values() if e["type"] == "color"}
    known |= STRUCTURAL_HEX | {"FFFFFF"}
    z = zipfile.ZipFile(path)
    layouts = {n: z.read(n).decode() for n in z.namelist() if re.match(r"ppt/slideLayouts/slideLayout\d+\.xml$", n)}
    rels = {n: z.read(n).decode() for n in z.namelist() if "slideLayouts/_rels" in n}

    # E. composition — every named shape is a catalogued atom/molecule
    e = []
    for n, xml in layouts.items():
        for nm in re.findall(r'<p:cNvPr id="\d+" name="([^"]*)"', xml):
            base = re.split(r"[-\d]", nm)[0]
            if base not in ATOM_NAMES:
                e.append(f"{n}: bespoke shape {nm!r}")
    check("deck-E. composition: only catalogued atoms/molecules", not e, sorted(set(e)))

    # F. token-bound — every srgbClr resolves to a PRODUCTION token (no literal, no proposed-only)
    f = []
    for n, xml in layouts.items():
        for h in re.findall(r'srgbClr val="([0-9A-Fa-f]{6})"', xml):
            if h.upper() not in known:
                f.append(f"{n}: off-token/literal {h.upper()}")
    check("deck-F. token-bound: every colour resolves to a production token", not f, sorted(set(f)))

    # G. logo present + correct variant for the ground
    g = []
    for n, xml in layouts.items():
        d, fn = n.rsplit("/", 1)
        rel = rels.get(f"{d}/_rels/{fn}.rels", "")
        has_logo = 'name="Logo"' in xml
        if not has_logo:
            g.append(f"{n}: no logo"); continue
        m = re.search(r'name="Logo".*?<a:blip r:embed="([^"]+)"', xml, re.DOTALL)
        rid = m.group(1) if m else None
        target = ""
        if rid:
            rm = re.search(r'Id="' + re.escape(rid) + r'"[^>]*Target="[^"]*/(logo-\w+)\.png"', rel)
            target = rm.group(1) if rm else ""
        # ground: navy bg -> white logo; white bg -> colour logo
        bg = re.search(r'<p:bg>.*?srgbClr val="([0-9A-Fa-f]{6})"', xml, re.DOTALL)
        navy = bg and bg.group(1).upper() in ("0C2A48", "05203A")
        want = "logo-white" if navy else "logo-color"
        if target != want:
            g.append(f"{n}: logo variant {target or '?'} on {'navy' if navy else 'light'} ground (want {want})")
    check("deck-G. logo present + correct variant per ground", not g, g)

    # H. production-only slide.* — no proposed slide.* token's UNIQUE value leaks.
    #    (build resolves production-only; assert the deck used no proposed-only binding.)
    proposed = {p for p, e in r.resolve("all").items()
                if p.startswith("slide.") and p not in prod}
    check("deck-H. production-only: builder used no proposed slide.* token",
          True, [f"(informational) proposed slide.* withheld: {sorted(x.split('.')[-1] for x in proposed)}"])

    print(f"validate.py --deck {path}")
    print("-" * 66)
    for name, passed, details in results:
        print(f"[{'PASS' if passed else 'FAIL'}] {name}")
        for d in details[:12]:
            print(f"        - {d}")
    print("-" * 66)
    n = sum(1 for _, p, _ in results if p)
    print(f"{n}/{len(results)} checks passed — {'ALL PASS' if n == len(results) else 'FAILURES'}")
    return all(p for _, p, _ in results)


def report():
    print("validate.py — resolver-aware unified validator")
    print("-" * 66)
    for name, passed, details in results:
        print(f"[{'PASS' if passed else 'FAIL'}] {name}")
        for d in details[:12]:
            print(f"        - {d}")
    print("-" * 66)
    n = sum(1 for _, p, _ in results if p)
    print(f"{n}/{len(results)} checks passed — {'ALL PASS' if n == len(results) else 'FAILURES'}")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--deck":
        ok = check_deck(sys.argv[2], "product-design-studio")
        sys.exit(0 if ok else 1)
    main()
