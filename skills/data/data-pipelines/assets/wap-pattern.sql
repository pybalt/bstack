-- Engine-Agnostic Write-Audit-Publish (WAP) & Idempotent Partition Template
-- Parameters injected by orchestrator:
--   :window_start_utc  (inclusive, e.g., TIMESTAMP '2026-05-01 00:00:00 UTC')
--   :window_end_utc    (exclusive, e.g., TIMESTAMP '2026-05-02 00:00:00 UTC')
--   :run_date          (DATE '2026-05-01')

-- STEP 1: WRITE to isolated staging table (deduplicated at declared grain)
CREATE OR REPLACE TABLE staging.fct_orders_stage AS
WITH ranked_source AS (
  SELECT
    TRIM(order_id)                                     AS order_id,
    tenant_id,
    order_status,
    CAST(ROUND(gross_amount * 100) AS BIGINT)          AS gross_amount_cents,
    CAST(created_at_utc AS TIMESTAMP)                  AS order_created_at_utc,
    CAST(_ingested_at_utc AS TIMESTAMP)                AS _ingested_at_utc,
    ROW_NUMBER() OVER (
      PARTITION BY TRIM(order_id)
      ORDER BY updated_at_utc DESC, _ingested_at_utc DESC
    )                                                  AS _rn
  FROM bronze.orders_raw
  WHERE created_at_utc >= :window_start_utc
    AND created_at_utc <  :window_end_utc
    AND order_id IS NOT NULL
)
SELECT
  order_id,
  tenant_id,
  order_status,
  gross_amount_cents,
  order_created_at_utc,
  _ingested_at_utc
FROM ranked_source
WHERE _rn = 1;

-- STEP 2: AUDIT staging before touching production (fail pipeline if any check > 0)
SELECT
  COUNT(*)                                                               AS row_count,
  COUNT(*) - COUNT(DISTINCT order_id)                                    AS duplicate_pk_rows,
  SUM(CASE WHEN tenant_id IS NULL OR gross_amount_cents < 0 THEN 1 ELSE 0 END) AS invalid_rows,
  COALESCE(SUM(gross_amount_cents), 0)                                   AS total_gross_cents
FROM staging.fct_orders_stage;

-- STEP 3: PUBLISH atomically (idempotent partition replacement inside transaction)
-- On BigQuery/Spark/Iceberg, prefer native partition overwrite (INSERT OVERWRITE / WRITE_TRUNCATE).
BEGIN TRANSACTION;

DELETE FROM gold.fct_orders
WHERE order_created_at_utc >= :window_start_utc
  AND order_created_at_utc <  :window_end_utc;

INSERT INTO gold.fct_orders (
  order_id,
  tenant_id,
  order_status,
  gross_amount_cents,
  order_created_at_utc,
  _ingested_at_utc
)
SELECT
  order_id,
  tenant_id,
  order_status,
  gross_amount_cents,
  order_created_at_utc,
  _ingested_at_utc
FROM staging.fct_orders_stage;

COMMIT;
