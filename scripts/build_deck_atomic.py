#!/usr/bin/env python3
"""
build_deck_atomic.py — Phase 2R. Rebuilds this-waay-deck.potx as COMPOSED NAMED
LAYOUTS from token-bound atoms, over the intact Phase 3b theme.

atoms -> molecules -> layouts  mirrors  primitive -> semantic -> component.
Every atom's colour resolves from a slide.* token (or theme) via the resolver —
no literal. The agenda-block molecule is defined ONCE and reused by the Agenda
and Stakeholders&agenda layouts (proving it is shared, not copied).

This pass builds the proof set + the most-reused layouts:
  Cover · Agenda · Stakeholders & agenda · Project goals · Timeline ·
  Section divider · Closing
The remaining content layouts are catalogued + token-bound in
references/slide-components.md and rebuilt in a follow-up.

Standard library + resolver/emit_pptx (local). Theme unchanged (emit_pptx).
Logo embedded as the real rasterised asset (assets/logo/), correct variant per
ground. No font binaries embedded.
"""
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import emit_pptx  # noqa: E402  (theme + named theme colours, resolver-driven)
from resolve_tokens import Resolver  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "assets" / "templates" / "this-waay-deck.potx"
LOGO_COLOR = REPO / "product-design-studio" / "assets" / "logo" / "logo-color.png"
LOGO_WHITE = REPO / "product-design-studio" / "assets" / "logo" / "logo-white.png"

A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
CW, CH = 12192000, 6858000
IX, IY = round(CW * 0.05), round(CH * 0.05)

# ---- resolved values: slide.* tokens + theme colours (NO literals below) ----
_r = Resolver()
_prod = _r.resolve("production")
S = {p.split(".", 1)[1]: e for p, e in _prod.items() if p.startswith("slide.")}


def col(name):
    """hex (no #) of a slide.* colour token — the atomic binding."""
    return S[name]["value"]["hex"].lstrip("#").upper()


def alpha(name):
    a = S[name]["value"].get("alpha")
    return a


C = {k: emit_pptx.hexof_named(k) for k in ("navy", "white", "teal", "green")} \
    if False else {k: emit_pptx.hexof_named(k) for k in ("navy", "navyDeep", "white", "green", "teal")}
GRAD = _prod["gradient.soft"]["value"]  # {stops:[{color,position}], angle}

_uid = [100]
def _id():
    _uid[0] += 1
    return _uid[0]


# ---- low-level OOXML ----
MIN_SZ = 1400  # deck projected-legibility floor (>=14pt) — enforced structurally by every atom
def _rpr(face, sz, hexv, b=False, i=False, defR=False, a=None, algn=None):
    sz = max(int(sz), MIN_SZ)
    tag = "a:defRPr" if defR else "a:rPr"
    at = f'sz="{sz}"' + (' b="1"' if b else '') + (' i="1"' if i else '')
    fill = (f'<a:solidFill><a:srgbClr val="{hexv}">'
            + (f'<a:alpha val="{int(a*100000)}"/>' if a else '') + '</a:srgbClr></a:solidFill>')
    return f'<{tag} {at} dirty="0">{fill}<a:latin typeface="{face}"/></{tag}>'


def _run(t, face, sz, hexv, b=False, i=False, a=None):
    return f'<a:r>{_rpr(face, sz, hexv, b, i, a=a)}<a:t>{t}</a:t></a:r>'


def _para(runs, algn=None, spc=None):
    ppr = ''
    if algn or spc:
        ppr = '<a:pPr' + (f' algn="{algn}"' if algn else '') + '>' \
              + (f'<a:spcBef><a:spcPts val="{spc}"/></a:spcBef>' if spc else '') + '</a:pPr>'
    return f'<a:p>{ppr}{"".join(runs)}</a:p>'


def _tb(name, x, y, cx, cy, paras, anchor="t"):
    """free textbox (structural, not a slot)."""
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{_id()}" name="{name}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" anchor="{anchor}"><a:normAutofit/></a:bodyPr>{"".join(paras)}</p:txBody></p:sp>')


