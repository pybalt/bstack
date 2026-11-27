---
name: data-pipelines
description: "Use when building or refactoring data ingestion (batch, API, CDC, streaming), ELT/ETL SQL or Python transformations (dbt, Dataform, DuckDB, Polars, Spark), orchestrating DAGs and safe chunked backfills (Airflow, Dagster, Prefect), or optimizing slow and expensive warehouse queries. Do not use for initial table grain or schema design (use data-modeling) or standalone dataset profiling and reconciliation audits (use data-quality)."
version: 1.0.0
author: Leonel Baltazar Bravo
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [data-pipelines, etl, elt, sql, dbt, dataform, duckdb, polars, spark, airflow, dagster, idempotency, backfill]
    related_skills: [data-modeling, data-quality, odd-build, systematic-debugging, qa-verify]
---

# Data Pipelines & Orchestration

Build **idempotent, cost-bounded, replayable data pipelines** across SQL warehouses, local columnar engines, distributed Spark clusters, and DAG orchestrators.

## When to Use — and When NOT to Use

- **Use when:** designing ingestion jobs (batch/CDC/API), writing incremental SQL/dbt/Dataform/Polars/DuckDB/Spark transforms, authoring Airflow/Dagster/Prefect DAGs, planning safe backfills, or diagnosing slow/expensive SQL and OOM shuffles.
- **Do NOT use for:** designing canonical table grains, SCD schemas, or data contracts first (use `data-modeling`), or executing row-level DQ profiling and migration reconciliation proofs (use `data-quality`).

## Progressive Disclosure Protocol

Load **only** the reference(s) needed for the active pipeline task:

| Need | Load ONLY this file | Inside |
| :--- | :--- | :--- |
| Batch vs CDC, watermarks, late data, DLQ, idempotency & WAP | `references/ingestion-and-idempotency.md` | Replayability patterns & Write-Audit-Publish flow |
| dbt, Dataform, DuckDB, Polars, or Apache Spark optimization | `references/transform-engines.md` | Per-engine incremental, memory & skew playbooks |
| Airflow, Dagster, Prefect DAGs, retries, pools & chunked backfills | `references/orchestration-and-backfills.md` | Orchestrator patterns & safe backfill runbooks |
| Query tuning, partition pruning, fan-out & destructive-SQL guardrails | `references/sql-performance-and-safety.md` | SQL performance checklist & data-loss consent gate |

**Executable Script & Copy-Ready Templates:**
- Lint SQL/SQLX files deterministically before execution: `python3 scripts/sql_safety_lint.py <file_or_dir>` (blocks destructive `DROP`/`TRUNCATE`/unfiltered `DELETE`/`UPDATE` and flags columnar anti-patterns in JSON stdout; exits `1` on blocking hazards).
- Document pipeline scope, idempotency proof, and backfill plan from **`assets/pipeline-spec-template.md`**.
- Bootstrap Write-Audit-Publish (WAP) SQL from **`assets/wap-pattern.sql`**.

## Non-Negotiable Operating Laws

1. **Every pipeline must be strictly idempotent.** Re-running the same logical date or partition twice MUST produce identical target state — prefer atomic partition overwrite or deterministic `MERGE` over bare `INSERT INTO`.
2. **Never execute destructive SQL without explicit human consent and dry-run proof.** `DROP TABLE/SCHEMA/DATABASE`, `TRUNCATE`, or `DELETE`/`UPDATE` without a narrow, verified `WHERE` predicate require explicit user approval first.
3. **Never write unverified data straight to production serving tables.** Use Write-Audit-Publish (WAP) staging or incremental assertion gates (`data-quality`) so malformed batches quarantine before consumers see them.
4. **Design for late-arriving data and partial failures.** Parameterize jobs by explicit `[start_utc, end_utc)` windows (never `CURRENT_DATE()` hardcoded inside business logic), include a bounded lookback window, and route unparseable records to a Dead-Letter Queue (DLQ) with error metadata.
5. **Measure cost and cardinality before scaling.** Dry-run queries to verify partition pruning and bytes scanned, assert join cardinality (`1:1` / `N:1`) to prevent silent fan-outs, and chunk historical backfills with concurrency caps so prod slots never saturate.
6. **Observability by default.** Emit per-run structured metrics (`rows_read`, `rows_written`, `rows_quarantined`, `bytes_scanned`, `duration_ms`, `watermark_utc`) on every batch so silent zero-row runs alert immediately.
