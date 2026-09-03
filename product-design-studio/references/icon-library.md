# Icon library — concept naming

Phase 2R extracted the real production icon library — 304 duotone icons — from the `.potx`,
closing a gap flagged three times earlier in the project. The files are committed and usable
today, but generically named `icon-001.png` … `icon-304.png`. A generator (human or AI) couldn't
request "the settings icon" or "the rocket icon" by meaning — only by a number nobody has
memorized. This adds a **naming/lookup layer on top of the existing files — not a rename.**

A second batch (2026-09) extends the library with 14 new, hand-authored icons for an **AI-usage
category** — see "Additions beyond the Phase 2R extraction," below. Those are born named; there
was never a numeric-only phase for them to be renamed out of.

Per house lesson #8 ("schema shape is the product — don't let convenience temptations reshape
it"), the source files, and every existing reference to them by number in `tokens.json`, the
`.potx` layouts, and `slide-components.md`, are untouched. `assets/icons/icon-manifest.json` is
the data; this file is the rule.

## Naming convention

- **Concept**: hyphenated-lowercase compound, describing what the icon *depicts* — never a bare
  category (`settings-gear`, not `settings`, when the library has other settings-adjacent icons
  like sliders or a wrench that would otherwise collide on the bare word). Never camelCase, never
  underscores — matches the project's existing semantic-token convention (`on-fill`, `ground-deep`).
- **Ambiguous glyphs** (abstract shapes with no clear real-world referent — a stray decorative
  fragment, a bare accent bar) are named by their most likely **usage context** instead of a forced
  literal object name, and the ambiguity is recorded in that icon's `notes` field rather than
  guessed at silently. 59 of the 304 icons fall into this category.
- **Category** — one of a fixed set, assigned from what the icons actually depict, not proposed
  in the abstract. `ai` was added 2026-09 for the new hand-authored batch (see below); the rest
  come from what the original 304 extracted icons actually depict:
  - `action` (23) — pencils, dials, cart actions, corner/focus brackets
  - `ai` (14) — AI-usage icons: model/agent/generate/chat/prompt at the core, plus the supporting
    cast a real product needs alongside them (human-in-the-loop, guardrails, training data,
    confidence, voice, document analysis, workflow intelligence, data pipeline)
  - `communication` (40) — megaphones, chat bubbles, email, headsets, notifications
  - `data` (78) — charts, dashboards, funnels, gauges, financial/growth compounds
  - `misc` (24) — abstract accent shapes, crowns, chess pieces, lightbulbs
  - `navigation` (8) — map pins, compass, location markers
  - `object` (55) — physical things: bags, buildings, wallets, devices, apparel
  - `people` (35) — person silhouettes, avatars, ID badges, team icons
  - `status` (41) — checkmarks, shields, badges, arrows-in-circles
- **Aliases** — 1–4 additional search terms per icon (e.g. `settings-gear` → `settings`,
  `configuration`, `preferences`), so a generator matching on meaning rather than the exact concept
  string still resolves to the right file.

## Collision log

Multiple icons legitimately share a base concept — different weights, angles, or color treatments
of what is recognizably the same glyph, extracted from different slide instances in the source
deck. Resolved with a qualifier describing the actual visual difference, never a bare `-1`/`-2`/`-3`.
Where two occurrences are genuinely visually indistinguishable (no described difference at all),
the qualifier is a real word (`-alt`, `-secondary`, `-tertiary`) and the `notes` field says so
explicitly, rather than inventing a distinction that isn't there.

