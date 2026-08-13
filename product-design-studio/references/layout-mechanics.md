# Layout mechanics

CSS engineering rules relocated from `tokens.json` `systemRules` in the v4.0 migration.
These reference tokens but are not tokens. Governs tokens: `angle.skew-*`,
`dimension.space.*`, `typography.*`, the `color.surface.*` roles.

All rules are `status: production` — adopted 2026-08 after building the AI Practice page on
the system; each exists because its absence produced a visible defect.

## Measure

Every block of running text is capped. Long lines are the most common readability failure on
wide screens. Headings get a *much* shorter measure than body copy on purpose — it forces them
to break on meaning rather than at the container edge, which prevents stranded words in display type.

| Measure | Value | Use |
|---|---|---|
| body | **68ch** | Body copy — the default for running text |
| tight | **46ch** | Lede, intro, card copy |
| head | **22ch** | Display headlines (H1 / large H2) |

**Hero exception:** Hero-scale H1s (46px+) do NOT take the 22ch head measure — that value is
tuned for in-page H2s at 40px; applied to a larger hero headline it collapses it to one line too
many. Let the hero H1 size to its actual column width (rag balance still applied) and verify the
*rendered* line count for that specific headline rather than assuming the token transfers.

## Rag — no widows, orphans, or ladders

- `text-wrap: balance` on headings, card titles, ledes — evens line lengths on **short** text in **wide** containers.
- `text-wrap: pretty` on paragraphs, list items, long quotes — fixes the last-line widow on **long** text.
- `hyphens: none` on all headings — display type never hyphenates.
- **Pitfall:** `balance` is wrong in a narrow column — in a `col-lg-3` card it shortens every line and the rag goes stubby. Balance short text in wide containers; pretty long text in narrow ones.

## Angled break (the signature diagonal)

Skew angles are tokens: `angle.skew-section` (−2°, the default), `skew-pricing` (−3°),
`skew-contact` (−5°), `skew-price-tag` (−6°, skewX), `skew-card` (−10°, the float-panel motif).
Applied on a `::before` behind the content — never on the content (which would shear the type).

- The diagonal must sit **flush** against the grounds above and below (no sliver of a third colour) and run **edge to edge** of the viewport.
- **How:** a skewed element rotates about its own centre, so its far corners lift out of its box. The skewed ground is a `::before` that overshoots its section — horizontally (`left/right: -8vw`) so the diagonal always reaches both viewport edges, and vertically (~2.2vw) so consecutive sections overlap rather than gap.
- **Clearance rule (the most common rebuild defect):** the diagonal rises above the section's own box by roughly `(width / 2) × tan(2°) ≈ 26px` at desktop, PLUS the overshoot. **A section on either side of a break needs ≥ 90px of vertical padding**, or its last line of copy slides under the neighbouring ground.

## Ground ownership

A component that carries its own ground owns its own text colour AND its own controls — not just
text. A light card dropped into a navy section must not inherit that section's light-on-dark styling.

- **Failure mode:** white text on a soft-gradient card reads as blank. An on-navy ghost button (white outline) rendered inside a light card that itself sits inside a navy section is the same bug one level down — a section-scoped rule like `.tw-on-navy .tw-btn--ghost` only knows the section's ground, not the actual ground the button is sitting on.
- **How:** any component with its own ground — including buttons and list markers inside it — sets those colours at a specificity high enough to beat a section-level descendant selector (e.g. doubled class), without reaching for `!important`. A bare class selector LOSES to a descendant selector like `.tw-step p` — that collision silently muted a green subtitle during the AI Practice build.
- **Prefer extend over invent:** a from-scratch card is a new opportunity to reintroduce this exact bug. Prefer extending an already-portable component (the generic content card) over inventing a new one.
- **Specificity check:** if the base selector already uses a doubled class, a single-class colour modifier will lose SILENTLY. Match or exceed the doubled pattern, or the override never applies and the failure is invisible until computed style is inspected.

## Ghost-button hover

On hover/focus a ghost button's fill becomes its outline colour, and the label knocks out to the
ground it was sitting on. Never a third colour, never a tint.
- On light: green outline → green fill, white label.
- On navy: white outline → white fill, navy label.

## Straddle element (a card/banner bridging two sections)

Built as the FIRST element of the section that comes AFTER the boundary. Correct mechanism is
`transform: translateY(-overlap)` + `margin-bottom: -overlap` on the SAME element (`.tw-overlap`),
**NOT** `margin-top`. The break renders behind it (z-index), so the diagonal appears to pass under
the straddling element.

- **Not margin-top (rewritten 2026-08 after shipping broken twice):** a negative `margin-top` on the first child of a zero-padding, zero-border parent collapses THROUGH the parent — it drags the section's own box (and the diagonal it paints) up with it, so changing the overlap moves the card AND the boundary together as a rigid unit; the card looks tuned by the numbers but sits almost entirely on one side of the seam when rendered. `transform` repaints pixels without touching layout, so the section stays put; the paired `margin-bottom` (between two siblings, not into the parent) gives back the flow space the lift no longer needs.
- **Block formatting context:** give `.tw-overlap` itself `display: flow-root`. Without it, a nested negative margin one level down re-introduces the same collapse — Bootstrap's own row gutter (`.g-4` sets `.row{margin-top:-gutter}`) is exactly that pattern, and silently ate part of the lift.
- **No redundant padding:** the section holding the straddle needs ZERO top padding (use a `.pad-after-overlap` variant, not the generic `.pad`) — the straddling element supplies its own clearance via the overlap value.
- **Verify against real pixels:** verify the split with actual rendered pixels (screenshot + sample colour on both sides of the line at an x with no other content), not box-model arithmetic — two DOM measurements that both depend on the same collapsing margin can validate a bug against itself. The diagonal also renders above the raw boundary Y by the overshoot (~2.2vw) plus a skew-dependent slope across the row (~44px total at −2° over 1280px).
- **Tall elements:** a tall straddle (a banner far taller than an entry card) needs correspondingly more lift to bisect the line — which can eat into the content above it, so increase that content's own bottom clearance to match.
- **Clearance:** give the copy above it room to breathe FIRST — production runs a generous gap between the preceding copy and the top of the straddle, well beyond the ~90px minimum. Tune the even split (roughly half above the boundary, half below) as a separate step.

## Text-CTA with arrow

A link styled as text, not a button, ending in a trailing arrow that nudges forward on
hover/focus. Extends production's `.link-txt` pattern ("Click to learn more"). Use where a CTA
shouldn't compete with the page's real buttons — e.g. closing out one of several parallel content blocks.
