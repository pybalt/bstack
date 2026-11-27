#!/usr/bin/env python3
"""Deterministic schema diff & breaking-change classifier for data-modeling.

Compares two schema specifications (JSON files, or CSV files using header row) and
classifies every delta as SAFE_ADDITIVE, WARNING, or BREAKING_CHANGE.

Expected JSON format:
{
  "table": "gold.fct_orders",
  "grain": "one row per order_id",
  "primary_key": ["order_id"],
  "columns": [
    {"name": "order_id", "type": "INT64", "nullable": false},
    {"name": "amount_cents", "type": "INT64", "nullable": false}
  ]
}

Outputs JSON to stdout.
Exit codes: 0 = safe/warnings only, 1 = breaking changes detected, 2 = error.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

WIDENING_CHAINS = [
    ["INT16", "INT32", "INT64", "NUMERIC", "BIGNUMERIC"],
    ["SMALLINT", "INTEGER", "INT", "BIGINT", "DECIMAL", "NUMERIC"],
    ["FLOAT32", "FLOAT", "FLOAT64", "DOUBLE"],
    ["DATE", "DATETIME", "TIMESTAMP"],
]


def normalize_type(raw: str) -> tuple[str, int | None]:
    s = raw.strip().upper()
    m = re.match(r"^(VARCHAR|CHAR|NVARCHAR|STRING|DECIMAL|NUMERIC)\s*\(\s*(\d+)", s)
    if m:
        base = "STRING" if m.group(1) in {"VARCHAR", "NVARCHAR", "STRING"} else m.group(1)
        return base, int(m.group(2))
    aliases = {
        "INT8": "INT64", "BIGINT": "INT64", "INT4": "INT32", "INTEGER": "INT32", "INT": "INT32",
        "FLOAT8": "FLOAT64", "DOUBLE PRECISION": "FLOAT64", "DOUBLE": "FLOAT64",
        "BOOL": "BOOLEAN", "TEXT": "STRING", "VARCHAR": "STRING", "STRING": "STRING",
        "TIMESTAMPTZ": "TIMESTAMP", "TIMESTAMP WITH TIME ZONE": "TIMESTAMP",
    }
    return aliases.get(s, s), None


def classify_type_change(old_raw: str, new_raw: str) -> tuple[str, str]:
    old_base, old_len = normalize_type(old_raw)
    new_base, new_len = normalize_type(new_raw)
    if old_base == new_base:
        if old_len is not None and new_len is not None:
            if new_len > old_len:
                return "WARNING", f"Length widened ({old_raw} -> {new_raw})"
            if new_len < old_len:
                return "BREAKING_CHANGE", f"Length narrowed ({old_raw} -> {new_raw})"
        if old_len is not None and new_len is None and old_base == "STRING":
            return "WARNING", f"Bounded string widened to unbounded ({old_raw} -> {new_raw})"
        if old_len is None and new_len is not None and old_base == "STRING":
            return "BREAKING_CHANGE", f"Unbounded string narrowed ({old_raw} -> {new_raw})"
        return "UNCHANGED", ""

    for chain in WIDENING_CHAINS:
        if old_base in chain and new_base in chain:
            if chain.index(new_base) > chain.index(old_base):
                return "WARNING", f"Type widened ({old_raw} -> {new_raw})"
            return "BREAKING_CHANGE", f"Type narrowed ({old_raw} -> {new_raw})"

    return "BREAKING_CHANGE", f"Incompatible type change ({old_raw} -> {new_raw})"


def load_schema(path: Path) -> dict:
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8", newline="") as f:
            header = next(csv.reader(f), [])
        return {
            "table": path.stem,
            "grain": None,
            "primary_key": [],
            "columns": [{"name": c.strip(), "type": "STRING", "nullable": True} for c in header if c.strip()],
        }
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "columns" not in data:
        raise ValueError(f"{path.name} must be a JSON object with a 'columns' array.")
    return data


def diff_schemas(old: dict, new: dict) -> dict:
    changes = []

    old_pk = old.get("primary_key") or []
    new_pk = new.get("primary_key") or []
    if old_pk != new_pk:
        changes.append({
            "severity": "BREAKING_CHANGE",
            "kind": "PRIMARY_KEY_CHANGED",
            "column": None,
            "detail": f"Primary key changed from {old_pk} to {new_pk}",
        })

    old_grain = (old.get("grain") or "").strip().lower()
    new_grain = (new.get("grain") or "").strip().lower()
    if old_grain and new_grain and old_grain != new_grain:
        changes.append({
            "severity": "BREAKING_CHANGE",
            "kind": "GRAIN_CHANGED",
            "column": None,
            "detail": f"Declared grain changed from '{old.get('grain')}' to '{new.get('grain')}'",
        })

    old_cols = {c["name"]: c for c in old.get("columns", [])}
    new_cols = {c["name"]: c for c in new.get("columns", [])}

    for name, oc in old_cols.items():
        if name not in new_cols:
            changes.append({
                "severity": "BREAKING_CHANGE",
                "kind": "COLUMN_REMOVED",
                "column": name,
                "detail": f"Column '{name}' ({oc.get('type', 'UNKNOWN')}) was removed or renamed.",
            })
            continue
        nc = new_cols[name]
        sev, msg = classify_type_change(str(oc.get("type", "")), str(nc.get("type", "")))
        if sev != "UNCHANGED":
            changes.append({"severity": sev, "kind": "TYPE_CHANGED", "column": name, "detail": msg})

        old_null = bool(oc.get("nullable", True))
        new_null = bool(nc.get("nullable", True))
        if old_null and not new_null:
            changes.append({
                "severity": "BREAKING_CHANGE",
                "kind": "NULLABILITY_TIGHTENED",
                "column": name,
                "detail": f"Column '{name}' changed from nullable to NOT NULL (requires backfill proof).",
            })
        elif not old_null and new_null:
            changes.append({
                "severity": "SAFE_ADDITIVE",
                "kind": "NULLABILITY_RELAXED",
                "column": name,
                "detail": f"Column '{name}' changed from NOT NULL to nullable.",
            })

    for name, nc in new_cols.items():
        if name not in old_cols:
            is_null = bool(nc.get("nullable", True))
            has_default = nc.get("default") is not None
            sev = "SAFE_ADDITIVE" if (is_null or has_default) else "BREAKING_CHANGE"
            detail = (
                f"Added nullable/defaulted column '{name}' ({nc.get('type', 'UNKNOWN')})."
                if sev == "SAFE_ADDITIVE"
                else f"Added required NOT NULL column '{name}' without default."
            )
            changes.append({"severity": sev, "kind": "COLUMN_ADDED", "column": name, "detail": detail})

    breaking = [c for c in changes if c["severity"] == "BREAKING_CHANGE"]
    warnings = [c for c in changes if c["severity"] == "WARNING"]
    safe = [c for c in changes if c["severity"] == "SAFE_ADDITIVE"]

    return {
        "status": "breaking" if breaking else ("warning" if warnings else "safe"),
        "table": new.get("table") or old.get("table") or "unknown",
        "counts": {
            "breaking": len(breaking),
            "warning": len(warnings),
            "safe_additive": len(safe),
        },
        "changes": changes,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("old_schema", type=Path, help="Baseline schema (.json or .csv)")
    ap.add_argument("new_schema", type=Path, help="Proposed schema (.json or .csv)")
    args = ap.parse_args()

    try:
        report = diff_schemas(load_schema(args.old_schema), load_schema(args.new_schema))
    except Exception as exc:
        print(json.dumps({"status": "error", "error": str(exc)}), file=sys.stderr)
        return 2

    print(json.dumps(report, indent=2))
    return 1 if report["counts"]["breaking"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
