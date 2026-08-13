# Brand Schema — the token contract

The canonical shape every Skill reads and writes. Defined once, here, before any Skill or pipeline
hardcodes a structure. This Waay is the worked example; the schema itself is brand-agnostic.

Grounded to **DTCG v2025.10** — the Design Tokens Community Group's first stable version, released
Oct 2025 and recommended for production. Schema URL:
`https://www.designtokens.org/schemas/2025.10/format.json`.

---

## The one idea

Three tiers, each referencing the one below:

```
PRIMITIVE   what the value IS      color.green.500 = #54B987
    ↓ referenced by
SEMANTIC    what the role MEANS    color.text.accent = {color.green.700}
    ↓ referenced by
COMPONENT   what the use REQUIRES  button.primary.label = {color.text.on-fill}
```

Why this matters for *your* philosophy specifically: **it turns your anti-drift rules from prose a
validator polices into structure a generator cannot violate.** Today This Waay enforces its rules
with `"never…"` / `"only…"` prose and a lint pass that greps for violations after the fact. Three
tiers make five of those rules *unrepresentable* rather than merely caught:

| This Waay rule (currently prose) | Becomes structure |
|---|---|
| "Green fails as text — use greenInk" | `text.*` roles reference `green.700`; the failing `green.500` is wired to no text role, so a generator picking a text color cannot reach it |
| "Never fill a surface with a bare gradient stop" | `mint/ice/sand` are referenced only by the gradient composite; no `surface.*` role points at them |
| "Numeric weight silently fake-bolds ExtraBold" | `boldFlag` maps to the composite's `fontWeight` (400 for name-carried cuts, 700 only for the real-bold family); the fake-bold pairing isn't expressible |
| "Punch green never in charts / recurring UI" | `fill.emphasis` is its only role; in the chart theme it lands at `accent6` where a default series never reaches it |
| "Deck Gray never on the website" | lives only in a deck-scoped component group, never in the site semantic layer |

That's the difference between a lint rule and a type system. It's also the exact failure mode your
`v3Change` note describes — "drifted by construction" — inverted: now correctness is by construction.

---

## What is a token, and what is not

The current `tokens.json` is three things fused: a **token file**, a **rulebook**, and a
**changelog**. The refactor separates them. Only the first goes in the token tree.

**Tokens** (→ the tiered JSON): colors, dimensions, radii, gradients, typography composites,
shadows, and the component values extracted from them (`button.radius`, `card.radius`).

**Not tokens** (→ `references/*.md`, loaded by need — which also serves the SKILL.md
progressive-disclosure goal from later phases):
- `systemRules` — straddle element, ground ownership, angled-break clearance, measure/rag. These are
  CSS *engineering* rules. They reference tokens but aren't tokens. → `references/layout-mechanics.md`
- `voice` → `references/voice.md`
- component *anatomy* and the 13-card / badge-placement catalogs → `references/components.md`
  (the extracted *values* still become tier-3 tokens; the prose describing the anatomy does not)
- illustration prompts → `references/illustration.md`

**Provenance, corrections, status, accepted deviations** — the stuff that makes This Waay excellent —
do *not* get dropped and do *not* clutter the values. They live in `$extensions`, DTCG's official
slot for vendor data (see below). Nothing excellent is lost; it moves to where the spec expects it.

---

## DTCG conventions this schema uses

- **Fields:** `$value`, `$type`, `$description`, `$extensions`. Groups may set `$type` once and all
  descendants inherit it.
- **References:** `"{group.subgroup.token}"` — curly braces, dot path, the whole string is the alias.
- **Color is an object, not a hex string** (this changed at v2025.10 — the bare-hex form is legacy):
  ```json
  { "$type": "color", "$value": { "colorSpace": "srgb", "components": [0.33, 0.72, 0.53], "hex": "#54B987" } }
  ```
  `hex` is the fallback for tools that don't read `components`. We author both.
- **`$extensions` namespace:** DTCG reserves this for vendor data under a reverse-domain key. I've
  used `com.thiswaay.brandkit` as a placeholder — **this should become the product's namespace when
  you name the product**, since the whole point is that it's not This-Waay-specific. One decision to
  make (below).

**Tooling caveat, load-bearing for Phase 3:** Style Dictionary v4 supports DTCG, but *not yet the
full 2025.10 module* — that lands in v5 (in progress). So `build_theme.py` should resolve references
itself rather than assuming the current Style Dictionary handles every 2025.10 nicety. Practically:
author to 2025.10, but own the resolver. That keeps you spec-current without being blocked on a
third-party release — and it's work Phase 3 was doing anyway.

