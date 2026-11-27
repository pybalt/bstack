# Cross-Engine DQ Tools Map (dbt, Dataform, Soda/GX, Pure SQL)

Keep quality assertions close to the transformation DAG so failing checks automatically halt downstream promotion.

## 1. Tool Selector

| Stack | Native DQ Primitive | Recommended Starter Checks |
| :--- | :--- | :--- |
| **dbt** | Schema YAML `data_tests` + `dbt_utils` + `elementary` | `unique`, `not_null`, `accepted_values`, `relationships`, `dbt_utils.unique_combination_of_columns`, `source freshness`, `store_failures: true` |
| **Dataform (BigQuery)** | Inline `assertions: { uniqueKey, nonNull, rowConditions }` + standalone `type: "assertion"` `.sqlx` | Built-in `uniqueKey` / `nonNull` on every Silver/Gold table; custom `.sqlx` assertions returning failing rows (0 rows = pass) wired into `dependencies` |
| **Soda / Great Expectations** | Declarative YAML checks / Expectation Suites | Best when auditing external lakes, Python/Spark jobs, or non-SQL sources where dbt/Dataform are absent |
| **Pure SQL / DuckDB** *(Zero-Infra Fallback)* | `assets/dq-assertions.sql` + `scripts/profile_dataset.py` | Portable across BigQuery, Snowflake, Postgres, Oracle, DuckDB; returns violating rows or structured summary counts |

## 2. Canonical Idioms

### dbt (`schema.yml`)
```yaml
models:
  - name: fct_orders
    data_tests:
      - dbt_utils.unique_combination_of_columns:
          combination_of_columns: [order_id]
    columns:
      - name: order_id
        data_tests: [unique, not_null]
      - name: order_status
        data_tests:
          - accepted_values:
              values: ["pending", "paid", "cancelled", "refunded"]
```

### Dataform (`.sqlx` config)
```sql
config {
  type: "incremental",
  schema: "gold",
  assertions: {
    uniqueKey: ["order_id"],
    nonNull: ["order_id", "tenant_id", "gross_amount_cents", "order_created_at_utc"],
    rowConditions: ["gross_amount_cents >= 0"]
  }
}
```

### Rule of Thumb: Zero-Row Failure Semantics
Write every custom SQL assertion so **returning 0 rows = PASS** and **returning `>= 1` rows = FAIL** (with the violating keys + reason in the output). That convention works identically across dbt singular tests, Dataform assertions, Airflow `SQLCheckOperator`, and CI harnesses.
