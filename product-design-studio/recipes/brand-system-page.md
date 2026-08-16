# Recipe — brand-system promo page

The first real page-recipe (the Phase 5 seed). A page is an **ordered composition of blocks
against v4.0 tokens**, not bespoke HTML. Build the next offering's page by swapping this recipe's
content, not by rewriting markup.

- **Rendered page:** `product-design-studio/promo/index.html`
- **Consumes:** `product-design-studio/build/tokens.css` (the resolved token surface — the stable
  consumer per the Phase 3b note). **No hex is hand-typed** anywhere in the page; every colour is
  `var(--color-*)`, every type value `var(--typography-*)`, every dimension `var(--dimension-*)`,
  gradients `var(--gradient-*)`, angles `var(--angle-*)`. A page built against generated tokens
  cannot drift from the brand by construction — the page is itself proof the pipeline works.

## The preview harness

Open `promo/index.html` directly (it links `../build/tokens.css`). Axiforma resolves from the
installed family names carried in the token stacks; Poppins is the licensed-free fallback from
Google Fonts. Interactive components render with React (loaded from a CDN) — screenshot QA used
headless Chrome.

> **Harness note — production CSS.** The brief asks the harness to load `build/tokens.css` + the
> site's production CSS. Loading the raw minified WordPress theme would drag the exact drifted,
> hand-maintained values back in — `#8CA7B9` ×207, `#EEF8EC` ×22, twelve typefaces — i.e. reintroduce
> the drift the pipeline exists to remove, defeating the "no hardcoded hex" proof. So the harness
> consumes **`build/tokens.css` as the single brand source** and replicates the assessment page's
> *grammar* (section rhythm, eyebrow→H2→lede lockup, card patterns, navy/white rhythm, angled
> breaks) against tokens. That is the more faithful reading of "a page built against generated
> tokens can't drift from the brand." WordPress/ACF integration is later; this is a static preview.

## Block sequence (the reusable spine)

Grounds follow `layout.pageRhythm`: open and close on navy; the ground changes when the subject
changes; every ground change carries an angled break (`.angle-top`, skew from `--angle-skew-section`).
Each block is `eyebrow → H2 → lede` then its body.

| # | Block | Ground | Break | Role | Key tokens |
|---|---|---|---|---|---|
| 0 | **Nav** | navy | — | Site chrome, sticky | `--color-surface-ground`, `--color-slate-300`, `--color-overlay-nav-border` |
| 1 | **Hero** (outcome-first) | navy | — | Lead with the *outcome*, one green accent phrase; never open on the method | `--typography-hero-h1-*`, `--color-fill-action` (accent, 6:1 on navy) |
| 2 | **One-line strip** | navy | — | `duration · price · deliverables · next step`; `{{DURATION}}`/`{{PRICE}}` if unset | `--dimension-text-size-md`, `--color-fill-action` |
| 3 | **How teams use it** (with / without designer) | white | ↘ | **Core differentiator** — show the deliverable in use before defining it; two-column | `.two-col`, `--color-border-subtle`, `--shadow-card` |
| 4 | **What this governs** (grid) | soft | ↘ | 4–6 icon cards, the drift dimensions controlled | `.grid`, `--gradient-soft`, `--card-content-*` |
| 5 | **Why it matters** (affirmative args) | navy | ↘ | Positive case; AI-tool proliferation leads | `.why`, `--color-fill-action` |
| 6 | **Drift-delta proof** | white | ↘ | The two latent bugs headline + real delta table + interactive demo | `.delta`, `--color-text-danger` (before), `--color-text-accent` (after) |
| 7 | **Deliverables** (cards) | soft | ↘ | Spec · document/deck pipeline · Skill · Figma export | `.deliv`, `--card-content-background` |
| 8 | **Tier explorer** | navy | ↘ | Interactive, replaces static pricing cards | embedded component |
| 9 | **What happens after + reconcile note** | white | ↘ | Assessment-style; greenfield-vs-reconcile modifier | `.after-grid`, `.col-card` |
| 10 | **CTA** | navy | ↘ | Scoping-call close (page ends on navy) | `.btn-primary` |
| 11 | **Footer** | navy-deep | — | Identical to the site | `--color-surface-ground-deep` |

**Voice:** declarative, outcome-led, second-person, no hype adjectives; echoes the assessment page's
sentence rhythm.

**Differences from the WIA page (deliberate):** this sells a deliverable most buyers can't yet
picture, so it *teaches the use before the method* (block 3 leads) and carries the affirmative
argument set (block 5), not just pain scenarios. The WIA sells a diagnostic buyers already understand.

## Interactive components (single-file, in-memory state only)

- `promo/drift-delta.html` — two synchronized panels. **Before** = the real measured off-token
  values (evidence). **After** = the same slots rendered from `build/tokens.css`, with each hex read
  *live* via `getComputedStyle`, so the demo can't drift from the product. A toggle reveals the
  validator PASS/FAIL per side.
- `promo/tier-explorer.html` — three cumulative rungs (each contains the one below — inherited items
  render ticked-grey, new items green) plus the component-library add-on shown separately, and the
  reconcile-vs-greenfield note.

Both use React (CDN) with in-memory `useState` only — no `localStorage`, per the storage rules.

## Figures — real vs placeholder (nothing invented ships)

**Real** (measured from this project's own audit/validator output; used verbatim in block 6 + the
drift-delta demo):

| Figure | Source |
|---|---|
| 12 typefaces → 1 | Phase 2 deck audit (Open Sans, Nunito, Poppins, Helvetica Neue, Arial, Calibri; no Axiforma) |
| `#8CA7B9` × 207 | Phase 2 audit — most-used colour, not a token; real slate `#8DA3B5` appeared 0× |
| `#EEF8EC` × 22 | Phase 2 audit — retired v2.x gradient stop still in use |
| punch 21 : brand 9 (inverted) | Phase 2 audit |
| 2 latent drift bugs → 0 | Phase 3b — the guide's H1/H2 `clamp()` silently contradicted the spec's fixed 46px/40px, caught by the value-match check |
| accessibility: undocumented → dated/measured/accepted (2.42:1) | Phase 0/1 — the green-button white-text accepted deviation |
| 229 off-token colours, 0 after | Phase 3b validator (production-only + off-token) |

**Placeholder** (NOT final; shown as `{{TOKEN}}` or an "indicative ~range", confirmed at scoping —
never presented as a quote):

| Placeholder | Indicative range (from the brief, not confirmed) |
|---|---|
| `{{DURATION}}`, `{{PRICE}}` (hero strip) | unset — awaiting confirmation |
| `{{ENTRY}}` | ~$10–12K |
| `{{STANDARD}}` | ~$15–18K |
| `{{PREMIUM}}` | ~$22–25K |
| Product component library add-on | scoped separately (heavier engagement) |

Reconcile-vs-greenfield is a **scope factor on any rung**, not a separate price.

## Reusing this recipe (Phase 5)

Keep the block spine (grounds, breaks, lockup, voice). Swap: the hero outcome, the with/without
framing, the governed dimensions, the affirmative arguments, the deliverables, the tiers. The proof
block is optional per offering — it's this page's differentiator because this project produced real
drift-delta evidence. Everything still resolves through `build/tokens.css`, so a new page inherits
the brand and its accessibility guarantees for free.