def _ph(name, ph_type, idx, x, y, cx, cy, paras, lst_defR, anchor="t"):
    """a real slot placeholder a generator fills."""
    ph = f' type="{ph_type}"' if ph_type else ''
    ph += f' idx="{idx}"' if idx is not None else ''
    lst = f'<a:lstStyle><a:lvl1pPr>{lst_defR}</a:lvl1pPr></a:lstStyle>'
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{_id()}" name="{name}"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
            f'<p:nvPr><p:ph{ph}/></p:nvPr></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
            f'<p:txBody><a:bodyPr anchor="{anchor}"/>{lst}{"".join(paras)}</p:txBody></p:sp>')


def _rect(name, x, y, cx, cy, hexv, rad=None, a=None, line=None):
    geom = f'<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val {rad}"/></a:avLst></a:prstGeom>' \
        if rad is not None else '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
    fill = f'<a:solidFill><a:srgbClr val="{hexv}">' + (f'<a:alpha val="{int(a*100000)}"/>' if a else '') + '</a:srgbClr></a:solidFill>'
    ln = f'<a:ln w="9525"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>' if line else '<a:ln><a:noFill/></a:ln>'
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{_id()}" name="{name}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>{geom}{fill}{ln}</p:spPr>'
            '<p:txBody><a:bodyPr/><a:p></a:p></p:txBody></p:sp>')


def _ellipse(name, x, y, d, hexv, inner_paras):
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{_id()}" name="{name}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{d}" cy="{d}"/></a:xfrm>'
            f'<a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="{hexv}"/></a:solidFill></p:spPr>'
            f'<p:txBody><a:bodyPr anchor="ctr"/>{"".join(inner_paras)}</p:txBody></p:sp>')


def _pic(name, rid, x, y, cx, cy):
    return (f'<p:pic><p:nvPicPr><p:cNvPr id="{_id()}" name="{name}"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr>'
            f'<p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')


def _grad_soft():
    stops = ''.join(f'<a:gs pos="{int(s["position"]*100000)}"><a:srgbClr val="{s["color"]["hex"].lstrip("#").upper()}"/></a:gs>'
                    for s in GRAD["stops"])
    return f'<a:gradFill><a:gsLst>{stops}</a:gsLst><a:lin ang="{int(GRAD["angle"]*60000)}" scaled="1"/></a:gradFill>'


EB = "Axiforma"           # eyebrow / body base
XB = "Axiforma ExtraBold" # headings
SB = "Axiforma SemiBold"

# ================= ATOMS =================
def a_eyebrow(x, y, w, text):
    return _tb("Eyebrow", x, y, w, 260000,
               [_para([_run(text.upper(), EB, 1200, col("eyebrow"), b=True)])])

def a_subhead(x, y, w, text):
    return _tb("Subhead", x, y, w, 300000, [_para([_run(text, SB, 1400, col("subhead"))])])

def a_h1(x, y, w, text, dark=False):
    hexv = col("headerTitleOnDark") if dark else col("headerTitle")
    return _tb("Title", x, y, w, 900000, [_para([_run(text, XB, 3200, hexv)])])

def a_pill(x, y, text, kind="subCategory"):
    fill = col({"opportunity": "pillOpportunity", "category": "pillCategory"}.get(kind, "pillSubCategory"))
    w = 300000 + len(text) * 78000
    return (_rect(f"Pill-{kind}", x, y, w, 300000, fill, rad=50000)
            + _tb(f"PillLabel", x, y, w, 300000, [_para([_run(text, EB, 1000, col("pillLabel"), b=True)], algn="ctr")], anchor="ctr"))

def a_timed_row(x, y, w, time, body):
    return (_tb("TimedTime", x, y, 900000, 300000, [_para([_run(time, XB, 1400, col("timedRowTime"))])])
            + _tb("TimedBody", x + 950000, y, w - 950000, 300000, [_para([_run(body, EB, 1300, col("timedRowBody"))])]))

