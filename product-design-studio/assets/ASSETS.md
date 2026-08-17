# Assets manifest

Named brand assets the slide layouts (and other artifacts) reference — so a layout points at a
**named asset**, never a raw `ppt/media/` path. Extracted from the reference deck
(`Examples/2026 This Waay Deck Template_NEW_BH`) or already-official exports.

## Logo (official — already in the repo, use these; never text-recreate)

| Asset | Variant | Use |
|---|---|---|
| `This-Waay-Logo-White-Horizontal.svg` | white-on-dark, horizontal | Content slides on navy; `slide.logo` white variant |
| `This-Waay-Logo-Blue-Horizontal.svg` | colour-on-light, horizontal | Content slides on white |
| `This-Waay-Logo-White.svg` / `This-Waay-Logo-Blue.svg` | stacked lockup | Cover / divider / closing feature placement |
| `This-Waay-Logo-White-Mark.svg` / `This-Waay-Logo-Blue-Mark.svg` | plane mark only | **The official single paper-plane** — the plane motif atom binds here |

## Paper-plane motif (`motif/`)

The official single plane is the logo **Mark** SVG above. The deck also uses decorative multi-plane
compositions (extracted as PNGs for reference — the deck art, not to be redrawn):

| File | What it is |
|---|---|
| `motif/paper-plane-1.png` | Large green/white cover plane (Cover feature art) |
| `motif/paper-plane-2.png`, `-6.png`, `-9.png` | Green/white plane + flight-path trail (light-ground accents) |
| `motif/paper-plane-3.png` | Plane + wordmark lockup |
| `motif/paper-plane-4.png`, `-5.png`, `-7.png` | Green/navy plane + navy dotted trail (Conclusion accent, s24) |

## Icon library (`icons/`)

The duotone icon library — **flagged three times as absent from the spec, now extracted.** 304 unique
icons (deduplicated from 329 media files; navy-outline + green-fill on light, white-outline + green on
dark). Source of the `icon-tile` atom.

- Named `icon-001.png` … `icon-304.png` (extraction order).
- **Concept-naming pending** (a bounded follow-up): each icon needs a semantic name (e.g. `chart-up`,
  `shield-check`, `database`) so a generator can request an icon by meaning. Until then they are
  addressable by number only. This is the one deliberately-deferred piece of Phase 2R.

## Not extracted (composed, not assets)

- **Double-diamond** — vector diamonds, composed from `process-diamond` atoms (`slide.diamond*`), not
  an image.
- **Isometric divider illustrations** — this template's dividers are text-only (huge green
  divider-word); there are no isometric illustrations to extract.
