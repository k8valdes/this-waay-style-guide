# This Waay — Style Guide (AI Reference)

> **For AI tools:** This is the canonical brand reference for This Waay. Use it as context when generating any asset — copy, layouts, illustrations, charts, slides, or components. Pair it with `tokens.json` for exact values. This document contains **brand expression only**; it intentionally excludes pricing, positioning, and business strategy.
>
> Version 3.0 · August 2026 · Living document.

> ### ⚠️ Read this before building anything
>
> **The production marketing site is the source of truth.** Values here were *extracted from* the shipped CSS (`theme.min.css` + Bootstrap 5.0.2), not designed in the abstract. The full extraction record is [`INVENTORY.md`](INVENTORY.md).
>
> This guide contains **two kinds of statement**, and confusing them is what causes drift:
>
> | | What it is | Authority |
> |---|---|---|
> | **Production** | What the brand *is* — color, type, layout, components | The site wins. If this doc disagrees with the site, **this doc is wrong.** |
> | **Proposed** ⬦ | What the brand *should do* — accessibility, motion, consolidation targets | A deliberate target the site does **not yet meet.** Never assume it describes current behavior. |
>
> Anything marked ⬦ is aspirational. Everything else matches what ships today.
>
> **v3.0 corrected real drift.** v2.x specified card radius 14px (actually **8px**), content width 1080px (actually **1140px**, Bootstrap), pill radius 999px (actually **25px**), body 16px/1.7 (actually **15px**), and a 2-stop soft gradient (actually **3 stops, ending warm**). Pages built from v2.x drifted *by construction* — which is what happened to the AI Practice page.

This Waay is a product design and AI strategy studio in Sacramento, California. The brand reads as **composed, structural, and quietly confident** — clarity over noise, restraint over decoration.

---

## Color

Navy is the ground; **Waay Green is the action, everywhere, on every surface.**

### Primary

| Role | Hex | Use |
|---|---|---|
| Navy | `#0C2A48` | The ground state — hero/section backgrounds, card bodies, body text, plane body on light. **The lighter of the two navies** |
| Deep Navy | `#05203A` | The deepest surface — footer, lowest layer. Sits *beneath* Navy, never beside it as a peer *(v3 fix — was `#081F37`)* |
| **White** | `#FFFFFF` | **A primary ground, not an absence.** The page alternates navy and white — white carries half the page rhythm *(v3 — promoted to primary)* |
| **Waay Green** | `#54B987` | **The brand green.** All actions, labels, icons, highlights, accents — any ground |
| Punch Green | `#3DD68C` | Rare, deliberate emphasis — **one moment per asset max.** Never buttons/labels/charts |

### Secondary

Support charts, documents, and illustration. **They never lead.**

| Role | Hex | Use |
|---|---|---|
| Teal | `#0BABAB` | Heritage accent — subheads, links, mid-sentence callouts in documents. Not a site UI color *(v3 — moved from primary)* |
| Steel | `#0D698A` | Charts, diagrams, supporting UI |
| Slate | `#8DA3B5` | Muted labels, captions, borders, chart gridlines |
| Coral | `#F2A08D` | **Illustration only** — the glowing path accent. Never UI, charts, or text |

