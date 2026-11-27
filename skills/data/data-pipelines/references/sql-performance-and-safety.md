# SQL Performance, Anti-Fanout & Destructive Safety Guardrails

Run `python3 scripts/sql_safety_lint.py <path.sql>` on every SQL/SQLX change before running against live warehouses.

## 1. Destructive Operation Consent Gate (Hard Block)

Before running ANY statement that causes irreversible data loss:
- `DROP TABLE`, `DROP VIEW`, `DROP SCHEMA`, `DROP DATABASE`
- `TRUNCATE TABLE`
- `DELETE FROM ...` or `UPDATE ...` without a narrow, verified `WHERE` predicate (or with `WHERE 1=1`)

**Mandatory steps:**
1. Run `SELECT COUNT(*)` with the exact target `WHERE` clause first to prove blast radius.
2. Obtain **explicit user confirmation** naming the exact environment, database/dataset, table, and estimated row count.
3. Prefer soft-delete flags, partition detach/drop with backup snapshot, or Time Travel / clone verification over blind in-place destruction.

## 2. Columnar & Warehouse Performance Checklist

| Anti-Pattern | Why It Hurts | Fix |
| :--- | :--- | :--- |
| `SELECT *` on columnar warehouses (BigQuery, Snowflake, Parquet) | Scans and bills **every** column even if only 3 are used; also breaks downstream contracts on column additions | Project explicit column lists at every layer |
| Non-sargable partition predicate (`WHERE DATE(event_at) = '2026-05-01'` or `WHERE YEAR(dt) = 2026`) | Defeats partition pruning and index range scans on many engines | Use half-open raw column bounds: `WHERE event_at >= TIMESTAMP '2026-05-01 00:00:00 UTC' AND event_at < TIMESTAMP '2026-05-02 00:00:00 UTC'` |
| `NOT IN (SELECT col FROM ...)` | Returns **0 rows** silently if the subquery produces even ONE `NULL`! | Use `NOT EXISTS (SELECT 1 FROM ... WHERE ...)` or `LEFT JOIN ... WHERE right.key IS NULL` |
| `UNION` when inputs are disjoint or dedup is unneeded | Forces an expensive global `DISTINCT` shuffle across all columns | Use `UNION ALL` by default; deduplicate explicitly only when required |
| `ORDER BY` inside a CTE or subquery without `LIMIT` | Wastes distributed sort memory and is ignored by outer queries | Remove inner `ORDER BY` unless paired with `LIMIT` or window framing |
| Self-join for latest-row-per-entity | Doubles scan bytes and triggers heavy shuffle | Use `QUALIFY ROW_NUMBER() OVER (PARTITION BY id ORDER BY updated_at DESC) = 1` (or CTE + `WHERE rn = 1`) |
| Unbounded `CROSS JOIN` | Cartesian explosion (`N × M` rows) crashing memory/slots | Explicitly bound with `ON` keys, or filter small calendar/spine tables first |

## 3. Anti-Fanout Join Discipline

The #1 silent bug in analytics engineering is joining a `1:N` table onto a fact table without pre-aggregating, silently multiplying revenue/counts by 2×–10×:
- Before every `JOIN`, state the cardinality (`1:1`, `N:1`, `1:N`, `M:N`).
- When joining `1:N` (e.g., `orders` → `order_discounts`), **pre-aggregate the right-hand CTE to the left-hand grain** (`GROUP BY order_id`) BEFORE joining.
- Verify post-join row count equals driving-table row count (`COUNT(*) = driving_count`) inside your staging audit (`data-quality`).
