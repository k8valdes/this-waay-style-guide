#!/usr/bin/env python3
"""
build_theme.py — generate the OOXML <a:clrScheme> and <a:fontScheme> for the
This Waay brand, straight from product-design-studio/tokens.json.

Generated, never hand-edited. A hand-maintained theme is the Phase 1 mirror
problem again: if a value is wrong, fix tokens.json (upstream) or this script,
never the emitted XML.

Consumed by build_deck.py and build_reference_docx.py, which splice the two
elements into each package's theme1.xml. Runnable standalone to inspect output:

    python3 scripts/build_theme.py                # prints clrScheme + fontScheme
    python3 scripts/build_theme.py --full         # prints a complete theme1.xml
    python3 scripts/build_theme.py --check         # asserts token source is v3.1

Standard-library only. XML is emitted as strings (not via ElementTree, which
rewrites namespace prefixes and corrupts the package).
"""

import argparse
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TOKENS = REPO_ROOT / "product-design-studio" / "tokens.json"

EXPECTED_VERSION = "3.1"
EXPECTED_UPDATED = "2026-08-13"

# Theme slot -> tokens.json color key. Order is the OOXML-required clrScheme
# child order (dk1, lt1, dk2, lt2, accent1-6, hlink, folHlink) — do not reorder.
#
# accent1..accent4 are dataViz.seriesOrder IN ORDER on purpose: native
# PowerPoint charts then inherit the brand series sequence with zero per-chart
# configuration. accent5 is gridlines (slate); accent6 is punch green, placed
# last so a default chart never reaches it.
SLOT_MAP = OrderedDict([
    ("dk1",      "navy"),        # -> tx1 (dark text / dark ground)
    ("lt1",      "white"),       # -> bg1 (light ground)
    ("dk2",      "navyDeep"),    # -> tx2
    ("lt2",      "ice"),         # -> bg2  (completeness only; NO layout may use as a ground)
    ("accent1",  "green"),       # seriesOrder[0]
    ("accent2",  "steel"),       # seriesOrder[1]
    ("accent3",  "teal"),        # seriesOrder[2]
    ("accent4",  "navy"),        # seriesOrder[3]
    ("accent5",  "slate"),       # chart gridlines
    ("accent6",  "greenPunch"),  # punch — last, so default charts never reach it
    ("hlink",    "tealInk"),
    ("folHlink", "inkMuted"),
])

# Cross-check: the values SLOT_MAP is expected to resolve to. If tokens.json
# ever drifts from these, tokens wins (it is the source of truth) and the theme
# follows — but a mismatch is surfaced as a warning so drift is never silent.
EXPECTED_VALUES = {
    "dk1": "#0C2A48", "lt1": "#FFFFFF", "dk2": "#05203A", "lt2": "#F2FBFB",
    "accent1": "#54B987", "accent2": "#0D698A", "accent3": "#0BABAB",
    "accent4": "#0C2A48", "accent5": "#8DA3B5", "accent6": "#3DD68C",
    "hlink": "#077373", "folHlink": "#5C7185",
}

