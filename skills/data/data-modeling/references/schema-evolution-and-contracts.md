# Schema Evolution, Data Contracts & Governance

Treat every Gold table (and shared Silver table) as a versioned public API consumed by downstream pipelines, dashboards, and ML models.

## 1. Change Classification Matrix

Run `python3 scripts/schema_diff.py <old.json> <new.json>` before merging schema PRs:

| Change Type | Classification | Safe Without Consumer Coordination? |
| :--- | :--- | :---: |
| Add new **nullable** column (or column with default) | `SAFE_ADDITIVE` | Yes |
| Relax constraint (`NOT NULL` → nullable) | `SAFE_ADDITIVE` | Yes (verify downstream null handling) |
| Widen numeric/string type (`INT32` → `INT64`, `VARCHAR(50)` → `VARCHAR(200)`) | `WARNING_TYPE_WIDEN` | Usually yes (check BI extracts & Avro/Parquet readers) |
| Add new enum value to open string field | `WARNING` | Verify downstream `CASE`/`ELSE` handling |
| Drop or rename existing column | `BREAKING_CHANGE` | **No** — requires Expand-Contract |
| Narrow type or change type family (`STRING` → `INT`, `FLOAT` → `INT`) | `BREAKING_CHANGE` | **No** |
| Tighten nullability (nullable → `NOT NULL`) without backfill proof | `BREAKING_CHANGE` | **No** |
| Change grain, primary key, unit (`dollars` → `cents`), or timezone | `BREAKING_CHANGE` | **No** — publish as `v2` view/table |

## 2. Expand-Contract Zero-Downtime Migration Pattern

Never rename or alter a consumed column in place. Execute in **3 bounded releases**:

1. **Expand (Release 1):** Add the new column (`amount_cents INT64`) alongside the deprecated column (`amount_usd`), populate both in the pipeline, and mark the old column `deprecated` in the contract with a sunset date.
2. **Migrate Consumers (Window):** Notify downstream owners, update BI/dbt/downstream models to read `amount_cents`, and verify zero queries reference `amount_usd` in warehouse audit logs (`INFORMATION_SCHEMA.JOBS` / query history) for 7–14 days.
3. **Contract (Release 2):** Drop `amount_usd` only after audit logs confirm zero active readers (or keep a thin compatibility view `v1` while advancing the canonical table to `v2`).

## 3. Data Contract Essentials (`assets/data-contract-template.yaml`)

Every Gold contract defines **six concrete commitments**:
1. **Identity & Ownership:** Dataset/table URI, team/owner handle, escalation channel.
2. **Grain & Keys:** Plain-English grain sentence, primary key column(s), partition & cluster keys.
3. **Freshness & Volume SLAs:** Max allowed lag (e.g., `<= 60 min` or `daily by 07:00 UTC`) and expected row-volume band.
4. **Schema & Semantics:** Column name, logical type, nullability, unit/timezone, and allowed values.
5. **Privacy & Retention:** `classification` (`public`, `internal`, `confidential`, `pii`, `pci`, `phi`), masking/hashing policy, and partition TTL retention days.
6. **Deprecation Policy:** Minimum notice window (e.g., 14 or 30 days) for breaking changes.

## 4. PII & Privacy-by-Design Checklist

- Never store raw PII (email, national ID, phone, credit card) in wide analytical Gold marts unless explicitly required and access-controlled via column-level policies / dynamic data masking.
- Separate direct identifiers into a dedicated restricted mapping table (`restricted.dim_user_pii`) joined only by authorized roles, while analytical facts use a salted/pseudonymized `user_key`.
- Honor deletion/GDPR/right-to-erasure requests cleanly via crypto-shredding (per-user key deletion) or partitioned delete jobs documented in the contract.
