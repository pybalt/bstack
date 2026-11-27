# Core Data Modeling Patterns (Grain, Medallion, Dimensional & SCD)

## 1. The Grain-First Law

Before naming columns or choosing a physical engine, write a **one-line grain statement**:
- **Good:** `"One row per payment_attempt_id (immutable event)"` · `"One row per customer_id per calendar UTC date (daily snapshot)"`
- **Bad:** `"Payment data"` · `"Customer metrics"` (ambiguous grain guarantees duplicate joins downstream)

Every Silver and Gold table MUST specify:
1. **Natural / Business Key** (e.g., `order_id`, `line_number`)
2. **Deterministic Surrogate Key** (hash of canonicalized natural key + source system when integrating multiple sources, e.g., `sha256(concat_ws('|', source_sys, coalesce(cast(id as string), '')))`)
3. **Time Semantics:** Distinguish `event_at_utc` (business occurrence), `updated_at_utc` (source mutation), and `_ingested_at_utc` (warehouse arrival). Never mix local timezones in storage — store UTC and convert only in the presentation layer.

## 2. Architecture Selector (Star Schema vs OBT vs Data Vault)

| Model Pattern | Best Fit | Avoid When | Trade-Off |
| :--- | :--- | :--- | :--- |
| **Kimball Star Schema** *(Facts + Conformed Dims)* | Shared enterprise BI, reusable dimensions (`dim_customer`, `dim_date`), multi-fact drill-across | Tiny single-use mart with 1 consumer | Clean single source of truth; moderate join overhead in legacy BI |
| **One Big Table (OBT)** *(Wide denormalized Gold mart)* | Columnar cloud warehouses (BigQuery, Snowflake, DuckDB) serving BI dashboards or ML feature exports | Source-of-truth canonical layer where dim updates must propagate cleanly | Fastest analytical scan & simplest BI SQL; build Gold OBT *from* Silver facts/dims, never raw Bronze |
| **Normalized 3NF (OLTP / Silver Core)** | Transactional databases (Postgres, Oracle), strict referential integrity, high write concurrency | Wide analytical scans across 10+ tables | Eliminates update anomalies; requires Gold rollups for analytics |
| **Data Vault 2.0** *(Hubs, Links, Satellites)* | Regulated multi-ERP integration requiring full historical lineage and parallel team ingestion | Small/mid teams (< 10 data engineers) or fast-moving product analytics | High auditability; heavy join complexity and boilerplate overhead |

## 3. Medallion Layer Contracts (Bronze → Silver → Gold)

| Layer | Purpose | Transformations Allowed | Immutability / Idempotency |
| :--- | :--- | :--- | :--- |
| **Bronze (Raw)** | Replayable landing zone matching source payloads | None to business values; add metadata (`_ingested_at_utc`, `_batch_id`, `_source_system`). Keep raw JSON/strings if schema drifts. | Append-only or partition-immutable; never edit historical facts in place |
| **Silver (Conformed)** | Clean, deduplicated, typed entities at declared grain | Cast types, normalize UTC timestamps, dedupe on natural key, standardize enums, quarantine malformed rows to DLQ | Deterministic & replayable from Bronze; enforced primary-key uniqueness |
| **Gold (Serving / Mart)** | Business-ready metrics, Star facts/dims, OBT, or ML features | Joins across Silver entities, conformed KPI calculations, pre-aggregations, metric contracts | Contract-governed (SLA, owner, breaking-change protection) |

## 4. Fact Table Taxonomy

- **Transaction Fact:** One row per discrete event (`fct_order_items`, `fct_payments`). Append/upsert by event partition. Additive measures (`amount_cents`, `quantity`).
- **Periodic Snapshot Fact:** One row per entity per fixed interval (`fct_account_balance_daily`). Semi-additive measures (do NOT sum balances across dates; average or take latest date!).
- **Accumulating Snapshot Fact:** One row per lifecycle (`fct_order_fulfillment` with `ordered_at`, `paid_at`, `shipped_at`, `delivered_at`). Updated via `MERGE` as milestones complete.

## 5. Slowly Changing Dimensions (SCD) Quick Reference

| Type | Behavior | When to Use |
| :--- | :--- | :--- |
| **SCD Type 1** | Overwrite attribute in place | Typo fixes, non-historical attributes (e.g., current email or display name) |
| **SCD Type 2** | Close old version (`valid_to_utc`, `is_current = false`) and insert new version (`valid_from_utc`, `is_current = true`) | Historical point-in-time attribution (customer tier, pricing plan, territory, contract status) |
| **SCD Type 6 (Hybrid)** | Type 2 history rows + `current_<attr>` column updated across all historical rows | Reporting requiring both *as-was* and *as-is* slicing without self-joins |

### Canonical SCD Type 2 Point-in-Time Join Pattern

```sql
SELECT
  f.order_id,
  f.event_at_utc,
  d.plan_tier AS plan_tier_at_order_time
FROM silver.fct_orders AS f
LEFT JOIN silver.dim_customer_scd2 AS d
  ON f.customer_id = d.customer_id
 AND f.event_at_utc >= d.valid_from_utc
 AND f.event_at_utc <  COALESCE(d.valid_to_utc, TIMESTAMP '9999-12-31 00:00:00 UTC');
```

**Anti-Bug Rule:** Always use half-open intervals `[valid_from_utc, valid_to_utc)` — never `BETWEEN`, which double-matches events landing on the exact boundary timestamp!
