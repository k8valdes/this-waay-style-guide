# Atomic slide system — catalog

The deck-side equivalent of the web page-recipes. **Atoms → molecules → layouts** mirrors the token
tiers **primitive → semantic → component**: an atom is the smallest reusable unit, a molecule composes
atoms, a layout composes molecules into a named, slot-fillable page. Every atom is token-bound (a
`slide.*` tier-3 token or the theme), so **filling a deck is populating slots, not painting slides.**

This is a permanent product capability (Part 7). This Waay is the worked example; the structure is
brand-agnostic — for another client only the token bindings and assets change.

- **Source of truth:** `2026 This Waay Deck Template_NEW_BH` (36 slides). Tokens: `slide.*` in
  `tokens.json` (v4.0) → resolved through `build/tokens.css` / the resolver.
- **Deck accent is TEAL, not green.** Eyebrows, subheads, timed-rows, numerals, and Opportunity/Sub-
  Category pills are teal (`fill.accent` / `text.accent-alt`). **GREEN (`fill.action`) is reserved** for
  divider-words, gantt bars, Category pills, and the closing word. This is the deck's most important
  binding and the opposite of the marketing site (green eyebrows).
- **Headers are NAVY** here (`text.body` / `text.on-ground`), not the legacy slideDeck "Deck Gray" —
  the real template supersedes that rule. Flagged in the report.

---

## Atoms

| Atom | Slots | Token binding | Notes |
|---|---|---|---|
| **logo** | asset, size, placement | `slide.logoInset` / `logoContentSize` / `logoFeatureSize` (+ asset refs in `$extensions`) | Real SVG (`assets/`), never text-recreated. See Logo governance below. |
| **eyebrow-label** | text | `slide.eyebrow` → `text.accent-alt` (teal ink) | Uppercase, tracked. |
| **subhead** | text | `slide.subhead` → `text.accent-alt` | The teal line above an H1. |
| **H1-display (light/dark)** | text | `slide.headerTitle` → `text.body` · `slide.headerTitleOnDark` → `text.on-ground` | Axiforma ExtraBold (theme). |
| **running-footer** | section-name, number | `slide.footer` → `text.muted` | Omitted on Cover/Divider/Closing. |
| **body-paragraph** | text | `slide.body` → `text.body` | Axiforma / muted via `overlay.muted-ink`. |
| **timed-row** | time, description | `slide.timedRowTime` → `text.accent-alt` · `slide.timedRowBody` → `text.body` | The agenda unit. |
| **numbered-item** | numeral, title, sub-text | `slide.numeralFill` → `fill.accent` (teal) · `slide.numeralText` → `text.on-fill` | Teal circle numeral. |
| **pill** | label | `slide.pillOpportunity`/`pillSubCategory` → `fill.accent` (teal) · `slide.pillCategory` → `fill.action` (green) · `slide.pillLabel` → `text.on-fill` · `slide.pillRadius` | Three states: Opportunity (teal), Sub-Category (teal), Category (green). |
| **card** | icon-tile, title, body, pill | `slide.cardGround` → `surface.ground` (navy) · `slide.cardTitle` → `text.on-ground` · `slide.cardBody` → `overlay.on-dark-body` · `slide.cardRadius` | Variants: compact / expanded / alt-light (`slide.cardAlt*`, proposed) / user-flow. |
| **icon-tile** | icon | icon asset (duotone library) | White/green icon in a card. |
| **divider-word** | word | `slide.dividerWord` → `fill.action` (**green**) | Huge; the section break. |
| **gantt-bar** | span | `slide.ganttBar` → `fill.action` (green) | |
| **table-header-cell** | text | `slide.ganttHeaderFill` → `surface.ground` · `slide.ganttHeaderText` → `text.on-ground` | Gantt week header. |
| **process-diamond** | label | `slide.diamondFill` → `fill.accent` (teal) · `diamondAlt` → navy (proposed) · `diamondEmphasis` → green (proposed) · `diamondLabel` → `text.on-ground` | Double-diamond stage. |
| **paper-plane motif** | — | asset (`assets/motif/`) | Official art; never redrawn. Cover / dividers / closing / Conclusion accent. |
| **image-panel** | image | `slide.imagePanelGround` → `surface.ground` (navy placeholder) | Screenshot frame. |

Colors resolve through the semantic role → primitive chain, so a change to `fill.accent` reflows every
teal atom at once. No atom carries a literal.

## Molecules

| Molecule | Composed of | Slots | Used in layouts |
|---|---|---|---|
| **slide-header** | eyebrow + subhead + H1-display + logo + footer | eyebrow, subhead, title | Every content layout |
| **agenda-block** | card ground (`slide.agendaCardGround` → `gradient.soft`) + ordered timed-rows | rows[] | **Agenda, Stakeholders & agenda, Company-info & agenda** (defined once, shared) |
| **stakeholder-columns** | 2 columns of name/role pairs | client[], thisWaay[] | Stakeholders & agenda |
| **numbered-list** | ordered numbered-items (+ sub-bullets) | items[] | Goals, Conclusion, Findings (B), Insight |
| **areas-of-focus-card** | soft card + icon+label rows | title, rows[] | Goals |
| **card-grid** | 2–4 cards | cards[] | Areas of interest |
| **gantt-grid** | table-header-cells + row-labels + gantt-bars | weeks[], rows[] | Timeline |
| **double-diamond** | process-diamonds (Discover/Define/Create/Validate) | stages[] | Project touchpoints |
| **opportunity-block** | pill(s) + suggested-changes numbered-list | pills[], changes[] | Insight / Specific Screen |
| **footer** | section-name + slide-number | name, n | Content layouts |

