---
name: grill
description: "Use when aligning on architecture, product design, technical trade-offs, or scope before planning or coding by interviewing branch-by-branch with measured problem sizing and solution competition. Do not use for trivial edits or active bug reproduction."
version: 1.0.0
author: Leonel Baltazar Bravo
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [grill, design, architecture, trade-offs, simplicity, frameworks, observability, security]
    related_skills: [visual-brief, spike, evolve, onboarding, environment, uiux]
---

# Grill (Measured Design Interview & Decision Alignment)

Walk down the decision tree with the user **one branch and one question at a time** until shared understanding is reached, using **measured trade-offs** instead of gut-feel recommendations.

## When to Use — and When NOT to Use

- **Use when:** designing a new feature, architecture, refactor, AI workflow, or infrastructure change where decisions have meaningful trade-offs, scope risk, or irreversibility.
- **Do NOT use for:** trivial 1-file edits, mechanical renames, or active bug diagnosis (use `systematic-debugging` first).

## Progressive Disclosure Protocol (Strict Budget)

Classify the problem domain first (1 primary lens, or 2 if hybrid), then load **only the matching references**:

| Need | Load ONLY this file | Inside |
| :--- | :--- | :--- |
| Problem sizing, Pugh scoring, Observability & Security Gate, Decision Brief | `references/scoring-and-brief.md` | Always load once per grill session |
| Engineering & product frameworks (Value Levers, RICE, CUJ, STRIDE, Pre-Mortem) | `references/frameworks.md` | Selective 1–2 framework picker |
| Backend, APIs, data models, queues, migrations | `references/lens-backend.md` | Contracts, consistency, RED metrics, edge security |
| Frontend, UX, visual taste, interactive flows | `references/lens-frontend.md` | Visual taste comparison, state matrix, a11y, perceived speed |
| AI features, LLM workflows, prompts, agents | `references/lens-ai.md` | Deterministic-first gate, evals, cost/latency, privacy, fallbacks |
| Cloud, infra, networking, deployments, platform | `references/lens-infra.md` | Blast radius, cost model, zero-trust connectivity, ops burden |

## Non-Negotiable Operating Laws

1. **Investigate before asking.** If a question can be answered by reading the repo or querying an Organizational Knowledge MCP (`environment`), answer it yourself — never waste the user's attention on discoverable facts.
2. **Size the problem before proposing solutions.** Establish real magnitude, blast radius, reversibility (*one-way vs two-way door*), and lifespan before scoring options.
3. **Overengineering is a defect; technical debt is rejected.** Always include a **Baseline Simple** option in every comparison. The goal is the simplest technically solid, zero-debt solution proportional to the measured problem.
4. **Burden of proof favors simplicity.** Never recommend a complex option unless concrete evidence shows the simple option fails the problem profile. Always state the **breakpoint** where the alternative would win.
5. **Observability & Security by Design are non-negotiable.** Structured logs, health/business metrics, and boundary security are part of technical solidity (scaled proportionally — never overkill).
6. **One question at a time, top-down.** Resolve *one-way doors* and structural dependencies before *two-way doors* and details. Offer your evidence-backed recommendation first.
7. **Hand off when text stops helping.**
   - IF trade-offs, frameworks, UI taste, or flows are visually dense → invoke `visual-brief`.
   - IF a key feasibility unknown cannot be decided on paper → invoke `spike` and resume with evidence.
   - IF two options have competing strengths worth synthesizing empirically against a benchmark → invoke `evolve`.

## Execution Flow

1. **Context Sweep:** Read relevant codebase/org context silently.
2. **Domain & Problem Sizing:** Declare active domain lens(es) + 4-axis Problem Profile + 1–2 selected frameworks (if useful).
3. **Decision Tree Interview:** Walk branch by branch (1 question per turn). For each non-trivial decision, present the compact competition table against the Baseline Simple and your justified recommendation.
4. **Observability & Security Gate:** Lock in out-of-the-box logs, metrics, never-log list, and security boundaries before finishing.
5. **Decision Brief Output:** Emit a concise **Decision Brief** (`references/scoring-and-brief.md`) ready to feed the IDE's native Plan Mode or the `build` stage.
