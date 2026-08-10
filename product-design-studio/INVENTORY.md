# This Waay — Real-Brand Style Inventory (WordPress source of truth)

> **Purpose.** This is a factual catalog of how the This Waay marketing site *actually* renders today, extracted from the production CSS and page markup. It is the **primary source of truth** for building the token system and component library — the brand as it exists, not as it was idealized.
>
> **Decision on record (2026-08-08):** where the real WP styling conflicts with an accessibility fix already in `tokens.json` (e.g. white-on-green buttons, raw-green eyebrows), **the WP styling wins for now.** A holistic accessibility pass happens as a *separate, later round*. Nothing in this inventory has been "corrected."
>
> **How to read this:** values are quoted verbatim from source. `tokens.json` and `STYLE.md` are an *idealized* system that has already drifted from this reality; where they differ, this document is right and they will be reconciled to it.

**Sources audited**
- `site/public/assets/css/theme.min.css` — the WordPress theme ("Kate Theme 2024"). The real brand lives here.
- `site/public/assets/css/style.css` — recent hand-authored overrides (fluid type, measure caps, Assessment additions).
- `site/public/assets/css/wp-inline.css` — WP-generated inline styles (not yet fully audited; flagged below).
- `site/src/pages/index.astro` — homepage (pure legacy classes).
- `site/src/pages/ai-guidance/assessment.astro` — **keepers** live in its inline `<style>`.
- `site/src/pages/ai-practice.astro` — **keepers** live in its inline `<style>` (not yet in production).

---

## 0. The three parallel systems (why reproduction is hard)

There is no shared CSS layer between the token definitions and the pages. Three systems render the brand, and none share code:

| System | Where | Reaches production? |
|---|---|---|
| **A — WordPress theme** | `theme.min.css` (+ `style.css` overrides) | ✅ Yes — this *is* the live brand |
| **B — Idealized tokens** | `tokens.json` + `:root{--tw-*}` in `Branding/.../index.html` | ❌ No — 0 references in `site/src` |
| **C — Per-page inline** | `<style>` blocks in `assessment.astro`, `ai-practice.astro` | ✅ On those pages only |

The goal of the whole effort: collapse A + the keepers from C into a single tokenized layer, then make B (the style guide) render from that same layer.

---

## 1. Color

The real palette, verbatim from `theme.min.css`. **Green and navy do all the work; everything else is text-opacity on those two grounds.**

| Role | Hex (real) | Where used | Notes |
|---|---|---|---|
| Navy | `#0c2a48` | Body text, hero/section grounds, card titles | The primary. tokens.json agrees. |
| Navy (deep) | `#05203a` | Footer ground, `.case-study-hero-section` | ⚠️ tokens.json says `#081F37` — **drift**. WP reality is `#05203a`. |
| Green | `#54b987` | Buttons, eyebrows (h6), hero h1, all accents | THE brand green. |
| Green (typo variant) | `#54b886` | `.c-btn.btn-white`, `.ai-explore-section .c-btn` | ⚠️ **Inconsistency inside the WP CSS** — a one-digit typo of the green. Should be normalized to `#54b987`. |
| White | `#ffffff` | Text on navy, button hover ground, card fills | |
| Black | `#000000` | Default `<p>` color (`p{color:#000}`) | ⚠️ Base body is navy `#0c2a48` but bare `<p>` is pure black — a real split. |

**Text-on-ground opacities (real, recurring):**
- On light: body `#000`; muted `rgba(12,42,72,0.65)`; card body sometimes `rgba(12,42,72,0.65)`.
- On navy: primary `rgba(255,255,255,0.85)`; meta `rgba(255,255,255,0.6)`; faint/italic `rgba(255,255,255,0.55)`.

> **No "ink" variants exist in production.** The `greenInk / tealInk / inkMuted / noInk` accessible text colors from tokens.json are **not used anywhere on the site**. Eyebrows and links use raw `#54b987`. (This is the crux of the deferred a11y round.)

---

## 2. Gradients (the "soft ground")

