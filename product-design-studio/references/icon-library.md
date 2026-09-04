# Icon library — concept naming

Phase 2R extracted the real production icon library — 304 duotone icons — from the `.potx`,
closing a gap flagged three times earlier in the project. The files are committed and usable
today, but generically named `icon-001.png` … `icon-304.png`. A generator (human or AI) couldn't
request "the settings icon" or "the rocket icon" by meaning — only by a number nobody has
memorized. This adds a **naming/lookup layer on top of the existing files — not a rename.**

A second batch (2026-09) extends the library with 16 new, hand-authored icons for an **AI-usage
category** — see "Additions beyond the Phase 2R extraction," below. Those are born named; there
was never a numeric-only phase for them to be renamed out of.

Per house lesson #8 ("schema shape is the product — don't let convenience temptations reshape
it"), the source files, and every existing reference to them by number in `tokens.json`, the
`.potx` layouts, and `slide-components.md`, are untouched. `assets/icons/icon-manifest.json` is
the data; this file is the rule.

A third pass (2026-09) found and fixed a rendering bug affecting 149 of the 304 extracted icons —
see "Recolor + re-identification pass," below. It touched pixels (a color fix) and this file's
own naming data (many names were guessed from a broken render and were wrong), but not file paths.

## Naming convention

- **Concept**: hyphenated-lowercase compound, describing what the icon *depicts* — never a bare
  category (`settings-gear`, not `settings`, when the library has other settings-adjacent icons
  like sliders or a wrench that would otherwise collide on the bare word). Never camelCase, never
  underscores — matches the project's existing semantic-token convention (`on-fill`, `ground-deep`).
- **Ambiguous glyphs** (abstract shapes with no clear real-world referent — a stray decorative
  fragment, a bare accent bar) are named by their most likely **usage context** instead of a forced
  literal object name, and the ambiguity is recorded in that icon's `notes` field rather than
  guessed at silently. 12 of the 320 icons fall into this category as of the 2026-09
  recolor + re-identification pass (down from an original 59 — most of those turned out to be
  concrete icons misread as abstract only because their line-art was invisible; see below).
- **Category** — one of a fixed set, assigned from what the icons actually depict, not proposed
  in the abstract. `ai` was added 2026-09 for the new hand-authored batch (see below); the rest
  come from what the original 304 extracted icons actually depict. Counts as of the 2026-09
  recolor + re-identification pass (many icons' categories changed once their true artwork became
  visible):
  - `action` (25) — pencils, dials, cart actions, corner/focus brackets
  - `ai` (16) — AI-usage icons: model/agent/generate/chat/prompt at the core, plus the supporting
    cast a real product needs alongside them (human-in-the-loop, guardrails, training data,
    confidence, voice, document analysis, workflow intelligence, data pipeline, strategy targeting,
    shipped experience)
  - `communication` (43) — megaphones, chat bubbles, email, headsets, notifications
  - `data` (83) — charts, dashboards, funnels, gauges, financial/growth compounds
  - `misc` (5) — genuinely abstract accent shapes with no clear referent
  - `navigation` (8) — map pins, compass, location markers
  - `object` (70) — physical things: bags, buildings, wallets, devices, apparel
  - `people` (29) — person silhouettes, avatars, ID badges, team icons
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
| `bar-chart-growth-arrow` | 088, 285 | 088 = arrow stands in place of the tallest bar; 285 = arrow curves over the top of the bars |
| `conversion-funnel-person` | 165, 168 | Visually indistinguishable |
| `document-edit` | 016, 110 | 016 = notepad + checkbox + separate pen; 110 = folded-corner page + pencil |
| `percentage-circle` | 106, 190 | 106 = no ring; 190 = framed by an additional navy outer ring |
| `storefront-shop` | 125, 082, 263 | 125/082 = arched doorway, plain green fill (indistinguishable repeats); 263 = distinct door with a keyhole/handle cutout (`storefront-shop-door`) |
| `presentation-board-chart` | 258, 185 | 258 = single center post with a round base; 185 = three-legged splayed tripod stand (`presentation-board-chart-tripod`) |

6 families, 13 icons total. Every other icon (307 of 320) is concept-unique.

**Known limit, intentionally out of scope for this pass:** this log resolves every collision
surfaced by comparing concept strings and their full visual descriptions. It is not a pixel-level
duplicate audit of the source assets — if two icons are truly identical source files under
different numbers, that's a separate, deeper de-duplication question than a naming layer is
positioned to answer. Reasonable fast-follow if it's ever worth doing.

**Eleven families from the original (pre-2026-09) version of this log are gone, not just
renumbered:** `check-circle` (6 members), `dollar-coin` (6), `arrow-up-circle` (7),
`user-avatar-circle` (4), `user-avatar-ringed` (2), `megaphone-right` (3), `megaphone-left` (3),
`shield-check` (2), `shopping-cart` (2), `analytics-card-mini` (2), and `pencil-edit` (2) — 39
icons total. Every one of those "collisions" turned out to be an artifact of the same white-line-
art bug described below: several *different* broken icons, each showing only a fragment of green,
independently got named as if they were near-identical instances of a generic shape (a bare
checkmark circle, a bare coin, a bare arrow). Once recolored, each is a distinct, unrelated icon
(a briefcase, a megaphone, a bell, a paperclip, a shield, ...) — see "Recolor + re-identification
pass" for the full story. `storefront-shop` and `presentation-board-chart`, above, are the only two
pre-existing families that survived contact with the fix — both were confirmed as real duplicate
artwork by direct visual comparison, not just string-matching.

