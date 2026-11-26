#!/usr/bin/env python3
"""bstack installer for Hermes, Claude Code, Codex, and Antigravity.

Reads bstack.yaml and installs the declared skills either from a built
bstack-*.zip bundle or directly from the local Hermes skills tree.
"""
import argparse
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

from build import ROOT, find_skill, parse_yaml, resolve_skills_dir

AGENT_CHOICES = ("hermes", "claude", "codex", "antigravity")


def agent_target(agent: str) -> tuple[Path, str]:
    """Return (skills_root, layout) for a supported agent."""
    home = Path.home()
    if agent == "hermes":
        return resolve_skills_dir(), "layered"
    if agent == "claude":
        return home / ".claude" / "skills", "flat"
    if agent == "codex":
        codex_dir = home / ".codex"
        base = codex_dir / "skills" if codex_dir.exists() else home / ".agents" / "skills"
        return base, "flat"
    if agent == "antigravity":
        return home / ".gemini" / "config" / "skills", "flat"
    raise ValueError(f"Agente no soportado: {agent}")


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
                raise FileNotFoundError(f"Falta {lid}/{name} dentro de {zip_path}")
            resolved.append((lid, name, src))
    return resolved


def resolve_sources_from_hermes(skills_dir: Path, manifest: dict) -> list[tuple[str, str, Path]]:
    """Resolve all declared skills from the local Hermes skills directory."""
    resolved: list[tuple[str, str, Path]] = []
    missing: list[str] = []
    for layer in manifest["layers"]:
        lid = layer["id"]
        for name in layer["skills"]:
            found = find_skill(name, skills_dir)
            if found is None:
                missing.append(f"{lid}/{name}")
            else:
                resolved.append((lid, name, found))
    if missing:
        raise FileNotFoundError(
            f"Faltan {len(missing)} skills en {skills_dir}: " + ", ".join(missing)
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
    ap = argparse.ArgumentParser(description="Instala los skills de bstack en un agente.")
    ap.add_argument(
        "--agent",
        choices=[*AGENT_CHOICES, "all"],
        help="Agente destino (hermes, claude, codex, antigravity, o all).",
    )
    ap.add_argument("--target", type=Path, help="Directorio destino personalizado.")
    ap.add_argument(
        "--layout",
        choices=["flat", "layered"],
        default=None,
        help="Estructura en destino: flat (<dir>/<skill>) o layered (<dir>/<etapa>/<skill>).",
    )
    ap.add_argument("--zip", type=Path, dest="zip_path", help="Bundle bstack-<version>.zip de origen.")
    ap.add_argument("--skills-dir", help="Directorio local de skills de Hermes.")
    ap.add_argument("--force", action="store_true", help="Sobrescribe skills existentes en destino.")
    ap.add_argument("--dry-run", action="store_true", help="Muestra qué haría sin copiar archivos.")
    args = ap.parse_args()

    if not args.agent and not args.target:
        ap.error("Indicá --agent {hermes,claude,codex,antigravity,all} o --target <ruta>.")

    manifest = parse_yaml(ROOT / "bstack.yaml")
    default_zip = ROOT / "dist" / f"{manifest.get('name', 'bstack')}-{manifest.get('version', '0.1.0')}.zip"
    zip_path = args.zip_path or (default_zip if not args.skills_dir and default_zip.is_file() and not resolve_skills_dir().exists() else None)

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
                print(f"Error: no existe el bundle {zip_path}", file=sys.stderr)
                return 1
            sources = resolve_sources_from_zip(zip_path, Path(tmp), manifest)
        else:
            skills_dir = resolve_skills_dir(args.skills_dir)
            sources = resolve_sources_from_hermes(skills_dir, manifest)

        for label, dest_root, layout in targets:
            counts = {"installed": 0, "updated": 0, "skipped": 0}
            for layer_id, name, src in sources:
                dst = (dest_root / layer_id / name) if layout == "layered" else (dest_root / name)
                status = copy_skill(src, dst, force=args.force, dry_run=args.dry_run)
                counts[status] += 1
            prefix = "[dry-run] " if args.dry_run else ""
            print(
                f"{prefix}{label} ({dest_root}, {layout}): "
                f"{counts['installed']} instalados, {counts['updated']} actualizados, {counts['skipped']} omitidos"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
