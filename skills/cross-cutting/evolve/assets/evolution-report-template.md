# Evolution Report: <Target EVOLVE-BLOCK>

- **Date:** YYYY-MM-DD
- **Fitness Vector:** `<Metric 1 (max/min)> · <Metric 2> · <Parsimony / Complexity (min)>`
- **Islands / Model Families:** Baseline + `<Anthropic / Gemini / GPT or isolated opposing paradigms>`
- **Generations Run:** `<N>` | **Stop Reason:** `Target met | <5% plateau (pareto_rank.py) | Budget cap`

## Pareto Frontier (Baseline vs Survivors)
| Candidate | Lineage / Island | Primary Metric | Secondary Metric | Complexity / LOC | Pareto Front | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| `gen0-base` | Baseline Simple | ... | ... | ... | ... | Baseline |
| `gen0-a` | Island A (`<family>`) | ... | ... | ... | ... | Parent |
| `gen0-b` | Island B (`<family>`) | ... | ... | ... | ... | Parent |
| `gen2-c1` | Crossover(`gen0-a` × `gen0-b`) | ... | ... | ... | **1** | **Winner** |

## Winning Genes Recombined
- From `gen0-a`: `<concrete mechanism>`
- From `gen0-b`: `<concrete mechanism>`

## Dead Ends Discarded (Anti-Bloat / Failed Cascade)
- `<candidate>`: `<why rejected — bloat, dominated, or failed stage N>`

## Promotion & Closure
- Promote `<Winner>` into `<target path>`, delete quarantine harness, run `qa-verify`, and record winning rationale + dead ends in cross-session memory (e.g., Engram).
