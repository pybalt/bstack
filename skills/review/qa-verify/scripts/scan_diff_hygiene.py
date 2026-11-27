#!/usr/bin/env python3
"""Scan added diff lines and untracked files for secrets, debug tags, private paths, and leftover spikes.

Fail-closed hygiene gate for qa-verify. Outputs JSON to stdout.
Exit 0 = clean, exit 1 = findings detected, exit 2 = error.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

RULES = [
    ("secret_token", re.compile(r"\b(ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{16,}|AIza[0-9A-Za-z_-]{20,}|AKIA[0-9A-Z]{16}|xox[baprs]-[0-9A-Za-z-]{10,})\b")),
    ("private_key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----")),
    ("debug_tag", re.compile(r"\[DEBUG-[A-Za-z0-9_-]+\]")),
    ("hardcoded_home_path", re.compile(r"(?:[A-Za-z]:\\Users\\|/Users/|/home/)[A-Za-z0-9._-]+")),
]


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


def scan_diff(cwd: Path, base: str) -> dict:
    findings = []
    status = run_git(cwd, ["status", "--porcelain"])

    # Flag leftover throwaway spike files or committed .env files
    for line in status.splitlines():
        if not line.strip():
            continue
        rel = line[3:].strip().strip('"')
        norm = rel.replace("\\", "/")
        if norm.startswith("spikes/") or "/spikes/" in norm:
            findings.append({"rule": "leftover_spike", "file": norm, "detail": "Throwaway spike file present in workspace"})
        name = Path(norm).name
        if name == ".env" or (name.startswith(".env.") and name not in {".env.example", ".env.sample", ".env.template"}):
            findings.append({"rule": "env_file_tracked", "file": norm, "detail": "Live .env file present in git status"})

    diff = run_git(cwd, ["diff", "-U0", base])
    cur_file = ""
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            cur_file = line[6:]
            continue
        if not line.startswith("+") or line.startswith("+++"):
            continue
        content = line[1:]
        for rule_name, rx in RULES:
            if rx.search(content):
                findings.append({
                    "rule": rule_name,
                    "file": cur_file,
                    "snippet": content.strip()[:120],
                })

    return {
        "status": "clean" if not findings else "findings",
        "base": base,
        "finding_count": len(findings),
        "findings": findings,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cwd", type=Path, default=Path.cwd(), help="Repository path.")
    ap.add_argument("--base", default="HEAD", help="Git ref to diff against (default: HEAD).")
    args = ap.parse_args()

    try:
        report = scan_diff(args.cwd.resolve(), args.base)
    except Exception as exc:
        print(json.dumps({"status": "error", "error": str(exc)}), file=sys.stderr)
        return 2

    print(json.dumps(report, indent=2))
    return 0 if report["finding_count"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
