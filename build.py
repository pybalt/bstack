#!/usr/bin/env python3
"""bstack builder.

Lee bstack.yaml, resuelve cada skill en los directorios locales de skills de
agentes, arma un bundle con MANIFEST.json (sha256 por archivo) y lo comprime en
dist/.

  python build.py           # construye dist/bstack-<version>.zip
  python build.py --check   # valida que todos los skills existan
"""
import argparse
import hashlib
import json
import os
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def resolve_skills_dirs(explicit: str | None = None) -> list[Path]:
    """Resolve candidate local skill directories across supported agents."""
    if explicit:
        return [Path(explicit).expanduser()]
    if env_dir := os.environ.get("BSTACK_SKILLS_DIR"):
        return [Path(env_dir).expanduser()]

    home = Path.home()
    candidates: list[Path] = [
        home / ".agents" / "skills",
        home / ".gemini" / "config" / "skills",
        home / ".claude" / "skills",
        home / ".codex" / "skills",
    ]
    if hermes_home := os.environ.get("HERMES_HOME"):
        candidates.append(Path(hermes_home).expanduser() / "skills")
    candidates.extend([
        home / "AppData" / "Local" / "hermes" / "skills",
        home / ".hermes" / "skills",
    ])

    seen: set[Path] = set()
    existing: list[Path] = []
    for c in candidates:
        resolved = c.resolve() if c.exists() else c
        if c.exists() and resolved not in seen:
            seen.add(resolved)
            existing.append(c)
    return existing or [candidates[0]]


def parse_yaml(path: Path) -> dict:
    data = {"layers": []}
    layer = None
    in_desc = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if in_desc:
            if line.startswith("  "):
                data["description"] = data.get("description", "") + " " + line.strip()
                continue
            in_desc = False
        if line.startswith("description:"):
            data["description"] = line.split(":", 1)[1].strip().lstrip(">").strip()
            in_desc = True
            continue
        if line.startswith("layers:"):
            continue
        if line.startswith("  - id:"):
            layer = {"id": line.split(":", 1)[1].strip(), "skills": []}
            data["layers"].append(layer)
            continue
        if line.startswith("    title:"):
            layer["title"] = line.split(":", 1)[1].strip()
            continue
        if line.startswith("    blurb:"):
            layer["blurb"] = line.split(":", 1)[1].strip().strip('"').strip("'")
            continue
        if line.startswith("      - "):
            layer["skills"].append(line[8:].strip())
            continue
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip()
    return data


def find_skill(name: str, skills_dirs: list[Path] | Path) -> Path | None:
    dirs = [skills_dirs] if isinstance(skills_dirs, Path) else skills_dirs
    for base in dirs:
        if not base.exists():
            continue
        direct = base / name / "SKILL.md"
        if direct.is_file():
            return direct.parent
        for match in base.rglob(f"{name}/SKILL.md"):
            rel_parts = match.relative_to(base).parts
            if any(part.startswith(".") for part in rel_parts):
                continue
            return match.parent
    return None


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--skills-dir", help="Directorio local donde buscar los skills.")
    args = ap.parse_args()

    skills_dirs = resolve_skills_dirs(args.skills_dir)
    manifest = parse_yaml(ROOT / "bstack.yaml")
    missing, resolved = [], []
    for layer in manifest["layers"]:
        for name in layer["skills"]:
            d = find_skill(name, skills_dirs)
            if d is None:
                missing.append(f"{layer['id']}/{name}")
            else:
                resolved.append((layer["id"], name, d))

    declared = sum(len(l["skills"]) for l in manifest["layers"])
    print(f"capas: {len(manifest['layers'])} | skills declarados: {declared}")
    print(f"resueltos: {len(resolved)} | faltantes: {len(missing)}")
    for m in missing:
        print("  FALTA:", m)
    if args.check or missing:
        return 1 if missing else 0

    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    stage = dist / "stage"
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir()

    entries = []
    for layer_id, name, src in resolved:
        dst = stage / "skills" / layer_id / name
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        files = {}
        for f in sorted(dst.rglob("*")):
            if f.is_file():
                files[str(f.relative_to(dst)).replace("\\", "/")] = sha256(f)
        entries.append({"layer": layer_id, "skill": name, "files": files})

    out = {
        "name": manifest.get("name"),
        "version": manifest.get("version"),
        "author": manifest.get("author"),
        "description": " ".join(manifest.get("description", "").split()),
        "license": manifest.get("license"),
        "layers": manifest["layers"],
        "skills": entries,
        "totals": {"skills": len(entries), "files": sum(len(e["files"]) for e in entries)},
    }
    (stage / "MANIFEST.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    (stage / "README.md").write_text(
        f"# bstack v{manifest.get('version')}\n\n"
        f"{' '.join(manifest.get('description', '').split())}\n\n"
        "## Instalar\n\n"
        "Copiar cada `skills/<etapa>/<skill>` (o `<skill>` en estructura plana) al directorio de skills de tu agente.\n\n"
        "## Etapas\n\n"
        + "\n".join(f"- **{l['title']}** (`{l['id']}`): {l.get('blurb','')} — {len(l['skills'])} skills" for l in manifest["layers"])
        + f"\n\nTotal: {out['totals']['skills']} skills, {out['totals']['files']} archivos.\n",
        encoding="utf-8",
    )

    zpath = dist / f"bstack-{manifest.get('version')}.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(stage.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(stage))
    shutil.rmtree(stage)
    print(f"OK -> {zpath} ({zpath.stat().st_size/1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
