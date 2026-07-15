# How This Waay Product Design Studio and Gridmark Partners relate

This Waay is the umbrella brand. **Product Design Studio** is its original, primary expression. **Gridmark Partners** is a civic-sector sibling brand — Gridmark's own in-page changelog notes it was "realigned to This Waay v1.7 exact tokens" early on, so the two systems share a common visual origin.

Since then, each has evolved independently. **This is intentional**: the two design-system documents are maintained as separate, standalone files, each with its own embedded token block. Nothing here is enforced by code — this file exists so a future editor of either doc can tell, at a glance, what's a deliberate brand difference versus something that just drifted and might be worth a look.

## Intentionally identical today

Both docs carry these forward from the same origin:

- Navy (`#0C2A48`), Waay Green (`#54B987`) + punch green (`#3DD68C`), teal (`#0BABAB`), steel (`#0D698A`), slate (`#8DA3B5`), mint (`#EEF8EC`), ice (`#F2FBFB`) — identical hex in both.
- Typography stack: `'Axiforma', 'Poppins', 'Segoe UI', sans-serif`, same 400/500/600/700 weight scale.
- 8px spacing rhythm, 14px card radius, pill (999px) button radius, `clamp(56px,8vw,110px)` section padding.
- Content measure of 1080px (This Waay's `.wrap` is `max-width: 1080px` directly; Gridmark's `.wrap` is `max-width: 1120px` but that includes outer drop-shadow chrome around a separate `--container: 1080px` content token) — same underlying content width, expressed differently. Don't "fix" this to make the two `.wrap` values match; they're already describing the same thing correctly.
- General motion philosophy: purposeful, directional, respects `prefers-reduced-motion`.

## Intentionally different, kept independent by design

- **Accessible text colors vs. status colors** — This Waay defines accessible "ink" variants for using saturated brand hues as readable text on light backgrounds (`--tw-green-ink #2C6D4D`, `--tw-teal-ink #077373`, `--tw-ink-muted #5C7185`, `--tw-no #D86A5A` / `--tw-no-ink #A53727`). Gridmark defines status colors for form/alert UI state (`--success-500 #2E7D55`, `--warning-500 #B7791F`, `--danger-500 #B23A2E`, `--info-500 #0D698A`). These solve adjacent but different problems and are not the same token, even where values are close — e.g. This Waay's `greenInk` (`#2C6D4D`, verified 6.2:1 contrast) and Gridmark's `success-500` (`#2E7D55`) are two different, independently-verified values. Treat this as a deliberate non-merge, not an oversight to reconcile.
- **Brass** (`--brass-500 #C8A46B` + `--accent-civic`) — Gridmark's civic-only accent. This Waay has no equivalent.
- **Coral** (`#F2A08D`) — This Waay's illustration-only accent (paper-cut landscape motif). Gridmark's doc doesn't define or use it.
- **Focus ring** — This Waay uses `outline: 3px solid var(--tw-green-ink)` (`outline-color` swaps to `--tw-green-bright` on dark grounds). Gridmark uses `box-shadow: var(--focus-ring)` (`rgba(84,185,135,.55)`, with a `--focus-ring-inverse` for dark grounds). Both meet WCAG AA; each is that brand's own implementation choice.
- **Token architecture** — Gridmark documents an explicit 3-layer model (Primitives → Semantic → Component) with a 4-step elevation scale, z-index scale, and named motion durations/easings (`--dur-fast/base/slow`, `--ease-standard/decelerate/accelerate`). This Waay's token block is flatter, with a single ad hoc card shadow and no named durations (motion timing is described in prose instead: "micro," "element," "reveal"). Each reflects that doc's own authoring history.
- **Type scale shape** — This Waay has a fully consolidated 10-step UI text scale (`--tw-text-2xs` … `--tw-text-5xl`). Gridmark's doc uses a mix of named type-scale classes (`.t-h1`, `.t-body`, etc.) and some ad hoc px values in component CSS. Not reconciled here.

## If a future project wants to actually unify these

This file is the starting map of what's already shared vs. what's a real brand distinction. Nothing here is a blocker to true unification later — it just means today's project is a relocation and documentation effort, not a token merge.