---

## Tier 1 — Primitives

Raw palette. Named by what they are, not where they're used. This is the *only* tier that contains
literal values; everything above references down into here.

```json
{
  "color": {
    "$type": "color",
    "navy":  {
      "900": { "$value": { "colorSpace": "srgb", "components": [0.047, 0.165, 0.282], "hex": "#0C2A48" } },
      "950": { "$value": { "colorSpace": "srgb", "components": [0.020, 0.125, 0.227], "hex": "#05203A" } }
    },
    "green": {
      "400": { "$value": { "colorSpace": "srgb", "components": [0.239, 0.839, 0.549], "hex": "#3DD68C" } },
      "500": { "$value": { "colorSpace": "srgb", "components": [0.329, 0.725, 0.529], "hex": "#54B987" } },
      "700": { "$value": { "colorSpace": "srgb", "components": [0.173, 0.427, 0.302], "hex": "#2C6D4D" } }
    },
    "teal":  {
      "500": { "$value": { "colorSpace": "srgb", "components": [0.043, 0.671, 0.671], "hex": "#0BABAB" } },
      "700": { "$value": { "colorSpace": "srgb", "components": [0.027, 0.451, 0.451], "hex": "#077373" } }
    },
    "steel": { "600": { "$value": { "colorSpace": "srgb", "components": [0.051, 0.412, 0.541], "hex": "#0D698A" } } },
    "slate": {
      "400": { "$value": { "colorSpace": "srgb", "components": [0.553, 0.639, 0.710], "hex": "#8DA3B5" } },
      "600": { "$value": { "colorSpace": "srgb", "components": [0.361, 0.443, 0.522], "hex": "#5C7185" } }
    },
    "coral": { "400": { "$value": { "colorSpace": "srgb", "components": [0.949, 0.627, 0.553], "hex": "#F2A08D" } } },
    "red":   {
      "400": { "$value": { "colorSpace": "srgb", "components": [0.847, 0.416, 0.353], "hex": "#D86A5A" } },
      "700": { "$value": { "colorSpace": "srgb", "components": [0.647, 0.216, 0.153], "hex": "#A53727" } }
    },
    "gray":  { "600": { "$value": { "colorSpace": "srgb", "components": [0.349, 0.349, 0.349], "hex": "#595959" } } },
    "white": { "$value": { "colorSpace": "srgb", "components": [1, 1, 1], "hex": "#FFFFFF" } },

    "_gradientStops": {
      "$description": "Referenced ONLY by gradient composites — never by a surface role. This is the structural form of This Waay's 'never fill a surface with a bare stop' rule.",
      "mint": { "$value": { "colorSpace": "srgb", "components": [0.910, 0.996, 0.984], "hex": "#E8FEFB" } },
      "ice":  { "$value": { "colorSpace": "srgb", "components": [0.949, 0.984, 0.984], "hex": "#F2FBFB" } },
      "sand": { "$value": { "colorSpace": "srgb", "components": [0.992, 0.961, 0.910], "hex": "#FDF5E8" } }
    }
  },
  "dimension": {
    "$type": "dimension",
    "space": {
      "1": { "$value": { "value": 4,  "unit": "px" } },
      "2": { "$value": { "value": 8,  "unit": "px" } },
      "3": { "$value": { "value": 16, "unit": "px" } },
      "4": { "$value": { "value": 24, "unit": "px" } },
      "5": { "$value": { "value": 32, "unit": "px" } },
      "6": { "$value": { "value": 48, "unit": "px" } },
      "7": { "$value": { "value": 64, "unit": "px" } }
    },
    "radius": {
      "card":  { "$value": { "value": 8,  "unit": "px" } },
      "track": { "$value": { "value": 14, "unit": "px" } },
      "pill":  { "$value": { "value": 25, "unit": "px" } },
      "input": { "$value": { "value": 2,  "unit": "px" } }
    }
  },
  "fontFamily": {
    "$type": "fontFamily",
    "regular":   { "$value": ["Axiforma", "Poppins", "Segoe UI", "sans-serif"] },
    "medium":    { "$value": ["Axiforma Medium", "Poppins", "Segoe UI", "sans-serif"] },
    "semibold":  { "$value": ["Axiforma SemiBold", "Poppins", "Segoe UI", "sans-serif"] },
    "extrabold": { "$value": ["Axiforma ExtraBold", "Poppins", "Segoe UI", "sans-serif"] }
  }
}
```

