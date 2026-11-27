#!/usr/bin/env python3
"""Audit local developer/agent environment readiness without exposing secrets.

Checks OS/shell suitability (Linux/macOS preferred over Windows/PowerShell),
presence of core agent tooling (git, rtk, docker, tmux, tailscale, engram),
and .env key names only (never values). Outputs JSON to stdout.
"""
import argparse
import json
import os
import platform
import re
import shutil
import sys
from pathlib import Path

TOOLS = ["git", "python3", "python", "rtk", "docker", "tmux", "tailscale", "engram", "gh", "uv", "pnpm", "node"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cwd", type=Path, default=Path.cwd(), help="Workspace directory to check for .env keys.")
    args = ap.parse_args()
    cwd = args.cwd.resolve()

    sys_name = platform.system().lower()
    is_wsl = sys_name == "linux" and "microsoft" in platform.release().lower()
    shell = os.environ.get("SHELL") or os.environ.get("COMSPEC") or "unknown"

    warnings = []
    if sys_name == "windows":
        warnings.append("Running on native Windows: prefer a Linux VM, container, WSL2, or macOS for coding agent loops.")

    tools_found = {t: bool(shutil.which(t)) for t in TOOLS}
    if not tools_found.get("rtk"):
        warnings.append("rtk (Rust Token Killer) not found on PATH; verbose test/build/git logs will consume extra tokens.")

    env_keys = {}
    for name in (".env", ".env.example"):
        p = cwd / name
        if p.is_file():
            env_keys[name] = re.findall(r"^([A-Z][A-Z0-9_]*)\s*=", p.read_text(encoding="utf-8", errors="ignore"), re.M)

    report = {
        "status": "ok",
        "os": sys_name,
        "is_wsl": is_wsl,
        "os_preferred_for_agents": sys_name in ("linux", "darwin"),
        "shell_hint": Path(shell).name if shell else "unknown",
        "tools": tools_found,
        "env_key_names_only": env_keys,
        "warnings": warnings,
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
