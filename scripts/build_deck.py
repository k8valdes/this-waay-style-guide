#!/usr/bin/env python3
"""
build_deck.py — assemble this-waay-deck.potx from tokens.json via the resolver (emit_pptx).

Authors the OOXML package directly (no python-pptx layout scaffolding) so the
template carries EXACTLY the six named layouts the deck spec calls for and no
stray Office defaults. The theme (clrScheme + fontScheme) comes from
emit_pptx (resolver-driven); every colour and font is read from the resolved set.

Output: assets/templates/this-waay-deck.potx  (a real .potx template part type)

Design rules enforced here (from slideDeck + accessibility in tokens.json):
  - 16:9 fixed canvas, 12192000 x 6858000 EMU
  - every placeholder inset >= 5% from all edges (safe area)
  - no text placeholder below 14pt
  - grounds are white or navy ONLY (never lt2/ice, never soft gradient)
  - slide number bottom-right; omitted on Title and Closing
  - headers = Deck Gray #595959 in Axiforma SemiBold; card titles / H2 = Axiforma ExtraBold
  - NEVER b="1" on Axiforma SemiBold / Medium / ExtraBold (they have no bold member);
    Axiforma (major/minor) DOES have a real Bold, so b="1" there is fine
  - no <p:transition>, no auto-advance timing
  - notes available via a real notes master (below the slide, never on it)

Standard library + emit_pptx/resolver (local). No font binaries are embedded — the
template references Axiforma by name only, so the package never redistributes a
font (Axiforma is fsType 4, Preview & Print only).
"""

import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emit_pptx  # noqa: E402 (Phase 3b: resolver-driven theme)

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT = REPO_ROOT / "assets" / "templates" / "this-waay-deck.potx"

# 16:9 canvas
CW, CH = 12192000, 6858000
# 5% safe-area insets
IX, IY = round(CW * 0.05), round(CH * 0.05)
INNER_W = CW - 2 * IX
INNER_H = CH - 2 * IY

A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

# Colors + theme now come from the resolver via emit_pptx (Phase 3b) — the
# same resolved set every other emitter reads, so the deck cannot disagree.
C = {k: emit_pptx.hexof_named(k) for k in
     ["navy", "navyDeep", "white", "green", "greenPunch", "greenInk",
      "teal", "tealInk", "steel", "slate", "inkMuted"]}
DECK_GRAY = emit_pptx.hexof_named("deckGray")

# ---- run / paragraph / textbody builders ---------------------------------
# Font-family guardrail: families with no bold member must never get b="1".
NO_BOLD_FAMILIES = {"Axiforma SemiBold", "Axiforma Medium", "Axiforma ExtraBold"}


def _rpr(face, sz, color, b=False, i=False, defRPr=False):
    if b and face in NO_BOLD_FAMILIES:
        raise ValueError(f"refusing to set b=1 on {face!r} (no bold member — would synthesize fake bold)")
    tag = "a:defRPr" if defRPr else "a:rPr"
    attrs = f'sz="{sz}"'
    if b:
        attrs += ' b="1"'
    if i:
        attrs += ' i="1"'
    return (f'<{tag} {attrs} dirty="0">'
            f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'<a:latin typeface="{face}"/></{tag}>')


def _run(text, face, sz, color, b=False, i=False):
    return f'<a:r>{_rpr(face, sz, color, b, i)}<a:t>{text}</a:t></a:r>'


def _para(runs, algn=None):
    ppr = f'<a:pPr algn="{algn}"/>' if algn else ""
    return f'<a:p>{ppr}{"".join(runs)}</a:p>'


def _fld_slidenum(face, sz, color, algn="r"):
    # a slide-number field; counts as a text placeholder run, so >=14pt too
    return (f'<a:p><a:pPr algn="{algn}"/>'
            f'<a:fld id="{{B7B4C6A2-1E4B-4C9A-9E2A-000000000001}}" type="slidenum">'
            f'{_rpr(face, sz, color)}<a:t>1</a:t></a:fld></a:p>')


def _txbody(paras, lst_face, lst_sz, lst_color, anchor="t", lst_b=False, lst_i=False, lst_algn=None):
    lst_algn_attr = f' algn="{lst_algn}"' if lst_algn else ""
    lst = (f'<a:lstStyle><a:lvl1pPr{lst_algn_attr}>'
           f'{_rpr(lst_face, lst_sz, lst_color, b=lst_b, i=lst_i, defRPr=True)}'
           f'</a:lvl1pPr></a:lstStyle>')
    return (f'<p:txBody><a:bodyPr anchor="{anchor}"/>{lst}{"".join(paras)}</p:txBody>')


