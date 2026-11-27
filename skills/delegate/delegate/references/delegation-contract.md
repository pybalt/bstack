# Delegation Contract, Context Isolation & Cross-Family Routing

Load this reference when deciding whether to delegate, structuring a worker brief, or routing work across agents/model families.

## 1. Delegate vs Inline Decision Gate

```text
IF task is <= 1-2 files AND low context load AND does not need independent eyes:
   -> RUN INLINE (do not add delegation overhead).
ELSE IF task needs heavy exploration, multi-file edits, parallel exploration,
     OR orchestrator context pressure is high,
     OR task requires Author != Reviewer / cross-family diversity:
   -> DELEGATE to fresh worker(s) with isolated context.
```

## 2. Surgical Worker Brief Template (Mandatory Fields)

Never send a vague prompt like *"implement auth"* or dump 200 messages of chat history. Send a compact, self-contained contract:

```markdown
### Worker Assignment: <short title>
- **Role:** <Explorer | Implementer | Adversarial Reviewer | Spike Runner | Evolve Island>
- **Goal (observable outcome):** <1–2 concrete sentences>
- **Owned Files (allowed to edit):** `<exact paths or globs>` (or "READ-ONLY")
- **Do-Not-Touch Boundaries:** `<files, schemas, harnesses, or modules off-limits>`
- **Constraints & Contracts:** <relevant slice of Decision Brief / ODD tracker / coding rules>
- **Required Verification Command(s):** `<exact test/lint/build command>`
- **Retry Cap:** Max 2 self-correction attempts; if still failing, stop and report root blocker.
- **Return Format:**
  1. Changed files + concise summary of what changed and why.
  2. Exact commands run + observed pass/fail output (distinguish Verified vs Not Run).
  3. Risks, open edge cases, or blockers discovered.
```

## 3. Parallelism & Workspace Isolation

- **Read-only workers (explorers, reviewers, log investigators):** Safe to fan out in parallel against the same workspace.
- **Concurrent editing workers:** MUST either:
  1. Work in separate **`git worktree`** branches (`environment/references/versioning.md`), OR
  2. Have strictly **disjoint owned-file sets** with zero shared lockfiles/generated artifacts.
- **Merge discipline:** Orchestrator merges one worker branch at a time and runs mechanical checks after each merge — never blind-overwrite concurrent edits.

## 4. Cross-Family Model Routing (Respecting Privacy Tier)

Models from the same family share training biases and blind spots. Route intentionally when multiple providers/CLIs are configured:

| Task Type | Preferred Routing | Privacy Guardrail (`environment`) |
| :--- | :--- | :--- |
| **Author → Reviewer (`adversarial-review`)** | Run reviewer on a **different model family** than the author (e.g., Anthropic ↔ Gemini ↔ GPT). | Verify target model satisfies the repo's Privacy Tier (ZDR/VPC) before sending internal code/diffs. |
| **Multi-Paradigm Exploration (`evolve` / `spike`)** | Assign isolated islands to distinct model families in parallel without sharing outputs across islands. | If only one ZDR-compliant family is permitted, stay on that family and enforce opposing constraints per island. |
| **High-Volume Read / Mechanical Sweeps** | Fast/lightweight model for broad read-only search; frontier reasoning model for architecture, security review, or hard root-cause synthesis. | Strip secrets/PII before cross-tool handoffs. |

## 5. Orchestrator Integration Checklist (Post-Delegation)

Before accepting any worker result:
- [ ] Inspected real `git status` and `git diff` (confirmed zero out-of-scope edits and zero leaked secrets).
- [ ] Verified that claimed test/build outputs actually ran against the final file state.
- [ ] Reconciled worker findings into the ODD tracker or cross-session memory (e.g., Engram) if durable.
