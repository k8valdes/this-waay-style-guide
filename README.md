# This Waay — Design System

The unified home for both This Waay design systems, under one umbrella entry point.

| Path | What it is |
|---|---|
| `index.html` | The umbrella landing page — "one system, two brands," with links to both. |
| `product-design-studio/` | This Waay Product Design Studio's living style guide (`index.html`, `STYLE.md`, `tokens.json`, `README.md`, `assets/`). |
| `gridmark-partners/` | Gridmark Partners' living design system (`gridmark-design-system-v3.html`, `tokens.json`, `Logos/` asset package). |
| `RELATIONSHIP.md` | What's intentionally shared vs. intentionally different between the two brands. |
| `CHANGELOG.md` | Version history for this unified home (not each brand's own internal changelog — see below). |

## How the two brands relate

This Waay is the parent brand. **Product Design Studio** is its original expression. **Gridmark Partners** is a civic-sector sibling brand — sharing This Waay's visual origin, but with its own accent color, status colors, and voice. See `RELATIONSHIP.md` for the specifics.

Each brand's design-system document is maintained independently, with its own embedded tokens, its own version line, and its own in-page changelog. This repo does not merge them — it gives them one shared entry point and documents how they relate.

## Licensing note

Both brand docs use **Axiforma** (Kastelov) as their primary typeface, with Poppins as the approved free fallback. **Resolved 2026-08 by Kate:** Axiforma's license covers Preview & Print embedding only (`fsType 4`, verified from the OS/2 table) — permitting PDF and read-only PPTX generation, but not a self-hosted webfont. The web stack stays as shipped: `'Axiforma', 'Poppins', 'Segoe UI', sans-serif`, no self-hosted woff2, no webfont license purchase at this time. See `product-design-studio/tokens.json` → `typography.family.primary.licensing` for the full permitted/not-permitted breakdown. No font files are hosted in this repo; both docs load Poppins from Google Fonts and reference Axiforma via `local()` only.

## Validating the spec

`scripts/validate-spec.py` lints `tokens.json` for internal contradictions (a value or rule stated differently in two places, including against its HTML guide), scans a file of generated output for off-brand hex colors, and validates the generated Office templates (`--template`). Run `python3 scripts/validate-spec.py --help` for usage.

## Templates (`assets/templates/`)

Deterministic Office templates generated from `tokens.json`, so decks and documents inherit the brand instead of re-deriving it from prose.

| Artifact | Built by | Consumes |
|---|---|---|
| `assets/templates/this-waay-deck.potx` | `scripts/build_deck.py` | `tokens.json` (+ `build_theme.py`) |
| `assets/templates/this-waay-reference.docx` | `scripts/build_reference_docx.py` | `tokens.json` + the branded letterhead |
| the shared OOXML theme (`clrScheme`/`fontScheme`) | `scripts/build_theme.py` | `tokens.json` |

- **Generated, never hand-edited.** If a value is wrong, fix `tokens.json` (or the script) and rebuild — do not edit the emitted XML.
- **Build/validate deps** (a local virtualenv, not committed): `python-pptx`, `python-docx`, `defusedxml`, `fonttools`. `build_theme.py`, `build_deck.py`, and `validate-spec.py` are standard-library only; only the render/inspect helpers use the extras.
- **Fonts are referenced by name, never embedded.** Axiforma is `fsType 4` (Preview & Print only), so the templates name the family and rely on the installed-font / Poppins fallback chain — no font binary is written into either package. The OTFs live in a local, git-ignored `axiforma/` folder and must never be committed (see the licensing note above).
- `build_reference_docx.py` transforms the existing branded letterhead (kept local in `Examples/`, git-ignored); pass `--letterhead <path>` to point at it elsewhere.

## Verifying a spec change

`scripts/verify-phase0.py` is a pass/fail gate asserting the Phase 0 reconciliation invariants against `product-design-studio/tokens.json`. Run it (exit 0 = all pass) as the last step of any spec change.

## Scope

This repo contains **visual brand expression only** — colors, type, spacing, motion, components, motifs, and logo assets. Voice & tone guidelines, pricing, positioning, and business strategy are intentionally excluded and live in private studio documents.

## Status

Published via GitHub Pages at [k8valdes.github.io/this-waay-style-guide](https://k8valdes.github.io/this-waay-style-guide/). The site is link-only: pages carry `noindex` and are meant to be shared directly, not discovered via search.
