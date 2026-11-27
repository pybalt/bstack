---
name: odd-build
description: "Use when implementing features, refactors, or fixes using Organic-Driven Development (ODD): scaling ceremony to change size and risk via the Diff Test + Risk Override, shipping reviewable slices with out-of-the-box observability, security, and proportionate tests. Do not use for initial architectural alignment (use grill), throwaway experiments (use spike), or undiagnosed bugs (use systematic-debugging)."
version: 1.0.0
author: Leonel Baltazar Bravo
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [odd, build, organic-driven-development, implementation, observability, security, slicing]
    related_skills: [grill, delegate, adversarial-review, qa-verify, uiux, evolve, environment]
---

# ODD Build (Organic-Driven Implementation)

Scale implementation ceremony **organically to the size and risk of the change** — avoiding both chaotic *vibe coding* and bureaucratic multi-document pipelines for small edits.

```text
ODD Loop: Explore -> Ask (only if ambiguous/risky) -> Implement in Reviewable Slices -> Verify (RDD)
```

## When to Use — and When NOT to Use

- **Use when:** writing production code for small fixes, medium features, or large multi-session builds once the problem is understood.
- **Do NOT use for:** unresolved design trade-offs (`grill`), unvalidated technical unknowns (`spike`), visual UI design systems (`uiux`), or bugs whose root cause is not yet proven (`systematic-debugging`).

## Progressive Disclosure

- Load **`references/odd-execution.md`** before starting any non-trivial or high-risk implementation (Diff Test + Risk Override table, Inline vs Tracked workflow, ~400 LOC slice discipline, Observability & Security build checklist, and proportionate testing guide).
- Copy **`assets/feature-tracker-template.md`** only when running the **Tracked Path** (zero doc overhead on Inline Path).

## Non-Negotiable Operating Laws

1. **Run the Diff Test + Risk Override first.**
   - **Inline Path (zero ceremony):** A human can fully verify intent and safety from the original prompt + `git diff`, AND no Risk Override fires → explore quickly, implement cleanly, run proportionate checks.
   - **Tracked Path (single resumable doc):** Multi-session, multi-module, or **Risk Override triggers** (even 3 lines touching auth/permissions, billing/money, DB migrations, public contracts, or concurrency) → anchor work in **one** concise resumable tracker (or `grill` Decision Brief) so context survives compaction.
2. **Never let small LOC disguise high risk.** Three lines in a permission check or payment calculation are **never** a "small inline tweak" — escalate scrutiny, tests, and review accordingly.
3. **Ship in reviewable change units (~400 LOC soft cap).** Build thin vertical slices (*Walking Skeleton* first) that compile, run, and can be reviewed cleanly instead of dumping 2,000-line diffs.
4. **Observability & Security out of the box.** Emit structured logs (with correlation IDs and an explicit never-log list), health/business metrics, and boundary input/authz checks as part of the slice — never deferred as "follow-up".
5. **Proportionate tests, zero dogma.** Write automated tests calibrated to behavioral risk (invariants, contracts, failure modes, regressions) — never skip tests on risky logic, and never write dogmatic TDD scaffolding or brittle mocks for trivial glue.
6. **Never self-certify completion — always close with QA + mandatory documentation.** Hand finished units to `adversarial-review` and `qa-verify` (RDD receipt), and as the **mandatory final post-QA step**, persist ADRs, architecture/design decisions, and actual changes into the configured Knowledge Sink(s) (Visual Architecture Board MCP / `docs/adr/` and/or cross-session memory like Engram).
