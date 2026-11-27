#!/usr/bin/env python3
"""Deterministic dataset profiler & contract validator (CSV, TSV, JSONL/NDJSON).

Computes per-column statistics (null rate, distinct count, inferred type, numeric
min/max/mean/median/p95/stddev, top values), checks declared primary-key grain
uniqueness (--pk), and validates an optional JSON contract (--contract).

Outputs JSON to stdout.
Exit codes: 0 = profile/contract OK, 1 = PK duplicates or contract failures, 2 = error.
"""
import argparse
import csv
import json
import math
import statistics
import sys
from collections import Counter
from pathlib import Path

NULL_TOKENS = {"", "null", "none", "nan", "na", "n/a"}


def is_null(v) -> bool:
    if v is None:
        return True
    if isinstance(v, str) and v.strip().lower() in NULL_TOKENS:
        return True
    return False


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
        rows = []
        cols_seen = []
        col_set = set()
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if not s:
                    continue
                obj = json.loads(s)
                if not isinstance(obj, dict):
                    raise ValueError("JSONL lines must be JSON objects.")
                rows.append(obj)
                for k in obj.keys():
                    if k not in col_set:
                        col_set.add(k)
                        cols_seen.append(k)
        return cols_seen, rows

    delimiter = "\t" if ext == ".tsv" else ","
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        cols = list(reader.fieldnames or [])
        rows = list(reader)
    return cols, rows


def percentile(sorted_vals: list[float], p: float) -> float:
    if not sorted_vals:
        return 0.0
    k = (len(sorted_vals) - 1) * p
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_vals[int(k)]
    return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)


def infer_type(non_null: list, nums: list[float]) -> str:
    if not non_null:
        return "EMPTY"
    if len(nums) == len(non_null):
        if all(float(x).is_integer() for x in nums):
            return "INTEGER"
        return "FLOAT"
    bools = {"true", "false"}
    if all(isinstance(v, bool) or (isinstance(v, str) and v.strip().lower() in bools) for v in non_null):
        return "BOOLEAN"
    return "STRING"


