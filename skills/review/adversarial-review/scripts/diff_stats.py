#!/usr/bin/env python3
"""Summarize git diff size, ODD slice limit (~400 LOC), and Risk Override triggers for adversarial-review.

Outputs JSON to stdout. Exit 0 on success, exit 2 on git error.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

RISK_PATTERNS = {
    "auth_or_permissions": re.compile(r"\b(auth|authn|authz|jwt|oauth|rbac|acl|permission|role|session|cookie|csrf|cors)\b", re.I),
    "money_or_billing": re.compile(r"\b(billing|invoice|payment|stripe|charge|refund|ledger|balance|price|currency|tax)\b", re.I),
    "schema_or_migration": re.compile(r"\b(migration|alembic|prisma|schema\.sql|alter\s+table|drop\s+table|create\s+index|ddl)\b", re.I),
    "concurrency_or_state": re.compile(r"\b(mutex|lock|semaphore|atomic|transaction|idempoten|retry|queue|deadlock|race)\b", re.I),
    "secrets_or_crypto": re.compile(r"\b(secret|credential|vault|kms|encrypt|decrypt|hmac|signature|token|apikey)\b", re.I),
}


def run_git(cwd: Path, args: list[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout


def analyze(cwd: Path, base: str, max_loc: int) -> dict:
    head = run_git(cwd, ["rev-parse", "--short", "HEAD"]).strip()
    numstat = run_git(cwd, ["diff", "--numstat", base])
    diff_text = run_git(cwd, ["diff", base])
    digest = hashlib.sha256(diff_text.encode("utf-8")).hexdigest()[:12]

    files = []
    added_total = 0
    deleted_total = 0
    for line in numstat.splitlines():
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        add_s, del_s, path = parts
        add_n = int(add_s) if add_s.isdigit() else 0
        del_n = int(del_s) if del_s.isdigit() else 0
        added_total += add_n
        deleted_total += del_n
        files.append({"path": path, "added": add_n, "deleted": del_n})

    risk_triggers = {}
    for label, rx in RISK_PATTERNS.items():
        hits = []
        for f in files:
            if rx.search(f["path"]):
                hits.append(f"path:{f['path']}")
        if not hits and rx.search(diff_text):
            hits.append("diff_content")
        if hits:
            risk_triggers[label] = hits[:5]

    total_changed_loc = added_total + deleted_total
    return {
        "status": "ok",
        "head": head,
        "base": base,
        "fingerprint": f"{head}:{digest}",
        "files_changed": len(files),
        "lines_added": added_total,
        "lines_deleted": deleted_total,
        "total_changed_loc": total_changed_loc,
        "exceeds_odd_slice_cap": total_changed_loc > max_loc,
        "odd_slice_cap": max_loc,
        "risk_overrides": risk_triggers,
        "recommended_odd_path": "tracked_high_rigor" if (risk_triggers or total_changed_loc > max_loc or len(files) > 5) else "inline_or_standard",
        "files": files,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cwd", type=Path, default=Path.cwd(), help="Repository path.")
    ap.add_argument("--base", default="HEAD", help="Git ref to diff against (default: HEAD).")
    ap.add_argument("--max-loc", type=int, default=400, help="ODD reviewable slice cap (default: 400).")
    args = ap.parse_args()

    try:
        report = analyze(args.cwd.resolve(), args.base, args.max_loc)
    except Exception as exc:
        print(json.dumps({"status": "error", "error": str(exc)}), file=sys.stderr)
        return 2

    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
