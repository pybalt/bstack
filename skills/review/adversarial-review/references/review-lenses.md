# Adversarial Review Lenses, Triage & Bounded Correction

Load this reference when executing an adversarial diff review.

## 1. The 4 Adversarial Lenses (Run All 4 Against the Frozen Diff)

Adopt a *red-team* mindset: assume a subtle bug, security flaw, or unnecessary abstraction exists until disproven by evidence in the diff.

| Lens | Red-Team Attack Questions |
| :--- | :--- |
| **1. Correctness & Spec** | Does every acceptance criterion map to real code? What breaks on `null`/empty/unicode/max-size/duplicate/retry/out-of-order inputs? Did the diff alter behavior outside stated scope? Are docs/specs reconciled? |
| **2. Security & Privacy** | Can an untrusted caller spoof identity, bypass authz, escalate privilege, inject SQL/shell/HTML/prompt text, or exhaust resources (missing bounds/timeouts)? Are any secrets, tokens, or PII written to logs, errors, client bundles, or git? |
| **3. Simplicity & Zero-Debt (*Simplify*)** | Is there premature abstraction, wrapper bloat, duplicated logic, dead code, or a complex pattern where a simpler standard primitive works? Does the change leave hidden coupling or TODO debt? |
| **4. Observability & Failure Modes** | If an external dependency times out or returns garbage, does it fail closed with actionable structured logs (`correlation_id`, cause) and increment error metrics — or fail silently? |

## 2. Severity Triage (Blocking vs Non-Blocking)

| Level | Criteria | Action |
| :--- | :--- | :--- |
| **BLOCKING** | Functional bug, unhandled edge case on risky path, spec mismatch, security/privacy vulnerability, missing mandatory observability on failure paths, or clear avoidable tech debt / bloat. | Must fix before `qa-verify` receipt can pass. Cite exact `file:line`, concrete failure scenario, and minimal fix. |
| **NON-BLOCKING** | Minor readability tweak, optional micro-optimization, naming preference, or follow-up idea outside current scope. | Record concisely in the report without halting delivery. Never let nitpicks block a clean change. |

## 3. Bounded Correction Protocol

To prevent endless review-fix thrashing:
1. **Pass 1:** Author applies minimal, surgical fixes addressing **only** `BLOCKING` findings (strict scope cap — no unrelated refactors).
2. **Re-inspect diff delta:** Reviewer checks the delta against the original blocking items and confirms zero new regressions were introduced.
3. **Pass 2 (Final Cap):** Allowed only if Pass 1 left a narrowly isolated residual issue.
4. **Hard Escalation:** If `BLOCKING` findings still remain after Pass 2 (or if fixing them expands scope beyond the original change) → **HALT** and escalate to the human with both findings and non-blocking notes visible.

## 4. Adversarial Review Report Format

```markdown
# Adversarial Review — <branch / slice>
- **Diff Fingerprint:** `<HEAD-sha>` | `<diff-sha256-short>`
- **Reviewer Context:** Fresh context | Model family: `<family>` (Author ≠ Reviewer: Yes/No)
- **Verdict:** APPROVED | CHANGES_REQUESTED (Pass <1|2> of 2) | HALTED_ESCALATE

## Blocking Findings (<N>)
1. **[<Lens>] `<file:line>`** — <concrete failure mode / vulnerability / bloat>. *Minimal fix:* <1 line>.

## Non-Blocking Notes (<N>)
- `<file:line>`: <optional improvement — does not block merge>

## Simplify Wins Checked
- <Confirmed lean / or exact complexity pruned>

## Next Step
- <If APPROVED -> run `qa-verify` on this exact fingerprint. If CHANGES_REQUESTED -> bounded Pass N, then re-verify.>
```
