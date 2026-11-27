---
name: adversarial-review
description: "Use when reviewing staged diffs, pull requests, or completed implementation slices using fresh-context, cross-model adversarial lenses (Correctness, Security, Simplicity/Zero-Debt, Observability) with strict Blocking vs Non-Blocking triage and bounded correction. Do not use as a substitute for running real tests or runtime QA (pair with qa-verify)."
version: 1.0.0
author: Leonel Baltazar Bravo
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [review, adversarial-review, rdd, cross-model, simplify, security, observability, code-review]
    related_skills: [qa-verify, odd-build, delegate, visual-brief, environment]
---

# Adversarial Review (Multi-Lens Cross-Model Diff Inspection)

Defeat single-agent blind spots and *AI sycophancy* by inspecting a **frozen diff** through independent adversarial lenses — actively trying to break the change and prune unnecessary complexity before shipping.

## When to Use — and When NOT to Use

- **Use when:** reviewing any completed `odd-build` slice, PR, refactor, or external diff before `qa-verify` and merge — **mandatory** whenever a Risk Override fired (auth, money, migrations, public contracts, concurrency).
- **Do NOT use as:** a substitute for executing tests or live QA (`qa-verify` proves runtime behavior; `adversarial-review` audits design, logic, security, and simplicity).

## Progressive Disclosure

- Load **`references/review-lenses.md`** before reviewing (4 adversarial lenses, Blocking vs Non-Blocking triage rules, Bounded Correction cap, and the Review Report template).

## Non-Negotiable Operating Laws

1. **Author ≠ Reviewer (fresh context, cross-family preferred).** Review in an isolated context without the author's narrative excuses. Prefer a **different model family** (Anthropic ↔ Gemini ↔ GPT via `delegate`) whenever available **and permitted by the `environment` Privacy Tier**.
2. **Mechanical gates pass first (fail-closed).** Never spend review effort on code with failing lint, typecheck, build, or unit tests — bounce it back immediately.
3. **Freeze the diff fingerprint.** Record the exact commit/diff hash being reviewed (`git rev-parse HEAD` + `git diff` hash). Any subsequent edit invalidates the review and requires re-checking changed areas.
4. **Apply 4 parallel adversarial lenses:**
   - **Lens 1 — Correctness & Spec Alignment:** Does it actually satisfy every acceptance criterion and edge case? Did it touch out-of-scope code?
   - **Lens 2 — Security & Privacy:** Trust boundaries, input validation, authz/least privilege, secret/PII leakage, injection vectors.
   - **Lens 3 — Simplicity, Bloat & Zero-Debt (*Simplify Pass*):** Is there overengineering, dead code, unnecessary abstractions, or avoidable tech debt that should be cut?
   - **Lens 4 — Observability & Failure Modes:** Do structured logs, metrics, timeouts, and error paths give clear visibility when this fails at 3 AM?
5. **Strict triage: Blocking vs Non-Blocking.** Block merge **only** on real correctness bugs, security/privacy gaps, spec drift, silent failures, or avoidable debt. Report style nitpicks and future improvements as **Non-Blocking** so proportional velocity is preserved.
6. **Bounded correction (anti-loop cap).** Allow at most **1–2 tightly scoped correction passes** with a strict scope budget. If blocking issues survive 2 passes → **STOP and escalate to the human** (never thrash in an infinite fix loop).
7. **Always close with `qa-verify`.** Any edit made during review invalidates prior test runs — hand the final state to `qa-verify` to issue the RDD Receipt.
