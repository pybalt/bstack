#!/usr/bin/env python3
"""Deterministic source-vs-target dataset reconciler (CSV, TSV, JSONL/NDJSON).

Verifies 4-tier parity between a source baseline and target dataset:
1. Row count parity
2. Primary-key set parity (--pk: missing & extra keys)
3. Per-column null-rate delta
4. Numeric aggregate parity (SUM, MIN, MAX, MEAN within --tol)

Outputs a JSON Data Reconciliation Receipt to stdout.
Exit codes: 0 = reconciled, 1 = mismatch detected, 2 = error.
"""
import argparse
import csv
import json
import math
import statistics
import sys
from pathlib import Path

NULL_TOKENS = {"", "null", "none", "nan", "na", "n/a"}


def is_null(v) -> bool:
    if v is None:
        return True
    return isinstance(v, str) and v.strip().lower() in NULL_TOKENS


def try_float(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return None if math.isnan(v) or math.isinf(v) else float(v)
    if isinstance(v, str):
        s = v.strip()
        if not s:
            return None
        try:
            f = float(s)
            return None if math.isnan(f) or math.isinf(f) else f
        except ValueError:
            return None
    return None


def load_rows(path: Path) -> tuple[list[str], list[dict]]:
    ext = path.suffix.lower()
    if ext in {".jsonl", ".ndjson"}:
        rows, cols, seen = [], [], set()
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if not s:
                    continue
                obj = json.loads(s)
                rows.append(obj)
                for k in obj.keys():
                    if k not in seen:
                        seen.add(k)
                        cols.append(k)
        return cols, rows
    delim = "\t" if ext == ".tsv" else ","
    with path.open("r", encoding="utf-8", newline="") as f:
        r = csv.DictReader(f, delimiter=delim)
        return list(r.fieldnames or []), list(r)


def reconcile(src_path: Path, tgt_path: Path, pk_cols: list[str], tol: float) -> dict:
    s_cols, s_rows = load_rows(src_path)
    t_cols, t_rows = load_rows(tgt_path)
    mismatches = []

    # Tier 1: Volume & Schema columns
    if len(s_rows) != len(t_rows):
        mismatches.append(f"Row count mismatch: source={len(s_rows)} vs target={len(t_rows)} (delta={len(t_rows) - len(s_rows):+d})")

    s_set, t_set = set(s_cols), set(t_cols)
    missing_cols = sorted(s_set - t_set)
    extra_cols = sorted(t_set - s_set)
    if missing_cols:
        mismatches.append(f"Columns missing in target: {missing_cols}")

    # Tier 2: Key-Set Parity
    key_diff = None
    if pk_cols:
        if any(c not in s_set or c not in t_set for c in pk_cols):
            mismatches.append(f"Primary key {pk_cols} missing in source or target schema.")
        else:
            sk = {tuple(str(r.get(c, "")).strip() for c in pk_cols) for r in s_rows}
            tk = {tuple(str(r.get(c, "")).strip() for c in pk_cols) for r in t_rows}
            miss_k = sorted(sk - tk)
            extra_k = sorted(tk - sk)
            key_diff = {
                "pk": pk_cols,
                "source_unique_keys": len(sk),
                "target_unique_keys": len(tk),
                "missing_in_target_count": len(miss_k),
                "extra_in_target_count": len(extra_k),
                "sample_missing": [list(k) for k in miss_k[:5]],
                "sample_extra": [list(k) for k in extra_k[:5]],
            }
            if miss_k:
                mismatches.append(f"Key-set mismatch: {len(miss_k)} key(s) missing in target.")
            if extra_k:
                mismatches.append(f"Key-set mismatch: {len(extra_k)} unexpected extra key(s) in target.")

    # Tier 3 & 4: Null-rate parity & Numeric aggregate checksums
    common_cols = [c for c in s_cols if c in t_set]
    col_checks = {}
    for col in common_cols:
        s_non = [r.get(col) for r in s_rows if not is_null(r.get(col))]
        t_non = [r.get(col) for r in t_rows if not is_null(r.get(col))]
        s_null_pct = round(((len(s_rows) - len(s_non)) / len(s_rows)) * 100.0, 2) if s_rows else 0.0
        t_null_pct = round(((len(t_rows) - len(t_non)) / len(t_rows)) * 100.0, 2) if t_rows else 0.0
        entry = {"source_null_pct": s_null_pct, "target_null_pct": t_null_pct, "null_pct_delta": round(t_null_pct - s_null_pct, 2)}
        if abs(t_null_pct - s_null_pct) > tol * 100.0 and abs(t_null_pct - s_null_pct) > 0.01:
            mismatches.append(f"Column '{col}' null_pct drift: source={s_null_pct}% vs target={t_null_pct}%")

        s_nums = [n for n in (try_float(v) for v in s_non) if n is not None]
        t_nums = [n for n in (try_float(v) for v in t_non) if n is not None]
        if s_non and t_non and len(s_nums) == len(s_non) and len(t_nums) == len(t_non):
            s_sum, t_sum = sum(s_nums), sum(t_nums)
            s_mean, t_mean = statistics.mean(s_nums), statistics.mean(t_nums)
            s_min, t_min = min(s_nums), min(t_nums)
            s_max, t_max = max(s_nums), max(t_nums)
            sum_delta = t_sum - s_sum
            entry["numeric"] = {
                "source_sum": round(s_sum, 4),
                "target_sum": round(t_sum, 4),
                "sum_delta": round(sum_delta, 4),
                "source_mean": round(s_mean, 4),
                "target_mean": round(t_mean, 4),
                "min_match": abs(t_min - s_min) <= tol,
                "max_match": abs(t_max - s_max) <= tol,
            }
            if abs(sum_delta) > tol:
                mismatches.append(f"Column '{col}' SUM mismatch: source={s_sum:.4f} vs target={t_sum:.4f} (delta={sum_delta:+.4f}, tol={tol})")
            if abs(t_min - s_min) > tol or abs(t_max - s_max) > tol:
                mismatches.append(f"Column '{col}' MIN/MAX mismatch: src=[{s_min},{s_max}] vs tgt=[{t_min},{t_max}]")
        col_checks[col] = entry

    return {
        "status": "mismatch" if mismatches else "reconciled",
        "source": src_path.name,
        "target": tgt_path.name,
        "tolerance": tol,
        "row_counts": {"source": len(s_rows), "target": len(t_rows), "delta": len(t_rows) - len(s_rows)},
        "schema_diff": {"missing_in_target": missing_cols, "extra_in_target": extra_cols},
        "key_diff": key_diff,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "columns": col_checks,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("source", type=Path, help="Source baseline dataset (.csv/.tsv/.jsonl)")
    ap.add_argument("target", type=Path, help="Target dataset (.csv/.tsv/.jsonl)")
    ap.add_argument("--pk", default="", help="Comma-separated primary key column(s) for Tier-2 key diff")
    ap.add_argument("--tol", type=float, default=1e-4, help="Numeric absolute tolerance (default: 0.0001)")
    args = ap.parse_args()

    try:
        pk_cols = [c.strip() for c in args.pk.split(",") if c.strip()]
        report = reconcile(args.source.resolve(), args.target.resolve(), pk_cols, args.tol)
    except Exception as exc:
        print(json.dumps({"status": "error", "error": str(exc)}), file=sys.stderr)
        return 2

    print(json.dumps(report, indent=2))
    return 1 if report["mismatch_count"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