Note the `components` arrays are computed sRGB (0–1) — Claude Code should derive these from the hex
during migration, not hand-type them. `dimension` uses the `{value, unit}` object form (also
2025.10). The `fontFamily` array *is* your fallback stack, first-class.

**The numeric step assignments above (`green.500`, `navy.900`, …) were estimated by eye and are NOT
final** (Decision 2). At migration, re-seat every step from a measured L\* value sorted within its
hue family, so `navy.900` isn't secretly a perceptual `950`. Eyeballed steps that calcify become
subtle, annoying corrections once a client maps their ramp onto yours.

---

## Tier 2 — Semantic

Named by role. **This is the tier that does the work** — it's where "green fails as text" stops being
prose and becomes wiring.

```json
{
  "color": {
    "$type": "color",
    "surface": {
      "ground":       { "$value": "{color.navy.900}",  "$description": "Primary dark ground — heroes, sections, card bodies." },
      "ground-deep":  { "$value": "{color.navy.950}",  "$description": "Footer, deepest layer." },
      "ground-light": { "$value": "{color.white}",     "$description": "The other primary ground — carries half the page rhythm." }
    },
    "fill": {
      "action":   { "$value": "{color.green.500}", "$description": "THE action fill — buttons, labels, icons, on any ground." },
      "accent":   { "$value": "{color.teal.500}",  "$description": "Heritage accent fill." },
      "emphasis": { "$value": "{color.green.400}", "$description": "Punch. One moment per asset. This is its ONLY role." },
      "info":     { "$value": "{color.steel.600}" },
      "danger":   { "$value": "{color.red.400}" }
    },
    "text": {
      "body":      { "$value": "{color.navy.900}",  "$description": "Default reading color on light grounds." },
      "on-ground": { "$value": "{color.white}",     "$description": "Text on the dark ground." },
      "accent":    { "$value": "{color.green.700}", "$description": "Accessible green for text — 6.2:1. NOTE it references .700, not the .500 fill. This is the enforcement." },
      "accent-alt":{ "$value": "{color.teal.700}",  "$description": "Accessible teal for text — 5.7:1." },
      "muted":     { "$value": "{color.slate.600}", "$description": "Captions, secondary labels — 5.1:1." },
      "on-fill":   { "$value": "{color.navy.900}",  "$description": "Default text ON a color fill: navy. Passes AA on green (6.02:1) and teal (5.2:1). Components override at their own risk — see button.primary." },
      "danger":    { "$value": "{color.red.700}" }
    },
    "border": {
      "subtle": { "$value": "{color.slate.400}", "$description": "Borders, gridlines. Fill-only hue — never used as text." }
    }
  },
  "gradient": {
    "$type": "gradient",
    "soft": {
      "$value": [
        { "color": "{color._gradientStops.mint}", "position": 0 },
        { "color": "{color._gradientStops.ice}",  "position": 0.55 },
        { "color": "{color._gradientStops.sand}", "position": 1 }
      ],
      "$extensions": { "com.thiswaay.brandkit": { "angle": "135deg", "status": "production" } }
    }
  }
}
```

**The payoff, stated plainly:** `text.accent` → `green.700` (accessible), `fill.action` → `green.500`
(vivid). No text role references `green.500`. A generator asked for an accent text color is
*structurally incapable* of selecting the value that fails contrast. The rule isn't enforced — it's
inexpressible. Same shape protects the gradient stops (referenced only under `gradient.soft`, no
surface role reaches them).

One DTCG gap to note: the `gradient` composite has **no angle field**. `135deg` therefore lives in
`$extensions`. Flagged as a decision below.

---

## Tier 3 — Component

Named by use. References semantic. This is where the **accepted deviation** lives — at exactly the
token where the choice was made, not in a footnote three sections away.

```json
{
  "button": {
    "primary": {
      "background": { "$value": "{color.fill.action}",  "$description": "green.500" },
      "label": {
        "$value": "{color.white}",
        "$description": "OVERRIDES the safe default (color.text.on-fill = navy) with white. This is the deviation.",
        "$extensions": {
          "com.thiswaay.brandkit": {
            "status": "production",
            "acceptedDeviation": {
              "verdict": "White on green.500 = 2.42:1; fails WCAG 2.2 AA 1.4.3 (4.5:1 required; 16px Bold is not large text).",
              "decided": "2026-08 by Kate",
              "reason": "Brand consistency with the shipped production site.",
              "rejected": "Navy on green = 6.02:1, passes at zero cost — rejected to match production.",
              "remediationLever": "If AA is ever required: darken the green to #36845D, never revert the text to navy."
            }
          }
        }
      },
      "radius": { "$value": "{dimension.radius.pill}" }
    }
  }
}
```

