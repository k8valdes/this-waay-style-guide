# This Waay Product Design Studio — Brand & Style Guide

The canonical source of truth for This Waay Product Design Studio's visual and verbal identity. One brand, documented in three forms.

This folder lives inside `Branding/`, the shared home for both This Waay brands. See `../index.html` for the umbrella landing page and `../RELATIONSHIP.md` for how this brand relates to its sibling, Gridmark Partners — the two design systems are maintained independently, not merged.

| File | Audience | Use |
|---|---|---|
| **`STYLE.md`** | AI tools + humans | Lean, readable rules. Paste into any AI project as context. Start here. |
| **`tokens.json`** | AI tools + code | Exact machine-readable values (color, type, spacing, motifs). |
| **`LOGO.md`** | AI tools + humans | Logo usage rules (draft — some values pending). |
| **`index.html`** | Humans | Rendered living style guide — see everything applied. View via Pages. |
| **`/assets`** | Both | Official SVGs (logo, plane mark). Lift these verbatim; don't redraw. See `LOGO.md` for usage rules. |

## Using this in another AI project

- **Most reliable:** paste the contents of `STYLE.md` (and `tokens.json` if values matter) directly into the project's context or system prompt.
- **By URL:** point a web-fetching tool at the raw file URL, e.g. `https://raw.githubusercontent.com/k8valdes/this-waay-design-system/main/product-design-studio/STYLE.md`.

## Scope

This repository contains **visual brand expression only** — colors, type, components, illustration, and motifs. It intentionally excludes pricing, positioning, business strategy, voice & tone guidelines, and any client-confidential material — those live in private studio documents.

## Maintaining

This is a living document. When a brand decision changes, edit the source files, bump the version line, and commit with a short note. Git history is the changelog.

_Current version: 2.3 · July 2026_
