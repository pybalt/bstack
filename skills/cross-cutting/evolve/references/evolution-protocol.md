# Evolutionary Crossover Protocol (MAP-Elites + Pareto + Cross-Family Islands)

Synthesizes proven mechanics from AlphaEvolve, FunSearch, OpenEvolve, ShinkaEvolve, GEPA, MAP-Elites, and NSGA-II into a practical workflow for coding agents.

## 1. Lock the Fitness Contract & Evaluation Cascade

Before generating any candidate:

1. **Mark the `EVOLVE-BLOCK`:** Isolate the exact function, query, prompt, or module under evolution. Keep the evaluator script, golden dataset, and assertions **read-only / immutable**.
2. **Define a multi-objective fitness vector (Pareto, not a single misleading float):**
   - Primary metric(s): e.g., accuracy/eval pass rate, p95 latency, throughput, token cost.
   - **Mandatory Parsimony axis:** complexity / LOC / dependency count / zero tech debt.
   - **Hard constraints (disqualifiers):** correctness invariants, security rules, observability signals intact.
3. **Build a 3-stage Evaluation Cascade:**
   - *Stage 1 (ms):* syntax/typecheck + smoke tests + invariant checks (kills broken candidates immediately).
   - *Stage 2 (seconds):* representative edge-case subset.
   - *Stage 3 (full):* complete benchmark / eval suite / profiler — **run only on Stage 2 survivors**.

## 2. Generation 0 — Cross-Family Orthogonal Islands

Generate **3–4 structurally different paradigms** in isolated contexts (each island sees ONLY the problem spec, `EVOLVE-BLOCK`, and fitness contract — **never** the other islands' solutions):

- **Species 0 (Mandatory):** Current **Baseline Simple** (measured first to set the bar).
- **Islands 1..3 (Distinct Model Families whenever available):**
  - Check available agent CLIs/providers (`delegate` stage: e.g., Anthropic / Claude, Google / Gemini, OpenAI / GPT-Codex) **AND verify the `environment` Privacy Tier** (never send Tier A/sensitive code to a non-ZDR model family).
  - Assign each island to a **different model family** AND/OR an **explicitly opposing algorithmic/design paradigm** (e.g., Island 1: streaming/incremental; Island 2: indexed/precomputed; Island 3: declarative/rule-driven).
  - **Single-family fallback:** If only one model family is available/permitted, isolate islands via separate subagents with **incompatible forcing constraints** so they cannot converge to the same pattern.
- **Novelty Rejection Gate:** Before evaluating a new candidate, verify it differs structurally (data structure, control flow, prompt strategy, or complexity class) from existing candidates; reject cosmetic rewrites.

## 3. Measure, Archive & Extract "Genes" (Artifact Side-Channel)

For every surviving candidate, capture BOTH:
- **Pareto Vector:** exact scores on every objective + complexity/size.
- **Execution Artifacts (Reflective Credit Assignment):** profiler hotspots, exact failing inputs, error traces, token breakdown — **why** it won in Dimension X and **why** it lost in Dimension Y.
- **Gene Tagging:** Name the 1–2 concrete mechanisms (*genes*) responsible for each strength (e.g., *"Gene A1: single-pass ring buffer"*, *"Gene B2: few-shot schema anchor"*).

Maintain two tiny archives:
- **Pareto + Niche Archive (MAP-Elites):** keep non-dominated solutions plus the best simple representative per paradigm.
- **Dead-Ends Log:** 1-line record of failed mutations/crossovers and why they failed (prevents cyclic regression).

## 4. Generation N — Semantic Crossover + Targeted Diff Mutation

For each next generation (budget: **2–3 generations max** unless user expands):

1. **Select diverse parents:** Pick two elites from **different paradigms / model families** whose strengths cover each other's weaknesses on the Pareto frontier.
2. **Semantic Crossover:** Instruct the synthesizer (ideally a strong reasoning model) with:
   - Parent A + its winning gene(s) + its bottleneck artifact,
   - Parent B + its winning gene(s) + its bottleneck artifact,
   - The Dead-Ends Log,
   - **Rule:** Produce a clean, unified implementation combining the winning genes — **prefer targeted diffs** over full rewrites when refining an elite.
3. **Targeted Mutation:** Optionally spawn 1 focused mutation attacking the #1 profiler/eval bottleneck of the current best Pareto leader.
4. **Parsimony Enforcement (Anti-Frankenstein Gate):**
   - Run the full Evaluation Cascade on offspring.
   - **Survive ONLY IF** the offspring strictly dominates a parent on the Pareto frontier OR opens a materially better simplicity/performance trade-off. If it adds complexity from both parents without a real net win → **kill it and log to Dead Ends**.

## 5. Stopping Gate & Promotion

Stop iterating as soon as **any** condition hits:
- Target fitness vector is met cleanly,
- Two consecutive generations improve `< 5%` on the primary metric without simplifying code, or
- Generation / time / token budget is reached.

Promote the chosen Pareto winner out of the quarantine sandbox into the real codebase with clean tests, zero leftover experiment files, and full suite verification.