def a_numbered_item(x, y, w, n, title, sub):
    d = 420000
    return (_ellipse(f"Numeral-{n}", x, y, d, col("numeralFill"),
                     [_para([_run(str(n), XB, 1600, col("numeralText"))], algn="ctr")])
            + _tb(f"NumTitle-{n}", x + d + 180000, y, w - d - 180000, 320000,
                  [_para([_run(title, XB, 1500, col("body"))])])
            + _tb(f"NumSub-{n}", x + d + 180000, y + 340000, w - d - 180000, 500000,
                  [_para([_run(sub, EB, 1200, col("body"), a=0.7)])]))

def a_divider_word(x, y, w, text):
    return _tb("DividerWord", x, y, w, 1500000, [_para([_run(text, XB, 8000, col("dividerWord"))])])


# ================= MOLECULES =================
def m_slide_header(eyebrow, subhead, title):
    """eyebrow + subhead + navy H1 (content layouts)."""
    return (a_eyebrow(IX, IY, 6000000, eyebrow)
            + a_subhead(IX, IY + 360000, 7000000, subhead)
            + a_h1(IX, IY + 720000, 8000000, title))


def m_agenda_block(x, y, w, rows):
    """THE SHARED agenda-block: soft-gradient card + ordered timed-rows.
    Defined ONCE; called by the Agenda and Stakeholders&agenda layouts."""
    h = 380000 + len(rows) * 470000
    card = (f'<p:sp><p:nvSpPr><p:cNvPr id="{_id()}" name="AgendaBlock"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>'
            f'<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 6000"/></a:avLst></a:prstGeom>'
            f'{_grad_soft()}<a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr/><a:p></a:p></p:txBody></p:sp>')
    rowxml = "".join(a_timed_row(x + 300000, y + 300000 + i * 470000, w - 600000, t, b)
                     for i, (t, b) in enumerate(rows))
    return card + rowxml


def m_numbered_list(x, y, w, items):
    return "".join(a_numbered_item(x, y + i * 980000, w, i + 1, t, s) for i, (t, s) in enumerate(items))


def m_areas_card(x, y, w, title, rows):
    h = 520000 + len(rows) * 430000
    card = _rect("AreasCard", x, y, w, h, col("cardGround"), rad=6000)  # navy? actually soft in template
    # template areas-of-focus card is soft-ground; use gradient for fidelity
    card = (f'<p:sp><p:nvSpPr><p:cNvPr id="{_id()}" name="AreasCard"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>'
            f'<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 6000"/></a:avLst></a:prstGeom>'
            f'{_grad_soft()}<a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr/><a:p></a:p></p:txBody></p:sp>')
    header = _tb("AreasTitle", x + 300000, y + 260000, w - 600000, 340000,
                 [_para([_run(title, XB, 1500, col("body"))], algn="ctr")])
    rowxml = "".join(_tb(f"AreaRow-{i}", x + 300000, y + 620000 + i * 430000, w - 600000, 360000,
                         [_para([_run("•  " + r, EB, 1300, col("body"))])]) for i, r in enumerate(rows))
    return card + header + rowxml


def m_gantt(x, y, w, h, weeks, rows):
    lab_w = 2400000
    grid_w = w - lab_w
    cw = grid_w // len(weeks)
    hh = 500000
    out = [_rect("GanttHeader", x + lab_w, y, grid_w, hh, col("ganttHeaderFill"))]
    for i, wk in enumerate(weeks):
        out.append(_tb(f"Wk-{i}", x + lab_w + i * cw, y + 90000, cw, 320000,
                       [_para([_run(wk, EB, 1000, col("ganttHeaderText"))], algn="ctr")]))
    rh = (h - hh) // len(rows)
    for r, (label, start, span) in enumerate(rows):
        ry = y + hh + r * rh
        out.append(_tb(f"GLabel-{r}", x, ry + 90000, lab_w - 80000, rh, [_para([_run(label, EB, 1200, col("ganttRowLabel"))])]))
        out.append(_rect(f"GLine-{r}", x + lab_w, ry + rh - 12700, grid_w, 12700, col("ganttGridline"), a=0.5))
        out.append(_rect(f"GBar-{r}", x + lab_w + start * cw + 40000, ry + 60000, span * cw - 80000, rh - 220000,
                         col("ganttBar"), rad=30000))
    return "".join(out)