# Brand-agnostic format scheme (fills/lines/effects) — references phClr
# placeholders only, so it carries no hardcoded colour and inherits the brand
# clrScheme automatically. Standard Office shape. Not brand data; kept verbatim.
FMT_SCHEME = (
    '<a:fmtScheme name="Office">'
    '<a:fillStyleLst>'
    '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
    '<a:gradFill rotWithShape="1"><a:gsLst>'
    '<a:gs pos="0"><a:schemeClr val="phClr"><a:lumMod val="110000"/><a:satMod val="105000"/><a:tint val="67000"/></a:schemeClr></a:gs>'
    '<a:gs pos="50000"><a:schemeClr val="phClr"><a:lumMod val="105000"/><a:satMod val="103000"/><a:tint val="73000"/></a:schemeClr></a:gs>'
    '<a:gs pos="100000"><a:schemeClr val="phClr"><a:lumMod val="105000"/><a:satMod val="109000"/><a:tint val="81000"/></a:schemeClr></a:gs>'
    '</a:gsLst><a:lin ang="5400000" scaled="0"/></a:gradFill>'
    '<a:gradFill rotWithShape="1"><a:gsLst>'
    '<a:gs pos="0"><a:schemeClr val="phClr"><a:satMod val="103000"/><a:lumMod val="102000"/><a:tint val="94000"/></a:schemeClr></a:gs>'
    '<a:gs pos="50000"><a:schemeClr val="phClr"><a:satMod val="110000"/><a:lumMod val="100000"/><a:shade val="100000"/></a:schemeClr></a:gs>'
    '<a:gs pos="100000"><a:schemeClr val="phClr"><a:lumMod val="99000"/><a:satMod val="120000"/><a:shade val="78000"/></a:schemeClr></a:gs>'
    '</a:gsLst><a:lin ang="5400000" scaled="0"/></a:gradFill>'
    '</a:fillStyleLst>'
    '<a:lnStyleLst>'
    '<a:ln w="6350" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/><a:miter lim="800000"/></a:ln>'
    '<a:ln w="12700" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/><a:miter lim="800000"/></a:ln>'
    '<a:ln w="19050" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/><a:miter lim="800000"/></a:ln>'
    '</a:lnStyleLst>'
    '<a:effectStyleLst>'
    '<a:effectStyle><a:effectLst/></a:effectStyle>'
    '<a:effectStyle><a:effectLst/></a:effectStyle>'
    '<a:effectStyle><a:effectLst><a:outerShdw blurRad="57150" dist="19050" dir="5400000" rotWithShape="0"><a:srgbClr val="000000"><a:alpha val="63000"/></a:srgbClr></a:outerShdw></a:effectLst></a:effectStyle>'
    '</a:effectStyleLst>'
    '<a:bgFillStyleLst>'
    '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
    '<a:solidFill><a:schemeClr val="phClr"><a:tint val="95000"/><a:satMod val="170000"/></a:schemeClr></a:solidFill>'
    '<a:gradFill rotWithShape="1"><a:gsLst>'
    '<a:gs pos="0"><a:schemeClr val="phClr"><a:tint val="93000"/><a:satMod val="150000"/><a:shade val="98000"/><a:lumMod val="102000"/></a:schemeClr></a:gs>'
    '<a:gs pos="50000"><a:schemeClr val="phClr"><a:tint val="98000"/><a:satMod val="130000"/><a:shade val="90000"/><a:lumMod val="103000"/></a:schemeClr></a:gs>'
    '<a:gs pos="100000"><a:schemeClr val="phClr"><a:shade val="63000"/><a:satMod val="120000"/></a:schemeClr></a:gs>'
    '</a:gsLst><a:lin ang="5400000" scaled="0"/></a:gradFill>'
    '</a:bgFillStyleLst>'
    '</a:fmtScheme>'
)


def load_tokens(path=DEFAULT_TOKENS):
    return json.loads(Path(path).read_text())


def assert_version(tokens, strict=True):
    v = tokens.get("meta", {}).get("version")
    u = tokens.get("meta", {}).get("updated")
    ok = (v == EXPECTED_VERSION and u == EXPECTED_UPDATED)
    if not ok and strict:
        sys.exit(f"error: token source is version={v!r} updated={u!r}; "
                 f"expected {EXPECTED_VERSION} / {EXPECTED_UPDATED}. "
                 f"Wrong or stale copy — stop and resolve before building.")
    return ok


def color_value(tokens, key):
    entry = tokens["color"].get(key)
    if not (isinstance(entry, dict) and isinstance(entry.get("value"), str)):
        sys.exit(f"error: color token {key!r} missing or malformed in tokens.json")
    return entry["value"]


