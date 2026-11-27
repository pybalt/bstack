# Transformation Engine Playbook (dbt, Dataform, DuckDB, Polars, Spark)

Pick the simplest engine that fits the data volume — never spin up Spark for a 2 GB dataset that DuckDB or Polars finishes in 1.5 seconds on one machine.

## 1. Engine Sizing Matrix

| Dataset Size / Workload | Preferred Engine | Why |
| :--- | :--- | :--- |
| `< 50 GB` local / CI / single-node | **DuckDB** (SQL) or **Polars** (Python DataFrame) | Vectorized columnar execution, out-of-core Parquet streaming, zero cluster startup latency |
| `10 GB – 100+ TB` warehouse-native SQL | **dbt** or **Dataform** (on BigQuery / Snowflake / Databricks / Postgres) | Pushdown compute, declarative DAG lineage, built-in incremental strategies & assertions |
| `> 100 GB` complex Python/ML/unstructured/distributed shuffles | **Apache Spark / PySpark** | Distributed shuffles, Iceberg/Delta native writes, adaptive query execution (AQE) |

## 2. dbt & Dataform Best Practices

- **Layered DAGs (`staging` → `intermediate` → `marts`):** Only `staging` reads raw `source()`/`ref()` Bronze tables (1:1 per source table, renaming & type casting only); `marts` join Silver entities into business contracts.
- **Incremental Guardrails:**
  - Always guard incremental scans with `{% if is_incremental() %}` (dbt) or `${ when(incremental(), ...) }` (Dataform) filtering on the **partition key** with a bounded lookback window (`>= DATE_SUB(max_dt, INTERVAL 3 DAY)`).
  - Specify `unique_key` + `partition_by` + `incremental_strategy` (`insert_overwrite` on BigQuery/Spark for date-partitioned facts; `merge` for mutable entities).
  - Add a **Slim CI** check (`dbt build --select state:modified+ --defer`) so PRs compile and test only affected downstream models against production state.
- **Zero Business Logic in Macros/UDFs When Plain SQL Suffices:** Keep SQL readable, testable, and optimizer-friendly.

## 3. DuckDB & Polars (High-Speed Local & Lightweight Pipelines)

- **DuckDB:**
  - Query Parquet/CSV/JSON directly with projection & predicate pushdown (`SELECT id, amount FROM read_parquet('s3://bucket/dt=2026-05-*/*.parquet', hive_partitioning=true)`).
  - Use `SET memory_limit='4GB'; SET temp_directory='/tmp/duckdb_spill';` for deterministic out-of-core execution on constrained VMs/containers.
  - Perfect for running local unit tests and WAP dry-runs against sample Parquet slices before hitting cloud warehouses.
- **Polars:**
  - Always prefer the **Lazy API** (`pl.scan_parquet(...)` → `.filter(...)` → `.select(...)` → `.sink_parquet(...)`) over eager `read_parquet` so the optimizer applies predicate/projection pushdown and streaming memory bounds.
  - Never use Python `.map_elements()` / row loops in hot paths — use native Polars expressions (`pl.col(...).when(...).then(...)`).

## 4. Apache Spark / PySpark Survival Guide

- **Eliminate Python UDFs:** Native `pyspark.sql.functions` execute in the JVM/Photon vectorized engine; row-wise Python UDFs serialize every row across the JVM-Python socket (10–100× slower). Use native expressions or vectorized `pandas_udf` only when unavoidable.
- **Enable Adaptive Query Execution (AQE):** Set `spark.sql.adaptive.enabled=true`, `spark.sql.adaptive.coalescePartitions.enabled=true`, and `spark.sql.adaptive.skewJoin.enabled=true` to auto-coalesce tiny shuffle partitions and split skewed join keys.
- **Broadcast Small Dimensions:** Explicitly `broadcast(dim_df)` when joining a large fact table against a dimension `< 50–100 MB` to eliminate full network shuffles.
- **Kill Skew & OOMs:** If one key (e.g., `tenant_id = 'unknown'` or `NULL`) holds 40% of rows, filter/split NULLs before joining or salt the join key (`concat(key, '_', floor(rand() * 16))`).
- **Avoid `.collect()` / `.toPandas()` on Unbounded DataFrames:** Always `.limit(N)` or aggregate before pulling to the driver to prevent driver OOM crashes.
