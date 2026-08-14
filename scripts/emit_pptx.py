#!/usr/bin/env python3
"""
emit_pptx.py — PPTX theme XML (clrScheme + fontScheme) from the resolved token
set. A pure function of the resolver's production-only output; replaces Phase 2's
inline build_theme logic. build_deck.py imports this.

Preserves the Phase 2 mapping exactly: accent1-4 = dataViz.seriesOrder in order
(brand chart series inherit with zero config), accent6 = punch green (where a
default series never reaches it), major/minor font = Axiforma.

    python3 scripts/emit_pptx.py            # print the full theme1.xml
"""
import sys
from collections import OrderedDict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from resolve_tokens import Resolver  # noqa: E402

A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"

# theme slot -> resolved color token PATH (v4.0 measured-re-seat names).
# accent1..4 are dataViz.seriesOrder in order: green.400, steel.600, teal.400, navy.900.
SLOT_MAP = OrderedDict([
    ("dk1",      "color.navy.900"),
    ("lt1",      "color.white"),
    ("dk2",      "color.navy.950"),
    ("lt2",      "color._gradientStops.ice"),   # completeness only; no layout uses it as a ground
    ("accent1",  "color.green.400"),            # seriesOrder[0]
    ("accent2",  "color.steel.600"),            # seriesOrder[1]
    ("accent3",  "color.teal.400"),             # seriesOrder[2]
    ("accent4",  "color.navy.900"),             # seriesOrder[3]
    ("accent5",  "color.slate.400"),            # gridlines
    ("accent6",  "color.green.300"),            # punch — last, default charts never reach it
    ("hlink",    "color.teal.600"),
    ("folHlink", "color.slate.600"),
])

# named colors build_deck.py needs, by v4.0 path
NAMED = OrderedDict([
    ("navy", "color.navy.900"), ("navyDeep", "color.navy.950"), ("white", "color.white"),
    ("green", "color.green.400"), ("greenPunch", "color.green.300"), ("greenInk", "color.green.600"),
    ("teal", "color.teal.400"), ("tealInk", "color.teal.600"), ("steel", "color.steel.600"),
    ("slate", "color.slate.400"), ("inkMuted", "color.slate.600"), ("deckGray", "color.gray.700"),
])

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

_R = None
def _resolver():
    global _R
    if _R is None:
        _R = Resolver()
    return _R


def _hex6(path):
    r = _R or _resolver()
    entry = r.resolve("production").get(path) or r.resolve("all").get(path)
    if not entry or entry["type"] != "color":
        sys.exit(f"emit_pptx: {path} is not a resolvable color")
    return entry["value"]["hex"].lstrip("#").upper()


def hexof_named(name):
    return _hex6(NAMED[name])


def clr_scheme_xml(name="This Waay"):
    parts = [f'<a:clrScheme name="{name}">']
    for slot, path in SLOT_MAP.items():
        parts.append(f'<a:{slot}><a:srgbClr val="{_hex6(path)}"/></a:{slot}>')
    parts.append("</a:clrScheme>")
    return "".join(parts)


def font_scheme_xml(name="This Waay"):
    return (
        f'<a:fontScheme name="{name}">'
        '<a:majorFont><a:latin typeface="Axiforma"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>'
        '<a:minorFont><a:latin typeface="Axiforma"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont>'
        '</a:fontScheme>'
    )


def full_theme_xml(name="This Waay"):
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
        f'<a:theme xmlns:a="{A_NS}" name="{name}"><a:themeElements>'
        + clr_scheme_xml(name) + font_scheme_xml(name) + FMT_SCHEME
        + '</a:themeElements><a:objectDefaults/><a:extraClrSchemeLst/></a:theme>'
    )


def splice_into_theme(base_theme_xml, name="This Waay"):
    import re
    out = re.sub(r"<a:clrScheme\b.*?</a:clrScheme>", lambda m: clr_scheme_xml(name),
                 base_theme_xml, count=1, flags=re.DOTALL)
    out = re.sub(r"<a:fontScheme\b.*?</a:fontScheme>", lambda m: font_scheme_xml(name),
                 out, count=1, flags=re.DOTALL)
    if "<a:clrScheme" not in out or "<a:fontScheme" not in out:
        sys.exit("emit_pptx: base theme had no clrScheme/fontScheme to replace")
    return out


if __name__ == "__main__":
    print(full_theme_xml())
