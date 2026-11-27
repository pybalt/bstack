---
name: qa-verify
description: "Use when proving that a completed change actually works before committing, merging, or delivering by running fail-closed mechanical gates, real behavioral/E2E QA, live observability/security signal checks, and issuing a fingerprint-bound RDD Verification Receipt. Do not use to assume correctness from reading code alone."
version: 1.0.0
author: Leonel Baltazar Bravo
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [qa, verification, rdd, receipt, e2e, observability, security, quality-gate]
    related_skills: [adversarial-review, odd-build, visual-brief, systematic-debugging, uiux, environment]
---

# QA Verify (Receipt-Driven Verification & Real Behavioral QA)

Close the *verification gap* with **executed proof**, not optimistic summaries. No task is complete until a **fingerprint-bound RDD Receipt** passes on the exact final state of the code.

```text
RDD LAW: VERIFYING BEATS GENERATING — ONE EDITED BYTE INVALIDATES THE RECEIPT
```

## When to Use — and When NOT to Use

- **Use before:** committing a milestone, opening a PR, merging, deploying, or telling the user *"it's done / fixed / ready"*.
- **Do NOT use to:** rubber-stamp code by inspection, cite stale test output from before your last edit, or mask broken tests by relaxing assertions.

## Progressive Disclosure

- Load **`references/qa-receipt-protocol.md`** before issuing a receipt (Fingerprint Freezing commands, Domain QA Matrix, Live Observability/Security Verification, RDD Receipt template, and `visual-brief` Change Walkthrough handoff).

## Non-Negotiable Operating Laws

1. **Freeze the exact candidate fingerprint first.** Capture `HEAD` SHA + working-tree diff hash before running verification. **If ANY file changes after QA starts, the receipt is VOID** — re-freeze and re-run affected gates.
2. **Mechanical gates are fail-closed.** Build, typecheck, linter, secret/credential scan, and affected automated tests MUST pass cleanly before behavioral QA. Never ignore or suppress a failing check to move forward.
3. **Exercise real behavior, not just unit mocks.** Run the actual CLI, API endpoint, prod-parity Tier A/B query (`environment`), or live browser UI across **happy paths AND edge states** (invalid inputs, empty, loading, error, timeout, mobile + desktop for UI).
4. **Verify emitted observability & security signals live.** Inspect actual structured logs, error responses, and metrics produced during QA: confirm key events fire, correlation IDs appear, and **zero secrets/tokens/PII leak**.
5. **Separate Verified from Unverified with brutal honesty.** Every RDD Receipt must list exact commands run + observed exit codes/counts AND explicitly list anything that could **not** be executed (e.g., staging-only webhook, manual hardware step). Never treat exit `0` or HTTP `200` alone as proof without checking the actual payload/state.
6. **Make human sign-off effortless.** For complex multi-module changes or releases, pair the receipt with a **`visual-brief`** (*Change Walkthrough*: *Before vs After*, impacted modules, Verified/Unverified semaphore) and persist newly learned verification commands to cross-session memory (e.g., Engram).