def _sp(name, ph_type, idx, x, y, cx, cy, txbody):
    ph_idx = f' idx="{idx}"' if idx is not None else ""
    ph_type_attr = f' type="{ph_type}"' if ph_type else ""
    return (
        '<p:sp><p:nvSpPr>'
        f'<p:cNvPr id="{abs(hash(name)) % 90000 + 100}" name="{name}"/>'
        '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
        f'<p:nvPr><p:ph{ph_type_attr}{ph_idx}/></p:nvPr>'
        '</p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
        f'{txbody}</p:sp>'
    )


def _bg(color):
    return (f'<p:bg><p:bgPr><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            '<a:effectLst/></p:bgPr></p:bg>')


def _sptree(shapes):
    return ('<p:spTree>'
            '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
            '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
            '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
            f'{"".join(shapes)}</p:spTree>')


def layout_xml(name, ground, shapes, show_slidenum):
    """One slideLayout part. `ground` is a hex; must be white or navy only."""
    if ground not in (C["white"], C["navy"], C["navyDeep"]):
        sys.exit(f"error: layout {name!r} ground {ground} is not white/navy — deck grounds are white or navy only")
    sldnum = ""
    if show_slidenum:
        sn_color = C["white"] if ground in (C["navy"], C["navyDeep"]) else C["inkMuted"]
        sldnum = _sp("Slide Number Placeholder", "sldNum", 12,
                     CW - IX - 1200000, CH - IY - 400000, 1200000, 400000,
                     _txbody([_fld_slidenum("Axiforma", 1400, sn_color, algn="r")],
                             "Axiforma", 1400, sn_color, anchor="ctr", lst_algn="r"))
    all_shapes = shapes + ([sldnum] if sldnum else [])
    # NOTE: no <p:transition> element is emitted anywhere — no transitions, no auto-advance.
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
        f'<p:sldLayout xmlns:a="{A_NS}" xmlns:r="{R_NS}" xmlns:p="{P_NS}" '
        'type="cust" preserve="1">'
        f'<p:cSld name="{name}">{_bg(ground)}{_sptree(all_shapes)}</p:cSld>'
        '<p:clrMapOvr><a:overrideClrMapping '
        'bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" '
        'accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" '
        'hlink="hlink" folHlink="folHlink"/></p:clrMapOvr>'
        '</p:sldLayout>'
    )


# ---- the six layouts ------------------------------------------------------