## Named layouts

Grounds follow `layout.pageRhythm` (open + close navy; ground changes carry an angled break). Every
value resolves from theme or `slide.*`. Safe-area ≥5%; body ≥14pt; no transitions; slide numbers except
Cover/Divider/Closing.

| Layout | Ground | Slots | Molecules / atoms | Logo | # |
|---|---|---|---|---|---|
| **Cover** | navy | eyebrow, title, "Prepared for [client] · [month]" | eyebrow, H1-display(dark), paper-plane, footer-prepared | white, feature top-left | no |
| **Agenda** | white | intro, agenda rows[] | slide-header + intro + **agenda-block** | colour, top-right | yes |
| **Stakeholders & agenda** | white | client[], thisWaay[], rows[] | slide-header + stakeholder-columns + **agenda-block** | colour, top-right | yes |
| **Company-info & agenda** | white | prose-blocks[], rows[] | slide-header + titled-prose + **agenda-block** | colour, top-right | yes |
| **Project touchpoints** | white | titled-text[], stages[] | slide-header + titled-text + double-diamond | colour, top-right | yes |
| **Project goals** | white | intro, items[], focus-rows[] | slide-header + numbered-list + areas-of-focus-card | colour, top-right | yes |
| **Section divider** | navy (full-bleed) | word, subtitle, secondary? | divider-word + paper-plane + subtitle | white, feature | no |
| **Findings / Design artifacts** | white | observations[] (bullet A / numbered B) + follow-up card? | slide-header + observations + card | colour, top-right | yes |
| **Insight / Specific Screen** (L/R mirror) | white | eyebrow, title, pills[], changes[], image | slide-header + opportunity-block + image-panel | colour, top-right | yes |
| **Areas of interest** | white | cards[] (2–4) | slide-header + card-grid | colour, top-right | yes |
| **Timeline / Project Schedule** | white | weeks[], rows[] | plain H1 + gantt-grid | colour, top-right | yes |
| **Conclusion / Recommendations** | white | recs[] (+sub-bullets) | slide-header + numbered-list + paper-plane accent | colour, top-right | yes |
| **Closing / Thank you** | navy (full-bleed) | word, sub, contact[] | closing-word + paper-plane + contact-block | white, feature top-left | no |

### Proof set — decomposed (the hardest molecules)

- **Agenda** = `slide-header` + intro `body-paragraph` + **agenda-block** (ordered `timed-row`s on
  `gradient.soft`). The agenda-block is the same molecule on slides 3–5.
- **Project goals** = `slide-header` + `numbered-list` (teal-numeral `numbered-item`s with sub-text) +
  `areas-of-focus-card` (soft card, icon+label rows).
- **Timeline** = plain `H1-display` + `gantt-grid` (`table-header-cell` navy week row + `gantt-bar`
  green spans + row labels). Exercises the navy-header/green-bar split.

The rebuilt `.potx` defines **agenda-block once** (`build_deck_atomic.py: agenda_block()`) and calls it
from the Agenda and Stakeholders & agenda layouts — proving it is shared, not copied.

---

## Logo governance (Part 5)

The logo is a first-class atom so a generator can't omit or misplace it.

- **Real asset, both variants** — `assets/This-Waay-Logo-White-Horizontal.svg` (white-on-dark) and
  `assets/This-Waay-Logo-Blue-Horizontal.svg` (colour-on-light). Never a type recreation.
- **Variant by ground:** white-on-dark on navy (Cover / Section divider / Closing); colour on white
  (all content layouts).
- **Placement by layout:** content → top-right, small (`slide.logoContentSize`); Cover / Divider /
  Closing → feature top-left (`slide.logoFeatureSize`).
- **Clear-space + inset:** `slide.logoInset` (≥ the safe-area). Min-size = `slide.logoContentSize`.
- **Validator check (Part 6):** every layout carries the logo, correct variant for its ground, within
  clear-space.

---

## Skill & client workflow (Part 7)

`references/slide-components.md` + the named-layout `.potx` are **Skill assets** — the deck-building
capability, recorded in the schema doc / SKILL.md as **"atomic deck system — audit, catalog, bind,
compose."**

The client motion is the same three steps, mirroring reconcile-vs-greenfield:

1. **Audit** their deck (existing) — or start greenfield.
2. **Catalog** atoms and **bind** to *their* tokens (this file is the template).
3. **Compose** named layouts, emitted from the resolver.

Structure is reused for every client; only bindings + assets change — the deck-side of "the shared
vocabulary is the product."
