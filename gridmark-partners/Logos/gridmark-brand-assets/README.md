# Gridmark Partners — Brand Asset Package v1.0
The Marked Cell identity · July 2026 · A This Waay Company

## Contents
- `marks/` — the symbol
  - `gridmark-mark-navy.svg` — primary (light grounds)
  - `gridmark-mark-white.svg` — reversed (Deep Navy grounds)
  - `gridmark-mark-brass.svg` — all-brass premium (Deep Navy only)
  - `gridmark-favicon-navy.svg` / `-white.svg` — simplified cut, use below 40px
  - `gridmark-favicon.svg` — browser favicon (navy tile); export .ico at 16/32/48 from this
- `lockups/` — mark + wordmark
  - stacked (master), horizontal (deck-aligned), signature (+tagline), endorsement (navy-grounded)
- `tokens/gridmark-logo-tokens.json` — W3C design tokens
- `css/gridmark-lockup.css` — the wordmark block as a web component

## Rules (the short version)
1. **Clear space** = one marked cell (26×13 artboard units) on all sides.
2. **Minimum sizes**: full mark ≥ 40px wide; below that, favicon cut; favicon ≥ 16px.
3. **The marked cell is always brass** (#C8A46B) — the one constant in every variant.
4. **Colors**: navy on light, white on navy, all-brass on navy for premium print. Never other colors.
5. **Wordmark**: Axiforma (Poppins fallback). GRIDMARK SemiBold 600, .14em tracking; PARTNERS Regular at 0.4× size, letters justified to GRIDMARK's width; single hairline rule with one brass cell flush right.
6. **Horizontal lockup**: the mark's deck line and the wordmark's rule share one axis.
7. **Tagline** (signature lockup only): sentence case, Regular, Steel #0D698A.

## Production notes
- SVG type uses `textLength` justification with Poppins fallback. **Before final print/vendor export, set in licensed Axiforma and outline the type in Illustrator.**
- Generate `favicon.ico` (16/32/48) from `gridmark-favicon.svg`; keep the SVG favicon for modern browsers.
- These masters supersede all prior bridge marks (v1 arch mark, Lattice Frame, dot-datum variants). Retire them.
