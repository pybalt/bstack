# Engine-Specific Warehouse & Storage Physics

Model logically once, then tune physical layout to the target engine's actual scan and pruning mechanics.

## 1. BigQuery (Columnar Serverless)

- **Partitioning:** Partition tables > 1 GB by a `DATE` or `TIMESTAMP` column (`PARTITION BY DATE(event_at_utc)`). Never partition by string or high-cardinality integer unless using explicit `RANGE_BUCKET`.
- **Mandatory Guardrail:** Set `OPTIONS(require_partition_filter = true)` on large fact tables (> 50 GB) so accidental full-table scans fail at dry-run instead of burning terabytes.
- **Clustering:** Cluster up to **4 columns** ordered by **most common equality/range filter first, then join key, then GROUP BY key** (e.g., `CLUSTER BY tenant_id, status, customer_id`). Clustering works automatically on top of partitions at zero extra storage cost.
- **Nested & Repeated (`STRUCT` / `ARRAY`):** Ideal for 1:N child attributes (e.g., order line items) inside Bronze/Silver when always queried together — avoids shuffle joins while preserving columnar compression.
- **Money / Precision:** Use `NUMERIC` / `BIGNUMERIC` (or integer minor units like `amount_cents INT64`) — never `FLOAT64` for financial totals.

## 2. Snowflake (Columnar Micro-Partitions)

- **Automatic Micro-Partitions (50–500 MB uncompressed):** Snowflake prunes automatically when data is inserted in natural time order. Avoid manual `CLUSTER BY` on tables < 1 TB (automatic reclustering consumes background credits).
- **Explicit Clustering Keys:** Add `CLUSTER BY (TO_DATE(event_at_utc), tenant_id)` only on multi-TB tables with high overlap depth (`SYSTEM$CLUSTERING_INFORMATION`). Order from lower to higher cardinality (unlike B-tree indexes!).
- **Zero-Copy Clones & Time Travel:** Use `CREATE TABLE staging CLONE prod` for safe schema rehearsals and Write-Audit-Publish staging without duplicating storage bytes.
- **Search Optimization Service:** Reserve for selective point-lookup queries (`WHERE user_uuid = '...'`) on massive tables where clustering cannot cover the column.

## 3. PostgreSQL & Oracle (Row-Store OLTP / Operational Marts)

- **Partitioning:** Use declarative `PARTITION BY RANGE (event_at_utc)` (monthly or daily) for append-heavy tables > 50–100M rows so old partitions drop instantaneously (`DROP TABLE` / `DETACH PARTITION`) without VACUUM storms.
- **Index Selection:**
  - **B-Tree (default):** Composite index column order = **Equality predicates first, Range predicate last** (`(tenant_id, status, created_at)`). Add `INCLUDE (amount_cents)` for covering index-only scans.
  - **BRIN (Postgres):** Tiny footprint (~1000× smaller than B-Tree) for physically ordered append-only timestamp columns.
  - **GIN / Bitmap:** GIN for Postgres `JSONB`/array containment (`@>`); Oracle Bitmap indexes ONLY on low-cardinality read-mostly DW tables (never high-concurrency OLTP!).
- **Postgres MVCC Hygiene:** Heavy `UPDATE`/`DELETE` batches cause table bloat; prefer partition replacement or batched `UPSERT` with tuned `autovacuum_vacuum_scale_factor`.

## 4. Open Table Formats — Apache Iceberg & Delta Lake (Spark / DuckDB / Trino)

- **Hidden Partitioning (Iceberg):** Partition via transforms (`days(event_at_utc)`, `bucket(16, tenant_id)`) without adding synthetic partition columns that users forget to filter.
- **Small Files Problem:** Streaming or frequent micro-batch appends degrade scan latency linearly with file count. Target **128–512 MB Parquet files** via scheduled compaction (`rewrite_data_files` / `OPTIMIZE`).
- **Multi-Dimensional Locality:** Use **Z-Ordering** or **Liquid Clustering** (Delta) / sort orders (Iceberg) on the 2–3 dominant filter keys.
- **Metadata Hygiene:** Schedule `expire_snapshots` (Iceberg) or `VACUUM` (Delta) respecting your time-travel retention window (typically 7–14 days) so orphan files do not silently inflate object storage bills.
