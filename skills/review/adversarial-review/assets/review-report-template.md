# Adversarial Review — <branch / slice>

- **Diff Fingerprint:** `<HEAD>:<diff-hash>` (from `scripts/diff_stats.py`)
- **Diff Size & Risk:** `<files> files · <LOC> LOC` (ODD cap 400: `OK | EXCEEDED`) · Risk Overrides: `<none | list>`
- **Reviewer Context:** Fresh context · Model family: `<family>` (Author ≠ Reviewer: `Yes | No`)
- **Verdict:** APPROVED | CHANGES_REQUESTED (Pass `<1|2>` of 2) | HALTED_ESCALATE

## Blocking Findings (<N>)
1. **[<Correctness | Security | Simplicity | Observability>] `<file:line>`** — `<concrete failure mode / vulnerability / bloat>`.
   - *Minimal fix:* `<1 line>`

## Non-Blocking Notes (<N>)
- `<file:line>`: `<optional improvement — does not block merge>`

## Simplify & Zero-Debt Check
- `<Confirmed lean / exact dead code or overengineering pruned>`

## Next Step
- `<If APPROVED -> run qa-verify on this exact fingerprint. If CHANGES_REQUESTED -> bounded fix pass, then re-verify.>`
