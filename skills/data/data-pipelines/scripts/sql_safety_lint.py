#!/usr/bin/env python3
"""Deterministic static SQL safety & performance linter for data-pipelines.

Scans one or more .sql / .sqlx files (or directories recursively) and outputs JSON:
- BLOCKING: Destructive ops (DROP TABLE/SCHEMA/DATABASE, TRUNCATE, DELETE/UPDATE
  without WHERE or with tautological WHERE 1=1).
- WARNING: Columnar/correctness smells (SELECT *, CROSS JOIN, NOT IN (SELECT ...),
  plain UNION instead of UNION ALL, non-sargable function on date/time predicate,
  ORDER BY inside CTE without LIMIT).

Exit codes: 0 = no blocking hazards, 1 = blocking hazards found, 2 = error.
"""
import argparse
import json
import re
import sys
from pathlib import Path

SQL_EXTS = {".sql", ".sqlx"}


def strip_comments_and_strings(sql: str) -> str:
    """Replace SQL comments and string literals with spaces while preserving line count."""
    out = []
    i, n = 0, len(sql)
    while i < n:
        ch = sql[i]
        nxt = sql[i + 1] if i + 1 < n else ""
        # Line comment --
        if ch == "-" and nxt == "-":
            while i < n and sql[i] != "\n":
                out.append(" ")
                i += 1
        # Block comment /* ... */
        elif ch == "/" and nxt == "*":
            out.append("  ")
            i += 2
            while i < n and not (sql[i] == "*" and i + 1 < n and sql[i + 1] == "/"):
                out.append("\n" if sql[i] == "\n" else " ")
                i += 1
            if i < n:
                out.append("  ")
                i += 2
        # Single-quoted string
        elif ch == "'":
            out.append("'")
            i += 1
            while i < n:
                if sql[i] == "'" and i + 1 < n and sql[i + 1] == "'":
                    out.append("  ")
                    i += 2
                elif sql[i] == "'":
                    out.append("'")
                    i += 1
                    break
                else:
                    out.append("\n" if sql[i] == "\n" else " ")
                    i += 1
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def line_at(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def split_statements(clean_sql: str) -> list[tuple[int, str]]:
    stmts = []
    start = 0
    for m in re.finditer(r";", clean_sql):
        chunk = clean_sql[start : m.start()]
        if chunk.strip():
            stmts.append((start, chunk))
        start = m.end()
    tail = clean_sql[start:]
    if tail.strip():
        stmts.append((start, tail))
    return stmts


def lint_file(path: Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    clean = strip_comments_and_strings(raw)
    findings = []

    def add(sev: str, rule: str, pos: int, message: str) -> None:
        findings.append({
            "file": path.name,
            "line": line_at(clean, pos),
            "severity": sev,
            "rule": rule,
            "message": message,
        })

    # Statement-level destructive checks
    for offset, stmt in split_statements(clean):
        for m in re.finditer(r"\bDROP\s+(?:TABLE|SCHEMA|DATABASE|DATASET|VIEW)\b", stmt, re.I):
            add("BLOCKING", "SQL001_DROP", offset + m.start(), "Irreversible DROP statement requires explicit user consent and backup check.")
        for m in re.finditer(r"\bTRUNCATE\s+(?:TABLE\s+)?[A-Za-z0-9_.\"`-]+", stmt, re.I):
            add("BLOCKING", "SQL002_TRUNCATE", offset + m.start(), "TRUNCATE wipes all table rows; prefer scoped partition overwrite or get explicit consent.")
        for m in re.finditer(r"\bDELETE\s+FROM\b", stmt, re.I):
            after = stmt[m.end() :]
            if not re.search(r"\bWHERE\b", after, re.I):
                add("BLOCKING", "SQL003_UNFILTERED_DELETE", offset + m.start(), "DELETE without WHERE clause deletes entire table.")
            elif re.search(r"\bWHERE\s+1\s*=\s*1\b|\bWHERE\s+TRUE\b", after, re.I):
                add("BLOCKING", "SQL003_BROAD_DELETE", offset + m.start(), "DELETE with tautological WHERE (1=1 / TRUE) deletes entire table.")
        for m in re.finditer(r"^\s*UPDATE\s+[A-Za-z0-9_.\"`-]+\s+SET\b", stmt, re.I | re.M):
            after = stmt[m.end() :]
            if not re.search(r"\bWHERE\b", after, re.I):
                add("BLOCKING", "SQL004_UNFILTERED_UPDATE", offset + m.start(), "UPDATE without WHERE clause mutates every row in the table.")
            elif re.search(r"\bWHERE\s+1\s*=\s*1\b|\bWHERE\s+TRUE\b", after, re.I):
                add("BLOCKING", "SQL004_BROAD_UPDATE", offset + m.start(), "UPDATE with tautological WHERE (1=1 / TRUE) mutates every row.")

    # File-level performance & correctness smells
    for m in re.finditer(r"\bSELECT\s+(?:DISTINCT\s+)?(?:[A-Za-z0-9_]+\.)?\*(?!\s*(?:EXCEPT|REPLACE))", clean, re.I):
        # Ignore COUNT(*) which does not match SELECT * directly, verify not inside COUNT(
        prefix = clean[max(0, m.start() - 10) : m.start()]
        if not re.search(r"\bCOUNT\s*\($", prefix, re.I):
            add("WARNING", "SQL101_SELECT_STAR", m.start(), "SELECT * scans all columns on columnar warehouses and weakens schema contracts.")

    for m in re.finditer(r"\bCROSS\s+JOIN\b", clean, re.I):
        add("WARNING", "SQL102_CROSS_JOIN", m.start(), "CROSS JOIN can trigger Cartesian row explosion; confirm small spine bounds.")

    for m in re.finditer(r"\bNOT\s+IN\s*\(\s*SELECT\b", clean, re.I):
        add("WARNING", "SQL103_NOT_IN_SUBQUERY", m.start(), "NOT IN (SELECT ...) silently returns 0 rows if subquery yields NULL; use NOT EXISTS.")

    for m in re.finditer(r"\bUNION\b(?!\s+ALL\b)", clean, re.I):
        add("WARNING", "SQL104_UNION_DISTINCT", m.start(), "UNION forces global deduplication shuffle; use UNION ALL unless dedup is intentional.")

    for m in re.finditer(r"\bWHERE\b[^;]{0,160}\b(?:DATE|YEAR|MONTH|TRUNC|DATE_TRUNC|CAST)\s*\([^)]*(?:date|time|_at|_ts|_dt)[^)]*\)\s*(?:=|>|<|>=|<=|BETWEEN)", clean, re.I):
        add("WARNING", "SQL105_NONSARGABLE_DATE", m.start(), "Function wrapped around date/timestamp column in WHERE may defeat partition pruning; use raw half-open range bounds.")

    for m in re.finditer(r"\bAS\s*\(([^()]*\bORDER\s+BY\b[^()]*)\)", clean, re.I):
        if not re.search(r"\bLIMIT\b|\bTOP\b|\bFETCH\s+FIRST\b|\bOVER\s*\(", m.group(1), re.I):
            add("WARNING", "SQL106_CTE_ORDER_BY", m.start(), "ORDER BY inside CTE without LIMIT wastes sort compute and is discarded by outer queries.")

    return findings


def collect_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    return sorted(p for p in target.rglob("*") if p.is_file() and p.suffix.lower() in SQL_EXTS)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("target", type=Path, help="SQL/SQLX file or directory to scan.")
    args = ap.parse_args()

    try:
        files = collect_files(args.target.resolve())
        if not files:
            raise FileNotFoundError(f"No .sql/.sqlx files found under {args.target}")
        all_findings = []
        for f in files:
            all_findings.extend(lint_file(f))
    except Exception as exc:
        print(json.dumps({"status": "error", "error": str(exc)}), file=sys.stderr)
        return 2

    blocking = [f for f in all_findings if f["severity"] == "BLOCKING"]
    warnings = [f for f in all_findings if f["severity"] == "WARNING"]
    report = {
        "status": "blocked" if blocking else ("warnings" if warnings else "clean"),
        "files_scanned": len(files),
        "blocking_count": len(blocking),
        "warning_count": len(warnings),
        "findings": all_findings,
    }
    print(json.dumps(report, indent=2))
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
