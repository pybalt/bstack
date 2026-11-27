# ODD Execution Playbook (Diff Test, Slicing & Built-in Quality)

Load this reference when sizing an implementation task, managing multi-session feature state, or wiring observability, security, and proportionate tests into a slice.

## 1. The Diff Test + Risk Override Gate

Classify every coding request before writing files:

| Path | Condition | Ceremony & Tracking |
| :--- | :--- | :--- |
| **Inline Path** | Understandable and safely reviewable from **prompt + `git diff`** alone, single session, easily reversible, AND **zero Risk Overrides**. | No planning doc. Quick targeted code read → clean edit → fast mechanical & behavioral check → short diff summary. |
| **Tracked Path** | Spans multiple modules/sessions, requires incremental milestones, OR **any Risk Override fires**. | **One** concise resumable tracker (e.g., `odd/tasks/<slug>.md` or the `grill` Decision Brief) + persist key milestones to cross-session memory (e.g., Engram) if available. |

### Mandatory Risk Overrides (Force Tracked Rigor Even for 3-Line Diffs)
- Authentication, authorization, tenant isolation, or secret handling.
- Financial calculations, billing, ledger state, or irreversible external side effects.
- Database schema migrations, data backfills, or public API / event contract changes (*one-way doors*).
- Concurrency, locking, caching invalidation, or retry/idempotency logic.

*If any architectural trade-off is still unclear when a Risk Override fires → pause and run `grill` first.*

## 2. Single Resumable Feature Tracker (Tracked Path Only)

Keep **one** concise file (never 5 separate spec/PRD/design docs) so any fresh session or subagent can resume in 30 seconds:

```markdown
# Feature: <slug>
- **Goal & Outcome:** <1–2 sentences>
- **In Scope / Out of Scope:** <explicit boundaries>
- **Decisions & Constraints:** <links to grill Decision Brief / contracts>
- **Observability & Security:** Logs (`<events>`, never log `<list>`) · Metrics (`<signals>`) · Guardrails (`<boundaries>`)

## Reviewable Slices (~<= 400 LOC each)
- [ ] Slice 1 (Walking Skeleton): <thin end-to-end path + verify command>
- [ ] Slice 2 (Edge cases & hardening): <failure modes + verify command>

## Execution Log & Evidence
- <date/slice>: <what shipped, exact command output, open hazards>
```

## 3. Reviewable Slicing & Simplicity Discipline

- **Walking Skeleton first:** Wire the thinnest working end-to-end slice before expanding edge cases or optimizations.
- **~400 LOC soft cap per review unit:** If a change grows past ~400 lines of meaningful logic, split it into coherent commits/slices that leave the repo green at every boundary.
- **No drive-by refactors:** Keep diffs laser-focused on the active task; note unrelated debt separately rather than polluting the diff.
- **Optimize only after measuring:** Build the Baseline Simple first; if a hot path or prompt misses a measurable target, invoke `evolve` instead of guessing optimizations.

## 4. Out-of-the-Box Observability, Security & Proportionate Testing

Check all three before calling any slice ready for review:

1. **Structured Logs & Metrics:**
   - Emit structured events (`correlation_id`, operation, outcome, `duration_ms`) on key state transitions and all rejected/failed paths.
   - Expose proportional metrics (CLI summary counters, service RED + domain counters, or infra USE metrics).
   - **Never-log check:** Confirm zero tokens, secrets, passwords, or raw PII enter logs or error messages.
2. **Security Boundaries:**
   - Validate and bound untrusted inputs at ingress; enforce authz on the server/resource owner side; apply timeouts to every network/DB call; fail closed on permission or parsing errors.
3. **Proportionate Testing (Behavior Over Dogma):**
   - **High-risk logic / state transitions / bugs:** Automated unit + integration tests covering happy path, boundary inputs, and failure/idempotency paths.
   - **Low-risk glue / thin wiring:** Integration smoke test or type/contract check — avoid brittle mock-heavy unit tests that mirror private implementation details.
   - **UI slices:** Delegate design/polish/a11y/anti-slop checks to `uiux` and verify live states (default, loading, empty, error).

## 5. Self-Reconciliation Before Handoff

Before invoking `adversarial-review` and `qa-verify`:
- Update the single tracker (or `README`/`AGENTS.md` if contracts changed) so documentation reflects what was **actually** built.
- Record durable project lessons, new commands, or resolved pitfalls into cross-session memory (e.g., Engram) if available.
