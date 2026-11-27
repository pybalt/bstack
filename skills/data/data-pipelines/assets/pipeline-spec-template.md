# Pipeline & Backfill Spec (ODD-Aligned)

## 1. Identity & SLA
- **Pipeline / Asset Name:** `<dag_or_model_name>`
- **Owner / Escalation:** `<team / channel>`
- **Target Table & Grain:** `<layer>.<table>` — 1 row per `<grain_key>`
- **Cadence & Freshness SLA:** `<hourly | daily by HH:MM UTC>` · Max lag: `<N min>`

## 2. Source & Incremental Contract
- **Upstream Source(s):** `<source table / API / CDC topic>`
- **Window Parameters:** `[window_start_utc, window_end_utc)` (zero hardcoded `CURRENT_DATE()`)
- **Lookback Window:** `<N days/hours>` for late-arriving records
- **Idempotency Strategy:** `atomic_partition_overwrite` | `deterministic_merge` | `tx_delete_insert`
- **DLQ Policy:** Malformed rows routed to `bronze.<name>_dlq` · Hard-fail if `dlq_ratio > 1%`

## 3. Write-Audit-Publish (WAP) Gate
1. **Write:** Build into `staging.<table_name>__<run_id>` (or Iceberg WAP branch).
2. **Audit (`data-quality`):**
   - Zero PK duplicates at declared grain
   - Zero nulls on required contract columns
   - Row count within `[min_expected, max_expected]`
   - Numeric totals reconcile with source within `<epsilon>`
3. **Publish:** Atomic partition swap / merge into target only if all blocking checks pass.

## 4. Cost, Observability & Backfill Plan
- **Dry-Run Baseline (1 partition):** `<X GB scanned · Y seconds · $Z est.>`
- **Emitted Run Metrics:** `rows_read`, `rows_written`, `rows_quarantined`, `bytes_scanned`, `duration_ms`, `watermark_utc`
- **Backfill Strategy:** Chunk size `<7 days>` · Max concurrency `<2>` · Dedicated slot/pool `<low_priority>`
- **Rollback Plan:** Restore previous partition via Time Travel / snapshot ID or re-run prior code version over affected partition range.
