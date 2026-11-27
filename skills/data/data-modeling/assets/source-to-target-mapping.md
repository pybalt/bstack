# Source-to-Target Schema Mapping Manifesto

## 1. Target Entity Summary
- **Target Table:** `<layer>.<table_name>`
- **Declared Grain:** One row per `<entity_key>` (enforced by PK: `[...]`)
- **Physical Layout:** Partitioned by `<date_col>` · Clustered/Indexed by `[...]`
- **Load Strategy:** `idempotent_partition_overwrite` | `merge_upsert` | `scd2` | `append_dedupe`

## 2. Source Inventory & Join Topology
| Alias | Source Table / Stream | Grain | Join Type & Keys | Fan-Out Risk Checked? |
| :--- | :--- | :--- | :--- | :---: |
| `src_a` | `bronze.orders_raw` | 1 row / `order_id` | Driving table | N/A |
| `src_b` | `silver.dim_customer_scd2` | 1 row / `customer_id` × validity range | `LEFT JOIN` on `customer_id` + `[valid_from, valid_to)` | Yes (half-open range) |

## 3. Column-Level Transformation Contract
| Target Column | Type | Nullable | Source Expression / Logic | Unit / TZ | PII Tag | Default / Null Policy |
| :--- | :--- | :---: | :--- | :--- | :---: | :--- |
| `order_id` | `STRING` | No | `TRIM(src_a.order_id)` | — | None | Quarantine if null |
| `gross_amount_cents` | `INT64` | No | `CAST(ROUND(src_a.gross_amount * 100) AS INT64)` | cents | None | Reject negative |
| `order_created_at_utc` | `TIMESTAMP` | No | `CAST(src_a.created_at AS TIMESTAMP)` | UTC | None | Quarantine if null |
| `customer_tier` | `STRING` | Yes | `COALESCE(src_b.plan_tier, 'unknown')` | — | None | `'unknown'` |

## 4. Open Edge Cases & Reconciliation Plan
- **Late-arriving records:** Reprocess lookback window of `N` days per run.
- **Reconciliation target:** Verify row count and `SUM(gross_amount_cents)` against `src_a` via `data-quality`.
