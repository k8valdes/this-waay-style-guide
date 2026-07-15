# Unified System Changelog

This tracks version milestones for the unified `Branding/` home itself — not each brand's own internal changelog. See `product-design-studio/index.html` (footer living-document note) and `gridmark-partners/gridmark-design-system-v3.html` (Governance & versioning) for brand-level changelogs.

## Unified v1.1 — 2026-07-05

Both brand docs realigned to a shared chapter spine — Principles → Architecture → Foundations (color, type, spacing, elevation, motion, accessibility) → Brand → System → Application → Language → Operations — so the two pages read in the same sequence while staying independently maintained.

- This Waay Product Design Studio → v2.3: new "Token architecture" section documenting its (deliberately) flat `--tw-*` block, motion/accessibility swapped within Foundations, motifs + illustration moved up into a Brand chapter (absorbing Canonical), Application sections now contiguous; nav groups and `tokens.json` navigation block updated to match.
- Gridmark Partners Design System → v3.1: Accessibility folded into Foundations (the late "Standards" chapter disappears), Principles split into its own chapter, section tints reflowed to keep strict alternation; nav and in-page changelog updated.
- Token architectures remain intentionally separate per `RELATIONSHIP.md` — no token values changed in either brand.

## Unified v1.0 — 2026-07-01

Initial unification of This Waay Product Design Studio and Gridmark Partners under one shared home and landing page.

- Relocated This Waay Product Design Studio (v2.2) and Gridmark Partners Design System (v3.0) into `Branding/` as sibling brand folders under a new umbrella landing page (`index.html`).
- Token architectures kept intentionally separate — each brand's design-system document retains its own embedded token block, unmodified. `RELATIONSHIP.md` documents which values are intentionally shared (inherited from a common origin) vs. intentionally different (brand-specific choices).
- Added `gridmark-partners/tokens.json`, a new machine-readable export of Gridmark's existing token values, bringing it to parity with This Waay's existing `tokens.json`.
- Both brand documents were consolidated here from their previous separate homes; this folder is now the canonical location for each.

Brand-doc versions at time of unification: This Waay Product Design Studio v2.2, Gridmark Partners Design System v3.0. Each brand doc continues independent versioning going forward.
