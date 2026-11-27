# Orchestration & Safe Backfill Runbooks (Airflow, Dagster, Prefect)

## 1. Orchestrator Selector & Core Idioms

| Orchestrator | Core Mental Model | Best Idioms to Enforce |
| :--- | :--- | :--- |
| **Airflow / Cloud Composer** | Task-based DAGs with logical date (`data_interval_start` / `data_interval_end`) | Keep top-level DAG parse time `< 2s` (ZERO DB queries or HTTP calls at module import time!); use TaskFlow API, **Deferrable Operators** for sensors (frees worker slots), `max_active_runs`, and `pool` caps |
| **Dagster** | Software-Defined Assets (asset lineage, partitions, freshness policies) | Model tables as `@asset` with `DailyPartitionsDefinition`, attach `@asset_check` for WAP gates, use `IOManager` cleanly so unit tests swap prod warehouse for DuckDB/memory |
| **Prefect** | Pythonic flows/tasks with dynamic runtime control | Use `@task(retries=3, retry_delay_seconds=exponential_backoff(10))`, explicit result persistence for resume-on-failure, and concurrency limits on external API tags |

## 2. Production DAG Hygiene Checklist

- **Thin orchestrator, fat compute:** The orchestrator schedules, passes parameters, retries, and tracks state — NEVER process gigabytes of data inside an Airflow scheduler or worker container; push compute to SQL warehouse, Spark, DuckDB container, or isolated K8s pod.
- **Explicit timeouts & bounded retries:** Every task sets `execution_timeout`, `retries` (typically 2–3), exponential backoff, and jitter so transient API/warehouse hiccups recover without infinite retry loops.
- **External API rate-limit respect:** Bound concurrency with orchestrator pools/semaphores and handle HTTP `429` (`Retry-After`) gracefully.
- **Alerts with actionable context:** On failure, emit `dag_id`, `task_id`, `logical_date`, `run_id`, log URL, and runbook link — never generic *"Task failed"* noise.

## 3. Safe Chunked Backfill Protocol

Reprocessing 2 years of history carelessly will exhaust warehouse slots, trigger API bans, or double-bill cloud budgets. Follow this 5-step sequence:

1. **Dry-run 1 single partition first:** Run a single historical date (`dt = 2025-06-15`) into staging, inspect `bytes_scanned`, duration, and `data-quality` checks. Extrapolate total cost (`single_day_cost × total_days`) and confirm budget before launching.
2. **Verify downstream impact:** Check whether downstream incremental models or BI extracts consume this table — decide if downstream needs a coordinated backfill or if historical updates should stay isolated until complete.
3. **Chunk into bounded batches:** Process in chronological or reverse-chronological chunks (e.g., 7–30 days per batch) with `max_active_runs = 2..4` (or dedicated low-priority warehouse slot/reservation pool) so scheduled prod SLAs never starve.
4. **Pause competing alerts / suppress noisy fan-out notifications** during planned backfills if downstream alerting triggers on historical partition writes — never silence hard-failure circuit breakers.
5. **Reconcile end-to-end post-backfill:** Run `data-quality` volume continuity check (confirm zero missing dates in the backfilled calendar range) and source-vs-target aggregate parity before closing the runbook.
