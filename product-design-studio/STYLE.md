# This Waay — Style Guide (AI Reference)

> **For AI tools:** This is the canonical brand reference for This Waay. Use it as context when generating any asset — copy, layouts, illustrations, charts, slides, or components. Pair it with `tokens.json` for exact values. This document contains **brand expression only**; it intentionally excludes pricing, positioning, and business strategy.
>
> Version 2.3 · July 2026 · Living document.

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

**Accessible "ink" variants — use these for TEXT on light grounds:**

| Role | Hex | Contrast on white | Use |
|---|---|---|---|
| Green — Ink | `#2C6D4D` | 6.2:1 | Eyebrows, links, inline emphasis on light grounds — raw Green is 2.4:1 here, fails AA |
| Teal — Ink | `#077373` | 5.7:1 | Subheads, links, callouts on light grounds — raw Teal is 2.8:1, fails AA |
| Ink — Muted | `#5C7185` | 5.1:1 | Captions, secondary labels — raw Slate is 2.6:1, fails AA |
| No — Ink | `#A53727` | 6.6:1 | "Don't" tags, form error text — raw `#D86A5A` is 3.4:1, fails AA |

The saturated originals (`Green`, `Teal`, `Slate`, `#D86A5A`) remain correct for **fills, large surfaces, and text on dark grounds** — they were never broken there. They only fail as small/normal text on white or soft-gradient backgrounds. On a green fill, use **navy** text, not white (white-on-green is 2.4:1; navy-on-green is 6:1) — see Accessibility.

---

## Typography

**Axiforma** (Kastelov) is the brand typeface — one family across every role, with weight doing the hierarchy work. **Poppins** is the only approved free fallback when Axiforma is unavailable. Stack: `'Axiforma', 'Poppins', 'Segoe UI', sans-serif`.

| Role | Weight | Notes |
|---|---|---|
| H1 | Bold 700 | `clamp(2.05rem, 4.8vw, 3.05rem)`, tracking −0.015em, sentence case |
| H2 | Bold 700 | tracking −0.01em, sentence case |
| Subhead | SemiBold 600 | often in teal-ink in docs/decks |
| Body | Regular 400 | 16px, line-height 1.7, measure 62–66ch |
| Eyebrow | Bold 700 | 0.22em tracking, UPPERCASE, green-ink on light / green on dark — the only uppercase element |

**Everything is token-based.** Every `font-size`/`font-weight`/`letter-spacing`/`line-height` in the system resolves to a named CSS custom property — see `tokens.json`'s `typography` block for exact values. Four scales:

- **Weight:** `regular` 400 · `medium` 500 · `semibold` 600 · `bold` 700 — weight alone carries hierarchy, never a second type family.
- **Size — 10 fixed steps** (`2xs` 0.62rem → `5xl` 2.6rem), plus dedicated `h1`/`h2` (fluid clamps), `body` (16px), and `lede` (1.08rem) sizes that sit outside the scale. This consolidates what had drifted into ~36 unrelated one-off sizes — everything now points at one shared step.
- **Letter-spacing — 11 steps** from `tightest` (−0.015em, H1) to `widestLg` (0.3em, nav wordmark tagline), with `widest` (0.22em) reserved for eyebrows.
- **Line-height — 8 steps** from `glyph` (0.6, oversized quote-mark glyphs only) to `loose` (1.7, body copy).

**Do:** sentence case headlines; at most one green-ink/teal-ink highlight per headline; short declarative lines; let whitespace pace the page; pull every size/weight/tracking/leading value from the scale, never a new one-off number.
**Don't:** all-caps headlines (caps are for eyebrows only); multiple accent colors in one text block; decorative or script faces; a second type family; a hand-picked font-size that isn't one of the scale steps.

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

## Accessibility

**WCAG 2.2 AA is the baseline for every This Waay and client deliverable** — not a follow-up pass.

