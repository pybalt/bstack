# Data Quality Dimensions & Write-Audit-Publish (WAP) Gates

## 1. The 6 Data Quality Pillars

| Pillar | Concrete Question | Default Check | Severity Tier |
| :--- | :--- | :--- | :--- |
| **1. Uniqueness (Grain)** | Does every primary key appear exactly once? | `COUNT(*) - COUNT(DISTINCT pk) = 0` | **Hard Fail (Block Publish)** |
| **2. Completeness** | Are required keys and measures non-null? | `null_rate(required_col) = 0`; optional cols within historical band | **Hard Fail** (required) / **Warn** (optional) |
| **3. Validity (Domain)** | Do values respect enums, ranges, formats, and signs? | `amount_cents >= 0`, `status IN (...)`, valid ISO currency/country | **Hard Fail** or **Route to DLQ** |
| **4. Timeliness (Freshness)** | Did the latest partition arrive within SLA? | `NOW_UTC - MAX(event_at_utc) <= sla_max_lag` | **Warn** → **Escalate** on SLA breach |
| **5. Consistency (Integrity)** | Do foreign keys match conformed dimensions and cross-field rules? | `orphan_fk_count = 0`; `shipped_at >= ordered_at` | **Hard Fail** (core FKs) / **Warn** (late dim) |
| **6. Volume & Drift** | Did row count or metric distribution shift unexpectedly? | Trailing 14-day z-score or `[0.5×, 2.0×]` rolling median band; zero-row check | **Hard Fail** (0 rows) / **Warn** (drift) |

## 2. Severity Tier Discipline (Avoid Alert Fatigue)

- **Tier 1 — Circuit Breaker (Block Publish / Quarantine):**
  - Duplicate primary keys at declared grain
  - Zero rows written for an expected non-empty partition
  - Nulls in primary key, partition key, or financial amount
  - Source-to-target reconciliation variance exceeding contract tolerance
  - Breaking schema drift (`schema_diff.py` exit `1`)
- **Tier 2 — Soft Warning (Publish + Alert Owner):**
  - Optional attribute null rate increased by > 5 percentage points vs 7-day baseline
  - Late-arriving dimension key temporarily mapped to `'unknown'` surrogate
  - Volume deviation `|z| > 2.5` (could be a legitimate holiday/campaign spike — confirm before rolling back)

## 3. Pairing DQ Reports with `visual-brief`

When auditing multiple tables or presenting a pipeline health review, map DQ signals directly to `visual-brief` blocks instead of dumping walls of SQL output:
- **Table × Pillar health status:** `heatmap` (`scale: "risk"`) showing failing/warning counts per table and DQ pillar.
- **Pipeline row retention (Bronze → Silver → Valid → Gold):** `funnel` highlighting drop-off % at deduplication and DLQ stages.
- **Distribution drift (Baseline vs Current batch):** `bell` or `histogram` + `boxplot` comparing quartiles and tail outliers.
- **Reconciliation delta breakdown:** `waterfall` showing exactly which filter/join explains source-vs-target variance.