def profile(path: Path, pk_cols: list[str], contract: dict | None) -> dict:
    cols, rows = load_rows(path)
    row_count = len(rows)
    failures = []
    col_profiles = {}

    for col in cols:
        vals = [r.get(col) for r in rows]
        non_null = [v for v in vals if not is_null(v)]
        null_count = row_count - len(non_null)
        null_pct = round((null_count / row_count) * 100.0, 2) if row_count else 0.0
        str_vals = [str(v).strip() for v in non_null]
        counts = Counter(str_vals)
        nums = [n for n in (try_float(v) for v in non_null) if n is not None]
        inferred = infer_type(non_null, nums)

        info = {
            "inferred_type": inferred,
            "null_count": null_count,
            "null_pct": null_pct,
            "distinct_count": len(counts),
            "top_values": [{"value": k, "count": c} for k, c in counts.most_common(5)],
        }
        if inferred in {"INTEGER", "FLOAT"} and nums:
            s_nums = sorted(nums)
            info["numeric"] = {
                "min": round(s_nums[0], 4),
                "median": round(statistics.median(s_nums), 4),
                "mean": round(statistics.mean(s_nums), 4),
                "p95": round(percentile(s_nums, 0.95), 4),
                "max": round(s_nums[-1], 4),
                "stddev": round(statistics.stdev(s_nums), 4) if len(s_nums) >= 2 else 0.0,
            }
        col_profiles[col] = info

    pk_report = None
    if pk_cols:
        missing_pk = [c for c in pk_cols if c not in col_profiles]
        if missing_pk:
            failures.append(f"Primary key column(s) missing from dataset: {missing_pk}")
        else:
            seen = Counter()
            null_pk_rows = 0
            for r in rows:
                if any(is_null(r.get(c)) for c in pk_cols):
                    null_pk_rows += 1
                key = tuple(str(r.get(c, "")).strip() for c in pk_cols)
                seen[key] += 1
            dups = [k for k, cnt in seen.items() if cnt > 1]
            dup_extra_rows = sum(cnt - 1 for cnt in seen.values() if cnt > 1)
            pk_report = {
                "columns": pk_cols,
                "unique_keys": len(seen),
                "duplicate_key_count": len(dups),
                "duplicate_extra_rows": dup_extra_rows,
                "null_pk_rows": null_pk_rows,
                "sample_duplicates": [list(k) for k in dups[:5]],
            }
            if dup_extra_rows > 0:
                failures.append(f"Grain violation on {pk_cols}: {dup_extra_rows} duplicate row(s) across {len(dups)} key(s).")
            if null_pk_rows > 0:
                failures.append(f"Null primary key detected in {null_pk_rows} row(s) on {pk_cols}.")

    if contract:
        min_rows = contract.get("min_rows")
        max_rows = contract.get("max_rows")
        if min_rows is not None and row_count < min_rows:
            failures.append(f"Row count {row_count} below contract min_rows ({min_rows}).")
        if max_rows is not None and row_count > max_rows:
            failures.append(f"Row count {row_count} exceeds contract max_rows ({max_rows}).")
        for spec in contract.get("columns", []):
            cname = spec["name"]
            if cname not in col_profiles:
                failures.append(f"Contract column missing: '{cname}'")
                continue
            cp = col_profiles[cname]
            if spec.get("nullable") is False and cp["null_count"] > 0:
                failures.append(f"Column '{cname}' violates nullable=false ({cp['null_count']} nulls).")
            max_null_pct = spec.get("max_null_pct")
            if max_null_pct is not None and cp["null_pct"] > max_null_pct:
                failures.append(f"Column '{cname}' null_pct {cp['null_pct']}% exceeds max_null_pct {max_null_pct}%.")
            if spec.get("unique") is True and cp["distinct_count"] != (row_count - cp["null_count"]):
                failures.append(f"Column '{cname}' violates unique=true ({cp['distinct_count']} distinct vs {row_count - cp['null_count']} non-null).")
            if "allowed_values" in spec:
                allowed = {str(x) for x in spec["allowed_values"]}
                bad = [str(r.get(cname)).strip() for r in rows if not is_null(r.get(cname)) and str(r.get(cname)).strip() not in allowed]
                if bad:
                    failures.append(f"Column '{cname}' has {len(bad)} value(s) outside allowed_values (sample: {bad[:3]}).")
            if "numeric" in cp:
                if spec.get("min_value") is not None and cp["numeric"]["min"] < spec["min_value"]:
                    failures.append(f"Column '{cname}' min {cp['numeric']['min']} < contract min_value {spec['min_value']}.")
                if spec.get("max_value") is not None and cp["numeric"]["max"] > spec["max_value"]:
                    failures.append(f"Column '{cname}' max {cp['numeric']['max']} > contract max_value {spec['max_value']}.")

    return {
        "status": "failed" if failures else "ok",
        "file": path.name,
        "row_count": row_count,
        "column_count": len(cols),
        "primary_key_check": pk_report,
        "failure_count": len(failures),
        "failures": failures,
        "columns": col_profiles,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("dataset", type=Path, help="Path to .csv, .tsv, or .jsonl/.ndjson dataset")
    ap.add_argument("--pk", default="", help="Comma-separated primary key column(s) to verify grain uniqueness")
    ap.add_argument("--contract", type=Path, default=None, help="Optional JSON contract file with row/column rules")
    args = ap.parse_args()

    try:
        pk_cols = [c.strip() for c in args.pk.split(",") if c.strip()]
        contract = json.loads(args.contract.read_text(encoding="utf-8")) if args.contract else None
        report = profile(args.dataset.resolve(), pk_cols, contract)
    except Exception as exc:
        print(json.dumps({"status": "error", "error": str(exc)}), file=sys.stderr)
        return 2

    print(json.dumps(report, indent=2))
    return 1 if report["failure_count"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
