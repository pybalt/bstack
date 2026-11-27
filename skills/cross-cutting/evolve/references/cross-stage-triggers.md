# Cross-Stage Triggers & Evolution Report

`evolve` has one canonical home (cross-cutting layer) and is invoked selectively from other lifecycle stages only when its Entry Gate passes.

## 1. Cross-Stage Trigger Matrix (IF / THEN)

| Calling Stage / Skill | Allowed Trigger | Hard Guardrail |
| :--- | :--- | :--- |
| **`plan` (`grill`)** | Two candidate designs tie with opposite strengths AND the decision justifies empirical benchmarking. | For non-empirical design choices, use lightweight **conceptual crossover** inside `grill` instead of running full `evolve`. |
| **`plan` (`spike`)** | A comparison spike (`002a` vs `002b`) reveals both approaches win on different axes and a hybrid could beat both. | Only promote from `spike` to `evolve` once an automated, immutable fitness script exists. |
| **`build` / `review`** | Working baseline exists (algorithm, SQL query, LLM prompt, caching strategy, hot path) and we need a measurable jump in quality, latency, or cost without adding debt. | Never skip the Baseline Simple benchmark; reject any offspring that inflates maintenance burden. |
| **`debug` (`systematic-debugging`)** | **Phase 4 ONLY:** root cause is proven, a red regression test exists, and the fix is an optimization problem (perf, memory, accuracy) with multiple competing approaches. | **HARD BLOCK in Phases 1–3.** Never evolve blind patches over an undiagnosed bug (prevents symptom masking & reward hacking). |

## 2. Evolution Report (Closing Output)

Summarize the run concisely (or render via **`visual-brief`** as a Pareto + Lineage view when there are ≥ 3 generations or complex trade-offs):

```markdown
# Evolution Report: <Target EVOLVE-BLOCK>
- **Fitness Vector:** <Metric 1> · <Metric 2> · <Parsimony / Complexity>
- **Islands / Families Used:** Baseline + <e.g., Anthropic / Gemini / GPT (or isolated paradigms)>
- **Generations Run:** <N> | **Stop Reason:** <Target met / <5% plateau / Budget cap>

## Pareto Frontier (Baseline vs Survivors)
| Candidate | Origin / Lineage | Primary Metric | Secondary Metric | Complexity / LOC | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `gen0-base` | Baseline Simple | ... | ... | ... | Baseline |
| `gen0-a` | Island A (Family X) | ... | ... | ... | Parent |
| `gen0-b` | Island B (Family Y) | ... | ... | ... | Parent |
| `gen2-c1` | Crossover(`gen0-a` × `gen0-b`) | ... | ... | ... | **Winner** |

## Winning Genes Combined
- From `gen0-a`: <concrete mechanism>
- From `gen0-b`: <concrete mechanism>

## Dead Ends Discarded (Anti-Bloat / Failed)
- `gen1-x`: <why it failed or added bloat>

## Next Step
- Promote `<Winner>` to `<target file>`, remove experiment harness, verify full test suite.
```