Several of these families were **not** caught by matching on the exact concept string alone —
different identification passes described the same glyph with different wording (e.g. "check
circle" vs. "checkmark circle", "dollar coin" vs. "dollar badge circle"). Each family below was
verified by comparing the full visual descriptions, not just the names, before merging.

| Family (base concept) | Members | What actually distinguishes them |
|---|---|---|
| `check-circle` | 001, 034, 037, 057, 248, 283 | 001/034/037/057 = white checkmark (034/057 indistinguishable repeats); 248/283 = navy checkmark instead of white |
| `dollar-coin` | 085, 108, 163, 184, 200, 266 | All the same green-circle-plus-white-$-sign composition; no described visual difference across any of the six — all qualifiers are indistinguishable-repeat markers |
| `arrow-up-circle` | 007, 012, 045, 091, 119, 162, 282 | 007/012/091 = white arrow (012/091 indistinguishable repeats); 045 = bolder stroke; 119 = thinner stroke; 162/282 = navy arrow instead of white |
| `user-avatar-circle` | 059, 074, 098, 251 | 074/059/098 = white cutout silhouette (059/098 indistinguishable repeats); 251 = solid navy silhouette instead of a white cutout |
| `user-avatar` (ringed) | 140, 176 | Both: navy ring/outline circle framing a solid green-filled silhouette (no cutout) — visually indistinguishable |
| `megaphone-right` | 065, 104, 123 | 065/123 = handle at the side (indistinguishable repeats); 104 = handle at the bottom |
| `megaphone-left` | 151, 195, 231 | 151 = no sound-wave lines; 195/231 = with sound-wave lines (indistinguishable repeats) |
| `shield-check` | 067, 081 | Visually indistinguishable — same shield + white-checkmark composition |
| `shopping-cart` | 002, 071 | 002 = navy-and-green duotone with grille detail; 071 = single-tone solid green silhouette |
| `bar-chart-ascending` | 185, 258 | Visually indistinguishable |
| `bar-chart-growth-arrow` | 088, 285 | 088 = arrow stands in place of the tallest bar; 285 = arrow curves over the top of the bars |
| `analytics-card-mini` | 004, 031 | Visually indistinguishable |
| `conversion-funnel-person` | 165, 168 | Visually indistinguishable |
| `document-edit` | 016, 110 | 016 = notepad + checkbox + separate pen; 110 = folded-corner page + pencil |
| `pencil-edit` | 063, 304 | 063 = navy pencil with green diamond accents; 304 = standalone solid green pencil with an eraser |
| `percentage-circle` | 106, 190 | 106 = no ring; 190 = framed by an additional navy outer ring |
| `storefront-shop` | 125, 263 | 125 = mostly-navy rendering with a green doorway; 263 = mostly-green rendering with navy accents (inverse duotone balance) |

17 families, 40 icons total. Every other icon (264 of 304) is concept-unique.

**Known limit, intentionally out of scope for this pass:** this log resolves every collision
surfaced by comparing concept strings and their full visual descriptions across all 304 icons. It
is not a pixel-level duplicate audit of the source assets — if two icons are truly identical
source files under different numbers, that's a separate, deeper de-duplication question than a
naming layer is positioned to answer. Reasonable fast-follow if it's ever worth doing.

## Additions beyond the Phase 2R extraction

The manifest isn't only a naming layer over extracted assets — new icons can be added directly,
born with a real name instead of a number waiting to be retrofitted. First batch (2026-09): 14
hand-authored icons for the `ai` category, at `assets/icons/ai/<concept>.png`.

- **Style, matched to spec, not to the eye:** navy (`#0C2A48`) outlines at ≈3.4 stroke on the
  documented 48-unit grid, round caps/joins, exactly one flat green (`#54B987`) fill element per
  icon — the same rule this file states in "Naming convention" and Section 15 states for every
  generator. No Punch Green. Rendered as SVG, then rasterized to the library's native 128×128
  PNG (headless Chrome — the same technique already used for the deck logo), so these files are
  indistinguishable in format from the extracted 304.
- **A rule the 304 demonstrate but nothing had written down:** a detail sitting *on top of a
  green-filled shape* is white, not navy (`check-circle`, `gauge-meter-check`,
  `document-analytics` all do this) — navy is for outlines and structure, white is for detail
  reads on a fill. Every new icon follows it; `guardrail-shield` was revised mid-build (solid
  green shield, white spark) specifically to match its closest existing analogue, `shield-check`,
  once this pattern was spotted by direct visual comparison rather than assumed from the prose
  style description alone.
- **A recurring motif marks the category:** a small 4-point spark glyph (distinct from the
  existing 5-point `favorite-star`) appears as an accent across several of the 14, tying
  otherwise-generic concepts (a speech bubble, a shield, a document) into a visually cohesive
  "AI-flavored" set — the same way the extracted library reuses its own atoms (person silhouette,
  shield, gauge) across many icons.
- **Zero collisions with the existing 304** — all 14 concept strings are new; nothing needed a
  qualifier. `notes` on every entry states the batch and date for provenance, the same way this
  file documents where the original 304 came from.

## How a generator uses this

1. Read `assets/icons/icon-manifest.json`.
2. Match the requested meaning against each entry's `concept` first, then its `aliases`.
3. Resolve to that entry's `file` — the existing, unchanged path (`icon-NNN.png` for the
   extraction, `ai/<concept>.png` for the 2026-09 addition). Nothing downstream needs to change;
   every current reference by number still works exactly as it did.
4. If an entry has a non-null `notes` field, it's either an ambiguity note (name reflects likely
   usage, not a literal object) or a collision note (this file is one of several sharing a base
   concept) — read it before presenting the icon as *the* canonical instance of that concept.

A thin query helper (e.g. `lookup_icon(term) -> file`) built on top of the manifest is a
reasonable fast-follow once this data exists, but wasn't part of this pass — the manifest is the
data layer; nothing currently reads it programmatically.
