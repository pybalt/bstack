---
name: spike
description: "Use when running fast, timeboxed, quarantined throwaway experiments to validate technical feasibility, compare approaches (A vs B), or resolve unknowns that reading docs or code cannot answer before committing to a build. Do not use for production implementation or questions answerable from existing docs/code."
version: 2.0.0
author: Leonel Baltazar Bravo
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [spike, prototype, experiment, feasibility, throwaway, timebox, proof-of-concept]
    related_skills: [grill, evolve, visual-brief, onboarding]
---

# Spike (Timeboxed, Quarantined Feasibility Experiments)

Validate high-risk technical unknowns with disposable, observable prototypes before committing to a real build. Throw spikes away once they have paid their uncertainty debt.

## When to Use — and When NOT to Use

- **Use when:** testing *"is X actually possible?"*, comparing two unfamiliar libraries/APIs (`002a` vs `002b`), measuring real latency/limits, or resolving an unmeasurable uncertainty surfaced during `grill`.
- **Do NOT use when:** the answer is knowable by reading docs or inspecting the codebase, the work is production code (move to the `build` stage), or you already have a working baseline and want multi-generation optimization (use `evolve`).

## Progressive Disclosure

- Load `references/templates.md` when decomposing multi-spike plans, formatting Given/When/Then tables, writing head-to-head comparisons, or running Frontier Mode.

## Core Loop

```text
Decompose (risk-first) -> Align -> Brief Research -> Quarantined Build -> Verdict
```

1. **Decompose (2–5 questions max, ordered by risk):** Frame each spike as a specific, observable **Given / When / Then** question. Run the spike most likely to kill the idea **first**. Skip decomposition only if the user already named a single exact spike.
2. **Align + Timebox:** For multi-spike sets, show the table + timebox per spike and confirm order before writing code.
3. **Brief Research:** Before coding a spike, compare credible candidate tools/approaches (2–3 lines, pros/cons, maintenance status) and state why you picked one (or spawn `a`/`b` comparison variants). Skip research for pure logic with no external deps.
4. **Quarantined Build (Observable & Honest):**
   - Put every spike in its own isolated folder: `spikes/NNN-slug/` with a `README.md` and minimal runnable code.
   - **Strict quarantine:** NEVER modify production `src/`, lockfiles, or shared config during a spike. Hardcode inputs and avoid build/Docker/config ceremony unless the spike specifically tests it.
   - **Make it tangible:** Prefer (1) runnable CLI with concrete output, (2) minimal interactive HTML, (3) single-endpoint server, (4) crisp assertion test — never a meaningless `"it works"` log.
   - **Test edge cases:** Never declare `VALIDATED` after a single happy-path run; probe failure modes and boundaries.
   - **Parallel comparisons:** For `002a` vs `002b`, run isolated subagents in parallel when both need real effort, then write one head-to-head verdict.
5. **Verdict (`VALIDATED` | `PARTIAL` | `INVALIDATED`):**
   - Record concrete evidence, what worked, what failed, surprises, and recommendation for the real build in `spikes/NNN-slug/README.md`.
   - `INVALIDATED` with clear proof is a **successful spike** — it just saved days of wasted build.

## Clean Handoffs

- Return verified verdicts to **`grill`** to finalize the architectural Decision Brief.
- If a comparison spike (`002a` vs `002b`) shows both approaches win on different measurable axes and you have an automated benchmark → promote to **`evolve`** to synthesize a hybrid via genetic crossover.
- Delete or archive `spikes/` once decisions are promoted into the real implementation.
