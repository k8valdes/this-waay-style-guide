# Component anatomy & variant catalogs

Relocated from `tokens.json` component prose in the v4.0 migration. The extracted *values*
became tier-3 tokens (`button.*`, `card.*`, `badge.*`); this is the prose that describes their
structure and usage. Governs tokens: `button.*`, `card.*`, `badge.*`, and the `color.*` roles they reference.

## Layout rule (all components)

NO component defines its own width, breakpoint, or outer margin. Width comes from the Bootstrap
column it sits in (`container` / `row` / `col-lg-*`). This is what makes a component reusable
across pages — re-authoring the grid with hand-rolled CSS grid is the single fastest way to lose
the site's whitespace and component sizing.

## Button

Base geometry: radius `25px` (`dimension.radius.pill`), `AxiformaBold 16px/24px`
(`typography.button`), padding `13px 30px 11px`, transition `all .3s ease`. Hover **inverts** fill
and text rather than darkening (see layout-mechanics → ghost-button hover). Only the `lg` size
ships today; `md`/`sm` are proposed.

- **primary** — green fill (`fill.action`), **white** label. This is the accepted deviation (see `button.primary.label` in `tokens.json`): 2.42:1, fails AA, held for brand consistency.
- **secondary / ghost** — transparent, green outline + accessible-green label (`text.accent`).
- **on-navy (white)** — white fill, green label, for navy grounds.
- **tag** — 2px outline, 2px radius, 12px — the squarest button.

## Cards — the 13→3 consolidation

Production carries **13 distinct card types**; the consolidation target is **3** (`card.content`,
`card.panel`, `card.badge`) plus `card.track`, which is already canonical. Each card is really
`(cardType × ground × badgePlacement)`, not 13 unrelated patterns. The token ledger (status =
`production` / `deprecated` + `supersededBy` / `proposed`) lives in `tokens.json` under `card.*`.

The 13 types: content, skewed accent, service primary (tall, priced), flip (work/case study),
testimonial, carousel, deliverable, quote, green centered, track pricing (on-navy), tall pricing
(+featured), banner, case-study highlight.

**Card grounds** every card can take: white, soft (gradient), soft-warm (gradient), green (solid),
navy-translucent (on-dark only), stroke/outline.

- **Flip card correction (2026-08):** title and description live INSIDE the card, never below it — front = image + bottom gradient scrim carrying the title; back (hover/focus) = full title + short description + CTA, centered on the accent-colour mask. Corrected after a rebuild rendered them as page copy underneath the card. **Test components with real, full-length content, not placeholder labels** — the style guide's own specimen never caught this because its demo cell didn't carry real copy.
- **Undecided consolidation targets:** `card.flip` and `card.carousel` are marked `proposed` in the token tree — the flat spec leaves their consolidation target genuinely undecided (flip is a distinct interaction pattern; carousel is multi-item). Not guessed.

## Float-panel card (signature)

A transparent box whose `::before` is a skewed (`−10°`, `angle.skew-card`) coloured panel starting
partway down (60–90px), with a large figure floating above and overlapping the panel's top edge.
This overlap is the brand's most recognizable card gesture. Invariants: radius 8px, title
`AxiformaExtraBold`, title centered. Variant axes: panel ground (soft-warm / green), panel top
(60/80/90px), figure height (120/173/190px), body copy (none / 14px white / 16px white).

## Segment card

Solid soft-gradient card, 8px radius, with a figure pulled UP 40px so it breaks the card's top
edge; title sits 55px below to clear the figure. The figure is NOT a fixed shape — it's whatever
pre-rendered icon graphic ships for that segment, and the three real assets disagree:

| Segment | Asset | Shape |
|---|---|---|
| Scaling & Emerging Technology Teams | `icon07.svg` | navy circle, green 3px ring, white clipboard+check, green accent circle |
| Investors & Portfolio Operators | `icon09.svg` | navy circle, green 3px ring, white document+lines, green sparkle |
| Government & Public Sector Systems | `icon06.svg` | green **`#72B68A`** (a distinct shade from `green.400`) skewed rectangle, white branching-path icon — the skew motif at icon scale |

> `#72B68A` is a pre-rendered asset colour, not a UI token — it lives only inside `icon06.svg`.

## Badge

Variant types: proprietary shield (metallic rim, star-field navy face, white icon), icon tile
(rounded square / circle / punch gradient), category pill (green fill, 25px radius), tag chip (2px
outline, 2px radius), price tag (skewX −6°). Placements: inside top-left/center/right, floating
above (overlaps panel top — the signature), floating side, corner tag.

- **Shield** ships as **raster** (`image26–31.webp`); an SVG recreation exists (silver-rim frame + navy star-field face, white icon slot). **Shield roster V1 vs V2 is pending Kate** — marked `proposed` in the token tree; the shield frame itself is `production`. 8 shield+icon pairings are in use (Product Strategy & UXR → viewfinder; Product Design & UX → ruler; AI Guidance → sparkles; Structural Readiness → 2×2 grid; User Enablement → user-plus; Business Advantage → trending-up; Data Access → database; Quality → double-check).
- **Icon sources:** Heroicons (existing single-tone). New iconography → **Google Material Icons** (decided 2026-08). A duotone-treatment experiment was built and discarded 2026-08.
- **Eyebrow tracking is unresolved:** 2.76px theme default (`dimension.tracking` → the eyebrow composite) vs 1.5px/1.6px on Assessment and AI Practice. 2.76px is the proposed canonical.

## Navigation

Sticky, `top: 0`, `z-index: 50`. Background navy (`color.navy.900` / `surface.ground`), bottom
border `color.overlay.nav-border` (white @ 8%). Two-row layout: logo/wordmark on the first row, a
second row of section-group buttons (`aria-expanded` + `aria-controls`) disclosing subsection
dropdowns — click/keyboard only, never hover-only; one group open at a time; Escape and
outside-click close it. Link text `color.slate.300` (`#B9CBDC`); link hover `color.fill.action`
(green); link size `text-size.md` (0.85rem), weight 600.
