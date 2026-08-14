#!/usr/bin/env python3
"""
build_reference_docx.py — assemble this-waay-reference.docx from the existing
branded letterhead + tokens.json via the resolver (emit_docx).

Transforms the letterhead (keeping its header/footer structure and logo
relationship) rather than authoring a new document:
  - redefines the existing named styles (Title, Subtitle, Heading1-6, Normal,
    Hyperlink) against tokens.json — teal is the DOCUMENT accent
  - writes a real brand clrScheme/fontScheme into word/theme/theme1.xml
    (was Office 2007 defaults: Calibri/Cambria, accent1 #4F81BD)
  - strips the placeholder specimen body ("Accent color 1", "Background
    color", "H1/H2/H3 - The Fox chases the blue Jay")
  - removes #374151 (Tailwind grey) -> inkMuted and #1155CC (Google Docs link
    blue) -> tealInk
  - strips ALL embedded font binaries (Poppins/Nunito/Open Sans) and the
    embed flags: the reference references Axiforma by name only, never carries
    a font binary (Axiforma is fsType 4)

Input:  the letterhead .docx (default Examples/…; override with --letterhead).
Output: assets/templates/this-waay-reference.docx

Standard library + build_theme (local). No font binaries are written into the
output package.

Style map (family, colour):
  Title      Axiforma ExtraBold  navy      Heading3   Axiforma SemiBold  tealInk
  Subtitle   Axiforma SemiBold   tealInk   Heading4-6 Axiforma Medium    inkMuted
  Heading1   Axiforma ExtraBold  navy      Normal     Axiforma           navy
  Heading2   Axiforma ExtraBold  navy      Hyperlink  Axiforma           tealInk
"""

import argparse
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emit_docx  # noqa: E402  (Phase 3b: resolver-driven theme + style colors)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LETTERHEAD = REPO_ROOT / "Examples" / "Branded Letterhead - (Make a Copy).docx"
OUT = REPO_ROOT / "assets" / "templates" / "this-waay-reference.docx"

# Named-style colours come from the resolver via emit_docx — teal is the
# document accent. Same resolved source the other emitters read.
NAVY, TEALINK, INKMUTED = (emit_docx.style_hex("navy"), emit_docx.style_hex("tealInk"),
                           emit_docx.style_hex("inkMuted"))

# styleId -> (font family, colour hex). Families with no bold member never get <w:b>.
STYLE_MAP = {
    "Title":    ("Axiforma ExtraBold", NAVY),
    "Subtitle": ("Axiforma SemiBold",  TEALINK),
    "Heading1": ("Axiforma ExtraBold", NAVY),
    "Heading2": ("Axiforma ExtraBold", NAVY),
    "Heading3": ("Axiforma SemiBold",  TEALINK),
    "Heading4": ("Axiforma Medium",    INKMUTED),
    "Heading5": ("Axiforma Medium",    INKMUTED),
    "Heading6": ("Axiforma Medium",    INKMUTED),
    "Normal":   ("Axiforma",           NAVY),
}

SPECIMEN_PHRASES = ["Accent color", "Background color", "Fox chases", "blue Jay",
                    "Accent colour", "Background colour", "TitleSUBTITLE"]

OFF_BRAND_FONTS = ["Poppins ExtraLight", "Poppins SemiBold", "Poppins Light",
                   "Poppins", "Nunito", "Open Sans", "OpenSans"]


def _rpr(family, color_hex, sz=None, szcs=None):
    """A brand run-properties block. Ordered per WordprocessingML schema
    (rFonts, color, sz, szCs). No <w:b> — the weight lives in the family name;
    Axiforma Medium/SemiBold/ExtraBold have no bold member, so bolding them
    would synthesize a fake bold."""
    parts = [f'<w:rFonts w:ascii="{family}" w:cs="{family}" '
             f'w:eastAsia="{family}" w:hAnsi="{family}"/>']
    parts.append(f'<w:color w:val="{color_hex}"/>')
    if sz:
        parts.append(f'<w:sz w:val="{sz}"/>')
    if szcs:
        parts.append(f'<w:szCs w:val="{szcs}"/>')
    return "<w:rPr>" + "".join(parts) + "</w:rPr>"


