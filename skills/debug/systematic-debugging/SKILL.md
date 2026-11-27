---
name: systematic-debugging
description: "Use when diagnosing any bug, test failure, regression, performance issue, or unexpected runtime behavior through 4-phase root-cause investigation, tight reproducible feedback loops, and automated git bisect before writing any fix. Do not use for greenfield feature design (use grill)."
version: 2.0.0
author: Leonel Baltazar Bravo
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [debugging, troubleshooting, root-cause, git-bisect, regression, investigation]
    related_skills: [evolve, visual-brief, environment]
---

# Systematic Debugging (4-Phase Root Cause & Regression Protocol)

Random fixes waste time and spawn secondary bugs. Symptom patches are failure.

```text
THE IRON LAW: NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

## When to Use — and When NOT to Use

- **Use for ANY technical failure:** test failures, regressions (*worked before, broken now*), production/staging bugs, flaky behavior, build/integration failures, or performance drops — **especially** under time pressure or after 1+ failed fix attempts.
- **Do NOT use for:** greenfield architecture/feature planning (`grill`) or blind multi-candidate patching before root cause is known (`evolve` is **hard-blocked** in Phases 1–3).

## Progressive Disclosure

- Load **`references/repro-and-bisect.md`** when building a hard reproduction loop, running automated **`git bisect run`** on regressions, minimizing a repro, or checking red-flag rationalizations.
- Copy **`assets/bisect-check.sh`** outside the repo (e.g., `/tmp/bisect_check.sh`) when automating `git bisect run` with exit code `125` build-skip safety.

## The Four Phases (Strict Sequence)

### Phase 1 — Root Cause Investigation *(Stop before fixing)*
1. **Read full errors & stack traces:** Every line, file, error code, and structured log/trace (use credential-free log proxies per `environment` if investigating staging/prod).
2. **Build a tight, red-capable feedback loop:** One fast, deterministic, runnable command that fails specifically on the user's exact symptom and passes only when fixed. For flaky bugs, raise repro rate first (repeat 100×, stress, narrow timing).
3. **Check recent changes — use `git bisect` for regressions:**
   - Inspect `git log --oneline -10` and `git diff`.
   - **IF the behavior worked in a previous commit/tag and fails now** → run automated **`git bisect run`** (`references/repro-and-bisect.md`) using your red-capable script to pinpoint the exact introducing commit in $O(\log n)$ steps instead of guessing.
4. **Instrument component boundaries & trace upstream:** In multi-component flows, log inputs/outputs/config at each boundary once to prove *which* component breaks, then trace bad values upstream to their origin. Fix at the source, never at the symptom.

*Gate:* Do NOT move to Phase 2 until the loop ran red at least once and the failing boundary is isolated.

### Phase 2 — Pattern Analysis
1. **Minimize the repro:** Strip inputs, config, and steps one at a time until removing any remaining piece makes the loop go green.
2. **Compare against working code:** Read similar working paths in full (don't skim), list every difference and implicit dependency/config assumption.

### Phase 3 — Ranked Falsifiable Hypotheses
1. **Generate 3–5 ranked hypotheses** before editing anything, each with an explicit prediction: *"If X is the cause, observing/changing Y will produce Z."*
2. **Test minimally, one variable at a time:** Prefer runtime inspection or temporary logs tagged with a unique searchable prefix (e.g. `[DEBUG-a4f2]`) for clean removal.
3. **Branch cleanly:** Confirmed → Phase 4. Falsified → revert probe and test next hypothesis (never stack fixes on top of failed guesses). If stuck, explicitly say *"I don't understand X"* and gather more data.

### Phase 4 — Single Root-Cause Fix & The Rule of Three
1. **Write an automated regression test first (RED)** reproducing the minimized bug before changing production code.
2. **Apply ONE surgical fix** targeting the root cause (no bundled refactors or "while I'm here" edits; remove all `[DEBUG-*]` instrumentation).
3. **Verify end-to-end (GREEN):** Run the regression test AND full relevant suite to prove zero regressions.
   - *Optional handoff:* ONLY here (once root cause is proven) may you invoke **`evolve`** if the fix is an optimization problem (perf/memory/query/accuracy) with measurable trade-offs, or **`visual-brief`** to present a complex *before vs after* root-cause report.
4. **The Rule of Three (Architectural Stop Gate):**
   - If fix fails and attempts `< 3` → return to Phase 1 with new evidence.
   - **If `>= 3` fixes failed → HARD STOP.** Do NOT try Fix #4. Each fix exposing new coupling/symptoms signals a **wrong architecture**, not a missed typo — escalate and discuss fundamentals with the user.
