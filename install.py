#!/usr/bin/env python3
"""bstack installer for Antigravity, Claude Code, Codex, and Hermes.

Reads bstack.yaml and installs the declared skills either from a built
bstack-*.zip bundle or directly from local agent skill directories.
"""
import argparse
import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

from build import ROOT, find_skill, parse_yaml, resolve_skills_dirs

AGENT_CHOICES = ("antigravity", "claude", "codex", "cursor", "hermes")


def agent_target(agent: str) -> tuple[Path, str]:
    """Return (skills_root, layout) for a supported agent."""
    home = Path.home()
    if agent == "antigravity":
        return home / ".gemini" / "config" / "skills", "flat"
    if agent == "claude":
        return home / ".claude" / "skills", "flat"
    if agent == "codex":
        codex_dir = home / ".codex"
        base = codex_dir / "skills" if codex_dir.exists() else home / ".agents" / "skills"
        return base, "flat"
    if agent == "cursor":
        return home / ".cursor" / "skills", "flat"
    if agent == "hermes":
        if hermes_home := os.environ.get("HERMES_HOME"):
            return Path(hermes_home).expanduser() / "skills", "layered"
        win_dir = home / "AppData" / "Local" / "hermes" / "skills"
        return (win_dir if win_dir.exists() else home / ".hermes" / "skills"), "layered"
    raise ValueError(f"Unsupported agent: {agent}")


def resolve_sources_from_zip(zip_path: Path, stage: Path, manifest: dict) -> list[tuple[str, str, Path]]:
    """Extract a bstack zip bundle into stage and return (layer, skill, dir) tuples."""
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(stage)
    resolved: list[tuple[str, str, Path]] = []
    for layer in manifest["layers"]:
        lid = layer["id"]
        for name in layer["skills"]:
            src = stage / "skills" / lid / name
            if not (src / "SKILL.md").is_file():
                raise FileNotFoundError(f"Missing {lid}/{name} inside {zip_path}")
            resolved.append((lid, name, src))
    return resolved


def resolve_sources_local(skills_dirs: list[Path], manifest: dict) -> list[tuple[str, str, Path]]:
    """Resolve all declared skills from local skill directories."""
    resolved: list[tuple[str, str, Path]] = []
    missing: list[str] = []
    for layer in manifest["layers"]:
        lid = layer["id"]
        for name in layer["skills"]:
            found = find_skill(name, skills_dirs)
            if found is None:
                missing.append(f"{lid}/{name}")
            else:
                resolved.append((lid, name, found))
    if missing:
        searched = ", ".join(str(d) for d in skills_dirs)
        raise FileNotFoundError(
            f"Missing {len(missing)} skills in [{searched}]: " + ", ".join(missing)
        )
    return resolved


def copy_skill(src: Path, dst: Path, force: bool, dry_run: bool) -> str:
    """Copy a single skill directory to dst and return status ('installed'|'updated'|'skipped')."""
    if dst.resolve() == src.resolve():
        return "skipped"
    existed = dst.exists()
    if existed and not force:
        return "skipped"
    if dry_run:
        return "updated" if existed else "installed"
    if existed:
        shutil.rmtree(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return "updated" if existed else "installed"


def main() -> int:
    ap = argparse.ArgumentParser(description="Install bstack skills into a target coding agent.")
    ap.add_argument(
        "--agent",
        choices=[*AGENT_CHOICES, "all"],
        help="Target agent (antigravity, claude, codex, cursor, hermes, or all).",
    )
    ap.add_argument("--target", type=Path, help="Custom destination directory.")
    ap.add_argument(
        "--layout",
        choices=["flat", "layered"],
        default=None,
        help="Destination layout: flat (<dir>/<skill>) or layered (<dir>/<stage>/<skill>).",
    )
    ap.add_argument("--zip", type=Path, dest="zip_path", help="Source bstack-<version>.zip bundle.")
    ap.add_argument("--skills-dir", help="Local source directory to search for skills.")
    ap.add_argument("--force", action="store_true", help="Overwrite existing skills at destination.")
    ap.add_argument("--dry-run", action="store_true", help="Preview actions without copying files.")
    args = ap.parse_args()

    if not args.agent and not args.target:
        ap.error("Specify --agent {antigravity,claude,codex,cursor,hermes,all} or --target <path>.")

    manifest = parse_yaml(ROOT / "bstack.yaml")
    default_zip = ROOT / "dist" / f"{manifest.get('name', 'bstack')}-{manifest.get('version', '0.1.0')}.zip"
    skills_dirs = resolve_skills_dirs(args.skills_dir)
    zip_path = args.zip_path or (
        default_zip if not args.skills_dir and default_zip.is_file() and not any(d.exists() for d in skills_dirs) else None
    )

    targets: list[tuple[str, Path, str]] = []
    if args.target:
        targets.append(("custom", args.target.expanduser(), args.layout or "flat"))
    else:
        chosen = list(AGENT_CHOICES) if args.agent == "all" else [args.agent]
        for agent in chosen:
            path, default_layout = agent_target(agent)
            targets.append((agent, path, args.layout or default_layout))

    with tempfile.TemporaryDirectory() as tmp:
        if zip_path is not None:
            if not zip_path.is_file():
                print(f"Error: bundle not found: {zip_path}", file=sys.stderr)
                return 1
            sources = resolve_sources_from_zip(zip_path, Path(tmp), manifest)
        else:
            sources = resolve_sources_local(skills_dirs, manifest)

        for label, dest_root, layout in targets:
            counts = {"installed": 0, "updated": 0, "skipped": 0}
            for layer_id, name, src in sources:
                dst = (dest_root / layer_id / name) if layout == "layered" else (dest_root / name)
                status = copy_skill(src, dst, force=args.force, dry_run=args.dry_run)
                counts[status] += 1
            prefix = "[dry-run] " if args.dry_run else ""
            print(
                f"{prefix}{label} ({dest_root}, {layout}): "
                f"{counts['installed']} installed, {counts['updated']} updated, {counts['skipped']} skipped"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