def _existing_sizes(block):
    sz = re.search(r'<w:sz w:val="([^"]+)"/>', block)
    szcs = re.search(r'<w:szCs w:val="([^"]+)"/>', block)
    return (sz.group(1) if sz else None, szcs.group(1) if szcs else None)


def redefine_styles(styles_xml):
    out = styles_xml
    for sid, (family, color) in STYLE_MAP.items():
        m = re.search(r'(<w:style [^>]*w:styleId="' + sid + r'"[^>]*>)(.*?)(</w:style>)',
                      out, re.DOTALL)
        if not m:
            print(f"warning: style {sid} not found in letterhead; skipping", file=sys.stderr)
            continue
        head, body, tail = m.group(1), m.group(2), m.group(3)
        sz, szcs = _existing_sizes(body)
        new_rpr = _rpr(family, color, sz, szcs)
        if "<w:rPr>" in body:
            body = re.sub(r'<w:rPr>.*?</w:rPr>', new_rpr, body, count=1, flags=re.DOTALL)
        else:
            # inject rPr right after the <w:name .../> element
            body = re.sub(r'(<w:name [^>]*/>)', r'\1' + new_rpr, body, count=1)
        out = out[:m.start()] + head + body + tail + out[m.end():]

    # ensure a Hyperlink character style exists, tealInk + Axiforma
    if 'w:styleId="Hyperlink"' not in out:
        hyper = ('<w:style w:type="character" w:styleId="Hyperlink"><w:name w:val="Hyperlink"/>'
                 f'<w:rPr><w:rFonts w:ascii="Axiforma" w:cs="Axiforma" w:eastAsia="Axiforma" '
                 f'w:hAnsi="Axiforma"/><w:color w:val="{TEALINK}"/><w:u w:val="single"/></w:rPr></w:style>')
        out = out.replace("</w:styles>", hyper + "</w:styles>")
    else:
        out = re.sub(r'(<w:style [^>]*w:styleId="Hyperlink"[^>]*>.*?<w:rPr>).*?(</w:rPr>)',
                     r'\1' + f'<w:rFonts w:ascii="Axiforma" w:cs="Axiforma" w:eastAsia="Axiforma" '
                     f'w:hAnsi="Axiforma"/><w:color w:val="{TEALINK}"/><w:u w:val="single"/>' + r'\2',
                     out, count=1, flags=re.DOTALL)

    # any lingering off-brand grey / hexes anywhere in styles
    out = out.replace("374151", INKMUTED).replace("1155CC", TEALINK).replace("1155cc", TEALINK)
    for f in OFF_BRAND_FONTS:
        out = out.replace(f'w:ascii="{f}"', 'w:ascii="Axiforma"') \
                 .replace(f'w:hAnsi="{f}"', 'w:hAnsi="Axiforma"') \
                 .replace(f'w:cs="{f}"', 'w:cs="Axiforma"') \
                 .replace(f'w:eastAsia="{f}"', 'w:eastAsia="Axiforma"')
    return out


def strip_specimens(doc_xml):
    """Remove whole <w:p> paragraphs whose text carries a specimen phrase.
    Operates only on complete <w:p ...>...</w:p> blocks (paragraphs do not
    nest in WordML), leaving the surrounding <w:document>/<w:body> structure —
    and the trailing <w:sectPr> paragraph — untouched."""
    def repl(m):
        block = m.group(0)
        text = "".join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', block))
        if any(p.lower() in text.lower() for p in SPECIMEN_PHRASES):
            return ""
        return block
    return re.sub(r'<w:p\b[^>]*>.*?</w:p>', repl, doc_xml, flags=re.DOTALL)


