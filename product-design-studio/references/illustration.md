# Motifs & illustration

Relocated from `tokens.json` `motif` prose in the v4.0 migration. Governs tokens:
`color.coral.300` (the illustration accent) — plus the **motif-only** wing-gradient colours below,
which were never UI tokens and therefore live here, not in the token tree.

## Paper plane

The wing is a gradient blade: **`#62D38C` (nose) → `#30737B` (tail)**, a `90°` (`angle.horizontal`)
sweep — deep teal at the tail to light green at the nose. Body navy on light grounds, white on
navy. Never outlined, never flat green. Use the official SVG paths, not redrawn geometry.

> `#62D38C` and `#30737B` are **motif-only** gradient stops — they render inside the wing artwork
> and appear nowhere in the UI, so they are documented here rather than as `color.*` primitives.
> (The `gradient.wing` recipe is intentionally not a token: it is composed at render time from
> these two stops + `angle.horizontal`.)

## Flight path

Round dots (`stroke-dasharray 0.1 8`, round caps, ~3px), navy on light / white on navy. Every
trail includes at least one loop. Never straight, never dashed. Bridges exactly two sections at a
transition — used 1–2× per page, never on every section. Five canonical variants (A single loop,
B S-wave, C tight coil, D wide arc, E double curl). Real assets: `line-hero`, `line-whowe`,
`line-testimonials`, `line-foot`, `dots.svg`.

## Icons

Bold navy outlines (~3.5px at 48px grid) with a single flat green fill element. On navy, outlines
invert to white; green fills stay green.

## Illustration accent

`color.coral.300` (`#F2A08D`) is the glowing path/node accent in the paper-cut landscape scenes.
**Illustration only** — never a UI, chart, or text colour.
