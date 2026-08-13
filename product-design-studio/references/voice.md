# Voice & messaging

The v3.1 `tokens.json` carried **no** voice tokens — voice has always lived outside the token
tree — so nothing was relocated here from the token file. This doc is the pointer the schema's
reference structure expects, so a future `SKILL.md` knows where voice lives.

**Canonical voice source (do not duplicate here):**
- `Context/THISWAAY_CONTEXT.md` §11 — Voice & Tone v2 (the master reference), including the §11.8 de-AI-ification pass and §11.13 checklist.
- `ThisWaay_Voice_Tone_Guidelines_v2.pdf` (repo-local, **git-ignored** — go-to-market strategy; never push).

Non-negotiables that touch any token-adjacent copy (from the project CLAUDE.md):
- Name is always **"This Waay"** — two words, double-a. Never "ThisWaay," "This Way," or "ThisWayUX."
- AI is "layered/integrated **into**" sound systems. "Onto" is critique-only ("layering AI onto fragile foundations").
- Every client-facing draft goes through CONTEXT §11 (Voice & Tone v2).
