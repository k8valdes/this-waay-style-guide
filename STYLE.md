# This Waay — Style Guide (AI Reference)

> **For AI tools:** This is the canonical brand reference for This Waay. Use it as context when generating any asset — copy, layouts, illustrations, charts, slides, or components. Pair it with `tokens.json` for exact values. This document contains **brand expression only**; it intentionally excludes pricing, positioning, and business strategy.
>
> Version 1.7 · June 2026 · Living document.

This Waay is a product design and AI strategy studio in Sacramento, California. The brand reads as **composed, structural, and quietly confident** — clarity over noise, restraint over decoration.

---

## Color

Navy is the ground; **Waay Green is the action, everywhere, on every surface.**

| Role | Hex | Use |
|---|---|---|
| Navy | `#0C2A48` | Primary dark — hero/section backgrounds, card bodies, plane body on light |
| Navy Deep | `#081F37` | Footer, deepest surfaces |
| **Waay Green** | `#54B987` | **The brand green.** All actions, labels, icons, highlights, accents — any ground |
| Punch Green | `#3DD68C` | Rare, deliberate emphasis — **one moment per asset max.** Never buttons/labels/charts |
| Teal | `#0BABAB` | Heritage — subheads, links, mid-sentence callouts in docs/decks |
| Steel | `#0D698A` | Secondary blue — charts, diagrams, supporting UI |
| Slate | `#8DA3B5` | Muted labels, captions, chart gridlines |
| Gray | `#595959` | Deck system — slide headers and body text on white |
| Coral | `#F2A08D` | **Illustration only** — the glowing path accent. Never UI, charts, or text |
| Mint / Ice | `#EEF8EC` / `#F2FBFB` | Soft gradient stops (135°) |

**Soft gradient:** `linear-gradient(135deg, #EEF8EC 0%, #F2FBFB 100%)` — standard light surface.

**The one-green rule:** `#54B987` is the only green for buttons, labels, icons, and recurring UI. Punch Green appears at most once per asset; if in doubt, don't use it. The green gradient counts as a punch usage.

---

## Typography

**Axiforma** (Kastelov) is the brand typeface — one family across every role, with weight doing the hierarchy work. **Poppins** is the only approved free fallback when Axiforma is unavailable. Stack: `'Axiforma', 'Poppins', 'Segoe UI', sans-serif`.

| Role | Weight | Notes |
|---|---|---|
| H1 | Bold 700 | `clamp(2.05rem, 4.8vw, 3.05rem)`, tracking −0.015em, sentence case |
| H2 | Bold 700 | tracking −0.01em, sentence case |
| Subhead | SemiBold 600 | often in teal in docs/decks |
| Body | Regular 400 | 16px, line-height 1.7, measure 62–66ch |
| Eyebrow | Bold 700 | 0.22em tracking, UPPERCASE, green — the only uppercase element |

**Do:** sentence case headlines; at most one green/teal highlight per headline; short declarative lines; let whitespace pace the page.
**Don't:** all-caps headlines (caps are for eyebrows only); multiple accent colors in one text block; decorative or script faces; a second type family.

---

## Spacing & layout

Everything is built on an **8px base unit** — generous breathing room is what makes a layout feel like This Waay.

- **Scale:** 4 · 8 · 16 · 24 · 32 · 48 · 64 · 96px (card gap 32; section padding clamps 56–110px)
- **Content width:** max 1080px · text measure 62–66ch
- **Radii:** cards/panels 14px · buttons/chips/labels 999px (pill)
- **Card grid:** `repeat(auto-fill, minmax(255px, 1fr))`, 30–34px gap
- **Shadows:** card `0 10px 30px rgba(12,42,72,0.10)` · screenshot `0 12px 30px rgba(12,42,72,0.18)`

**Page archetype:** navy hero → alternating navy and soft-gradient sections joined by shallow (2–4°) angled breaks. Every section opens with the same centered lockup: **eyebrow → H2 → lede.**

---

## Components

- **Buttons:** primary = green pill; ghost-on-navy = green outline pill; light = white pill with card shadow. Sentence case.
- **Category labels:** green pill, SemiBold. (A teal variant survives in legacy decks; use green in new work.)
- **Cards:** 14px radius, soft shadow. The system is consolidating toward three canonical types — **badge card** (centered, navy shield), **content card** (left-aligned, green icon tab), **panel card** (testimonial/pricing/data surfaces). Until consolidation lands, match the nearest existing pattern and prefer soft-gradient grounds with left-aligned text.

---

## Screenshots & product imagery

Product screenshots are **never dropped in raw** — always framed in one of two treatments:

- **A · Light ground** (default for in-flow): soft-gradient or white ground, 8px screenshot corners, one soft navy shadow, true product aspect ratio.
- **B · Navy hero + callouts** (case-study heros, spotlights): navy ground with faint topographic contour lines, screenshot floated with shadow, **green callout pills/boxes** marking the relevant UI region.

