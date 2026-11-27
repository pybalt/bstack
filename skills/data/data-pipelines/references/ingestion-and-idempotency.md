# Ingestion, Idempotency & Write-Audit-Publish (WAP)

## 1. Ingestion Mode Selector

| Mode | Best For | Watch Out For |
| :--- | :--- | :--- |
| **Incremental Watermark Pull** (`updated_at >= watermark`) | SaaS APIs, OLTP replicas with reliable indexed `updated_at` | Misses hard deletes unless source emits soft-delete flags (`deleted_at`); requires lookback overlap for clock skew/late commits |
| **Log-Based CDC** (Debezium, Datastream, Fivetran/Airbyte CDC) | High-volume OLTP databases needing hard-delete capture with minimal source load | Requires WAL/binlog retention tuning; downstream must deduplicate at-least-once delivery using `(lsn/offset, op_ts)` |
| **Full Snapshot + Partition Stamp** | Small dimensions (< 5M rows) lacking reliable `updated_at` or delete flags | Expensive at scale; store snapshot date to enable SCD Type 2 diffing downstream |
| **Event Stream / Micro-Batch** (Kafka, Pub/Sub → Iceberg/BQ) | Sub-minute freshness or clickstream/telemetry | Small-file proliferation (schedule compaction), out-of-order events, poison-pill messages |

## 2. The Idempotency Law

**Test:** If a scheduler retries the exact same run for logical date `2026-05-01` three times in a row, are the final rows, counts, and sums **byte-identical**?

| Strategy | How It Works | Best Fit |
| :--- | :--- | :--- |
| **Atomic Partition Overwrite** *(Preferred)* | Compute complete output for `dt = :run_date` into staging, then atomically replace partition `dt = :run_date` (`INSERT OVERWRITE` / `LOAD ... WRITE_TRUNCATE` on `table$YYYYMMDD`) | Event facts partitioned by date (cleanest, zero duplicate risk, fast rollbacks) |
| **Deterministic `MERGE` (Upsert)** | Deduplicate incoming batch on `(primary_key)` picking latest `(updated_at_utc, _ingested_at_utc)` first, then `MERGE` on `(partition_key, primary_key)` | Mutable entities (orders, accounts, accumulating facts) — include partition predicate in `ON` clause so the engine prunes target partitions! |
| **Delete + Insert in Transaction** | `BEGIN; DELETE FROM target WHERE dt = :run_date; INSERT INTO target SELECT ...; COMMIT;` | Row-stores (Postgres, Oracle) or warehouses without partition-swap syntax |

**Never use bare `INSERT INTO target SELECT ...`** without an explicit partition replacement or unique key merge — the first retry silently doubles every metric.

## 3. Watermarks, Lookback & Dead-Letter Queues (DLQ)

- **Parameterize time windows explicitly:** Pass `window_start_utc` and `window_end_utc` from the orchestrator rather than calling `NOW()` / `CURRENT_DATE()` inside transforms — otherwise historical backfills silently compute *today's* data instead of the target date!
- **Lookback window:** Reprocess `[window_start_utc - lookback, window_end_utc)` (e.g., 3 days for mobile offline events or payment settlements) using idempotent `MERGE` or partition overwrite to capture late-arriving records cleanly.
- **Dead-Letter Queue (DLQ):** When schema parsing or type casting fails on a subset of rows, never silently drop them AND never let 1 malformed record block 10M valid records unless contract requires hard fail. Route rejected payloads to `bronze.<source>_dlq` with `raw_payload`, `error_reason`, `batch_id`, and `failed_at_utc`, and alert if `dlq_ratio > threshold`.

## 4. Write-Audit-Publish (WAP) Pattern

Guarantees consumers never read corrupted or duplicate data:
1. **Write:** Load transformed output into an isolated staging table/branch/partition (`staging.fct_orders__run_20260501` or Iceberg/Nessie WAP branch).
2. **Audit:** Run `data-quality` assertions against staging (zero PK duplicates, non-zero volume within expected band, zero null violations on required columns, reconciliation totals match source).
3. **Publish:** If ALL blocking audits pass, atomically swap/merge staging into production (`ALTER TABLE ... SWAP`, partition replacement, or fast-forward Iceberg branch). If ANY blocking audit fails, abort publish, preserve staging for forensics, and alert.