The real soft ground is **not** the 2-stop mint→ice in tokens.json. It's a family of **warm-ended multi-stop gradients** (cool mint/ice in the middle, warm sand at the end), all at `135deg`:

| Recipe | Used on |
|---|---|
| `linear-gradient(135deg, #e8fefb 0, #f2fbfb 55%, #fdf5e8 100%)` | `.we-serve-section .box`, `.ecosystem-section .box` |
| `linear-gradient(135deg, #e8fefb 0, #f2fbfb 66%, #fdf5e8 100%)` | `.testimonials .slide` |
| `linear-gradient(135deg, #f1fbfb 0, #e5fffb 75%, #faf6e9 100%)` | `.about-hero-section` skewed panel |
| `linear-gradient(135deg, #f5f7ec 0, #eafdfa 20%, #f2fbfb 80%, #f8f7f0 100%)` | `.why-us-section .box` (4-stop) |
| `linear-gradient(135deg, #f8f6ea 0, #e5fffb 50%, #effcfb 100%)` | `.what-you-receive-section` (Assessment) |

> **Inconsistency:** five near-identical-but-different recipes. This is a prime candidate to consolidate into **one** canonical soft-gradient token. The green fill (`#54b987`) is used as a *solid*, skewed card ground (not a gradient) in the WP theme.

---

## 3. Typography

**Font families (real):** five *separately named* Axiforma families, self-hosted in `site/public/assets/fonts/` (`.eot/.woff2/.woff/.ttf/.svg`), each declared `font-weight:normal`:
`AxiformaRegular` · `AxiformaMedium` · `AxiformaSemiBold` · `AxiformaBold` · `AxiformaExtraBold`.

> ⚠️ **Key structural difference from tokens.json**, which models *one* `'Axiforma'` family with `font-weight` 400/500/600/700 and **no ExtraBold**. In reality ExtraBold carries nearly every heading, and hierarchy is done by *switching family name*, not by `font-weight`. Base.astro also loads Google **Poppins + Work Sans** — Work Sans is not a brand font and appears unused.

**Base / body**
```
body { color:#0c2a48; font-size:15px; font-family:'AxiformaRegular'; line-height:normal; }
p    { color:#000; margin:0 0 20px; line-height:normal; }
```
- Reading base is **15px**, `line-height:normal` (not 16px / 1.7 as tokens.json states).
- Measure cap `max-width:65ch` on `.section-title p` and `.text-block p` (from `style.css`).
- `h1–h5 { text-wrap:balance }`, `p,li { text-wrap:pretty }` (from `style.css`).

**Headings (real, by role)**

| Element | Real spec | Role |
|---|---|---|
| `h6` (**eyebrow**) | `#54b987`, 12px, AxiformaBold, UPPERCASE, `letter-spacing:2.76px`, `margin:0 0 10px` | The eyebrow label. Semantic h6. |
| `h2` | 40px → `clamp(36px, 34.2px+0.49vw, 40px)`, AxiformaExtraBold | Section headline |
| `h3` (supp-comp) | 26px → `clamp(22px, …, 26px)`, ExtraBold | Sub-headline |
| `h3` (about text) | `clamp(21px, …, 24px)` | Bio/about |
| `h5` | 20px, AxiformaExtraBold, `line-height:normal` | Card titles |
| `h1` — home hero | **green `#54b987`**, 46px → `clamp(32px, 25.6px+1.7vw, 46px)`, AxiformaSemiBold, `line-height:60px`/1.3 | Home headline (green!) |
| `h1` — work/case/guidance hero | white/navy, 40px → `clamp(36px, …, 40px)`, ExtraBold | Interior hero headline |
| `h1` — contact hero | green `#54b987`, 28px, SemiBold, `line-height:38px` | Contact headline |

> **Eyebrow drift across systems:** theme `h6` = 12px / `2.76px` tracking. Assessment inline eyebrow = 12px / `1.5px`. AI Practice eyebrow = 12px / `1.6px`. Three different trackings for the "same" element.

---

## 4. Buttons