def m_stakeholder_cols(x, y, w, client, thiswaay):
    cw = w // 2
    def colblock(cx, head, people):
        b = [_tb(f"SHhead", cx, y, cw - 200000, 300000, [_para([_run(head.upper(), EB, 1100, col("eyebrow"), b=True)])])]
        for i, (name, role) in enumerate(people):
            b.append(_tb(f"SHn-{i}", cx, y + 400000 + i * 620000, cw - 200000, 300000, [_para([_run(name, XB, 1300, col("body"))])]))
            b.append(_tb(f"SHr-{i}", cx, y + 680000 + i * 620000, cw - 200000, 300000, [_para([_run(role, EB, 1100, col("body"), a=0.7)])]))
        return "".join(b)
    return colblock(x, "Client team", client) + colblock(x + cw, "This Waay", thiswaay)


# ================= LAYOUTS =================
LOGO_CONTENT_W, LOGO_CONTENT_H = 1500000, 247000   # 509:84 aspect
LOGO_FEATURE_W, LOGO_FEATURE_H = 2200000, 363000


def _logo(rid_variant, feature=False):
    w, h = (LOGO_FEATURE_W, LOGO_FEATURE_H) if feature else (LOGO_CONTENT_W, LOGO_CONTENT_H)
    x = IX if feature else CW - IX - w
    y = IY
    return _pic("Logo", rid_variant, x, y, w, h)


