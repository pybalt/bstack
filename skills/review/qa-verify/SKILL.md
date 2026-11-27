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

## Progressive Disclosure & Executable Helpers

- Load **`references/qa-receipt-protocol.md`** before issuing a receipt (Domain QA Matrix, Live Observability/Security Verification, and Knowledge Closure rules).
- **Scripts:**
  - `python3 scripts/fingerprint.py --cwd .` — freeze pre-QA fingerprint; re-run with `--compare <fingerprint>` right before delivery (exits `1` on 1-byte drift).
  - `python3 scripts/scan_diff_hygiene.py --cwd .` — fail-closed scan for secrets, `[DEBUG-*]` tags, hardcoded home paths, `.env`, and leftover `spikes/`.
- **Assets:** Format the receipt with **`assets/receipt-template.md`** and document final ADRs/architecture/changes using **`assets/adr-and-closure-template.md`**.

## Non-Negotiable Operating Laws

1. **Freeze the exact candidate fingerprint first.** Run `scripts/fingerprint.py` before QA and `--compare` at closure. **If ANY file changes after QA starts, the receipt is VOID** — re-freeze and re-run affected gates.
2. **Mechanical gates are fail-closed.** Build, typecheck, linter, `scripts/scan_diff_hygiene.py`, and affected automated tests MUST pass cleanly before behavioral QA. Never ignore or suppress a failing check to move forward.
3. **Exercise real behavior, not just unit mocks.** Run the actual CLI, API endpoint, prod-parity Tier A/B query (`environment`), or live browser UI across **happy paths AND edge states** (invalid inputs, empty, loading, error, timeout, mobile + desktop for UI).
4. **Verify emitted observability & security signals live.** Inspect actual structured logs, error responses, and metrics produced during QA: confirm key events fire, correlation IDs appear, and **zero secrets/tokens/PII leak**.
5. **Separate Verified from Unverified with brutal honesty.** Every RDD Receipt must list exact commands run + observed exit codes/counts AND explicitly list anything that could **not** be executed. Never treat exit `0` or HTTP `200` alone as proof without checking actual payload/state.
6. **Mandatory post-QA documentation closure (last step before declaring done).** For every non-trivial feature, architectural decision, refactor, or resolved incident, **persist ADRs, design/architecture updates, and actual changes** (`assets/adr-and-closure-template.md`) to the workspace's configured **Knowledge Sink(s)**: Visual Architecture Board (via MCP) and/or Repo ADRs (`docs/adr/`, `ARCHITECTURE.md`) **and/or** cross-session memory (e.g., **Engram**). Pair complex releases with a **`visual-brief`** (*Change Walkthrough*). Only trivial inline edits with zero design impact may mark this `N/A`.
