# Feature Tracker (ODD): <feature-slug>

- **Started:** YYYY-MM-DD | **Path:** Tracked (`Risk Override: <none | auth | billing | migration | concurrency>`)
- **Goal & Outcome:** `<1–2 observable sentences>`
- **In Scope:** `<exact modules/behaviors>`
- **Out of Scope:** `<explicit exclusions>`
- **Decision Brief / References:** `<link or summary>`
- **Observability & Security Contract:**
  - Logs: `<structured events + correlation_id>` | Never log: `<list>`
  - Metrics: `<RED / USE / domain counters>`
  - Security: `<validation, authz, fail-closed boundaries>`

## Reviewable Slices (~<= 400 LOC each)
- [ ] **Slice 1 (Walking Skeleton):** `<thin end-to-end path>` · Verify: `<exact command>`
- [ ] **Slice 2 (Edge Cases & Hardening):** `<failure modes/retries/states>` · Verify: `<exact command>`

## Execution Log & Evidence
- `YYYY-MM-DD` — Slice `<N>`: `<files changed, exact command results, open hazards>`

## Mandatory Post-QA Documentation Closure
- [ ] ADR / Architecture / Design decisions updated in `<Visual Architecture Board / docs/adr/>`
- [ ] Durable lessons & verified commands persisted in `<Engram / cross-session memory>`