def layouts():
    """Return [(name, ground_hex, shapes, show_num, logo_variant)]. logo_variant: 'white'|'color'."""
    L = []
    navy, white = C["navy"], C["white"]

    # 1. Cover — navy; white feature logo; eyebrow; big title; prepared-for
    cover = (_logo("rIdW", feature=True)
             + a_eyebrow(IX, round(CH*0.42), 6000000, "Stage 3 — UX overhaul check-in")
             + _tb("CoverTitle", IX, round(CH*0.48), 9000000, 1400000, [_para([_run("Client, Inc.", XB, 5400, col("headerTitleOnDark"))])])
             + _tb("Prepared", IX, CH - IY - 360000, 8000000, 300000,
                   [_para([_run("Prepared for [Client name] · [Month YYYY]", EB, 1200, col("headerTitleOnDark"), a=0.7)])]))
    L.append(("Cover", navy, cover, False, "white"))

    # 2. Agenda — white; header; intro; SHARED agenda-block
    agenda_rows = [("5 min", "Recap — project goals, methodology, approach"),
                   ("15 min", "The second stage of our meeting"),
                   ("45+ min", "Deep dive on north-star design")]
    agenda = (_logo("rIdC")
              + m_slide_header("Agenda", "Project review — October 1st", "Agenda")
              + _tb("Intro", IX, IY + 1500000, 4600000, 1200000,
                    [_para([_run("Cross-functional regroup to review the outcome of our 8-week project.", EB, 1300, col("body"), a=0.8)])])
              + m_agenda_block(IX + 5200000, IY + 1500000, 5200000, agenda_rows))
    L.append(("Agenda", white, agenda, True, "color"))

    # 3. Stakeholders & agenda — white; header; stakeholder columns; SHARED agenda-block
    stake = (_logo("rIdC")
             + m_slide_header("Agenda", "Stage 3 check-in — 1.5 hours", "Stakeholders and agenda")
             + m_stakeholder_cols(IX, IY + 1600000, 4600000,
                                  [("[Name]", "Sponsor · Decision-maker"), ("[Name]", "Head of Product · CPO"), ("[Name]", "Engineering lead")],
                                  [("Kate Valdes", "Principal · Assessment lead"), ("[Name]", "Design · Research"), ("[Name]", "Facilitation")])
             + m_agenda_block(IX + 5200000, IY + 1500000, 5200000, agenda_rows))
    L.append(("Stakeholders and agenda", white, stake, True, "color"))

    # 4. Project goals — white; header; numbered-list; areas-of-focus card
    goals = (_logo("rIdC")
             + m_slide_header("Header", "Deliver lasting value", "Project goals")
             + m_numbered_list(IX, IY + 1700000, 5000000,
                               [("Deliver a modern, trustworthy UX", "Refresh key interface and interaction patterns to reflect a contemporary, high-quality experience."),
                                ("Reduce friction in critical workflows", "Study how power users perform critical tasks and reveal opportunities for design improvements.")])
             + m_areas_card(IX + 5800000, IY + 1600000, 4600000, "Areas of focus",
                            ["Home / Landing page", "Sequencer visualization", "3rd level of editability"]))
    L.append(("Project goals", white, goals, True, "color"))

    # 5. Timeline / Project Schedule — white; plain H1; gantt-grid
    timeline = (_logo("rIdC")
                + a_h1(IX, IY, 8000000, "Project Schedule")
                + m_gantt(IX, IY + 1300000, CW - 2*IX, 3400000,
                          ["Wk 1", "Wk 2", "Wk 3", "Wk 4", "Wk 5", "Wk 6", "Wk 7", "Wk 8"],
                          [("Project Planning", 0, 1), ("Kick Off", 1, 1), ("Demos", 2, 1),
                           ("Evaluation", 3, 2), ("Results Readout", 5, 1)]))
    L.append(("Timeline / Project Schedule", white, timeline, True, "color"))

    # 6. Section divider — full navy; huge green divider-word; subtitle; white logo
    divider = (_logo("rIdW", feature=True)
               + a_divider_word(IX, round(CH*0.36), 10000000, "Discover")
               + _tb("DivSub", IX, round(CH*0.60), 8000000, 400000,
                     [_para([_run("A couple more words about this", EB, 1600, col("headerTitleOnDark"), a=0.8)])]))
    L.append(("Section divider", navy, divider, False, "white"))

    # 7. Closing — full navy; green Thank you; contact; white logo
    closing = (_logo("rIdW", feature=True)
               + _tb("ThankYou", IX, round(CH*0.42), 9000000, 1200000, [_para([_run("Thank you.", XB, 5400, col("closingWord"))])])
               + _tb("CloseSub", IX, round(CH*0.60), 9000000, 400000,
                     [_para([_run("Where would you like to go from here?", XB, 1800, col("headerTitleOnDark"))])])
               + _tb("Contact", IX, CH - IY - 560000, 8000000, 500000,
                     [_para([_run("Kate Valdes · This Waay — Product Design Studio", EB, 1200, col("headerTitleOnDark"), a=0.75)]),
                      _para([_run("thiswaay.ai", EB, 1200, col("eyebrow"))])]))
    L.append(("Closing", navy, closing, False, "white"))
    return L


# ================= ASSEMBLY =================
def _sptree(shapes):
    body = "".join(shapes) if isinstance(shapes, (list, tuple)) else (shapes or "")
    return ('<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
            '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
            f'{body}</p:spTree>')


def _bg(hexv):
    return f'<p:bg><p:bgPr><a:solidFill><a:srgbClr val="{hexv}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>'


def layout_xml(name, ground, shapes, show_num):
    sldnum = ""
    if show_num:
        sldnum = _tb("SlideNumber", CW - IX - 800000, CH - IY - 300000, 800000, 300000,
                     [_para([_run("#", EB, 1100, col("footer"))], algn="r")])
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
            f'<p:sldLayout xmlns:a="{A_NS}" xmlns:r="{R_NS}" xmlns:p="{P_NS}" type="cust" preserve="1">'
            f'<p:cSld name="{name}">{_bg(ground)}{_sptree(shapes + (sldnum if sldnum else ""))}</p:cSld>'
            '<p:clrMapOvr><a:overrideClrMapping bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" '
            'accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/></p:clrMapOvr>'
            '</p:sldLayout>')


def slide_master_xml(n):
    ids = "".join(f'<p:sldLayoutId id="{2147483649+i}" r:id="rId{i+2}"/>' for i in range(n))
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
            f'<p:sldMaster xmlns:a="{A_NS}" xmlns:r="{R_NS}" xmlns:p="{P_NS}">'
            f'<p:cSld>{_bg(C["white"])}{_sptree([])}</p:cSld>'
            '<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" '
            'accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>'
            f'<p:sldLayoutIdLst>{ids}</p:sldLayoutIdLst></p:sldMaster>')