**Moved out:** `#595959` (Deck Gray) is **decks-only** and no longer part of the site palette — see [Slide decks](#slide-decks).

### Surfaces
| Mint | `#E8FEFB` | Soft gradient stop A (0%) *(v3 fix — was `#EEF8EC`)* |
| Ice | `#F2FBFB` | Soft gradient stop B (55%) |
| **Sand** | `#FDF5E8` | Soft gradient stop C (100%) — **the warm stop** *(v3 addition)* |
| Muted-on-light | `rgba(12,42,72,.65)` | Body/secondary copy on light grounds — navy at 65%, **not a grey** *(v3 addition)* |

**Soft gradient (canonical):**
```css
linear-gradient(135deg, #E8FEFB 0%, #F2FBFB 55%, #FDF5E8 100%)
```

**This gradient ends warm, and that matters more than any other single value in this document.** v2.x modelled it as a two-stop cool gradient (mint → ice). The real ground travels from cool aqua to warm sand, which is what makes This Waay surfaces read as *paper* rather than *glass*. Reproducing a card without the warm stop is the most common reason a rebuild looks "close but not right."

**Soft gradient — warm variant** (behind the why-us float-panel cards; warm at both ends):
```css
linear-gradient(135deg, #F5F7EC 0%, #EAFDFA 20%, #F2FBFB 80%, #F8F7F0 100%)
```

⬦ *Production contains ~5 near-identical soft-gradient recipes (the testimonial panel puts its midpoint at 66%). These two are the proposed canonical survivors — until that consolidation ships, match the section you're extending rather than assuming the canonical one.*

**The one-green rule:** `#54B987` is the only green for buttons, labels, icons, and recurring UI. Punch Green appears at most once per asset; if in doubt, don't use it. The green gradient counts as a punch usage.

### ⬦ Accessible "ink" variants — PROPOSED, not shipped

**These do not exist in production.** The site uses raw `#54B987` for eyebrows on light grounds today. They are the agreed accessibility target for *new* work; applying them to an existing page is a deliberate change, not a correction.

| Role | Hex | Contrast on white | Use |
|---|---|---|---|
| Green — Ink | `#2C6D4D` | 6.2:1 | Eyebrows, links, inline emphasis on light grounds — raw Green is 2.4:1 here, fails AA |
| Teal — Ink | `#077373` | 5.7:1 | Subheads, links, callouts on light grounds — raw Teal is 2.8:1, fails AA |
| Ink — Muted | `#5C7185` | 5.1:1 | Captions, secondary labels — raw Slate is 2.6:1, fails AA |
| No — Ink | `#A53727` | 6.6:1 | "Don't" tags, form error text — raw `#D86A5A` is 3.4:1, fails AA |

The saturated originals (`Green`, `Teal`, `Slate`, `#D86A5A`) remain correct for **fills, large surfaces, and text on dark grounds** — they were never broken there. They only fail as small/normal text on white or soft-gradient backgrounds.

> **✔ Decided (Aug 2026) — green buttons carry WHITE text.** The primary button is a green fill with white text, matching production. This closes the previously-open white-vs-navy question; new work uses white.
>
> *Accessibility footnote:* white-on-green measures ~2.4:1, below the AA 4.5:1 minimum for normal text (it clears the 3:1 large-text threshold, so at the shipped 16px Bold it is borderline). If a future audit requires AA on this element, the lever is **darkening the green behind white text** — not reverting to navy, which would undo the decision.

**Known typo in production:** `#54b886` appears in some shipped rules (buttons, explore links) — a one-digit slip from `#54B987`. Never propagate it.

---

## Typography

**Axiforma** (Kastelov) is the brand typeface. **Poppins** is the only approved free fallback.

> **⚠️ Production does not use `font-weight`.** Each cut is a **separately-named, self-hosted family** declared at `font-weight: normal`, and hierarchy is selected by family *name*. v2.x described this as "one family, weight does the hierarchy work" — that is not what ships, and building against it silently renders the wrong cut (setting `font-weight:700` on a family with no bold gets you a synthesized fake bold).

| Family | Role in production | ≈Weight |
|---|---|---|
| `AxiformaRegular` | Body copy, hero body, captions, footer links | 400 |
| `AxiformaMedium` | Card body, form labels, muted secondary text | 500 |
| `AxiformaSemiBold` | **Hero H1** — the one place SemiBold leads | 600 |
| `AxiformaBold` | Buttons, eyebrows, work-card meta | 700 |
| **`AxiformaExtraBold`** | **H2 and every card title** — the dominant heading cut | 800 |

`AxiformaExtraBold` was absent from v2.x entirely, despite carrying nearly all heading weight on the site. The ≈Weight column exists **only** to translate into environments that demand numbers (Figma variable modes, PPTX export) — never as a substitute for naming the family in web work.

**Production sizes are fixed pixels, not fluid clamps.** v2.x specified `clamp()` ranges that matched the site at no viewport.

| Role | Size | Family | Notes |
|---|---|---|---|
| Hero H1 | 46px / 60px | SemiBold | **Green**, sentence case (home). Assessment ships a white H1 |
| H2 | 40px | ExtraBold | Section headings — navy on light, white on navy |
| H3 | 32px | ExtraBold | |
| H4 / H5 | 20px | ExtraBold | **Every card title.** Why-us float cards drop to 18px |
| Body | 15px | Regular | `line-height: normal` |
| Card body | 14px | Medium | at `rgba(12,42,72,.65)`. Approach cards ship 16px |
| Button | 16px / 24px | Bold | |
| Eyebrow | 12px | Bold | tracking **2.76px** (≈0.23em), UPPERCASE, green — the only uppercase element |

⬦ *Eyebrow tracking is inconsistent in production — Assessment and AI Practice ship 1.5px/1.6px against the theme's 2.76px. 2.76px is the proposed canonical.*
⬦ *Body leading: production's `normal` (~1.2) is tight for sustained reading. **1.6** is proposed for new long-form work — it will not match existing pages.*

**Two type systems exist — don't mix them.**

- **The marketing site** (production, the table above): named Axiforma families at fixed pixel sizes. Use this for anything that must sit alongside the live site.
- **This style guide's own page** (`index.html`): a consolidated 10-step size scale (`2xs` 0.62rem → `5xl` 2.6rem), 11 tracking steps, and 8 leading steps, all as `--tw-*` custom properties. Built to tame ~36 one-off sizes *within the guide*, it was never the marketing site's system.

⬦ *Unifying the two is a proposed future step, not a current fact. Until then: building a page for thiswaay.com → use the production table. Extending the style guide → use its scale.*

### Measure — cap every line of running text

Long lines are the most common readability failure on wide screens, and the easiest to prevent. **Every block of running text gets a measure.**

| Token | Value | Use |
|---|---|---|
| `--tw-measure` | **68ch** | Body copy — the default for running text |
| `--tw-measure-tight` | 46ch | Lede, intro, card copy — shorter and denser |
| `--tw-measure-head` | 22ch | Display headlines (H1, large H2) |

Headings get a *much* shorter measure than body copy on purpose: it forces them to break on meaning rather than at the container edge, which is what prevents stranded words in display type.

**Exception: hero-scale H1s don't take `--tw-measure-head`.** That token is tuned for in-page H2s at 40px; a 46px+ hero headline is wider per character, so the same 22ch collapses it to three lines instead of two. Let a hero H1 size to its actual column (with `balance` still on) and **verify the rendered line count** rather than assuming a token value carries over — a hero headline is display copy specific to that page, not a value to standardize.

### Rag — no widows, orphans, or ladders

| Rule | Applies to | Why |
|---|---|---|
| `text-wrap: balance` | headings, card titles, ledes | Evens line lengths on short blocks so the last line is never one stranded word |
| `text-wrap: pretty` | paragraphs, list items, long quotes | Fixes the last-line widow without restructuring the whole block |
| `hyphens: none` | all headings | Display type never hyphenates |

**`balance` is wrong in a narrow column.** In a card at `col-lg-3`, balancing shortens *every* line and the rag goes stubby. Long text in a narrow measure wants `pretty`. Rule of thumb: **balance short text in wide containers, pretty long text in narrow ones.**

**Do:** sentence case headlines; at most one green-ink/teal-ink highlight per headline; short declarative lines; let whitespace pace the page; pull every size/weight/tracking/leading value from the scale, never a new one-off number.
**Don't:** all-caps headlines (caps are for eyebrows only); multiple accent colors in one text block; decorative or script faces; a second type family; a hand-picked font-size that isn't one of the scale steps.

---

## Spacing & layout

> ### ⚠️ The layout engine is Bootstrap 5.0.2 — do not re-author it
>
> The site's responsive behavior, whitespace, and component sizing all come from Bootstrap's grid. **Use `container` / `row` / `col-lg-*`.** This Waay components live *inside* those columns and never set their own width, breakpoints, or gutters.
>
> Hand-rolling a CSS grid to replace this is the fastest way to lose the site's proportions — a rebuild that copied every component value correctly but substituted its own grid still read as visibly wrong, because whitespace *is* the design.
>
> | Breakpoint | sm | md | lg | xl | xxl |
> |---|---|---|---|---|---|
> | Min-width | 576px | 768px | 992px | 1200px | 1400px |
> | Container | 540px | 720px | 960px | **1140px** | 1320px |
>
> Three-up card sections are `.row` + three `.col-lg-4` — they collapse to full width at **992px**, not a custom breakpoint.

- **Radii:** cards/panels **8px** · buttons **25px** · form inputs **2px** *(v3 fix — was 14px / 999px)*
  - `14px` is real but belongs **only** to the on-navy track card. ⬦ AI Practice's 16/20px is drift and should collapse to 8px.
- **Card gap:** 30px — Bootstrap's default gutter, inherited rather than set
- **Section padding:** varies per section (60–170px vertical). There is **no single token** in production; each section ships its own. ⬦ Proposed canonical for new sections: `clamp(60px, 8vw, 130px)`
- **Shadows:** card `0 10px 30px rgba(12,42,72,0.10)` · screenshot `0 12px 30px rgba(12,42,72,0.18)`
- **Spacing rhythm:** 8px base — 4 · 8 · 16 · 24 · 32 · 48 · 64 · 96

### The skew motif — exact angles

The signature diagonal. Applied via `transform: skew(0deg, N)` on a **`::before` pseudo-element behind the content**, never on the content itself (which would shear the type). v2.x described this loosely as "2–4°"; these are the shipped values:

| Angle | Used for |
|---|---|
| **−2°** | Section breaks and the hero band — *the default* |
| −3° | Pricing panels |
| −5° | Contact panel |
| −6° | Corner price tag (`skewX`) |
| **−10°** | Card panels — the float-panel motif, steepest and most characteristic |

### Page rhythm

> **There is no fixed page template, and the page does not alternate.** v2.x claimed "navy hero → *alternating* navy and soft-gradient sections." Production doesn't do that.

Pages **open on navy and close on navy.** Between them the ground changes between **navy** and a light ground (**white** or **soft gradient**) — but the sequence follows **the content**, not a repeating pattern. Sections that belong together share a ground and run consecutively; the ground changes when the subject does.

The actual homepage, in DOM order:

```
navy   hero
white  logo cloud
white  why work with us          ← grouped ×2
navy   who we serve
navy   our services              ← grouped ×2
white  our work
white  studio perspective
white  testimonials
white  our approach              ← grouped ×4
navy   contact (+ maze texture)
navy   footer (deep navy)
```

Navy runs twice consecutively; white runs **four** times. Consecutive same-ground sections are correct and common — not something to "fix" by alternating.

**What is consistent:** open and close on navy · every section uses the centered **eyebrow → H2 → lede** lockup · every ground *change* is carried by an angled break.

**The angle marks a change**, so it appears only where the ground actually changes — consecutive same-ground sections run together with no break at all.

#### Building the break correctly

Two failures show up every time this is rebuilt from scratch:

1. **The diagonal must be flush** — no sliver of a third colour between the two grounds.
2. **The diagonal must run edge to edge** — a skew that stops at the container leaves a visible notch at the viewport edges.

Both come from the same cause: a skewed element rotates about its own centre, so its far corners lift *out* of its box. The fix is to **overshoot**. The skewed ground is a `::before` that extends beyond its section horizontally (`left/right: -8vw`) so the diagonal always reaches both edges, and vertically (~2.2vw) so consecutive sections overlap instead of leaving a gap.

**Clearance rule.** Because the diagonal rises above the section's own box — roughly `(width ÷ 2) × tan 2°` ≈ **26px** at desktop, plus the overshoot — **a section on either side of a break needs ≥ 90px of vertical padding.** Less than that and the last line of copy slides under the neighbouring ground. This is the single most common defect when the motif is rebuilt.

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
- **Buttons:** green pill, **25px radius**, AxiformaBold 16px/24px, padding `13px 30px 11px`. **Primary = green fill, white text** (decided Aug 2026). Variants: primary · ghost · white (for navy grounds) · tag (2px outline, 2px radius, 12px). Sentence case. ⬦ Only the large size ships; md/sm are proposed.
  - **Ghost hover rule:** the fill becomes the **outline colour**, and the label **knocks out to the ground it was sitting on**. Never a third colour, never a tint. On light: green outline → green fill, white label. On navy: white outline → white fill, navy label.
- **A component that carries its own ground owns its own text colour** — and its own **controls**, not just its own text. A light card dropped into a navy section must not inherit that section's light-on-dark styling — the failure mode is white text on a soft-gradient card (reads as blank) or an on-navy ghost button (white outline) rendered inside a light card sitting inside a navy section (also reads as blank, for the same reason one level down). A section-scoped rule like `.tw-on-navy .tw-btn--ghost` only knows the *section's* ground, not the ground of whatever card the button actually sits on. Any component with its own ground — including the buttons and list markers inside it — sets those colours at a specificity high enough to beat a section-level descendant selector. This is what makes a card portable to *any* section, not just the one it was designed next to.
  - **Prefer extending an existing portable component over inventing a new one.** A from-scratch card is a new opportunity to reintroduce this exact bug. A CTA block built as its own translucent-on-dark card broke the moment its section's ground changed from navy to soft; replacing it with the already-portable content card (self-contained, correct on any ground) removed the bug rather than patched it.
  - **Specificity check when adding a colour modifier:** if a base selector for the element you're overriding already uses a doubled class (the pattern above), a single-class modifier will lose silently. Match or exceed the doubled pattern, or the override never applies and the failure is invisible until you inspect computed style.
- **Category labels:** green pill, navy text, SemiBold. (A teal variant survives in legacy decks — also navy text; use green in new work.)
- **Cards: 8px radius** *(v3 fix — 14px belongs only to the on-navy track card)*. Production ships **13 distinct card types**, catalogued with full anatomy in [`INVENTORY.md`](INVENTORY.md) §10: content · skewed accent · service primary (tall, priced) · flip (work) · testimonial · carousel · deliverable · quote · green centered · track pricing · tall pricing (+featured) · banner · case-study highlight.
  - ⬦ **Consolidation target:** these should resolve to *(card type × ground × badge placement)* rather than 13 unrelated patterns. **Grounds:** white · soft · soft-warm · green · navy-translucent · stroke.
  - **Flip card — title and description live INSIDE the card, never below it.** Front: the image with a bottom gradient scrim carrying the title. Back (hover/focus): the full title, a short description, and the CTA, centered on the accent-colour mask. *(Corrected 2026-08 — a rebuild had briefly rendered the title/meta as page copy underneath the card; the style guide's own specimen never caught it because its demo cell didn't carry real copy. Any component review should test with real, full-length content, not placeholder labels.)*
- **Float-panel card — the signature.** A transparent box whose `::before` is a **skewed (−10°) colored panel starting 60–90px down**, with a large figure floating above and **overlapping the panel's top edge**. That overlap is the brand's most recognizable card gesture. Three shipped variants: why-us (soft-warm panel, top 60px, 18px title, no body) · services (green panel, top 90px, white body) · approach (green panel, top 80px, 16px white body).
- **Segment card** *(the "Who We Serve" homepage cards — Scaling & Emerging Technology Teams · Investors & Portfolio Operators · Government & Public Sector Systems)*: solid soft-gradient card, 8px radius, a figure pulled **up 40px** to break the top edge; title sits 55px below to clear it. **The figure is NOT a fixed shape** — it's whatever pre-made icon graphic ships for that segment, and the three real assets don't agree with each other: two (`icon07.svg`, `icon09.svg`) are navy-circle-with-green-ring icons, the third (`icon06.svg`) is a green skewed rectangle with a white glyph — same skew motif as the float-panel card, at icon scale. **Corrected 2026-08** — this was previously documented as a uniform "circular badge," which only described two of the three real assets.
- **Straddle element.** A card or banner that visually bridges the boundary between two sections, rather than living inside one — e.g. two entry cards spanning a hero into the section below, or an offer banner spanning two body sections. Built as the *first* element of the section that comes **after** the boundary. Reuses the same mechanism regardless of which two grounds are involved — no per-case CSS.
  - **Not `margin-top`.** ⚠️ *This shipped broken twice before the mechanism below was correct.* A negative top margin on the first child of a zero-padding, zero-border parent **collapses through the parent** — it drags the *section's own box*, and the diagonal that section paints, up by the same amount. Changing the overlap value then moves the card and the boundary **together as a rigid unit**, so the card's position relative to the boundary barely changes no matter what you pick. The symptom is a card that looks correctly tuned by the numbers but sits almost entirely on one side of the seam when actually rendered.
  - **The correct pair:** `transform: translateY(-overlap)` (repaints pixels without touching layout — the section and its diagonal stay exactly where flow puts them) + `margin-bottom: -overlap` on the *same* element (a sibling-to-sibling margin, which gives back the flow space the lift no longer needs — this one doesn't collapse into the parent).
  - **Block a second collapse one level down:** give the straddle wrapper `display:flow-root`. Without it, *any* nested negative margin re-introduces the identical bug — Bootstrap's own row gutter (`.g-4` sets `.row{margin-top:-gutter}`) is exactly that pattern, and silently ate part of the lift.
  - **No redundant section padding.** The section holding the straddle needs **zero top padding** — a generic `.pad` class here adds an un-tuned offset on top of the overlap math and desyncs the numbers from what renders. Use a zero-top variant instead.
  - **Give the copy above it room to breathe first.** Production doesn't run the straddling element right up against the preceding copy — there's a generous gap between (e.g. the hero's headline/subhead) and the top of the straddling card, well beyond the ~90px minimum the diagonal's clearance rule requires. Tune the straddle for an even split (roughly half above the boundary, half below) as its own step, separate from that breathing room — and for a *tall* straddling element, that lift can be large enough to collide with whatever content precedes it, not just eat into the section's padding; give that content matching bottom clearance too.
  - **Verify against real pixels, not box-model arithmetic.** Screenshot and sample colour on both sides of the line at an x-position with no other content. Comparing two DOM measurements that both depend on the same collapsing margin can validate a bug against itself. The diagonal also renders *above* the raw section-boundary Y by the deliberate overshoot (~2.2vw) plus a skew-dependent slope across the row's width (~44px total at −2° over 1280px) — a naive box-model read won't account for either.
- **Badges:** **proprietary shield** (metallic rim, star-field navy face, white icon — the signature) · icon tile · category pill · tag chip · price tag (`skewX −6°`). **Placements:** inside top-left / top-center / top-right · **floating above** (the signature) · floating side · corner tag.
  - **Shield roster (8 pairings in current use):** Product Strategy & UXR (crosshair) · Product Design & UX (ruler) · AI Guidance & Enablement (sparkles) · Structural Readiness (2×2 squares) · User Enablement (user-plus) · Business Advantage (trending-up) · Data Access (database) · Quality / This Waay mark (double-check). Same shield frame every time — only the inner icon changes.
  - ⚠️ *"Flat vector" (navy circle, green ring) was removed from this list 2026-08 — it isn't a deliberate, reusable badge type. It was two of the homepage segment icons (below) happening to share a look, generalized into a "type" that was never actually a template.*
  - ⚠️ The shield's metallic chrome ships as **raster** (`image26–31.webp`), not vector. Recreating it as true SVG is an open task and a prerequisite for the Figma library.
- **Icons: Heroicons.** The shipped dimension icons are literally `sparkles` / `squares-2x2` / `user-plus` / `arrow-trending-up`. Reference **by name** on a 24px grid, ~1.7 stroke, at most one green accent.
- **Lists:** paper-plane · circle-check · plain dot · numbered step (green 44px numeral) · dotted connector.
  - Numbered step works stacked (default) **or as a horizontal row of columns** — same markup, wrapped in the Bootstrap grid instead of a single column. No separate "horizontal" component needed.
  - **The numeral's placement changes with the layout.** Floated to the left of the text (the stacked default) reads fine in one wide column; in a narrower row column it leaves a visible orphaned gap before the title with no shared alignment. In the row layout, stack the numeral directly above the title instead — same counter, just no longer absolutely positioned.
- **Text CTA with arrow** (production's `.link-txt` pattern, extended) — a link styled as text, not a button, ending in a trailing arrow that nudges forward on hover/focus. Use where a call to action shouldn't compete with the page's real buttons, e.g. closing out one of several parallel content blocks.

- **Icon source, going forward: [Google Material Icons](https://github.com/google/material-design-icons).** *(Decided 2026-08, superseding an earlier duotone-treatment experiment that didn't meet the mark and was discarded — that attempt's roster, CSS, and preview file have been removed.)* Any **new** iconography introduced into the system should be pulled from this library rather than hand-drawn. It sits alongside, not in place of, the existing sources already in production use: Heroicons for single-tone dimension icons (badge fills, list markers) and the studio's own pre-rendered graphic assets for the shield and segment-card figures (below) — those stay as they are.
  - **A caution for whoever builds the next sprite-based icon system:** if icons are assembled as `<symbol>` defs referenced via `<use>`, a CSS selector like `.wrapper .inner-part` will **never match** the inner part, no matter what renders on screen — the symbol's content lives inside `<defs>`, structurally outside the wrapper, and CSS selector matching for `<use>` follows the *source* tree, not the rendered instance. *Inherited values* (custom properties, `currentColor`) DO correctly flow through the instance — style through those, consumed by plain, ancestor-free class rules, never an ancestor selector reaching toward the symbol's internals.
- **Flight path:** hand-flown dotted trail (round caps, `stroke-dasharray: 0.1 8`) with at least one loop, **bridging exactly two sections** at a transition — 1–2× per page, never on every section.
- **Track card** (`.tw-track`, new): the one canonical on-dark card — navy ground only, translucent-white fill (`rgba(255,255,255,0.04)`, `1px solid rgba(255,255,255,0.1)`) that needs the dark backdrop to read. Header row pairs a Semibold title with a green price; a meta line (`4 weeks · Materials ready`) sits below at 60% white — not Figma's spec'd 45%, which measures ~4.1:1 on navy and fails AA. A divider separates the description from an "Includes" checklist (green dot markers, 72% white text). Used in pairs for tiered offers — e.g. the Assessment page pricing section.
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
- **Angled section breaks:** sections meet on a shallow **−2°** diagonal wherever the ground changes (cards use −10°). The angle marks a *change*, so consecutive same-ground sections run together with no break — see [Page rhythm](#page-rhythm).

---

## Slide decks

> **Decks are a separate surface with their own rules.** They're projected, read at a distance, and often shared as PDFs. Everything deck-specific lives in this section — no other section of this guide assumes a slide, and nothing here applies to the website.

**How decks differ from the marketing site:**

| | Marketing site | Decks |
|---|---|---|
| Grounds | navy · white · soft-gradient | **white or navy only** — gradients wash out projected |
| Header color | navy | **Deck Gray `#595959`** — deck-only |
| Minimum text | 15px body | **~18px @ 1080p** — distance legibility |
| Motion | scroll reveals, flight-path draw-on | **fade or cut only**, presenter-controlled |
| Canvas | Bootstrap responsive, 1140px | **fixed 16:9** — not a breakpoint system |
| Radius | 8px cards | n/a — slides aren't cards |

**Deck color & type:** Deck Gray `#595959` (headers/body on white, deck-only) · Navy `#0C2A48` (title/divider/closing grounds) · Teal-Ink `#077373` (subheads, attribution) · Waay Green `#54B987` (category labels, chart series, presenter line). Axiforma throughout — SemiBold slide headers, Bold display titles, Regular body.

Six templates cover most decks: **title/cover, section divider, content/bullet, quote, chart/data, closing.**

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
