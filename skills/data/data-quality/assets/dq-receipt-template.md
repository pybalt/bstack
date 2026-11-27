# Data RDD Verification Receipt

## 1. Scope & Execution Context
- **Target Table / Asset:** `<layer>.<table_name>`
- **Engine / Environment:** `<BigQuery / Snowflake / Postgres / DuckDB — staging | prod>`
- **Partition Window Verified:** `[YYYY-MM-DD 00:00 UTC, YYYY-MM-DD 00:00 UTC)`
- **Verification Coverage:** `Full partition` | `Sampled (N rows)`
- **Pipeline / Commit Ref:** `<git_sha / run_id>`

## 2. Automated Quality Gate Results
| Pillar | Check Executed | Observed Result | Threshold | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Uniqueness (Grain)** | `COUNT(*) - COUNT(DISTINCT pk)` | `0 duplicates` | `0` | PASS |
| **Completeness** | Required column nulls (`pk`, `tenant_id`, `amount_cents`) | `0 nulls` | `0` | PASS |
| **Validity** | Domain enums & non-negative bounds | `0 violations` | `0` | PASS |
| **Freshness** | `NOW_UTC - MAX(event_at_utc)` | `14 min` | `<= 60 min` | PASS |
| **Consistency** | Orphan FK check vs `dim_customer` | `0 orphans` | `0` | PASS |
| **Volume / Drift** | Row count vs 14-day median band | `48,210 rows (+2.1%)` | `[0.5×, 2.0×]` | PASS |

## 3. Source-vs-Target Reconciliation Proof (If Refactor / Migration)
- **Tier 1 (Rows):** Source `48,210` vs Target `48,210` (`delta = 0`)
- **Tier 2 (PK Set Diff):** Missing `0` · Extra `0`
- **Tier 3 (Null Delta):** Max column delta `0.00%`
- **Tier 4 (Checksums):** `SUM(gross_amount_cents)` Source `942180500` vs Target `942180500` (`delta = 0`)

## 4. Residual Risks & Promotion Verdict
- **Verdict:** `APPROVED FOR PUBLISH` | `QUARANTINED (BLOCKED)`
- **Unverified / Deferred Scope:** `<none | list exact unchecked partitions or historical backfill window>`
- **Knowledge Closure:** Contract & ADR updated in `<docs/adr/ | Board + Engram>`.