def _hex6(v):
    """'#0C2A48' -> '0C2A48' (OOXML srgbClr wants no leading #, upper case)."""
    return v.lstrip("#").upper()


def clr_scheme_xml(tokens, name="This Waay"):
    warnings = []
    parts = [f'<a:clrScheme name="{name}">']
    for slot, token in SLOT_MAP.items():
        val = color_value(tokens, token)
        exp = EXPECTED_VALUES.get(slot)
        if exp and val.upper() != exp.upper():
            warnings.append(f"  slot {slot} ({token}) = {val}, expected {exp}")
        parts.append(f'<a:{slot}><a:srgbClr val="{_hex6(val)}"/></a:{slot}>')
    parts.append('</a:clrScheme>')
    for w in warnings:
        print("warning: token/theme mapping drift:\n" + w, file=sys.stderr)
    return "".join(parts)


def font_scheme_xml(name="This Waay"):
    # majorFont = minorFont = "Axiforma". That family contains a genuine Bold,
    # so b="1" on a run resolves to real Bold 700 (not synthesized). SemiBold /
    # ExtraBold / Medium are SEPARATE families and are unreachable via the theme
    # — layouts set them explicitly on the placeholder. ea/cs empty; Poppins is
    # NOT a theme entry (fallback is the installed-font resolution chain).
    return (
        f'<a:fontScheme name="{name}">'
        '<a:majorFont><a:latin typeface="Axiforma"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>'
        '<a:minorFont><a:latin typeface="Axiforma"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont>'
        '</a:fontScheme>'
    )


def full_theme_xml(tokens, name="This Waay"):
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
        '<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        f'name="{name}"><a:themeElements>'
        + clr_scheme_xml(tokens, name)
        + font_scheme_xml(name)
        + FMT_SCHEME
        + '</a:themeElements><a:objectDefaults/><a:extraClrSchemeLst/></a:theme>'
    )


def splice_into_theme(base_theme_xml, tokens, name="This Waay"):
    """Replace the <a:clrScheme> and <a:fontScheme> elements in an existing
    theme1.xml (e.g. one python-pptx/python-docx generated) with the
    brand-generated ones, leaving fmtScheme and everything else untouched.
    Surgical string replacement — no XML round-trip, so namespace prefixes and
    the rest of the package are preserved byte-for-byte outside the two blocks.
    """
    out = re.sub(r"<a:clrScheme\b.*?</a:clrScheme>",
                 lambda m: clr_scheme_xml(tokens, name), base_theme_xml, count=1, flags=re.DOTALL)
    out = re.sub(r"<a:fontScheme\b.*?</a:fontScheme>",
                 lambda m: font_scheme_xml(name), out, count=1, flags=re.DOTALL)
    if "<a:clrScheme" not in out or "<a:fontScheme" not in out:
        sys.exit("error: base theme had no clrScheme/fontScheme to replace")
    return out


def main():
    ap = argparse.ArgumentParser(description="Generate This Waay OOXML theme from tokens.json")
    ap.add_argument("--tokens", default=str(DEFAULT_TOKENS))
    ap.add_argument("--full", action="store_true", help="emit a complete theme1.xml")
    ap.add_argument("--check", action="store_true", help="only assert token source version, then exit")
    ap.add_argument("--no-strict", action="store_true", help="warn instead of exit on version mismatch")
    args = ap.parse_args()

    tokens = load_tokens(args.tokens)
    ok = assert_version(tokens, strict=not args.no_strict)
    if args.check:
        print(f"token source: version={tokens['meta']['version']} updated={tokens['meta']['updated']} "
              f"-> {'OK' if ok else 'MISMATCH'}")
        sys.exit(0 if ok else 1)

    if args.full:
        print(full_theme_xml(tokens))
    else:
        print(clr_scheme_xml(tokens))
        print()
        print(font_scheme_xml())


if __name__ == "__main__":
    main()
