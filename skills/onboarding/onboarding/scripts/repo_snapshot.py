#!/usr/bin/env python3
"""Read-only Batch-1 repository snapshot for fast onboarding.

Collects git truth, project contracts, manifests, runnable script names,
.env.example key names (never values), and a depth-2 tree in one JSON call.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

IGNORED_DIRS = {
    ".git", "node_modules", ".venv", "venv", "dist", "build", "__pycache__",
    ".next", ".nuxt", ".turbo", "target", "coverage", ".cache",
}
CONTRACTS = ["AGENTS.md", "CLAUDE.md", "GEMINI.md", "DESIGN.md", "README.md", ".cursor/rules", ".agents"]
MANIFESTS = [
    "package.json", "pnpm-lock.yaml", "yarn.lock", "package-lock.json",
    "pyproject.toml", "uv.lock", "requirements.txt", "Cargo.toml", "go.mod",
    "Makefile", "Dockerfile", "docker-compose.yml", "compose.yaml",
    ".env.example", ".nvmrc", ".python-version", "mise.toml",
]


def git_opt(cwd: Path, args: list[str]) -> str | None:
    proc = subprocess.run(
        ["git", *args], cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    return proc.stdout.strip() if proc.returncode == 0 else None


def depth2_tree(cwd: Path) -> list[str]:
    entries = []
    for p in sorted(cwd.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
        if p.name in IGNORED_DIRS:
            continue
        if p.is_dir():
            entries.append(p.name + "/")
            for sub in sorted(p.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))[:20]:
                if sub.name in IGNORED_DIRS:
                    continue
                entries.append(f"  {p.name}/{sub.name}{'/' if sub.is_dir() else ''}")
        else:
            entries.append(p.name)
    return entries[:120]


def discover_commands(cwd: Path) -> dict:
    cmds = {}
    pkg = cwd / "package.json"
    if pkg.is_file():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
            if isinstance(data.get("scripts"), dict):
                cmds["npm_scripts"] = list(data["scripts"].keys())
        except Exception:
            pass
    mk = cwd / "Makefile"
    if mk.is_file():
        targets = re.findall(r"^([A-Za-z0-9_.-]+)\s*:", mk.read_text(encoding="utf-8", errors="ignore"), re.M)
        cmds["make_targets"] = [t for t in targets if not t.startswith(".")][:30]
    return cmds


def env_key_names(cwd: Path) -> dict:
    out = {}
    for fn in (".env.example", ".env.sample", ".env"):
        p = cwd / fn
        if p.is_file():
            keys = re.findall(r"^([A-Z][A-Z0-9_]*)\s*=", p.read_text(encoding="utf-8", errors="ignore"), re.M)
            out[fn] = keys
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cwd", type=Path, default=Path.cwd(), help="Target repository directory.")
    args = ap.parse_args()
    cwd = args.cwd.resolve()
    if not cwd.is_dir():
        print(json.dumps({"status": "error", "error": f"Not a directory: {cwd}"}), file=sys.stderr)
        return 2

    ci_files = []
    for pattern in (".github/workflows/*.yml", ".github/workflows/*.yaml", ".gitlab-ci.yml"):
        ci_files.extend(str(p.relative_to(cwd)).replace("\\", "/") for p in sorted(cwd.glob(pattern)))

    status_raw = git_opt(cwd, ["status", "-sb"])
    log_raw = git_opt(cwd, ["log", "--oneline", "-12"])
    wt_raw = git_opt(cwd, ["worktree", "list"])

    snapshot = {
        "status": "ok",
        "repo_name": cwd.name,
        "git": {
            "is_repo": status_raw is not None,
            "status_lines": status_raw.splitlines()[:30] if status_raw else [],
            "recent_commits": log_raw.splitlines() if log_raw else [],
            "worktree_count": len(wt_raw.splitlines()) if wt_raw else 0,
        },
        "contracts_found": [c for c in CONTRACTS if (cwd / c).exists()],
        "manifests_found": [m for m in MANIFESTS if (cwd / m).exists()],
        "ci_files": ci_files,
        "discovered_commands_not_run": discover_commands(cwd),
        "env_key_names_only": env_key_names(cwd),
        "tree_depth_2": depth2_tree(cwd),
    }
    print(json.dumps(snapshot, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
