# Asset inventory — gaps the spec doesn't yet record

Tracks brand assets that exist in production but are **absent from `tokens.json`**, so a future
extraction pass (a Phase 0 follow-up) has a to-do list.

## ~200-icon duotone library — NOT in the spec

The old deck template (`2026 This Waay Deck Template_NEW_BH.pptx`) carries a **~200-icon duotone
icon library** in its `ppt/media/` folder. It is entirely absent from `tokens.json` and from the
brand guide. This surfaced during the Phase 2 template build.

- **Status:** unextracted. No token, no reference geometry, no naming convention recorded.
- **Why it matters:** any generator asked for iconography today reaches Heroicons or Google Material Icons (the decided sources) and never sees this library — so the deck's own visual language isn't reproducible from the spec.
- **Next step (Phase 0 follow-up):** extract the set, decide whether it survives (it may be superseded by the Google Material Icons decision, 2026-08), and if it survives, record a naming convention + provenance. If it's retired, note that explicitly so it isn't rediscovered as a mystery later.

## Shield chrome — raster only

The proprietary shield badge ships as **raster** (`image26–31.webp`); an SVG recreation exists but
the **roster V1 vs V2 is pending Kate** (see `components.md` → Badge). The shield frame is
`production`; the roster is `proposed` in the token tree.

## Font binaries — deliberately absent (not a gap)

The Axiforma OTFs are **intentionally** not in the repo — `fsType 4` (Preview & Print only) means a
public repo would be unlicensed redistribution. They live in a local, git-ignored `axiforma/`
folder. This is a compliance decision, recorded here so it's not mistaken for a missing asset. See
`fontFamily.$extensions.licensing` in `tokens.json`.
