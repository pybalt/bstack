#!/usr/bin/env python3
"""Compute or verify a deterministic git workspace fingerprint for RDD receipts.

Outputs JSON to stdout. Exit 0 on success (or matching --compare), exit 1 on
fingerprint drift, exit 2 on git/runtime errors.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


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


def compute_fingerprint(cwd: Path) -> dict:
    head = run_git(cwd, ["rev-parse", "--short", "HEAD"]).strip()
    branch = run_git(cwd, ["rev-parse", "--abbrev-ref", "HEAD"]).strip()
    status = run_git(cwd, ["status", "--porcelain"])
    diff = run_git(cwd, ["diff", "HEAD"])

    h = hashlib.sha256()
    h.update(head.encode("utf-8"))
    h.update(b"\n---STATUS---\n")
    h.update(status.encode("utf-8"))
    h.update(b"\n---DIFF---\n")
    h.update(diff.encode("utf-8"))

    # Include untracked non-ignored file contents so new untracked files cannot drift silently
    for line in status.splitlines():
        if line.startswith("?? "):
            rel = line[3:].strip().strip('"')
            p = cwd / rel
            if p.is_file():
                h.update(f"\n---UNTRACKED:{rel}---\n".encode("utf-8"))
                h.update(p.read_bytes())

    digest = h.hexdigest()[:12]
    dirty = bool(status.strip())
    return {
        "head": head,
        "branch": branch,
        "dirty": dirty,
        "changed_entries": len([l for l in status.splitlines() if l.strip()]),
        "fingerprint": f"{head}:{digest}",
        "diff_hash": digest,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cwd", type=Path, default=Path.cwd(), help="Repository path.")
    ap.add_argument("--compare", help="Previously recorded fingerprint (<head>:<hash> or <hash>) to check for drift.")
    args = ap.parse_args()

    try:
        info = compute_fingerprint(args.cwd.resolve())
    except Exception as exc:
        print(json.dumps({"status": "error", "error": str(exc)}), file=sys.stderr)
        return 2

    if args.compare:
        matched = args.compare in (info["fingerprint"], info["diff_hash"])
        info["compare_expected"] = args.compare
        info["unchanged"] = matched
        info["status"] = "valid" if matched else "invalidated_drift"
        print(json.dumps(info, indent=2))
        return 0 if matched else 1

    info["status"] = "ok"
    print(json.dumps(info, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
