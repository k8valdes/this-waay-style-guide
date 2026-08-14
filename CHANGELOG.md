# Unified System Changelog

This tracks version milestones for the unified `Branding/` home itself — not each brand's own internal changelog. See `product-design-studio/index.html` (footer living-document note) and `gridmark-partners/gridmark-design-system-v3.html` (Governance & versioning) for brand-level changelogs.

## Unified v1.5 — 2026-08-14 — Phase 3b resolver & build pipeline

Built the tooling that *consumes* the v4.0 tiered spec: one resolver that flattens the tiers, five emitters that are pure functions of it, and a production-only validator — so every generated format reads one resolved source and cannot disagree. Merged together with Phase 3a (v4.0 goes live in the same step; no half-migrated window).

- `scripts/resolve_tokens.py` — follows `{group.token}` aliases (component → semantic → primitive) to literals, detects cycles/dangling, resolves colours to the object form, typography composites (fontFamily stack + fontWeight, never synthesizing bold), and gradients to stops + resolved angle. The **production-only filter** exposes only `status:production` tokens to emitters (148 of 174); the 15 deprecated/proposed ledger items are readable but structurally un-generatable. Namespace read from `meta.extensionsNamespace`, never hardcoded.
- Five emitters, each a pure function of the resolved set: `emit_css.py` (CSS custom properties — replaces the hand-mirrored `:root`), `emit_pptx.py` (the deck theme, now driving Phase 2's `build_deck.py`), `emit_docx.py` (the reference-doc theme + named-style colours), `emit_figma.py` (variables JSON in 3 tier collections), `emit_dtcg.py` (flat resolved DTCG 2025.10 export). `build_theme.py` is now a deprecation shim re-pointed at `emit_pptx`.
- `scripts/validate.py` — unified resolver-aware validator: **production-only** (no ledger item in any artifact — proven non-vacuous: 15/15 caught if leaked, 0 in production), off-token colour, rules-as-structure re-run on the resolved *output*, stock-Office/fake-bold in the emitted theme. `validate-spec.py`'s typo logic made tiered-aware so the Phase 2 template checks pass on v4.0 (deck 4/4, docx 3/3).
- Regenerated every downstream artifact from the resolver: `build/tokens.css`, `build/figma-variables.json`, `build/tokens.flat.dtcg.json`, the deck `.potx`, the reference `.docx`, and the style guide's `:root` (generated + a value-matched legacy `--tw-*` alias shim — no hand-mirror). The guide's Token-architecture section now describes the tiered structure; the 3a superseded marker is removed; guide → v4.0. Re-render QA (QuickLook + installed Axiforma): no regression.
- `scripts/verify-phase3b.py` — 6-check gate (resolver / determinism / production-only / round-trip / no-regression / guide-non-contradiction). **All 6 pass.**
- Value-match proof: 63/73 old `:root` values reproduce verbatim; the 10 that don't are 5 deliberate 3a relocations (measure, wing, retired section-pad clamp), 3 formatting-only differences, and 2 latent drifts the automation *exposed* (the guide's hero `clamp()` sizes contradicted the spec's fixed px).

## Unified v1.4 — 2026-08-13 — Phase 3a tiered-schema migration (branch: schema-migration)

Migrated `product-design-studio/tokens.json` from the flat v3.1 shape to the three-tier
DTCG-2025.10 structure defined in `brand-schema.md` (primitive → semantic → component). Structural
migration only — every shipped value survives unchanged; only primitive step *names* were re-seated
from measured CIE L\*. On the `schema-migration` branch; `main` stays v3.1 (the served spec) until merge.

- **tokens.json → v4.0.** `$schema` = the DTCG 2025.10 URL; colors are object-form (`colorSpace`/`components`/`hex`, components derived from hex); dimensions are `{value, unit}`; references are `{group.token}` aliases. `meta.extensionsNamespace: "x.brandkit"` single-sources the provisional namespace (Decision 1 — rename target).
- **Primitives re-seated by measured L\*** (Decision 2 — the schema doc's step numbers were eyeballed and were not reused): green fill `.500→.400`, green ink `.700→.600`, teal `.500→.400`/`.700→.600`, punch/coral `→.300`, red fill `→.500`, gray `→.700`; navy/steel/slate unchanged. Every step carries its computed L\* rationale in `$extensions`.
- **The anti-drift rules are now structure, not prose:** no `text.*` role can reach a fill primitive (text.accent → green.600 ink, never the green.400 fill); no `surface.*` role can reach a gradient stop; the fake-bold pairing is unrepresentable (boldFlag→fontWeight, 700 only on the real-bold `Axiforma` base). The standard semantic vocabulary (Decision 3, lean+4) and the four new proposed roles are wired.
- **Component tier full, with a governed status ledger** (Decision 5): survivors `production`, retiring card/gradient variants `deprecated` + `supersededBy` from the first commit (the anti-`#8CA7B9` rule), genuinely-undecided mappings `proposed`. The accepted deviation lives on `button.primary.label` with all five fields.
- **Non-token content relocated to `product-design-studio/references/`** (`layout-mechanics.md`, `components.md`, `illustration.md`, `voice.md`, `assets-inventory.md`, `README.md`) — engineering rules, component anatomy, motifs, and the motif-only wing/segment colours that were never UI tokens.
- Added `scripts/verify-schema.py` — an 11-check pass/fail gate (structure, the rules-as-structure invariants, governance, preservation). **All 11 pass.** A value-preservation audit confirms every v3.1 hex/dimension survives across `tokens.json` + `references/`.
- The HTML guide's "Token architecture" section is marked **superseded** (it described the retired flat model); values on the page are unchanged. Full regeneration is Phase 3b's resolver, not a hand-remirror.

## Unified v1.3 — 2026-08-13 — Phase 2 structured templates & themes

Turned `product-design-studio/tokens.json` into two deterministic Office artifacts so generated decks and documents inherit the brand instead of re-deriving it from prose. Consumes the spec; does not author it (no `tokens.json` change this pass).

- Added `assets/templates/this-waay-deck.potx` — a real `.potx` template with a brand OOXML theme (clrScheme/fontScheme generated from tokens) and exactly six named layouts (Title / Cover, Section Divider, Content / Bullet, Quote, Chart / Data, Closing). 16:9, ≥5% safe areas, white/navy grounds only, ≥14pt text, slide numbers on all but Title/Closing, a notes master, and no transitions. `accent1–4` are `dataViz.seriesOrder` in order, so native charts inherit the brand series sequence with zero config. Deck Gray `#595959` headers, Axiforma SemiBold/ExtraBold set explicitly on placeholders (theme major/minor = `Axiforma`; `b=1` never applied to a no-bold cut).
- Added `assets/templates/this-waay-reference.docx` — the branded letterhead transformed: named styles (Title/Subtitle/Heading1–6/Normal/Hyperlink) redefined against tokens (teal is the document accent), a real brand theme written over the Office-2007 defaults (was Calibri/Cambria, accent1 #4F81BD), specimen body text stripped, off-brand `#374151`/`#1155CC` replaced, header/footer + logo relationship preserved. All embedded font binaries stripped — the doc references Axiforma by name only.
- Added `scripts/build_theme.py`, `scripts/build_deck.py`, `scripts/build_reference_docx.py` (theme is stdlib-only; the deck/docx builders are stdlib zip authoring). No font binary is embedded in either package — Axiforma is `fsType 4`, and the local `axiforma/` OTF folder is now git-ignored so no `git add -A` can ever commit a font.
- Extended `scripts/validate-spec.py` with a `--template` mode: (1) no stock Office theme values, (2) every package hex resolves to a token (000000 shadow allowed), (3) approved font families only + no fake-bold on a no-bold cut, (4) deck rules (no transition/auto-advance, ≥14pt, white/navy grounds). Both templates pass; a negative test confirms it catches injected `#8CA7B9`/stock-Office/fake-bold/transition/sub-14pt defects. Render QA via macOS QuickLook (installed Axiforma) confirmed Deck Gray headers read grey (not navy) and Axiforma resolves rather than falling back.

## Unified v1.2b — 2026-08-13 — Phase 0 verification gate + string cleanup

Follow-up to v1.2. The v1.2 reconciliation landed in substance, but left the exact literal
strings a checker (human or AI) would grep to confirm the fix — so the served file still *read*
as unfixed even though it was v3.1: the phrase `"Navy text, never white"` remained (in the still-
correct teal rule and in an audit-trail quote of the old rule), and the word `borderline` remained
inside `color.green`. This pass removes those literal strings without losing any meaning, and adds
a hard verification gate so this class of "reported done but not checkable" cannot recur.

- `accessibility.textOnGreenOrTealFill` restructured into `tealFill` / `greenFill` / `supersededRule`
  — the literal `"Navy text, never white"` is gone; the green case now states white-on-green,
  the measured `2.42:1` vs `4.5:1`, the accepted-deviation date, and the `#36845D` remediation
  lever directly in the accessibility block; the teal case is unchanged.
- `color.green.textOnGreenFill`: removed the word `borderline` (both the "not borderline"
  assertion and the quoted old claim) — reworded to say the same thing without the trigger word.
- Added `scripts/verify-phase0.py` — a stdlib-only pass/fail gate asserting all eight Phase 0
  invariants against `product-design-studio/tokens.json` (version 3.1, contradiction strings
  absent, white-on-green @ 2.42 present, weightEquivalents production, every family has a
  `familyName`, valid JSON round-trip). Exits 0 only on all-pass; wire as the last step of any
  future spec change. `meta.updated` bumped to 2026-08-13.

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
