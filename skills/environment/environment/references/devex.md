# DevEX (Feedback Loops, Golden Paths & Prod-Parity Data)

Load this reference when designing developer/agent workflows, local parity labs, or production-like data access.

## 1. Decision Lens: The DevEX Triad (Forsgren / Noda / Storey / Greiler)

Before adding a tool, wrapper, or abstraction, test it against all three axes — cut anything that worsens them:

1. **Feedback Loops:** Does it shorten edit → verified evidence? Provide a cloud-free local parity loop (Docker lab / DevContainer) exercising the same contract as production before touching cloud infra.
2. **Cognitive Load (Golden Paths):** Does it replace tribal knowledge with a single declarative contract (`dev.env` / YAML / feature flags) and one verifiable entrypoint (`--verify`)?
3. **Flow State:** Does it let the agent/human act autonomously inside structural guardrails instead of stopping for manual approval on every safe read?

## 2. Prod-Parity Data Decision Gate (IF / THEN)

Mocks drift fast (stale schemas, missing indexes, divergent query plans, absent PL/SQL). Choose the data tier strictly by **verified model privacy**, never by convenience:

```text
IF model/endpoint has verified privacy guarantees (ZDR, no training, VPC/private residency)
   AND network policy allows private VPN read-only DB access:
   -> USE TIER A (Prod Read-Only + Ephemeral Shadow Writes)
ELSE:
   -> HARD STOP on real rows. USE TIER B (Metadata-Only + Synthetic Data)
```

### Tier A — Read-Through Prod + Ephemeral Shadow Writes
- **Reads:** Dedicated DB user with `SELECT`-only privileges behind a query guard enforcing `SELECT`/`WITH` allowlist, single-statement execution, row caps, statement timeouts, and zero DML/DDL.
- **Writes:** Redirect sandbox/app writes to a short-TTL **ephemeral overlay (e.g., Redis)** scoped per session/branch. App reads resolve **`overlay ?? production`** (read-your-own-writes) so state transitions are verified end-to-end without touching production and auto-expire.
- **Boundary:** Agents hit the query/shadow proxy only — never raw admin DB credentials.

### Tier B — Metadata-Only + Synthetic Data (Default Safe Fallback)
- **Access:** DB user permitted **only** to inspect metadata (schemas, DDL, indexes, constraints, views, stored procedures/PL-SQL) — **zero `SELECT` on live rows/PII**.
- **Synthesis:** Generate realistic synthetic fixtures from the real schema/constraints/PL-SQL (matching cardinalities, nulls, edge cases, encodings) into an ephemeral local DB (Docker Postgres/Oracle/SQLite).
- **Anti-rationalization:** Never pull "just 5 real rows" into a non-ZDR model context to debug faster.

## 3. Local Parity, Toolchains & `.env` Hygiene

- **Linux-first execution (macOS fallback):** Keep workspaces in Linux (VM, container, WSL2) or macOS — avoid native PowerShell / Windows Terminal for agent coding loops.
- **Containerized local lab:** Mirror target VM/runtime locally (`lab.sh build / up / run <role> / destroy`) with mock identity shims to iterate in seconds instead of 10-minute cloud deploys.
- **Match the lockfile:** `uv.lock`/`pyproject.toml` → `uv` + `.venv`; `pnpm-lock.yaml` → `pnpm`; check `.nvmrc`/`.python-version`/`mise.toml`. Never mix package managers or global-install project deps.
- **Secrets & test flags:** Inspect `.env` key names only (`grep -E '^[A-Z0-9_]+=' .env | cut -d= -f1`). Never gate test modes (`MOCK_MODE`, `MAX_SECONDS`) on inherited shell env vars — use explicit CLI flags.
- **Ports:** Check listeners (`ss -ltnp`, `lsof -i :PORT`, `Get-NetTCPConnection`) before binding. Default `127.0.0.1`; bind `0.0.0.0` only for explicit LAN/device testing.

## Completion Criteria

- [ ] Privacy tier (Tier A vs Tier B) stated explicitly with the model/endpoint basis.
- [ ] Local feedback command ran cleanly with zero leaked `.env` values or global toolchain pollution.
