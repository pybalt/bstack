---
name: data-modeling
description: "Use when designing warehouse schemas, declaring table grain and primary keys, modeling Medallion layers (Bronze/Silver/Gold) or dimensional facts/dimensions (Star, OBT, SCD Type 1/2/6), tuning physical storage (BigQuery, Snowflake, Postgres/Oracle, Iceberg/Delta), mapping source-to-target schemas, or auditing breaking schema evolution and data contracts. Do not use for writing DAGs/ETL execution code (use data-pipelines) or profiling/reconciling live data (use data-quality)."
version: 1.0.0
author: Leonel Baltazar Bravo
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [data-modeling, warehouse, schema, grain, kimball, medallion, scd, data-contracts, bigquery, snowflake, iceberg, postgres]
    related_skills: [grill, data-pipelines, data-quality, visual-brief, qa-verify]
---

# Data Modeling & Contracts

Design **grain-first, evolvable, engine-aware data models** that prevent silent join fan-outs, broken downstream BI, and runaway warehouse storage or scan costs.

## When to Use — and When NOT to Use

- **Use when:** defining new tables or semantic layers, choosing between Star Schema, One Big Table (OBT), or Medallion layers, implementing SCD Type 1/2/6, mapping 3+ source tables into target models, tuning partitions/clustering/indexes, or reviewing schema changes against data contracts.
- **Do NOT use for:** writing ingestion/ETL orchestration code or fixing slow pipeline DAGs (use `data-pipelines`), auditing row-level quality or reconciling live counts (use `data-quality`), or general application architecture trade-offs outside data models (use `grill`).

## Progressive Disclosure Protocol

Load **only** the reference(s) needed for the active modeling task:

| Need | Load ONLY this file | Inside |
| :--- | :--- | :--- |
| Grain, Star vs OBT vs Data Vault, Medallion layers, SCD 1/2/6 SQL | `references/modeling-patterns.md` | Pattern selector, fact/dim taxonomy, SCD templates |
| Partitioning, clustering, indexes, Iceberg/Delta compaction | `references/warehouse-storage-tuning.md` | BigQuery, Snowflake, Postgres/Oracle, Iceberg/Delta physics |
| Additive vs breaking changes, expand-contract, PII & SLAs | `references/schema-evolution-and-contracts.md` | Zero-downtime evolution rules & contract governance |

**Executable Script & Copy-Ready Templates:**
- Compare before/after schemas deterministically for breaking drift: `python3 scripts/schema_diff.py <old_schema.json> <new_schema.json>` (classifies `SAFE_ADDITIVE`, `WARNING`, and `BREAKING_CHANGE` in JSON stdout; exits `1` on breaking changes).
- Author a production table contract from **`assets/data-contract-template.yaml`**.
- Document multi-table schema transformations from **`assets/source-to-target-mapping.md`**.

## Non-Negotiable Operating Laws

1. **Declare grain before writing a single column.** State in one sentence what exactly one row represents (*"one row per order_line_id"* or *"one row per account_id per UTC day"*) and name the enforcing primary key. A model without an explicit grain is a fan-out bug waiting to happen.
2. **Enforce Medallion boundary discipline.** Bronze preserves raw, immutable source fidelity with ingestion metadata (`_ingested_at`, `_source_file`); Silver standardizes types, timezone (UTC), deduplication, and explicit grain; Gold serves consumer-ready facts, dimensions, or OBT marts backed by a data contract.
3. **Choose the simplest model that fits the query workload.** Default to Kimball Star Schema (or Silver normalized + Gold OBT for BI tools that penalize joins). Avoid Data Vault unless multi-source enterprise auditability is a measured requirement.
4. **Treat schema changes as public API changes.** Additive nullable columns are safe; dropping, renaming, narrowing types, changing units/timezones, or altering grain are **breaking changes** requiring expand-contract migration and consumer notice.
5. **Align physical layout to the actual query predicate.** Partition by the dominant time/event filter column (never high-cardinality IDs), cluster/sort by the top 2–4 filter/join keys in selectivity order, and enforce partition filters on large analytical tables.
6. **Classify PII and retention at design time.** Tag sensitive columns (`PII`, `PCI`, `PHI`) in the contract before ingestion, separate direct identifiers into restricted vaults when required, and persist major model decisions as ADRs at task closure.
