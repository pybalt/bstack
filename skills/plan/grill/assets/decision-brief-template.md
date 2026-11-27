# Decision Brief: <Feature / Change>

- **Date:** YYYY-MM-DD
- **Domain Lens(es):** Backend | Frontend | AI | Infra
- **Problem Profile:** Magnitude: `<...>` · Blast Radius: `<...>` · Reversibility: `<one-way | two-way>` · Lifespan: `<...>`
- **Frameworks Applied (max 1–2):** `<e.g., 4 Value Levers + CUJ>`

## Decisions Made
1. **<Decision Branch>:** Chose **<Winner>** over `<Alternatives>` — `<1-line measured justification>`.
   - *Breakpoint:* Revisit `<Alternative>` only if `<concrete threshold changes>`.

## Rejected (Overkill or Tech Debt)
- **<Option>:** Rejected because `<excess complexity, ops burden, or avoidable debt>`.

## Observability & Security Contract (Out of the Box)
- **Structured Logs:** `<events + correlation_id>`
- **Never-Log List:** `<tokens, secrets, passwords, raw PII>`
- **Metrics:** `<RED / USE / business / eval signals>`
- **Security Boundaries:** `<input validation, authz, fail-closed limits>`

## Acceptance Criteria & Next Step
- [ ] `<Observable, testable criterion>`
- **Next Stage:** `odd-build` | `spike` | `evolve` | Native IDE Plan Mode
- **Post-Delivery Documentation Sink:** `<Architecture Board / docs/adr/ + Engram>`
