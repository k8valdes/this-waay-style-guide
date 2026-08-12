# Unified System Changelog

This tracks version milestones for the unified `Branding/` home itself — not each brand's own internal changelog. See `product-design-studio/index.html` (footer living-document note) and `gridmark-partners/gridmark-design-system-v3.html` (Governance & versioning) for brand-level changelogs.

## Unified v1.2 — 2026-08-12 — Phase 0 spec reconciliation

Made the This Waay Product Design Studio spec internally consistent (`tokens.json` ↔ `index.html`) without making new brand decisions — decisions already on record from Kate (green-button white text, Axiforma licensing) were reconciled and dated; disagreements with no decision on record were left alone and reported instead. See `product-design-studio/index.html` footer for the full v3.1 note.

- This Waay Product Design Studio → tokens.json v3.1: reconciled the green-fill/white-text button contrast note (was internally contradictory and mismeasured — now a dated, measured accepted deviation with a remediation lever); removed the retired `clamp(56px,8vw,110px)` section-padding claim from `spacing.use`; collapsed the duplicate `layout.textMeasure` block into `systemRules.measure`; promoted `weightEquivalents` to production and added an authoritative `familyName` per font cut (numeric weight alone silently resolves to the wrong Axiforma cut); resolved the Axiforma web-licensing caveat (Preview & Print embedding only — PDF/deck generation permitted, web stack unchanged).
- Gridmark Partners — audited, not changed: no equivalent internal contradiction found with a decision on record. Flagged for Kate: the design system's own primary button (and at least one card component) ship white text on the shared `#54B987` green fill — the same measured ~2.42:1 failure as This Waay's button — while the doc's contrast-pairings table and blanket "WCAG 2.1 AA... AA contrast on all text" claim don't cover that pairing. No fix applied; this is a decision for Kate, and This Waay's specific deviation should not be imported into Gridmark without one (`RELATIONSHIP.md`).
- Added `scripts/validate-spec.py` — a dependency-free linter that checks a brand's `tokens.json` for internal contradictions and can scan generated output for off-token hex colors.
- Token architectures remain intentionally separate per `RELATIONSHIP.md` — this pass touched only This Waay's token values.

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
