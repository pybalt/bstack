-- Engine-Agnostic Data Quality Assertion Suite (Zero-Row Failure Convention)
-- Every query below returns 0 rows on PASS and >= 1 failing rows on FAIL.

-- 1. GRAIN UNIQUENESS: Detect duplicate primary keys in target partition
SELECT
  order_id,
  COUNT(*) AS duplicate_count
FROM staging.fct_orders_stage
GROUP BY order_id
HAVING COUNT(*) > 1;

-- 2. COMPLETENESS & DOMAIN VALIDITY: Null required keys or invalid values
SELECT
  order_id,
  tenant_id,
  order_status,
  gross_amount_cents
FROM staging.fct_orders_stage
WHERE order_id IS NULL
   OR tenant_id IS NULL
   OR gross_amount_cents IS NULL
   OR gross_amount_cents < 0
   OR order_status NOT IN ('pending', 'paid', 'cancelled', 'refunded');

-- 3. REFERENTIAL INTEGRITY: Detect orphan foreign keys missing in conformed dimension
SELECT
  f.order_id,
  f.customer_id
FROM staging.fct_orders_stage AS f
LEFT JOIN silver.dim_customer AS d
  ON f.customer_id = d.customer_id
WHERE f.customer_id IS NOT NULL
  AND d.customer_id IS NULL;

-- 4. FRESHNESS SLA: Emit a row only when partition lag exceeds 60 minutes
SELECT
  MAX(order_created_at_utc) AS latest_event_utc,
  CURRENT_TIMESTAMP         AS checked_at_utc
FROM staging.fct_orders_stage
HAVING MAX(order_created_at_utc) IS NULL
    OR MAX(order_created_at_utc) < CURRENT_TIMESTAMP - INTERVAL '60' MINUTE;

-- 5. SOURCE-VS-TARGET RECONCILIATION (Volume & Numeric Checksum Parity)
WITH src AS (
  SELECT
    COUNT(*)                            AS row_count,
    COALESCE(SUM(gross_amount_cents), 0) AS total_cents
  FROM silver.orders_conformed
  WHERE order_created_at_utc >= :window_start_utc
    AND order_created_at_utc <  :window_end_utc
),
tgt AS (
  SELECT
    COUNT(*)                            AS row_count,
    COALESCE(SUM(gross_amount_cents), 0) AS total_cents
  FROM staging.fct_orders_stage
)
SELECT
  src.row_count   AS source_rows,
  tgt.row_count   AS target_rows,
  src.total_cents AS source_cents,
  tgt.total_cents AS target_cents
FROM src
JOIN tgt
  ON src.row_count <> tgt.row_count
  OR src.total_cents <> tgt.total_cents;
