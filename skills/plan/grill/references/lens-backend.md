# Domain Lens: Backend & Data

Load this lens when grilling APIs, services, workers, data pipelines, schemas, or business logic.

## 1. High-Leverage Decision Branches (Order by Irreversibility)

1. **Contracts & Schemas (*One-Way Doors*):**
   - Public/internal API shape, event payloads, DB schema, and backward-compatibility / migration strategy (expand-and-contract vs breaking).
   - Confirm downstream consumers via codebase or Organizational Knowledge MCP before proposing changes.
2. **Consistency, Idempotency & Failure Semantics:**
   - What happens on retry, duplicate delivery, partial failure, or timeout?
   - Does the problem genuinely require strong transactions, or is idempotent eventual consistency simpler and safer?
3. **Complexity vs Expected Behavior:**
   - Challenge premature queues, microservices, event buses, or caching layers. Start with a direct modular call / SQL query / transaction unless measured volume or isolation demands decoupling.
   - Apply **Build vs Buy vs Commodity**: avoid custom schedulers, auth, or retry engines when boring primitives suffice.
4. **Data Integrity & Query Path:**
   - Expected cardinality, indexing, N+1 risks, pagination/bounds, and hard timeouts on external calls.
   - Verify prod-parity testing strategy (Tier A read-prod + shadow writes vs Tier B metadata + synthetic data per `environment`).

## 2. Backend Observability & Security Baseline

- **Logs:** Structured JSON with `correlation_id` / `request_id`, actor/tenant ID (non-PII), operation name, outcome, and latency (`duration_ms`). Log all state transitions and rejected requests with clear reason codes.
- **Metrics (RED + Business):** Request **R**ate, **E**rror rate (split 4xx vs 5xx), **D**uration (p50/p95/p99), plus 1–3 domain counters (e.g. orders processed, retries exhausted).
- **Security:** Schema validation at ingress, explicit authz check per resource (never trust client-supplied tenant/role IDs), parameterized queries, bounded payload sizes, rate limits, and zero secrets/PII in logs or error responses.

## 3. Recommended Frameworks
`Pugh Matrix` · `CUJ Blocks & Outputs` · `Lightweight Event Storming` · `RED / SLI` · `Lightweight STRIDE`.
