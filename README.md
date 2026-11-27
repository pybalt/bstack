# bstack

Personal development skill stack for coding agents, organized **by engineering workflow stage** rather than by language or vendor tool.

The canonical stack manifest lives in [`bstack.yaml`](./bstack.yaml) (**8 stages** — currently **8 curated skills**, remaining stages WIP), compatible with any agent supporting the `SKILL.md` standard (Antigravity, Claude Code, Codex, Cursor, Hermes, etc.).

## Workflow Stages

| # | Stage (`id`) | Scope | Skills |
| - | ------------ | ----- | ------ |
| 1 | **Environment** (`environment`) | DevEX, Organizational Knowledge MCP, deployments, private VMs, terminal proxies, versioning, and harnesses. | `environment` |
| 2 | **Onboarding** (`onboarding`) | Fast codebase mapping for existing repos and guided seeding for new projects. | `onboarding` |
| 3 | **Plan & Decide** (`plan`) | Measured domain-aware grilling with engineering frameworks and quarantined spikes before coding. | `grill`, `spike` |
| 4 | **Build** (`build`) | *WIP* | `uiux` |
| 5 | **Delegate** (`delegate`) | *WIP* | — |
| 6 | **Debug** (`debug`) | Systematic 4-phase root-cause investigation with tight feedback loops and automated `git bisect`. | `systematic-debugging` |
| 7 | **Review** (`review`) | *WIP* | — |
| 8 | **Cross-Cutting** (`cross-cutting`) | Interactive visual briefs (desktop + mobile) and multi-family evolutionary crossover optimization. | `visual-brief`, `evolve` |

## Repository Layout

This repository versions **the stack manifest, builder, and installers** (without redistributing raw third-party skill trees):

- `bstack.yaml`: declarative manifest of workflow stages and skills.
- `build.py`: validates declared skills against your local skill directories and packages `dist/bstack-<version>.zip` with `MANIFEST.json` (`sha256` per file).
- `install.py` / `install.ps1` / `install.sh`: installs the stack into your target agent from a built `.zip` bundle or directly from local skill directories.

## Usage

### 1. Validate and Package

Requires Python 3.10+ (standard library only). By default, `build.py` resolves skills from `~/.agents/skills`, `~/.gemini/config/skills`, `~/.claude/skills`, `~/.codex/skills`, and Hermes skill folders, or you can override with `--skills-dir` / `BSTACK_SKILLS_DIR`.

```bash
# Check that all declared skills exist locally
python build.py --check

# Build dist/bstack-0.1.0.zip with MANIFEST.json
python build.py
```

### 2. Install into Your Agent

Install from your local skill directories or from a packaged bundle with `--zip dist/bstack-0.1.0.zip`:

```bash
# Linux / macOS (recommended for coding agent workflows)
./install.sh --agent claude
./install.sh --agent codex
./install.sh --agent antigravity
./install.sh --agent all --dry-run
```

```powershell
# Windows (PowerShell)
.\install.ps1 -Agent antigravity
.\install.ps1 -Agent claude
.\install.ps1 -Agent codex
.\install.ps1 -Agent all -DryRun
```

Default destination paths:

- **Antigravity**: `~/.gemini/config/skills/<skill>`
- **Claude Code**: `~/.claude/skills/<skill>`
- **Codex**: `~/.codex/skills/<skill>` (falls back to `~/.agents/skills/<skill>` if `~/.codex` does not exist)
- **Hermes**: `~/.hermes/skills/<stage>/<skill>` (Unix) or `~/AppData/Local/hermes/skills/<stage>/<skill>` (Windows)

Useful flags: `--force` to overwrite existing skills, `--target <path>` for a custom directory, `--layout flat|layered` to choose flat or stage-nested folders, and `--dry-run` to preview changes.

## License

[MIT](./LICENSE) — Leonel Baltazar Bravo
