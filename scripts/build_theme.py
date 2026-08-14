#!/usr/bin/env python3
"""
build_theme.py — DEPRECATED compatibility shim (Phase 3b).

Phase 2's flat-file theme generator has been superseded by the resolver pipeline.
The theme (clrScheme + fontScheme) is now emitted by scripts/emit_pptx.py from the
resolved token set, so every emitter shares one source and cannot disagree.

This module re-points at that emitter: its theme functions delegate to emit_pptx.
New code should import emit_pptx (or emit_docx for the Word theme) directly.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emit_pptx  # noqa: E402

# re-pointed at the resolver-driven emitter
clr_scheme_xml = emit_pptx.clr_scheme_xml
font_scheme_xml = emit_pptx.font_scheme_xml
full_theme_xml = emit_pptx.full_theme_xml
splice_into_theme = emit_pptx.splice_into_theme
FMT_SCHEME = emit_pptx.FMT_SCHEME

if __name__ == "__main__":
    print(full_theme_xml())