def build():
    L = layouts()
    n = len(L)
    theme = emit_pptx.full_theme_xml()
    logo_c = LOGO_COLOR.read_bytes()
    logo_w = LOGO_WHITE.read_bytes()

    def layout_rels(variant_needed):
        rels = ['<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>']
        rels.append('<Relationship Id="rIdC" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/logo-color.png"/>')
        rels.append('<Relationship Id="rIdW" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/logo-white.png"/>')
        return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(rels) + '</Relationships>')

    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Default Extension="png" ContentType="image/png"/>'
          '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.template.main+xml"/>'
          '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>'
          + "".join(f'<Override PartName="/ppt/slideLayouts/slideLayout{i+1}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>' for i in range(n))
          + '<Override PartName="/ppt/notesMasters/notesMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesMaster+xml"/>'
          '<Override PartName="/ppt/presProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/>'
          '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
          '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
          '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>')

    presentation = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
                    f'<p:presentation xmlns:a="{A_NS}" xmlns:r="{R_NS}" xmlns:p="{P_NS}">'
                    '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>'
                    '<p:notesMasterIdLst><p:notesMasterId r:id="rId2"/></p:notesMasterIdLst>'
                    f'<p:sldSz cx="{CW}" cy="{CH}" type="screen16x9"/><p:notesSz cx="{CH}" cy="{CW}"/></p:presentation>')
    pres_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>'
                 '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster" Target="notesMasters/notesMaster1.xml"/>'
                 '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/presProps" Target="presProps.xml"/>'
                 '<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/></Relationships>')
    master_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>'
                   + "".join(f'<Relationship Id="rId{i+2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout{i+1}.xml"/>' for i in range(n))
                   + '</Relationships>')
    notes_master = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
                    f'<p:notesMaster xmlns:a="{A_NS}" xmlns:r="{R_NS}" xmlns:p="{P_NS}"><p:cSld>{_bg(C["white"])}{_sptree([])}</p:cSld>'
                    '<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/></p:notesMaster>')
    notes_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
                  '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                  '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/></Relationships>')
    root_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>'
                 '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
                 '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>')
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>This Waay — Deck Template (atomic)</dc:title><dc:creator>This Waay</dc:creator></cp:coreProperties>')
    app = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>This Waay build_deck_atomic.py</Application></Properties>')
    presprops = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n<p:presentationPr xmlns:a="{A_NS}" xmlns:r="{R_NS}" xmlns:p="{P_NS}"/>'

    parts = {
        "[Content_Types].xml": ct, "_rels/.rels": root_rels,
        "docProps/core.xml": core, "docProps/app.xml": app,
        "ppt/presentation.xml": presentation, "ppt/_rels/presentation.xml.rels": pres_rels,
        "ppt/presProps.xml": presprops, "ppt/theme/theme1.xml": theme,
        "ppt/slideMasters/slideMaster1.xml": slide_master_xml(n),
        "ppt/slideMasters/_rels/slideMaster1.xml.rels": master_rels,
        "ppt/notesMasters/notesMaster1.xml": notes_master,
        "ppt/notesMasters/_rels/notesMaster1.xml.rels": notes_rels,
        "ppt/media/logo-color.png": logo_c, "ppt/media/logo-white.png": logo_w,
    }
    for i, (name, ground, shapes, show, variant) in enumerate(L, 1):
        parts[f"ppt/slideLayouts/slideLayout{i}.xml"] = layout_xml(name, ground, shapes, show)
        parts[f"ppt/slideLayouts/_rels/slideLayout{i}.xml.rels"] = layout_rels(variant)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for nm, data in parts.items():
            z.writestr(nm, data if isinstance(data, bytes) else data)
    print(f"wrote {OUT} ({len(parts)} parts, {n} named layouts)")
    print("  layouts:", [x[0] for x in L])


if __name__ == "__main__":
    build()
