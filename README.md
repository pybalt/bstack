# bstack

Personal development skill stack for coding agents, organized **by engineering workflow stage** rather than by programming language or vendor CLI.

The canonical stack manifest lives in [`bstack.yaml`](./bstack.yaml) (**8 stages, 12 curated skills**), compatible with any agent supporting the `SKILL.md` standard (Antigravity, Claude Code, Codex, Cursor, Hermes, etc.).

## Core Principles

- **Proportional simplicity, zero technical debt:** overengineering is treated as a defect; ceremony and architecture scale with measured problem size and risk (**ODD** — Organic-Driven Development).
- **Observability & Security by Design:** structured logs, health/business metrics, and trust-boundary guardrails are built in from day one, never deferred.
- **Verifying beats generating (RDD) + mandatory documentation closure:** frozen diff fingerprints, cross-model adversarial review (*Author ≠ Reviewer*), real behavioral QA, evidence-backed receipts that invalidate on 1-byte drift, and mandatory post-QA ADR/architecture/decision persistence to the workspace's knowledge sink(s) (Visual Architecture Board / `docs/adr/` + Engram).
- **Standards-compliant 3-tier Progressive Disclosure:** every skill separates lean `SKILL.md` routers from on-demand `references/`, deterministic Python `scripts/` (JSON stdout), and copy-ready `assets/` templates (including engineering frameworks and a standalone interactive HTML shell).
- **Context & environment parity:** prod-parity sandboxes gated by model privacy, Organizational Knowledge MCP, cross-session memory (e.g., [Engram](https://github.com/Gentleman-Programming/engram)), token-saving CLI proxies, and Linux-first execution.

## Workflow Stages

| # | Stage (`id`) | Scope | Skills |
| - | ------------ | ----- | ------ |
| 1 | **Environment** (`environment`) | DevEX, Organizational Knowledge MCP, persistent memory (Engram), deployments, private VMs, terminal proxies, versioning, and harnesses. | `environment` |
| 2 | **Onboarding** (`onboarding`) | Fast codebase mapping for existing repos and guided seeding for new projects. | `onboarding` |
| 3 | **Plan & Decide** (`plan`) | Measured domain-aware grilling with engineering frameworks and quarantined spikes before coding. | `grill`, `spike` |
| 4 | **Build** (`build`) | Organic-Driven Development (ODD) execution with out-of-the-box observability/security and unified UI/UX. | `odd-build`, `uiux` |
| 5 | **Delegate** (`delegate`) | Context-safe multi-agent orchestration, worktree isolation, and cross-family model routing. | `delegate` |
| 6 | **Debug** (`debug`) | Systematic 4-phase root-cause investigation with tight feedback loops and automated `git bisect`. | `systematic-debugging` |
| 7 | **Review & QA** (`review`) | Receipt-Driven Development (RDD): cross-model adversarial review, live behavioral QA, and fingerprint-bound receipts. | `adversarial-review`, `qa-verify` |
| 8 | **Cross-Cutting** (`cross-cutting`) | Composable interactive visual briefs (19 pure-SVG engineering charts, zero CDN, desktop + mobile) and multi-family evolutionary crossover optimization. | `visual-brief`, `evolve` |

## Repository Layout

- `bstack.yaml`: declarative manifest of workflow stages and skills.
- `skills/<stage>/<skill>/`: all 12 canonical, agent-agnostic skills (`SKILL.md`, `references/`, `scripts/`, `assets/`).
- `adapters/<agent>.json`: lightweight per-IDE runtime adapters (`antigravity`, `claude`, `codex`, `cursor`, `hermes`) automatically appended during install so skills leverage each host's native primitives (e.g., Antigravity HTML Artifacts & `<agent-embed>`, `ask_question`, `invoke_subagent`) without polluting the canonical skills.
- `install.py` / `install.ps1` / `install.sh`: installs the stack directly from `./skills/` (or a `.zip` bundle) and applies the matching host adapter (disable with `--no-adapter`).
- `build.py`: validates every declared skill and optionally builds an offline `dist/bstack-<version>.zip` bundle with `MANIFEST.json` (`sha256` per file).

## Quick Install

Requires Python 3.10+ (standard library only). Clone and install directly into your agent:

```bash
git clone https://github.com/pybalt/bstack.git
cd bstack

# Linux / macOS (recommended for coding agent workflows)
./install.sh --agent claude
./install.sh --agent codex
./install.sh --agent cursor
./install.sh --agent antigravity
./install.sh --agent all --dry-run
```

```powershell
# Windows (PowerShell)
.\install.ps1 -Agent antigravity
.\install.ps1 -Agent claude
.\install.ps1 -Agent codex
.\install.ps1 -Agent cursor
.\install.ps1 -Agent all -DryRun
```

Default destination paths:

- **Antigravity**: `~/.gemini/config/skills/<skill>`
- **Claude Code**: `~/.claude/skills/<skill>`
- **Codex**: `~/.codex/skills/<skill>` (falls back to `~/.agents/skills/<skill>` if `~/.codex` does not exist)
- **Cursor**: `~/.cursor/skills/<skill>`
- **Hermes**: `~/.hermes/skills/<stage>/<skill>` (Unix) or `~/AppData/Local/hermes/skills/<stage>/<skill>` (Windows)

Useful flags: `--force` to overwrite existing skills, `--no-adapter` to install raw agent-agnostic skills without IDE-specific bindings, `--target <path>` for a custom directory, `--layout flat|layered` to choose flat or stage-nested folders, `--zip <bundle>` to install from a packaged archive, and `--dry-run` to preview changes.

### Validate & Package (Optional Offline Bundle)

```bash
# Verify all 12 declared skills resolve cleanly
python build.py --check

# Build dist/bstack-0.6.0.zip with MANIFEST.json (sha256 per file)
python build.py
```

## License

[MIT](./LICENSE) — Leonel Baltazar Bravo
