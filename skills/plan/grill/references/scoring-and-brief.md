# Problem Sizing, Solution Scoring & Decision Brief

Load this reference in every `grill` session. It defines how to measure the problem, score competing options, enforce Observability & Security by Design, and close the interview.

## 1. Measure the Problem First (4-Axis Profile)

Before proposing options for a branch, classify the real problem — never hypothetical 5-year scale:

| Axis | Measure concretely | Sets what |
| :--- | :--- | :--- |
| **Magnitude** | Current volume, users, RPS, data size, frequency (+ realistic near-term horizon) | Performance & architecture ceiling |
| **Blast Radius** | If this fails, who/what breaks? (dev script vs internal tool vs prod revenue/data) | Required safety, redundancy & rollback |
| **Reversibility** | *Two-way door* (easy/cheap to change later) vs *One-way door* (schema, public API, migration) | Depth of upfront rigor needed |
| **Lifespan** | Throwaway / short-term experiment vs internal long-lived vs core platform | Justifiable engineering investment |

## 2. Compete Solutions Against the Problem (Pugh Matrix)

For every non-trivial decision, pit **2–3 concrete options** against each other. **Rule: Option A MUST be the Baseline Simple** (minimum technically solid, zero-debt path).

Score each option `1–5` with 1-line factual justification (never vague adjectives):

| Criterion | What it measures | Scoring rule |
| :--- | :--- | :--- |
| **Problem Fit (No-Overkill)** | Proportionality to the 4-axis Problem Profile | Penalizes **both** under-sizing AND over-sizing. Unjustified layers/services lose points. |
| **Low Friction** | Effort to build, test, deploy, operate, and understand in 5 minutes | Lower friction & smaller change surface = higher score. |
| **Zero Tech Debt** | Does it leave hacks, hidden coupling, or deferred cleanup? | **Target = 0 debt.** Avoidable debt scores `1` or disqualifies the option. |
| **Technical Solidity** | Invariants, error handling, edge security, and built-in observability | Must pass minimum bar; fragile shortcuts are disqualified. |
| **Evolutionary Exit** | If the problem grows 10x later, can this evolve cleanly without a rewrite? | Rewards simple-today designs with clean seams. |

### Burden-of-Proof & Synthesis Rules
- **Default winner:** The simplest, lowest-friction option that passes Technical Solidity and Zero Tech Debt.
- **Complex option burden:** You may recommend a heavier option **only** if you demonstrate concretely where Baseline Simple fails the measured Problem Profile.
- **Conceptual Crossover:** If Option A wins on simplicity and Option B wins on one critical requirement, check whether you can **combine the winning trait of B into A** without bloat before picking either raw option.
- **Mandatory Breakpoint:** Every recommendation must state: *"Choose [Winner]; switch to [Alternative] only if [concrete threshold/condition changes]."*

## 3. Observability & Security by Design Gate (Required Before Closing)

In the agentic era, code is iterated faster than humans read every line. Systems that fail silently or lack guardrails are unacceptable technical debt. Define all three **proportionally to the problem size**:

| Problem Tier | Out-of-the-Box Logs | Out-of-the-Box Metrics | Security by Design |
| :--- | :--- | :--- | :--- |
| **Script / CLI** | Structured `stderr` logs with clear error causes & exit codes | End-of-run summary counters (processed, failed, duration) | Never log env/secrets; validate CLI args & file paths |
| **Service / API** | Structured JSON logs with `correlation_id`, entity IDs, state transitions | RED metrics (Rate, Errors, Duration) + key business counters + `/health` | Strict input validation, authn/authz (least privilege), timeouts, fail-closed |
| **Core / High-Impact** | All of the above + immutable audit trail of state mutations | SLI/SLO tied to CUJs + distributed traces + actionable alert thresholds | Threat model (STRIDE), secret redaction at boundary, blast-radius isolation |

Always state an explicit **Never-Log List** (tokens, secrets, passwords, raw PII/customer payloads).

## 4. Decision Brief (Closing Output)

End the grill with a scannable brief ready for native IDE Plan Mode or implementation:

```markdown
# Decision Brief: <Feature / Change>
- **Domain(s):** Backend / Frontend / AI / Infra
- **Problem Profile:** Magnitude · Blast Radius · Reversibility · Lifespan
- **Frameworks Used:** (max 1–2, e.g., 4 Value Levers + CUJ)

## Decisions Made
1. **<Decision>:** Chose **<Option>** — <1-line measured reason>. *Breakpoint:* revisit if <threshold>.

## Rejected (Overkill or Debt)
- **<Option>:** Rejected because <concrete excess complexity or debt>.

## Observability & Security Contract
- **Logs:** <structured events + correlation key> | **Never log:** <list>
- **Metrics:** <health + business signals>
- **Security:** <input/authz/fail-closed boundaries>

## Acceptance Criteria & Next Step
- [ ] <Observable, testable outcome>
- **Next:** <Native Plan Mode / `spike` / `evolve` / `build`>
```
