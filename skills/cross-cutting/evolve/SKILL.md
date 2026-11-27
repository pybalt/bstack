---
name: evolve
description: "Use when optimizing or enhancing an existing algorithm, prompt, query, architecture, or UX against objective measurable metrics by generating structurally diverse solutions (ideally across distinct model families) and recombining winning genes via evolutionary crossover. Do not use without measurable fitness metrics, for trivial changes, or before root cause is isolated in debugging."
version: 1.0.0
author: Leonel Baltazar Bravo
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [evolve, genetic-crossover, evolutionary-search, map-elites, pareto, optimization, enhancement, multi-model]
    related_skills: [grill, spike, visual-brief, systematic-debugging, environment]
---

# Evolve (Multi-Family Evolutionary Crossover Optimization)

Synthesize superior solutions by evolving **structurally diverse candidates** (preferring **distinct model families** — Anthropic, Gemini, GPT — whenever available), scoring them with an **immutable evaluator**, and performing **semantic crossover** of winning genes under strict anti-bloat control.

## Hard Entry Gate (ALL 3 Required — Otherwise Do NOT Use)

```text
1. Measurable fitness exists?   (Automated benchmark, eval suite, perf/cost metric, or strict rubric)
2. Baseline Simple exists?      (Already measured, and still short of target or facing multi-objective trade-offs)
3. Value justifies compute?     (High-leverage hot path, core prompt, critical query, key algorithm/UX)

IF any condition is FALSE -> STOP. Use normal implementation, `grill`, or `spike` instead.
IF debugging and root cause is NOT yet proven -> HARD BLOCK. Run `systematic-debugging` Phases 1–3 first.
```

## Progressive Disclosure Protocol

| Need | Load ONLY this file | Inside |
| :--- | :--- | :--- |
| Full evolutionary loop (Cascades, Cross-Family Islands, Pareto, Parsimony, Crossover) | `references/evolution-protocol.md` | Always load before running Gen 0 |
| Cross-stage handoffs (`grill`, `build`, `review`, Debug Phase 4) & Evolution Report | `references/cross-stage-triggers.md` | Integration triggers + report template |

## Non-Negotiable Operating Laws

1. **Immutable evaluator, isolated `EVOLVE-BLOCK`.** Never let candidate generators modify the test harness, metrics, or benchmark inputs (prevents *reward hacking*).
2. **Maximum structural diversity first — prefer distinct model families.** Seed Gen 0 with **3–4 genuinely orthogonal paradigms** (always keeping **Baseline Simple** as Species 0). Whenever multiple model families (Anthropic, Gemini, GPT) are available AND allowed by the active **Privacy Tier** (`environment`), run Gen 0 islands on **different model families** in isolation so shared training biases don't collapse diversity.
3. **Novelty rejection before evaluation.** Reject cosmetic variations of an already-evaluated candidate before spending benchmark/eval budget.
4. **Cascaded evaluation (cheap → expensive).** Filter broken or weak candidates in milliseconds (syntax/smoke) before running medium cases and full benchmarks.
5. **Reflective semantic crossover, not blind splicing.** Feed the next generation **execution artifacts** (traces, profiler bottlenecks, failing edge cases) + **lineage dead ends** so crossover explicitly combines *the winning gene of Parent A* with *the winning gene of Parent B*.
6. **Parsimony pressure (anti-Frankenstein law).** Treat **simplicity / code size / zero tech debt** as an explicit Pareto objective. An offspring that merges complexity from A + B without a clear net Pareto win is **discarded**.
7. **Hard stopping gate.** Stop when target fitness is met, when 2 consecutive generations gain `< 5%` on the Pareto frontier, or at the generation budget cap (default: **2–3 generations**).