- **Contrast:** use the ink tokens above for text on light grounds; on a green or teal fill, text is **navy**, not white. Never distinguish meaning by color alone (links, chart series, form errors, "don't" tags all need a second cue — weight, icon, pattern, or text).
- **Focus:** every interactive element needs a visible `:focus-visible` ring — never rely on the browser default, and never remove it without replacing it.
- **Structure:** one `<main>`, one `<h1>`, sequential `<h2>`s, a skip-to-content link as the first focusable element.
- **Keyboard & custom widgets:** every clickable thing is a real `<button>`/`<a>`, or has `role` + `tabindex="0"` + a keydown handler. Async state changes (copied, saved, submitted) announce via `aria-live`, not a visual-only change.
- **Images & icons:** decorative SVGs get `aria-hidden="true"`; meaningful ones (the logo, a narrative illustration used as a hero) get `role="img"` + real `aria-label`/`alt` describing the *meaning*, not the literal scene.
- **Forms:** every field has a visible, associated `<label>`; required fields are marked with text, not an asterisk-only color cue; errors use `aria-describedby` + `role="alert"`.
- **Data viz:** never color-only — pair series color with a line style, marker shape, or direct label.

---

## Motion

Motion should feel like the flight path — **purposeful and directional, never decorative-for-its-own-sake.**

- **Duration scale:** micro 120–160ms ease-out (hover/focus feedback) · element 200–300ms ease-out (card lift, menu open/close, tabs) · reveal 400–600ms ease-out (one-directional scroll reveals, the flight-path draw-on). Nothing slower without a specific reason. No bounce/spring/elastic easing.
- **Signature moment:** the flight-path draw-on — a one-time `stroke-dashoffset` reveal (~2.4s ease-out) for hero/section entrances, never looping.
- **May animate:** hover/focus micro-feedback, one-directional scroll reveals, the flight-path draw-on, loading indicators (with a text alternative).
- **Must never:** parallax layers at conflicting speeds; autoplaying/looping motion with no pause control; anything flashing >3×/second; motion as the *only* carrier of meaning.
- **Reduced motion is a per-component contract**, not just a global reset: every new animated component defines its own `prefers-reduced-motion` fallback next to the animation itself.
- **Slide decks:** fade or cut transitions only, no per-slide novelty transitions, always presenter-controlled — never auto-advance.

---

## Components

