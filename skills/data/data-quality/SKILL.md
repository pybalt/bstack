---
name: data-quality
description: "Use when profiling datasets, writing data quality assertions (grain uniqueness, nulls, freshness, volume drift, referential integrity), auditing Write-Audit-Publish (WAP) staging tables, reconciling source-vs-target migrations or pipeline refactors, diagnosing silent row fan-outs or metric drift, or issuing a Data Verification Receipt before promoting tables. Do not use for schema modeling (use data-modeling), writing ETL/DAG pipelines (use data-pipelines), or software code QA (use qa-verify)."
version: 1.0.0
author: Leonel Baltazar Bravo
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [data-quality, data-observability, profiling, reconciliation, wap, assertions, dbt-tests, dataform, drift, rdd]
    related_skills: [data-modeling, data-pipelines, qa-verify, visual-brief, systematic-debugging]
---

# Data Quality, Observability & Reconciliation

Prove **data truth** before tables reach downstream consumers — catching duplicate grains, silent fan-out joins, null spikes, freshness lag, and migration mismatches with deterministic evidence.

## When to Use — and When NOT to Use

- **Use when:** profiling unfamiliar CSV/JSONL/warehouse datasets, implementing Write-Audit-Publish (WAP) circuit breakers, reconciling source-vs-target migrations or SQL refactors, triaging sudden KPI/row-count anomalies, or issuing a Data Verification Receipt.
- **Do NOT use for:** designing schemas or physical storage layout (use `data-modeling`), authoring ingestion/transformation pipelines or DAGs (use `data-pipelines`), or running software unit/E2E tests (use `qa-verify`).

## Progressive Disclosure Protocol

Load **only** the reference(s) needed for the active quality or reconciliation task:

| Need | Load ONLY this file | Inside |
| :--- | :--- | :--- |
| 6 DQ dimensions, blocking vs warning severity, WAP circuit breakers | `references/dq-dimensions-and-wap.md` | Pillar checklist, alert thresholds & `visual-brief` pairing |
| Source-vs-target migration parity, fan-out & timezone drift triage | `references/reconciliation-and-drift.md` | 4-tier reconciliation protocol & root-cause playbook |
| Implementing checks in dbt, Dataform, Soda/GX, or pure SQL/DuckDB | `references/dq-tools-map.md` | Cross-tool assertion syntax & selection guide |

**Executable Scripts & Copy-Ready Templates:**
- Profile CSV/TSV/JSONL datasets and validate grain/contract rules: `python3 scripts/profile_dataset.py <data.csv|jsonl> [--pk col1,col2] [--contract contract.json]` (JSON stdout; exits `1` on PK duplicates or contract failures).
- Reconcile source vs target datasets deterministically: `python3 scripts/reconcile_datasets.py <source.csv|jsonl> <target.csv|jsonl> [--pk id] [--tol 0.001]` (JSON reconciliation receipt; exits `1` on parity mismatch).
- Record data proof from **`assets/dq-receipt-template.md`** and bootstrap SQL assertions from **`assets/dq-assertions.sql`**.

## Non-Negotiable Operating Laws

1. **Green pipeline logs do NOT prove clean data.** A job returning exit `0` can still write 0 rows, double every dollar via a `1:N` fan-out join, or shift timestamps by a timezone offset. Verify data invariants directly.
2. **Always prove grain uniqueness first.** Check `COUNT(*) == COUNT(DISTINCT pk)` on every Silver/Gold table before computing or trusting any aggregate metric.
3. **Separate Hard-Fail Quarantine from Soft-Warn Alerts.** Primary-key duplicates, negative money, broken FKs on critical keys, and zero-row partitions MUST block publish (WAP circuit breaker); gradual distribution drift or optional-field null shifts emit warnings without paging at 3 AM unnecessarily.
4. **Reconcile refactors and migrations across all 4 tiers.** Never declare parity from row count alone — verify (1) row counts, (2) primary-key set diff, (3) null-rate delta, and (4) numeric checksum totals (`SUM`/`MIN`/`MAX`) within explicit tolerance.
5. **Distinguish Verified vs Sampled vs Unchecked scope.** State exact partition range, row counts inspected, and query/script outputs in the Data Verification Receipt; never extrapolate a 100-row preview into a full-table guarantee.
6. **Visualize complex DQ audits and drift with `visual-brief`.** For multi-table health reviews or drift investigations, present a concise `visual-brief` (`heatmap` for table × check severity, `funnel` for stage row retention, `bell`/`histogram` for distribution drift, `waterfall` for reconciliation variance).
