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

`scripts/validate-spec.py` lints `tokens.json` for internal contradictions (a value or rule stated differently in two places, including against its HTML guide) and can scan a file of generated output for off-brand hex colors. Run `python3 scripts/validate-spec.py --help` for usage.

## Scope

This repo contains **visual brand expression only** — colors, type, spacing, motion, components, motifs, and logo assets. Voice & tone guidelines, pricing, positioning, and business strategy are intentionally excluded and live in private studio documents.

## Status

Published via GitHub Pages at [k8valdes.github.io/this-waay-design-system](https://k8valdes.github.io/this-waay-design-system/). The site is link-only: pages carry `noindex` and are meant to be shared directly, not discovered via search.
