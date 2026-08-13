# This Waay — token references

Non-token content extracted from `tokens.json` during the Phase 3a tiered-schema
migration (v3.1 flat → v4.0 DTCG-2025.10). **Only tokens live in `tokens.json`.**
The engineering rules, voice, component anatomy, and motif/illustration prose that
used to be fused into the token file live here — loaded by need (this also
pre-stages the Phase 4 `SKILL.md` progressive-disclosure work).

| File | Governs | Tokens it references |
|---|---|---|
| [`layout-mechanics.md`](layout-mechanics.md) | The CSS engineering rules — straddle element, ground ownership, angled-break clearance (the ≥90px rule), measure & rag, skew | `angle.skew-*`, `dimension.space.*`, `typography.*` |
| [`components.md`](components.md) | Component *anatomy* and the variant catalogs (13-card, badge placement, float-panel, segment card, navigation) | `button.*`, `card.*`, `badge.*`, `color.*` roles |
| [`illustration.md`](illustration.md) | Paper-plane / flight-path motifs, illustration style — including the wing-gradient stops that are motif-only, not tokens | `color.coral.300`, motif-only wing colors |
| [`voice.md`](voice.md) | Voice & messaging (pointer — canonical source is private) | — |
| [`assets-inventory.md`](assets-inventory.md) | Asset gaps the spec doesn't yet record — the ~200-icon duotone library | pending Phase 0 extraction |

Every value that appears here is preserved verbatim from v3.1; nothing was dropped
in the migration. Values that are genuinely tokens went to `tokens.json`; the prose
that *describes* them, and the motif/asset colors that were never UI tokens, are here.
