#!/usr/bin/env python3
"""
emit_docx.py — DOCX theme + named-style colors from the resolved token set.

The DrawingML theme (clrScheme + fontScheme) is the SAME OOXML theme the PPTX
uses, so the theme functions are shared from emit_pptx (one resolved source,
one theme). What's Word-specific — and where 'teal is the document accent' lives
— is the named-style colour map below, which build_reference_docx.py consumes.

    python3 scripts/emit_docx.py   # print the theme1.xml
"""
import sys
from collections import OrderedDict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emit_pptx  # noqa: E402  (shared DrawingML theme, resolver-driven)

# Word named-style colours (teal is the DOCUMENT accent). Resolver token paths.
STYLE_PATHS = OrderedDict([
    ("navy",     "color.navy.900"),
    ("tealInk",  "color.teal.600"),
    ("inkMuted", "color.slate.600"),
])


def _hex(path):
    r = emit_pptx._resolver()
    entry = r.resolve("all").get(path)
    return entry["value"]["hex"].lstrip("#").upper()


def style_hex(name):
    return _hex(STYLE_PATHS[name])


# theme functions are the shared DrawingML theme (identical to the deck's)
splice_into_theme = emit_pptx.splice_into_theme
full_theme_xml = emit_pptx.full_theme_xml


if __name__ == "__main__":
    print(full_theme_xml())