- **Navigation:** sticky bar on navy, `1px solid rgba(255,255,255,0.08)` bottom border. **Two-row layout:** logo/wordmark sits on its own line; a second row holds section-group buttons, each disclosing its subsections as a dropdown (**Architecture** · Token architecture, **Foundations** · Color/Type/Spacing/Motion/Accessibility, **Brand** · Motifs/Illustration, **System** · Components, **Application** · Screenshots/Data viz/Diagrams/Slide decks, **Language** · Voice, **Operations** · AI usage). Group buttons are real `<button>`s with `aria-expanded`/`aria-controls`, click/keyboard-triggered — never hover-only — with only one group open at a time, and Escape/outside-click/focus-out closing it. Links are Axiforma SemiBold 600, 0.85rem, `#B9CBDC` default, Waay Green on hover. A collapsed/mobile state uses the same real-`<button>` disclosure pattern — never a bare icon with no accessible name.
- **Buttons:** primary = green pill, **navy text** (not white — see Accessibility); ghost-on-navy = green outline pill; light = white pill with card shadow, teal-ink text. Sentence case.
- **Category labels:** green pill, navy text, SemiBold. (A teal variant survives in legacy decks — also navy text; use green in new work.)
- **Cards:** 14px radius, soft shadow. The system is consolidating toward three canonical types — **badge card** (centered, navy shield), **content card** (left-aligned, green icon tab), **panel card** (testimonial/pricing/data surfaces). Until consolidation lands, match the nearest existing pattern and prefer soft-gradient grounds with left-aligned text.
- **Forms:** labeled inputs/textarea/select, native checkbox/radio (`accent-color: var(--tw-green)` — don't hand-roll custom controls), inline error state with `role="alert"`.
- **FAQ/accordion:** native `<details>/<summary>` — accessible by default, no ARIA to hand-roll.
- **Tabs:** WAI-ARIA APG pattern — roving tabindex, arrow-key navigation, automatic activation.
- **Modal/dialog:** native `<dialog>.showModal()` — built-in focus trap and Esc-to-close; return focus to the trigger on close.
- **Alerts/banners:** info/success/warning, each with an icon + copy carrying the meaning — never background color alone.
- **Also documented:** breadcrumb, pagination, tooltip (shown on hover *and* focus), logo cloud, stats row, blog/article card, expanded multi-column footer with social links and newsletter signup.

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
- **Dotted flight path:** round dots (`stroke-dasharray: 0.1 8`, round caps, ~3px), navy on light / white on navy. **Every trail includes at least one loop** — hand-flown, never straight, never dashed. Five canonical variants are defined: **A — Single loop**, **B — S-wave**, **C — Tight coil**, **D — Wide arc**, **E — Double curl**. New trail shapes should follow the same hand-flown character; reference these before drawing something new.
- **Icons:** bold navy outlines (~3.5px at a 48px grid) with a single flat green fill element. On navy, outlines invert to white; green fills stay green.
- **Angled section breaks:** sections meet on a shallow 2–4° diagonal, alternating navy and soft-gradient grounds.

---

## Slide decks

Six templates cover most decks: **title/cover, section divider, content/bullet, quote, chart/data, closing.** Same system as the rest of the brand — gray deck headers, teal-ink subheads, green category labels, Axiforma throughout — adapted for a projected 16:9 surface.

- **Aspect ratio:** 16:9, text inset ≥5% from every edge for projector/crop tolerance.
- **Slide numbering:** bottom-right; omit on title and closing slides.
- **Presenter notes:** live below the slide, never on it.
- **Minimum text size:** ~18px equivalent at 1080p — larger than web body minimums for projected/shared-screen legibility.
- **Contrast and motion rules carry over unchanged** from Accessibility and Motion — transitions are fade/cut only, presenter-controlled, never auto-advance.
- Any embedded chart/diagram still needs its data conveyed in words somewhere (a takeaway line, a table, presenter notes) for PDF/read-aloud contexts.

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
2. **One green:** `#54B987` for all recurring use; Punch Green `#3DD68C` at most once per asset. On a green or teal fill, text is **navy** — never white.
3. **Text on light grounds uses the ink tokens** (`greenInk`, `tealInk`, `inkMuted`, `noInk`), not the raw saturated hues — the raw hues fail WCAG AA as text on white/soft-gradient backgrounds.
4. Typography is **Axiforma**, Poppins only as fallback; never a second family.
5. Headlines sentence case; one highlight max; eyebrows are the only uppercase.
6. Illustrations start from the **base style block**; never the deprecated isometric style. Alt text describes the metaphor, not the literal scene.
7. Charts follow the fixed series order; single-series is green; no chart-junk; never distinguish series by color alone — pair with line style, marker shape, or a direct label.
8. Screenshots are always framed; annotate only in green.
9. Coral is illustration-only — never UI, charts, or text.
10. Spacing on the 8px scale; content maxes at 1080px; sections alternate navy/soft on angled breaks.
11. Every interactive element gets a visible focus state and real keyboard operability — no clickable `<div>`s, no color-only signaling, no auto-advancing/looping motion without a pause control.
12. Motion is purposeful and directional (120–600ms, ease-out); every animated component ships its own `prefers-reduced-motion` fallback.
13. Every font-size/weight/letter-spacing/line-height is a token from the scale in `tokens.json` — never a new one-off number.
14. Voice: shorter, calmer, more structural. When in doubt, say less.