The deviation record is byte-for-byte your v3.1 content — it just lives on the component token that
carries the risk. Anyone reading `button.primary.label` sees immediately that it overrides the safe
default, why, what it costs, and how to fix it. Far better than the reader having to cross-reference a
color-block footnote.

---

## The hard case: the font model

This is the one mapping Claude Code is most likely to get wrong, so it's specified exactly. Your
five-named-families model maps cleanly onto DTCG's `typography` composite — and your v3.1 `boldFlag`
field turns out to *be* the DTCG `fontWeight`, which is quiet confirmation the v3.1 work was right.

```json
{
  "typography": {
    "$type": "typography",
    "h2": {
      "$value": {
        "fontFamily": "{fontFamily.extrabold}",
        "fontWeight": 400,
        "fontSize":   { "value": 40, "unit": "px" },
        "lineHeight": 1.2,
        "letterSpacing": { "value": -0.01, "unit": "em" }
      },
      "$extensions": { "com.thiswaay.brandkit": { "boldFlag": false, "status": "production",
        "note": "fontWeight 400 is deliberate: 'Axiforma ExtraBold' is a family declared at normal. Requesting 700 here would synthesize a fake bold ON TOP of an already-bold family." } }
    },
    "button": {
      "$value": {
        "fontFamily": "{fontFamily.regular}",
        "fontWeight": 700,
        "fontSize":   { "value": 16, "unit": "px" },
        "lineHeight": 1.5
      },
      "$extensions": { "com.thiswaay.brandkit": { "boldFlag": true, "status": "production",
        "note": "The ONE real-bold case: the 'Axiforma' family HAS a genuine Bold member, so 700 resolves to true Bold, not a synthesis." } }
    }
  }
}
```

**The rule, mechanically:** `boldFlag: false` → `fontWeight: 400` (for the name-carried cuts —
Medium, SemiBold, ExtraBold — which have no bold member). `boldFlag: true` → `fontWeight: 700`, valid
*only* on `fontFamily.regular` (the "Axiforma" base family, which does have a real Bold). `build_theme.py`
reads `fontFamily` + `fontWeight` straight out of the composite and the PPTX/CSS/Figma output is
correct with no special-casing. The trap is encoded, not documented.

---

## What this preserves from This Waay v3.1 — nothing excellent is lost