The real button, verbatim:
```
.c-btn        { display:inline-block; padding:13px 30px 11px; color:#fff;
                font-size:16px; font-family:'AxiformaBold'; line-height:24px;
                background-color:#54b987; border:1px solid #54b987;
                white-space:nowrap; border-radius:25px; text-align:center; }
.c-btn:hover  { background-color:#fff; color:#54b987; }
.c-btn.v2     { background-color:transparent; color:#54b987; }      /* ghost */
.c-btn.v2:hover { color:#fff; background-color:#54b987; }
.c-btn.btn-white { background-color:#fff; color:#54b886; border:1px solid #fff; }  /* note typo green */
.c-btn.btn-white:hover { background-color:#54b886; color:#fff; }
```
- **Radius is `25px`** (fixed), not a 999px pill and not 14px.
- **Text is white on green** (the a11y item deferred by decision).
- Contextual variants exist inline: `.our-work-section … .mask .c-btn` (white/green on the flip mask) and `.ai-explore-section .c-btn` (white ground + `shape07.svg` arrow via `::after`).
- Three canonical states: **primary** (green fill), **`.v2`** (ghost/transparent), **`.btn-white`** (white fill). The AI Practice `.c-btn--ghost` is a *fourth*, inline reinvention of `.v2`.

---

## 5. Cards

**All cards are `border-radius:8px`** (the one exception is `.tw-track` at 14px — imported from the design system on the Assessment page). There is no single card component; `.box` is styled per-section. Grouped by real pattern:

**5a. Skewed-pseudo icon cards** — transparent box, colored ground on a `skew(0deg,-10deg)` `::before` sitting behind it:
- `.why-us-section .box` — skewed **gradient** ground; centered icon + `h5`.
- `.artifacts-section .box`, `.our-process-section .box`, `.quality-section .box` — skewed **solid green** ground; white text.

**5b. Gradient-ground cards** (no skew) — 8px radius, warm 3-stop gradient fill:
- `.we-serve-section .box`, `.ecosystem-section .box` — navy `h5` (20px ExtraBold) + muted body.

**5c. Flip cards** (3D `rotateY(180deg)` on hover):
- `.our-work-section .box` — image front / green `.mask` with CTA back.
- `.ai-work-section .box-holder` — front navy image (`.box-1`, `1px solid rgba(255,255,255,0.16)`) / back green (`.box-2`) with `.link-txt` + `shape07.svg` arrow. This is the case-study card the AI Practice page replicated inline.

**5d. NEW — keepers from Assessment** (`assessment.astro`):
- `.deliverable-card` — white, `border-radius:8px`, `padding:32px`, `box-shadow:0 20px 40px -24px rgba(12,42,72,0.25)`, icon bleeds up (`margin:-60px 0 20px`) with `drop-shadow`. **Worth promoting to canonical.**
- `.tw-track` — the design system's on-navy pricing card: `rgba(255,255,255,0.04)` fill, `1px solid rgba(255,255,255,0.1)`, **14px radius**, green price, dotted "Includes" list. Already token-aligned. **Canonical.**
- `.divider-list-section .list-item` — left-aligned, top-bordered (`rgba(255,255,255,0.12)`) list on navy; `h5` white + muted body. **Promote as the "dividered list" pattern.**
- `.tq-item` — numbered item: green `44px` AxiformaBold numeral over `h5` + body. No card chrome. **Promote as "numbered step."**

**5e. NEW — keepers from AI Practice** (`ai-practice.astro`, currently on `--aip-*` inline tokens with one-off px):
- `.aip-quote-card` — 2-col quote grid; white, `1px solid`, hover-lift + green focus ring. **Promote.**
- `.aip-wia` — feature banner: navy, `20px` radius, green left accent bar, large shadow. **Promote as "feature/offer banner."**
- `.aip-step`, `.aip-offer-card`, `.aip-service`, `.aip-door` — white/border/16-20px-radius content cards. These are *reinventions* of 5b/5d with different radii (16/20px) and a non-brand gradient (`#f5f8fb`). **Fold into the canonical content card, don't keep as-is.**

> **The card problem in one line:** ~8 card treatments on the AI Practice page alone, radii of 8/14/16/20px across the site, and no shared definition. Consolidation target proposed in §10.

---