def build_layouts():
    L = []

    # 1. Title / Cover — navy, green eyebrow, big display title (Axiforma Bold), presenter line
    title_shapes = [
        _sp("Eyebrow", "body", 10, IX, round(CH * 0.30), INNER_W, 500000,
            _txbody([_para([_run("EYEBROW", "Axiforma", 1400, C["green"], b=True)])],
                    "Axiforma", 1400, C["green"], lst_b=True)),
        _sp("Title", "ctrTitle", None, IX, round(CH * 0.38), INNER_W, 1800000,
            _txbody([_para([_run("Presentation title", "Axiforma", 4000, C["white"], b=True)])],
                    "Axiforma", 4000, C["white"], lst_b=True)),
        _sp("Presenter", "subTitle", 1, IX, round(CH * 0.66), INNER_W, 700000,
            _txbody([_para([_run("Presenter · Client · Date", "Axiforma", 1800, C["slate"])])],
                    "Axiforma", 1800, C["slate"])),
    ]
    L.append(("Title / Cover", C["navy"], title_shapes, False))

    # 2. Section Divider — navy, numeral eyebrow, one line, slide number
    sect_shapes = [
        _sp("Section Number", "body", 10, IX, round(CH * 0.30), INNER_W, 700000,
            _txbody([_para([_run("01", "Axiforma", 2000, C["green"], b=True)])],
                    "Axiforma", 2000, C["green"], lst_b=True)),
        _sp("Section Title", "title", None, IX, round(CH * 0.42), INNER_W, 1400000,
            _txbody([_para([_run("Section title", "Axiforma ExtraBold", 3200, C["white"])])],
                    "Axiforma ExtraBold", 3200, C["white"])),
    ]
    L.append(("Section Divider", C["navy"], sect_shapes, True))

    # 3. Content / Bullet — white, Deck Gray header (SemiBold), short bullets
    content_shapes = [
        _sp("Header", "title", None, IX, IY, INNER_W, 900000,
            _txbody([_para([_run("Slide header", "Axiforma SemiBold", 2600, DECK_GRAY)])],
                    "Axiforma SemiBold", 2600, DECK_GRAY)),
        _sp("Body", "body", 1, IX, IY + 1100000, INNER_W, INNER_H - 1100000,
            _txbody([
                _para([_run("First declarative point", "Axiforma", 1800, C["navy"])]),
                _para([_run("Second declarative point", "Axiforma", 1800, C["navy"])]),
                _para([_run("Third declarative point", "Axiforma", 1800, C["navy"])]),
            ], "Axiforma", 1800, C["navy"])),
    ]
    L.append(("Content / Bullet", C["white"], content_shapes, True))

    # 4. Quote — white, green-ink quote mark, italic quote, Teal-Ink attribution
    quote_shapes = [
        _sp("Quote Mark", "body", 10, IX, IY, 1200000, 1200000,
            _txbody([_para([_run("&#8220;", "Axiforma ExtraBold", 6000, C["greenInk"])])],
                    "Axiforma ExtraBold", 6000, C["greenInk"])),
        _sp("Quote", "body", 1, IX, IY + 1200000, INNER_W, 2400000,
            _txbody([_para([_run("The quotation goes here, set large and readable.",
                                 "Axiforma", 2800, C["navy"], i=True)])],
                    "Axiforma", 2800, C["navy"], lst_i=True)),
        _sp("Attribution", "body", 11, IX, IY + 3800000, INNER_W, 700000,
            _txbody([_para([_run("Name, Role, Organization", "Axiforma SemiBold", 1600, C["tealInk"])])],
                    "Axiforma SemiBold", 1600, C["tealInk"])),
    ]
    L.append(("Quote", C["white"], quote_shapes, True))

    # 5. Chart / Data — white, header, chart placeholder
    chart_shapes = [
        _sp("Header", "title", None, IX, IY, INNER_W, 900000,
            _txbody([_para([_run("Chart title", "Axiforma SemiBold", 2600, DECK_GRAY)])],
                    "Axiforma SemiBold", 2600, DECK_GRAY)),
        _sp("Chart Placeholder", "body", 1, IX, IY + 1100000, INNER_W, INNER_H - 1100000,
            _txbody([_para([_run("Chart / data placeholder — native chart inherits accent1-4 series order",
                                 "Axiforma", 1400, C["inkMuted"])])],
                    "Axiforma", 1400, C["inkMuted"], anchor="ctr", lst_algn="ctr")),
    ]
    L.append(("Chart / Data", C["white"], chart_shapes, True))

    # 6. Closing — navy, centered, one contact line, NO slide number
    closing_shapes = [
        _sp("Closing", "ctrTitle", None, IX, round(CH * 0.40), INNER_W, 1200000,
            _txbody([_para([_run("Thank you", "Axiforma", 3600, C["white"], b=True)], algn="ctr")],
                    "Axiforma", 3600, C["white"], lst_b=True, anchor="ctr", lst_algn="ctr")),
        _sp("Contact", "subTitle", 1, IX, round(CH * 0.58), INNER_W, 700000,
            _txbody([_para([_run("hello@thiswaay.com", "Axiforma", 1800, C["green"])], algn="ctr")],
                    "Axiforma", 1800, C["green"], anchor="ctr", lst_algn="ctr")),
    ]
    L.append(("Closing", C["navy"], closing_shapes, False))

    return [layout_xml(n, g, s, sn) for (n, g, s, sn) in L]


# ---- master, notes master, presentation, package scaffolding --------------

def slide_master_xml():
    # master ground = white; placeholder geometry defaults live here too.
    master_shapes = [
        _sp("Title Placeholder", "title", None, IX, IY, INNER_W, 900000,
            _txbody([_para([])], "Axiforma SemiBold", 2600, DECK_GRAY)),
        _sp("Body Placeholder", "body", 1, IX, IY + 1100000, INNER_W, INNER_H - 1100000,
            _txbody([_para([])], "Axiforma", 1800, C["navy"])),
    ]
    txstyles = (
        '<p:txStyles>'
        f'<p:titleStyle><a:lvl1pPr><a:defRPr sz="2600"><a:solidFill><a:srgbClr val="{DECK_GRAY}"/></a:solidFill><a:latin typeface="Axiforma SemiBold"/></a:defRPr></a:lvl1pPr></p:titleStyle>'
        f'<p:bodyStyle><a:lvl1pPr><a:defRPr sz="1800"><a:solidFill><a:srgbClr val="{C["navy"]}"/></a:solidFill><a:latin typeface="Axiforma"/></a:defRPr></a:lvl1pPr></p:bodyStyle>'
        f'<p:otherStyle><a:lvl1pPr><a:defRPr sz="1400"><a:solidFill><a:srgbClr val="{C["inkMuted"]}"/></a:solidFill><a:latin typeface="Axiforma"/></a:defRPr></a:lvl1pPr></p:otherStyle>'
        '</p:txStyles>'
    )
    layout_ids = "".join(
        f'<p:sldLayoutId id="{2147483649 + i}" r:id="rId{i + 2}"/>' for i in range(6)
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
        f'<p:sldMaster xmlns:a="{A_NS}" xmlns:r="{R_NS}" xmlns:p="{P_NS}">'
        f'<p:cSld>{_bg(C["white"])}{_sptree(master_shapes)}</p:cSld>'
        '<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" '
        'accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" '
        'hlink="hlink" folHlink="folHlink"/>'
        f'<p:sldLayoutIdLst>{layout_ids}</p:sldLayoutIdLst>'
        f'{txstyles}</p:sldMaster>'
    )