## Additions beyond the Phase 2R extraction

The manifest isn't only a naming layer over extracted assets — new icons can be added directly,
born with a real name instead of a number waiting to be retrofitted. First batch (2026-09): 16
hand-authored icons for the `ai` category, at `assets/icons/ai/<concept>.png` — the original 14
(model/agent/generate/chat/prompt core plus supporting cast), plus `target-spark` (AI product
strategy — deciding where AI belongs) and `app-window-spark` (the AI experience shipped as working
software), added the same batch.

- **Style, matched to spec, not to the eye:** navy (`#0C2A48`) outlines at ≈3.4 stroke on the
  documented 48-unit grid, round caps/joins, exactly one flat green (`#54B987`) fill element per
  icon — the same rule this file states in "Naming convention" and Section 15 states for every
  generator. No Punch Green. Rendered as SVG, then rasterized to the library's native 128×128
  PNG (headless Chrome — the same technique already used for the deck logo), so these files are
  indistinguishable in format from the extracted 304.
- **A rule the 304 demonstrate but nothing had written down:** a detail sitting *on top of a
  green-filled shape* is white, not navy (the checkmark badges on `briefcase-verified-alt` and
  `headphones-verified`, and `document-analytics`, all do this) — navy is for outlines and
  structure, white is for detail reads on a fill. Every new icon follows it; `guardrail-shield`
  was revised mid-build (solid green shield, white spark) specifically to match its closest
  existing analogue, `id-card-verified`, once this pattern was spotted by direct visual comparison
  rather than assumed from the prose style description alone. (Those first two examples' *own*
  concept names changed in the 2026-09 recolor pass below — the badge detail was always correctly
  white, only the surrounding outline had the bug — which is exactly how that bug was first
  spotted: by noticing a detail rule held even where the icon around it had gone missing.)
- **A recurring motif marks the category:** a small 4-point spark glyph (distinct from the
  existing 5-point `favorite-star`) appears as an accent across several of the 16, tying
  otherwise-generic concepts (a speech bubble, a shield, a document) into a visually cohesive
  "AI-flavored" set — the same way the extracted library reuses its own atoms (person silhouette,
  shield, gauge) across many icons.
- **Zero collisions with the existing 304** — all 16 concept strings are new; nothing needed a
  qualifier. `notes` on every entry states the batch and date for provenance, the same way this
  file documents where the original 304 came from.

## Recolor + re-identification pass (2026-09)

149 of the 304 extracted icons (49%) turned out to have their line-art drawn in **white** instead
of navy — extracted from deck slide instances built for a dark background. On this guide's white
`.icon-tile` cards, the white outline is invisible: only the one green fill element survives,
leaving a floating fragment instead of the real icon. Confirmed by compositing each flagged icon
on both a white and a navy background side by side — the navy-background render showed the
complete artwork every time, proving the shape itself was never wrong, only its ink color.

**The naming layer inherited the bug.** Whoever catalogued these 149 icons in the original Phase
2R pass could only see what the broken render showed them — a green fragment — so a real number of
them were named from that fragment alone: `icon-215`'s six-window office tower was catalogued as
`pause-bars-abstract` ("two green vertical bars, no other elements") because the tower outline
was invisible; `icon-001`'s briefcase-with-checkmark was catalogued as plain `check-circle` because
only the checkmark badge showed. 51 of the original 59 "abstract/ambiguous" icons fell in this
set — concrete icons misread as unidentifiable shapes, not genuinely abstract ones (see "Naming
convention," above). The eleven now-dissolved collision families in the log above are the same
failure from a different angle: several unrelated broken icons, each reduced to a similar-looking
bare fragment (a checkmark circle, a coin, an arrow), got catalogued as if they were near-duplicate
copies of one generic shape.

**Fix, in two parts:**

1. **Pixels.** A per-pixel recolor: any pixel on the white↔green color axis got projected onto
   that axis and remapped to navy↔green at the same position, alpha untouched — so anti-aliased
   edges stay smooth and the green fill is byte-for-byte unchanged. This is a targeted ink-swap,
   not a redraw; the shape data was always correct.
2. **Names.** All 149 recolored icons were re-identified from the corrected artwork (not the old
   catalogue entry) and checked for new collisions against the full manifest — 13 turned out to be
   duplicate or near-duplicate artwork, 11 of an already-catalogued icon and 2 of each other, and
   got a qualifier (see the collision log above); the rest are concept-unique. Each entry's `notes`
   field records the old (wrong) concept name and what's actually visible now, for anyone auditing
   the change.

4 icons remained genuinely ambiguous even after recoloring (no clear real-world referent) and are
marked as such rather than forced into a fake-concrete name, joining the 8 originally-ambiguous
icons that had nothing to do with this bug — 12 total, down from 59.

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