## 6. Page & section backgrounds

**Page shell**
```
.wrapper { position:relative; width:100%; overflow-x:hidden; }   /* clips the skewed bleeds */
body     { color:#0c2a48; }   /* no explicit page background — defaults to white */
```

**Section grounds** alternate between three treatments:
- **Navy** `#0c2a48` — `.home-hero-section`, `.we-serve-section`, `.artifacts-section`, `.specialization-section`, `.pricing-section` (Assessment), `.divider-list-section`.
- **White** `#fff` — `.about-us-section`, `.about-hero-section`, `.location-section`.
- **Navy + texture** — `.contact-us-section`, `.contact-us2-section`, `.ai-explore-section` add `maze_15x.webp` (`background-size:1440px auto`, top-centered). *(This is the texture the AI Practice hero borrowed.)*

**The skew break motif** — the signature "angled section" is a `transform:skew(0deg, −Ndeg)` on a `::before`/`::after` pseudo, at several angles:
- `−2°` — hero/section grounds (`.home-hero`, `.work-hero`, `.services-hero`, `.contact-hero`).
- `−3°` — `.about-hero` gradient panel.
- `−5°` — `.contact-hero .text-block` green panel.
- `−10°` — cards (§5a).

> tokens.json describes only "2–4°". Reality spans −2° to −10°. This motif is core and is **absent from the token system** — it needs first-class tokens (`--tw-skew-section`, `--tw-skew-card`) and a documented component.

