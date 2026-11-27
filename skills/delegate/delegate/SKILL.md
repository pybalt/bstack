---
name: delegate
description: "Use when offloading scoped execution, parallel workstreams, heavy research, or independent cross-model reviews to isolated subagents or external coding CLIs to prevent orchestrator context rot and single-model blind spots. Do not use for trivial 1-file edits or tightly coupled work requiring shared mutable state."
version: 1.0.0
author: Leonel Baltazar Bravo
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [delegate, orchestration, subagents, multi-model, context-budget, worktrees, cross-family]
    related_skills: [odd-build, adversarial-review, evolve, spike, environment]
---

# Delegate (Context-Safe Multi-Agent & Cross-Family Orchestration)

Treat the main agent as a **lean orchestrator** that protects its context window and delegates heavy or independent execution to fresh, isolated workers — prioritizing **distinct model families** when independence or diversity matters.

## When to Use — and When NOT to Use

- **Use when:**
  - Orchestrator context / compaction pressure is climbing and a sub-task needs deep file reading or multi-file implementation.
  - 2+ independent slices, comparison spikes (`002a`/`002b`), or `evolve` islands can run in parallel without touching the same files.
  - You need **Author ≠ Reviewer** independence (`adversarial-review`) or cross-family diversity (`evolve`).
- **Do NOT use when:** a task is a quick 1-file edit or 2-tool lookup where writing a brief costs more than doing it inline, or two tasks mutate the same files simultaneously without worktree isolation.

## Progressive Disclosure

- Load **`references/delegation-contract.md`** before dispatching workers (Delegation Decision Gate, Surgical Worker Brief template, Worktree Isolation rules, Cross-Family Routing + Privacy Gate, and Bounded Retry / External Verification protocol).

## Non-Negotiable Operating Laws

1. **Delegate before *context rot*, not after.** Keep the orchestrator focused on decomposition, boundaries, and integration; offload high-volume reads, logs, and multi-file edits to fresh workers with clean context.
2. **Pass minimal, surgical context — never dump full chat history.** Every worker brief must specify: exact goal, **owned files**, explicit **do-not-touch files**, acceptance/verification command, and required return format.
3. **Isolate concurrent writers with `git worktree`.** Readers/reviewers may share the workspace; parallel writers **must** run in isolated worktrees or disjoint file sets (`environment/references/versioning.md`).
4. **Use cross-family models for independence & diversity.** Prefer a **different model family** (Anthropic / Gemini / GPT) for independent code review (`adversarial-review`) and `evolve` islands whenever available **AND allowed by the active `environment` Privacy Tier** (never send Tier A/sensitive code to non-ZDR providers).
5. **Enforce bounded retries.** Cap autonomous worker retry loops (max **2–3 attempts** or fixed scope cap) so a stuck worker escalates instead of burning tokens or thrashing code.
6. **Verify worker outputs externally.** Treat every subagent/CLI summary as **untrusted** until the orchestrator inspects the actual `git diff` and verifies real command outputs.