def recolor_and_refont(xml):
    xml = xml.replace("374151", INKMUTED).replace("1155CC", TEALINK).replace("1155cc", TEALINK)
    for f in OFF_BRAND_FONTS:
        xml = xml.replace(f'w:ascii="{f}"', 'w:ascii="Axiforma"') \
                 .replace(f'w:hAnsi="{f}"', 'w:hAnsi="Axiforma"') \
                 .replace(f'w:cs="{f}"', 'w:cs="Axiforma"') \
                 .replace(f'w:eastAsia="{f}"', 'w:eastAsia="Axiforma"')
    return xml


def clean_settings(settings_xml):
    for flag in ("embedTrueTypeFonts", "embedSystemFonts", "saveSubsetFonts"):
        settings_xml = re.sub(r'<w:' + flag + r'[^>]*/>', "", settings_xml)
    return settings_xml


def fresh_font_table():
    fams = ["Axiforma", "Axiforma Medium", "Axiforma SemiBold", "Axiforma ExtraBold", "Poppins"]
    fonts = "".join(
        f'<w:font w:name="{f}"><w:charset w:val="00"/><w:family w:val="swiss"/>'
        '<w:pitch w:val="variable"/></w:font>' for f in fams)
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
            '<w:fonts xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            + fonts + '</w:fonts>')


def clean_content_types(ct):
    # drop the Default entries for embedded-font extensions (ttf, odttf)
    ct = re.sub(r'<Default Extension="ttf"[^>]*/>', "", ct)
    ct = re.sub(r'<Default Extension="odttf"[^>]*/>', "", ct)
    return ct


def build(letterhead):
    if not Path(letterhead).exists():
        sys.exit(f"error: letterhead not found at {letterhead}. Pass --letterhead <path>.")
    zin = zipfile.ZipFile(letterhead)
    items = {n: zin.read(n) for n in zin.namelist()}

    # 1. styles
    items["word/styles.xml"] = redefine_styles(items["word/styles.xml"].decode()).encode()

    # 2. theme — brand clrScheme + fontScheme spliced in (resolver-driven)
    items["word/theme/theme1.xml"] = emit_docx.splice_into_theme(
        items["word/theme/theme1.xml"].decode()).encode()

    # 3. document + headers + footers — strip specimens, recolor, refont
    doc = strip_specimens(items["word/document.xml"].decode())
    items["word/document.xml"] = recolor_and_refont(doc).encode()
    for part in list(items):
        if re.match(r'word/(header|footer)\d+\.xml$', part):
            items[part] = recolor_and_refont(items[part].decode()).encode()

    # 4. settings — drop embed flags
    if "word/settings.xml" in items:
        items["word/settings.xml"] = clean_settings(items["word/settings.xml"].decode()).encode()

    # 5. fontTable — replace with a clean Axiforma/Poppins declaration (no embeds)
    items["word/fontTable.xml"] = fresh_font_table().encode()

    # 6. content types — drop font-extension defaults
    items["[Content_Types].xml"] = clean_content_types(items["[Content_Types].xml"].decode()).encode()

    # 7. drop the embedded font binaries and their rels part
    dropped = []
    for part in list(items):
        if part.startswith("word/fonts/") or part == "word/_rels/fontTable.xml.rels":
            del items[part]
            dropped.append(part)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in items.items():
            z.writestr(name, data)
    print(f"wrote {OUT}  ({len(items)} parts, {OUT.stat().st_size} bytes)")
    print(f"  stripped {len(dropped)} embedded-font parts")


def main():
    ap = argparse.ArgumentParser(description="Build this-waay-reference.docx from the letterhead")
    ap.add_argument("--letterhead", default=str(DEFAULT_LETTERHEAD))
    args = ap.parse_args()
    build(args.letterhead)


if __name__ == "__main__":
    main()