| v3.1 feature | Where it goes |
|---|---|
| descriptive vs prescriptive | `$extensions.…status: production \| proposed` |
| `v3Correction` / `removed2026_08` audit trail | `$extensions.…provenance[]` on the affected token |
| accepted deviation record | `$extensions` on the component token (shown above) |
| `familyName` / `boldFlag` | map to `fontFamily` / `fontWeight` in the typography composite |
| the `use` prose | `$description` (DTCG's native field for exactly this) |
| `knownTypo` (`#54b886`) | `$extensions` note on `color.green.500` |
| RELATIONSHIP.md, two-brand separation | unchanged — each brand is its own DTCG file |

---

## Migration: flat → tiered, without a fork

The worry you named — "don't let greenfield mean differently-shaped" — is resolved structurally:

- **This Waay** (flat today): populate all three tiers. Its hand-picked palette becomes primitives;
  the `use` prose tells you which semantic role each maps to; the extracted component values become
  tier 3. A one-time adapter, not a rewrite.
- **Greenfield client** (no tokens): author top-down — pick primitives, define the *same standard
  semantic role set*, wire components. Cleaner, because spec and site are born from one source.
- **Mature client** (already tiered): arrives in roughly this shape; you map their names to the
  standard role vocabulary.

All three produce the **identical schema**. Flat-vs-tiered stops being a fork and becomes a
*fill-level*. Every downstream Skill, `build_theme.py`, `validate.py`, the `.potx` pipeline, the page
recipes — all read one shape and are brand-agnostic by construction. **That shared semantic
vocabulary is the actual product** — more than any single brand's values.

---

## How this changes Phase 3

Phase 3 was "plumbing." With a tiered source it sharpens into one clear job: **a resolver that
flattens tiers → target formats.** `build_theme.py` generalizes from "read flat tokens, emit PPTX
theme" into "resolve references, emit {CSS custom properties, PPTX theme, Figma variables, DTCG
export}." `validate.py` gains a new and stronger check: **every `{reference}` resolves, and no text
role resolves to a fill-only primitive** — i.e. the anti-drift rules become automated invariants, not
prose. This is a better Phase 3 than the flat version would have produced. Getting the schema right
now is what makes it so.

---

## Decisions — LOCKED 2026-08-13

All five resolved with Kate. These are now schema law; Claude Code builds to them.

### 1. `$extensions` namespace → `x.brandkit` (provisional)
The product is unnamed. `x.` is the recognized "vendor-specific, not a real domain" prefix, so it
can't be mistaken for a claim. It's a deliberate rename target. **Single-source it:** define the
string once as a `NAMESPACE` constant that `build_theme.py`, `validate.py`, and every Skill import;
document it as the find-replace target for token files. When the product is named and its domain
registered, the rename is one config change plus a mechanical sweep — not archaeology.

### 2. Primitive naming → numeric scale, gaps allowed
`green.400/500/700`, `navy.900/950`, etc. Industry default; maps 1:1 onto a mature client's full
ramp with zero renaming — the right bet given the growth-stage-scaling-to-enterprise market.
**Populate only the steps that exist**; do not invent intermediate steps to fill the scale (no
fictional `green.600`). Empty steps read as "unused," not as lies.
**Migration requirement:** assign each step from a *measured* L\* value, sorted within its hue
family — not eyeballed. The numeric values shown in Tiers 1–3 of this doc were estimated by eye and
must be re-seated against real lightness before they calcify, or a client's ramp maps onto a
mis-seated step.

### 3. Semantic vocabulary → middle path (lean + 4)
The standard role set every client inherits. Additions marked `(+)`:

```
surface.*   ground · ground-deep · ground-light · raised(+) · sunken(+)
fill.*      action · accent · emphasis · success(+) · info · danger · subtle(+)
text.*      body · on-ground · accent · accent-alt · link(+) · muted · on-fill · danger
border.*    subtle
```

- `text.link` — interactive text, split from decorative `text.accent`. Wire to a `.700` primitive so
  it inherits the accessible-ink protection by default.
- `fill.success` — split from `emphasis` on *meaning*; value may point at the same primitive today,
  but the roles must not share a name or they collide the moment success ≠ punch.
- `surface.raised` / `surface.sunken` / `fill.subtle` — the elevated-panel and recessed-zone roles
  data-dense SaaS needs constantly.

Stop here. No `text.disabled`, no `surface.overlay`, no full state matrix — those vary by client and
would be speculative.
**Naming convention:** hyphenated-compound, everywhere (`on-fill`, `ground-deep`). Never camelCase.
Apply to all future role names so a generator never has to guess `onFill` vs `on-fill`.

### 4. Gradient angle → sibling `number` primitive
Angle varies per client, so it's a design variable and belongs in the token tree, not `$extensions`.

```json
{ "angle": { "$type": "number",
  "diagonal": { "$value": 135, "$description": "degrees clockwise from vertical" } } }
```

The gradient composite references it: `"x.brandkit": { "angle": "{angle.diagonal}" }`. Angles are
**bare numbers meaning degrees** (DTCG has no `deg` dimension unit; a plain `number` is the
spec-honest form). **Build-layer note:** a gradient cannot render from its DTCG value alone —
`build_theme.py` composes stops + angle into the actual `linear-gradient(...)` / PPTX fill. Gradient
rendering is a build-layer composition, not a naive token read; no off-the-shelf DTCG tool will
produce it correctly on its own.

### 5. Component tier → full, with governed cleanup
Tokenize the complete component set now (button, card ×all, badge, track, …), not just the stable
three. Rationale: build the *product's* tier-3 story, don't enshrine This Waay's 13-card mess.

**But every retiring variant ships its status from the first commit** — no dead tokens left
reachable (that's the `#8CA7B9` failure mode: a value that outlived its decision):

```json
"$extensions": { "x.brandkit": {
  "status": "deprecated", "supersededBy": "card.standard",
  "note": "One of 13; consolidating to 3. Reference only, not for new generation." } }
```

**New validator invariant (the strongest in the system):** a generator may select only
`status: production` tokens. `deprecated` and `proposed` are readable for reference but never
selectable for output. This turns "clean up later" from a promise into an enforced state — cleanup
becomes flipping a status, reversible and auditable, and cruft cannot leak in the interim.
This pattern *is* the output shape of the future `brand-audit` Skill: everything tokenized, cruft
marked `deprecated` + `supersededBy`, only the clean set selectable. This Waay's 13→3 is the worked
example for every client who arrives with an overgrown system.
