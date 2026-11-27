# Post-Delivery Documentation & ADR Closure

Mandatory final step after `qa-verify` passes for any non-trivial feature, refactor, architectural decision, or resolved production incident. Persist to the project's configured knowledge sink(s): **Visual Architecture Board (via MCP)** and/or **Repo ADRs (`docs/adr/`)** and/or **Cross-Session Memory (e.g., Engram)**.

---

## Compact ADR (Architecture Decision Record)
```markdown
# ADR-NNN: <Decision Title>
- **Date:** YYYY-MM-DD | **Status:** Accepted | **Commit / PR:** `<sha>`
- **Context & Problem Profile:** `<magnitude, blast radius, constraints>`
- **Options Considered:**
  1. `<Baseline Simple>` — `<pros/cons>`
  2. `<Alternative>` — `<pros/cons>`
- **Decision:** Chose `<Winner>` because `<measured evidence>`.
- **Consequences & Breakpoint:** `<trade-offs accepted; revisit if threshold X is crossed>`.
- **Observability & Security:** Logs `<events>` · Metrics `<signals>` · Guardrails `<boundaries>`.
```

## Architecture & Change Record (For Visual Board / Repo Docs / Engram)
```markdown
### Delivery Record: <Feature / Change>
- **What Changed (Architecture & Contracts):** `<modules, APIs, events, schemas added or updated>`
- **Design & Trade-Offs Locked:** `<summary or link to ADR-NNN>`
- **Verified Commands & QA Evidence:** `<exact commands + RDD receipt fingerprint>`
- **Operational Notes & Known Limits:** `<runbook hints, feature flags, rollback path, deferred non-blocking items>`
```
