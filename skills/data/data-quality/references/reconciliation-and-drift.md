# Source-vs-Target Reconciliation & Silent Drift Triage

*Note: This reference covers the 4-tier reconciliation protocol and root-cause triage for data mismatches.*

## 1. The 4-Tier Reconciliation Protocol

Whenever migrating warehouses (e.g., Oracle → BigQuery), refactoring a SQL pipeline, or switching engines (Spark → DuckDB/dbt), run all **4 tiers** over the exact same date partition window (`[start_utc, end_utc)`):

| Tier | What It Proves | How to Compute | Pass Criterion |
| :--- | :--- | :--- | :--- |
| **Tier 1 — Volume Parity** | No missing batches or silent row fan-outs | `source_rows` vs `target_rows` per partition date | Exact match (or documented intentional dedup/filter delta) |
| **Tier 2 — Key-Set Parity** | Exact same business entities exist in both | `EXCEPT` / `MINUS` on `primary_key` (both `source - target` and `target - source`) | `0` missing keys, `0` unexpected extra keys |
| **Tier 3 — Null & Cardinality Parity** | No broken casts, dropped columns, or truncated strings | Per-column `null_count` and `COUNT(DISTINCT col)` delta | `0` unexpected null spikes or cardinality collapse |
| **Tier 4 — Numeric Checksum Parity** | Financial and metric totals match end-to-end | `SUM`, `MIN`, `MAX`, `AVG` on key measures (plus sampled row-hash diff for strings) | Exact match for integers/cents; `|delta| <= epsilon` (e.g. `1e-4`) for floats |

For local CSV/JSONL exports, run `python3 scripts/reconcile_datasets.py source.csv target.csv --pk order_id --tol 0.001` to produce a deterministic JSON receipt across all 4 tiers.

## 2. Silent Corruption Root-Cause Playbook

| Symptom | Most Likely Root Cause | Fast Verification Test |
| :--- | :--- | :--- |
| Target row count is **> 1.0×** source (e.g., 1.3× or 2.0×) | **Join fan-out (`1:N`)** or un-deduplicated SCD2 join using `BETWEEN` | Run `GROUP BY pk HAVING COUNT(*) > 1`; inspect which joined table has > 1 match per key |
| Totals match on 29 days, off on **1 day near boundary** | **Timezone / DST mismatch** (mixing UTC and local midnight) or inclusive `<=` instead of half-open `<` | Compare hourly bucket counts around `00:00` and `03:00` UTC between source and target |
| Target row count is **slightly lower** than source | **Inner join dropping null/orphan FKs** or **`NOT IN (SELECT ...)` NULL trap** | Swap `INNER JOIN` → `LEFT JOIN` in diagnostic query and count `WHERE right.pk IS NULL` |
| Dollar totals off by **pennies across millions of rows** | **Floating-point rounding (`FLOAT64`)** vs fixed-point `NUMERIC`/integer cents | Cast amounts to `NUMERIC` or minor integer units (`amount_cents INT64`) before summing |
| Sudden **0 rows** in latest partition while job is green | Upstream partition delayed + query filtered `CURRENT_DATE()` or silent empty file landed | Check upstream watermark lag and enforce a `row_count > 0` WAP circuit breaker |
| One metric jumps **10×** on specific dates | **Double-counted replay** from non-idempotent `INSERT INTO` retry | Check `_ingested_at_utc` distribution per `pk` — multiple ingestion timestamps per PK prove duplicate replay |