**Section padding (real, representative):** heroes `135–215px` top; content sections `40–120px` vertical; `.section-title` bottom padding `30–50px`. No single scale — values are per-section. (tokens.json's `clamp(56px,8vw,110px)` is aspirational, not applied.)

---

## 7. Heroes

Shared anatomy: **navy ground + `skew(−2°)` break + a decorative SVG illustration**, generous top padding.

| Hero | Ground | Decoration | H1 |
|---|---|---|---|
| Home | navy `#0c2a48`, `pad 135px 0 60px` | `line-hero.svg` (`::after`), skewed navy `::before` | green 46px SemiBold |
| Work | navy, `pad 215px 0 115px` | `dora_work_1.svg` | white 40px ExtraBold |
| Services | navy, `pad 135px 0 40px`, `margin-bottom:-150px` | skewed navy `::before` | — |
| Contact | `pad 175px 0 40px` | `dora_contact_1.svg`; form in skewed `−5°` green panel | green 28px SemiBold |
| About | **white**, `pad 170px` | `dora_about_1.svg`; skewed `−3°` warm gradient panel | — |
| Case study | `#05203a`, cover image | — | 36px |
| Guidance (Assessment) | inherits base | green `.accent` span + green `.meta-line` | 40px |

> The AI Practice hero (`ai-practice.astro`) is a **bespoke** navy + radial-green-glow + `maze_15x.webp` treatment — it doesn't match the canonical `skew(−2°) + line-hero.svg` home hero. Decide whether AI Practice adopts the canonical hero or its texture treatment becomes a documented variant.

---

## 8. Footer & header

**Footer** (`theme.min.css`)
```
footer { padding:76px 0 25px; background-color:#05203a; }
footer .footer-menu > li > a { color:#fff; font-size:16px; font-family:'AxiformaRegular'; line-height:24px; }
footer .footer-menu > li > a:hover { opacity:.7; }
footer .subfooter { margin-top:42px; padding-top:24px; border-top:1px solid rgba(255,255,255,0.1); }
footer .subfooter .privacy-block p { color:rgba(255,255,255,0.6); font-size:16px; }
footer .social-media li a img { width:18px; height:18px; }
```

**Header** — sticky bar, logo `224×37`, primary menu (Home / Our Story / Services / AI Practice / Work / Contact Us). `style.css` adds the mobile hamburger sub-menu behavior (theme only shipped a desktop hover dropdown). *(Full nav CSS not exhaustively extracted; low priority for the six focus areas.)*

---

## 9. Inconsistencies found (the punch list)

Documented so consolidation can resolve them deliberately:

1. **Green typo** — `#54b886` vs `#54b987` (buttons/explore). Normalize to `#54b987`.
2. **Deep navy** — footer `#05203a` vs tokens.json `#081F37`. Reality wins → `#05203a`.
3. **Card radius** — 8px everywhere except `.tw-track` (14px) and AI Practice (16/20px). Pick one (proposal: 8px standard, `.tw-track` keeps 14px as the on-dark exception).
4. **Soft gradient** — 5 different multi-stop recipes. Consolidate to one.
5. **Eyebrow tracking** — 2.76px / 1.5px / 1.6px across theme / Assessment / AI Practice. Pick one.
6. **Body size/leading** — 15px `normal` (theme) vs 16px/1.7 (tokens.json). Reality wins → 15px, but confirm leading (`normal` ≈ 1.2 is tight for body).
7. **Font model** — 5 named families + ExtraBold (real) vs 1 family + weights, no ExtraBold (tokens.json). Reality wins.
8. **Buttons** — 3 real states (`.c-btn`, `.v2`, `.btn-white`) + inline `.c-btn--ghost` reinvention. Collapse `--ghost` into `.v2`.
9. **AI Practice `--aip-*` tokens** — a full parallel re-declaration with approximate values (`#7fd0aa`, `#1f6b47`, `#f5f8fb`). Delete once the shared layer exists.
10. **wp-inline.css** — 16KB of WP-generated styles not yet audited; may hold more overrides. *(Open item.)*

---

## 10. Canonical component set (validated in the live preview)

The full taxonomy, expanded through the preview passes and confirmed against the live CSS. A working visual reference lives in the component-preview artifact; a homepage rebuilt on this engine is the match test.

**Color**
- Primary: navy `#0c2a48` · deep navy `#05203a` (footer) · green `#54b987` · white.
- Punch: **punch green `#3dd68c`** — one intentional moment per page; the green gradient `#54b987→#3dd68c` counts as a punch.
- Secondary: **teal `#0babab`** (heritage subheads/links) · **steel `#0d698a`** (support/charts) · **coral `#f2a08d`** (illustration only — never UI).
- Grounds: **one soft gradient** `linear-gradient(135deg,#e8fefb,#f2fbfb 55%,#fdf5e8)` (consolidated from the 5 in §2); green fill; navy; navy+`maze` texture; white.
- Text: on-navy `#fff` @ .85 / .6 ramp; on-light navy + `rgba(12,42,72,.65)` muted. (Ink variants deferred to the a11y round.)

**Type** — 5 Axiforma families kept (Regular/Medium/SemiBold/Bold/**ExtraBold**); scale from §3 (eyebrow 12px, body 15px, h5 20px, h4 20px, h3 32px, h2 clamp 36–40px, h1 clamps per hero); one eyebrow tracking; green highlight accent (one per headline).

**Buttons** — sizes **sm / md / lg** (lg = current `.c-btn`: 25px pill, AxiformaBold 16px, pad 13/30/11); variants **primary / `.v2` ghost / `.btn-white` / `.d-btn` tag** (outline, 2px radius, 12px) / **arrow**; states default/hover/focus/disabled. (Collapse the AI Practice `.c-btn--ghost` into `.v2`.)

**Cards (canonical types)**
1. **Content card** — 8px; ground = any of the 5 variants below; ExtraBold `h5` + muted body; optional pill/CTA (absorbs we-serve/ecosystem + AI Practice step/offer/service/door).
2. **Skewed accent card** — 8px + `skewY(−10°)` colored pseudo panel (§5a).
3. **Service primary (tall)** — gradient ground, `shape04` image at bottom, skewed price badge, heading/subhead/bullets (§5c projects/solutions).
4. **Flip card** — case-study / our-work `.box-holder` (navy image front / green back).
5. **Testimonial card** — gradient ground, `quotes.svg`, logo, quote, author + green role.
6. **Carousel card** — solid-green slide + circle arrows + elongating pill dots (specs-slider).
7. **Deliverable card** — white, top-bleed icon, soft shadow (assessment).
8. **Quote card** — hover-lift, green focus (AI Practice).
9. **Green centered card** — solid green, centered icon + `h5` (this-work / case-decisions).
10. **Track pricing card** — on-navy translucent, 14px, green price, dotted includes (assessment).
11. **Tall pricing card** — `.price-box`: gradient ground + green 48px price; **featured green `.box-alt`** variant.
12. **Banner card** — navy, green accent bar, highlights + CTA (AI Practice `.aip-wia`); image variant.
13. **Case-study highlight** — green-rule quote (regular + bold), "our role" block, centered pull-quote.

**Card background variants** (the axis every card can take): **white · gradient (soft) · green · stroke · translucent (on-navy)**.

**Lists** — bullet systems: **paper-plane** · **circle-check** (`check-circle.svg`) · **plain dot**; plus **dividered list** (on-navy) · **numbered step** (green 44px numeral) · **dotted connector** (`dots.svg`).

**Sections & motion** — grounds navy / white / soft / green / navy-textured; the **skew break** motif as tokens: `skew(−2°)` section break · `−3°` pricing · `−5°` contact panel · `−6°` price badge · `−10°` cards; plus the **diagonal triangle** cut (case-study hero). Naturally alternating ground rhythm frames content down the page.

**Hero variants** — navy + `skew(−2°)` + illustration (home, green H1) · navy white-H1 + green accent + meta (assessment) · navy+texture + highlighted subhead + 2 CTA (AI Practice) · white/soft-gradient panel (about). Vary by ground, H1 color, accent, CTA count.

**Flight path** — the hand-flown dotted trail (round dots `stroke-dasharray:0.1 8`, ≥1 loop) that **bridges exactly two sections at a transition**; used 1–2× per page, not on every section. Real assets: `line-hero`, `line-whowe`, `line-testimonials`, `line-foot`, `line23/24`, `dots.svg`, `dora_*`.

## 11. Icon library

**Heroicons-based** — the studio already ships Heroicons (the assessment dimension icons are literally `sparkles`, `squares-2x2`, `user-plus`, `arrow-trending-up`). Canonical library = a named SVG sprite on a **24px grid, ~1.7 stroke**, navy-on-light / white-on-navy, with an optional **single green accent** (per the icon spec). Referenced **by name** so badges and the AI→Figma pipeline can slot any glyph. ~46 curated in the preview; extensible to the full Heroicons set (~300). Solid variants exist where the brand ships them (`sparkles`, `squares`, `user-plus`, `trending-up`, `check-badge`).

## 12. Badges & icon placement

**Badge containers**
- **Proprietary shield** (signature) — metallic silver rim, star-field navy face, top gloss, drop shadow; white icon slot. *The live chrome is a raster render (`image26–31.webp`); recreate as true SVG for the pipeline.* All current examples: strategy (viewfinder), design (ruler), AI (sparkles), structural (squares), enablement (user-plus), business (trending-up), data (database), quality (double-check).
- **Icon badge** — rounded square / circle / punch-gradient tile with a library icon.
- **Category pill** (green, navy text) · **tag chip** (outline) · **skewed price tag** (`skewX(−6°)`).

**Icon / badge placement** (captured from the live site)
- **Inside:** top-left · top-center (`margin:0 auto`) · top-right (absolute corner).
- **Floating above** (the signature): large figure bleeds above a skewed panel that starts 60–90px down — centered (why-us/services, `margin:0 auto`) or left (`margin-top:-40/-60px`, deliverable/ai-solutions).
- **Floating side:** badge overlaps the card's left edge.
- **Corner tag:** absolute top-right skewed price badge (`.projects .price`).

---

## Roadmap (after you review this inventory)

1. **Inventory** ✅ *(this doc — review & correct)*
2. **Reconcile** `tokens.json` + `STYLE.md` to match this reality (reality wins; log the a11y items as deferred).
3. **Build** `tokens.css` + `components.css` from these real values; point the style-guide `index.html` at them.
4. **Wire & migrate** — load the shared CSS in `Base.astro`; migrate AI Practice (the un-shipped pilot) first, then production pages, strangling `theme.min.css`.
5. **Accessibility round** — the deferred holistic pass (button text, eyebrow color, body leading, focus states).