**Annotate only in Waay green.** Max 2–3 callouts per shot. Use phone/browser mockup frames for mobile and responsive work. Never: black shadows, mismatched radii, stretched/skewed shots, or non-brand annotation colors.

---

## Data visualization

Charts must look composed, never default-garish.

- **Series order (fixed):** green `#54B987` → steel `#0D698A` → teal `#0BABAB` → navy `#0C2A48`. **Single-series is always Waay green.**
- **Gridlines:** slate at 50%, 0.8px, horizontal where possible.
- **Labels:** Axiforma/Poppins; slate axes, navy emphasis; 8–11px.
- **Bars/lines:** 3px weight, 3px rounded corners/caps.
- **No** 3D, heavy borders, chart-junk, or background fills. Punch Green never appears in charts.

---

## Diagrams & frameworks

Structural clarity is the studio's signature, so diagrams must look unmistakably its own. Three recurring forms:

- **Double-diamond process:** four triangles progressing **slate → navy → steel → green** (Discover · Define · Create · Validate), paired into Problem and Solution diamonds. Color order is fixed — muted uncertainty resolving toward green.
- **Shield principle badge:** navy shield, green ring outline, white icon — the container for a principle or pillar.
- **Numbered step flow:** navy circle numerals on a vertical connector, SemiBold navy titles, slate descriptions.

**Shared rules:** bold navy outlines (~3px), one flat green accent per element, thin navy connectors, generous whitespace. No gradients, no 3D, no decorative fills.

---

## Illustration (canonical style)

The canonical illustration style is **layered paper-cut night landscapes**. Terrain stands in for system complexity; a glowing coral path is the guided route through it.

**Anatomy:** layered paper-cut / low-poly collage, matte paper texture, soft shadows between layers · night setting (deep navy sky `#0C2A48`, faint topographic contour lines, sparse stars, crescent moon) · terrain in sage/mint/teal greens stepping into navy shadow · a glowing coral (`#F2A08D`) path of connected nodes as the focal point · one warm-lit destination structure (lighthouse, cabin, bridge house) · journey-through-complex-terrain metaphors. No people, no text.

**Base style block** (append to every scene prompt):

```
Layered paper-cut illustration, low-poly geometric landscape at night, deep navy sky (#0C2A48) with subtle topographic contour lines and sparse stars, terrain in sage and teal greens, glowing coral path of connected dots and lines (#F2A08D) winding through the scene, one structure with warm amber window light, matte paper texture, soft layered shadows, muted sophisticated enterprise palette, no people, no text
```

**Named scenes:** Bridge = integration/crossing to a future state · Lighthouse = guidance/governance/trust/synthesis · Mountain path = approach/framework, the work before the destination.

**Deprecated:** the older isometric flat-icon style (globe/target/circuit vignettes on floating platforms). Do not generate new assets in this style.

---

## Motifs & iconography

- **Paper plane:** wing is the gradient blade `#62D38C` (nose) → `#30737B` (tail); body navy on light grounds, white on navy. Never outlined, never flat green. Use the official SVG paths, not redrawn geometry. Faded oversized silhouettes (6–10% opacity) texture backgrounds.
- **Dotted flight path:** round dots (`stroke-dasharray: 0.1 8.5`, round caps, ~3px), navy on light / white on navy. **Every trail includes at least one loop** — hand-flown, never straight, never dashed.
- **Icons:** bold navy outlines (~3.5px at a 48px grid) with a single flat green fill element. On navy, outlines invert to white; green fills stay green.
- **Angled section breaks:** sections meet on a shallow 2–4° diagonal, alternating navy and soft-gradient grounds.

---

## Voice & messaging

Composed, observational, structural. This Waay earns authority through **specificity, not volume.**

**Sounds like us:**
- "We didn't add AI. We prepared the system for intelligence."
- "AI doesn't resolve these things. It exposes them."
- Short declarative sentences. Observational cadence. Restraint.

**Never:** hype language ("revolutionary," "game-changing," "supercharge"); trend commentary; "we implement AI features"; exclamation points in professional contexts.

**Recurring themes:** intelligence magnifies structure · AI is a systems decision, not a feature decision · governance builds trust · validation reduces risk · architecture enables scale.

---

## Quick rules for AI assistants

1. Read `tokens.json` for exact values; never approximate brand colors or type from memory.
2. **One green:** `#54B987` for all recurring use; Punch Green `#3DD68C` at most once per asset.
3. Typography is **Axiforma**, Poppins only as fallback; never a second family.
4. Headlines sentence case; one highlight max; eyebrows are the only uppercase.
5. Illustrations start from the **base style block**; never the deprecated isometric style.
6. Charts follow the fixed series order; single-series is green; no chart-junk.
7. Screenshots are always framed; annotate only in green.
8. Coral is illustration-only — never UI, charts, or text.
9. Spacing on the 8px scale; content maxes at 1080px; sections alternate navy/soft on angled breaks.
10. Voice: shorter, calmer, more structural. When in doubt, say less.