def notes_master_xml():
    notes_ph = _sp("Notes Placeholder", "body", 1, IX, round(CH * 0.5), INNER_W, round(CH * 0.45),
                   _txbody([_para([])], "Axiforma", 1400, C["navy"]))
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
        f'<p:notesMaster xmlns:a="{A_NS}" xmlns:r="{R_NS}" xmlns:p="{P_NS}">'
        f'<p:cSld>{_bg(C["white"])}{_sptree([notes_ph])}</p:cSld>'
        '<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" '
        'accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" '
        'hlink="hlink" folHlink="folHlink"/></p:notesMaster>'
    )


def presentation_xml():
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
        f'<p:presentation xmlns:a="{A_NS}" xmlns:r="{R_NS}" xmlns:p="{P_NS}" saveSubsetFonts="1">'
        '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
        '<p:notesMasterIdLst><p:notesMasterId r:id="rId2"/></p:notesMasterIdLst>'
        f'<p:sldSz cx="{CW}" cy="{CH}" type="screen16x9"/>'
        f'<p:notesSz cx="{CH}" cy="{CW}"/>'
        '</p:presentation>'
    )


CONTENT_TYPES = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    # .potx => the presentation part is the TEMPLATE main type
    '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.template.main+xml"/>'
    '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>'
    + "".join(
        f'<Override PartName="/ppt/slideLayouts/slideLayout{i}.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>'
        for i in range(1, 7))
    + '<Override PartName="/ppt/notesMasters/notesMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesMaster+xml"/>'
    '<Override PartName="/ppt/presProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/>'
    '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
    '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
    '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
    '</Types>'
)

ROOT_RELS = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
    '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
    '</Relationships>'
)


def presentation_rels():
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster" Target="notesMasters/notesMaster1.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/presProps" Target="presProps.xml"/>'
        '<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>'
        '</Relationships>'
    )


def master_rels():
    rels = ['<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>']
    for i in range(6):
        rels.append(
            f'<Relationship Id="rId{i + 2}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" '
            f'Target="../slideLayouts/slideLayout{i + 1}.xml"/>')
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + "".join(rels) + '</Relationships>')


def layout_rels():
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>'
        '</Relationships>'
    )


def notesmaster_rels():
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>'
        '</Relationships>'
    )


PRESPROPS = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
             f'<p:presentationPr xmlns:a="{A_NS}" xmlns:r="{R_NS}" xmlns:p="{P_NS}"/>')

CORE = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
    '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
    'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
    '<dc:title>This Waay — Deck Template</dc:title>'
    '<dc:creator>This Waay</dc:creator>'
    '<cp:revision>1</cp:revision></cp:coreProperties>'
)

APP = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
    '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
    'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
    '<Application>This Waay build_deck.py</Application>'
    '<PresentationFormat>Widescreen</PresentationFormat></Properties>'
)


def build():
    layouts = build_layouts()
    theme1 = emit_pptx.full_theme_xml()

    parts = {
        "[Content_Types].xml": CONTENT_TYPES,
        "_rels/.rels": ROOT_RELS,
        "docProps/core.xml": CORE,
        "docProps/app.xml": APP,
        "ppt/presentation.xml": presentation_xml(),
        "ppt/_rels/presentation.xml.rels": presentation_rels(),
        "ppt/presProps.xml": PRESPROPS,
        "ppt/theme/theme1.xml": theme1,
        "ppt/slideMasters/slideMaster1.xml": slide_master_xml(),
        "ppt/slideMasters/_rels/slideMaster1.xml.rels": master_rels(),
        "ppt/notesMasters/notesMaster1.xml": notes_master_xml(),
        "ppt/notesMasters/_rels/notesMaster1.xml.rels": notesmaster_rels(),
    }
    for i, xml in enumerate(layouts, start=1):
        parts[f"ppt/slideLayouts/slideLayout{i}.xml"] = xml
        parts[f"ppt/slideLayouts/_rels/slideLayout{i}.xml.rels"] = layout_rels()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in parts.items():
            z.writestr(name, data)
    print(f"wrote {OUT}  ({len(parts)} parts, {OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    # SUPERSEDED by build_deck_atomic.py (Phase 2R): the atomic builder produces the
    # full named-layout set. This 6-generic-layout builder is kept for reference only;
    # it will not overwrite the shipped .potx unless run with --force.
    import sys as _sys
    if "--force" not in _sys.argv:
        print("build_deck.py is superseded by build_deck_atomic.py (Phase 2R). Re-run with --force to use the old 6-generic-layout builder.")
        _sys.exit(0)
    build()
