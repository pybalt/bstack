# bstack

Stack personal de skills de desarrollo para agentes de código, ordenado **por etapa del flujo de trabajo** y no por herramienta o lenguaje.

La definición canónica del stack vive en [`bstack.yaml`](./bstack.yaml) (**7 etapas, 16 skills**), compatible con cualquier agente que use el estándar `SKILL.md` (Antigravity, Claude Code, Codex, Cursor, Hermes, etc.).

## Etapas del stack

| # | Etapa (`id`) | Qué resuelve | Skills |
| - | ------------ | ------------ | ------ |
| 1 | **Environment** (`environment`) | DevEX, Deployments, VM, Terminal, Versioning y Harness. | `environment` |
| 2 | **Onboarding** (`onboarding`) | Mapeo real de repos existentes y arranque guiado de proyectos nuevos. | `onboarding` |
| 3 | **Entender antes de escribir** (`plan`) | Leer el terreno, experimentar rápido y aislar la causa antes de editar. | `plan`, `spike`, `systematic-debugging` |
| 4 | **Construir** (`construir`) | TDD, portado fiel de librerías y stack unificado de UI/UX y motion. | `test-driven-development`, `portado-fiel-de-libreria`, `uiux` |
| 5 | **Delegar a CLIs de codigo** (`delegar`) | Cuando conviene delegar ejecución: qué CLI usar y con qué encargo. | `claude-code`, `codex`, `opencode`, `cursor-orchestration` |
| 6 | **Depurar** (`depurar`) | Cuando algo no cierra: debugger real y análisis de causa raíz. | `node-inspect-debugger`, `python-debugpy`, `rea-reverse-engineering` |
| 7 | **Revisar y verificar** (`revisar`) | Revisión de calidad, simplificación y verificación con evidencia ejecutada. | `requesting-code-review`, `simplify-code`, `verification-before-completion` |

## Estructura del repositorio

Este repositorio versiona **el manifiesto del stack, el builder y el instalador** (sin redistribuir archivos de skills de terceros):

- `bstack.yaml`: manifiesto declarativo de etapas y skills.
- `build.py`: valida los skills declarados contra tus directorios locales de skills y genera `dist/bstack-<version>.zip` con `MANIFEST.json` (`sha256` por archivo).
- `install.py` / `install.ps1` / `install.sh`: instala el stack en tu agente destino desde un bundle `.zip` o desde tus directorios locales.

## Uso

### 1. Validar y empaquetar

Requiere Python 3.10+ (sin dependencias externas). Por defecto busca tus skills en `~/.agents/skills`, `~/.gemini/config/skills`, `~/.claude/skills`, `~/.codex/skills` o podés indicar la carpeta con `--skills-dir` o `BSTACK_SKILLS_DIR`.

```bash
# Verificar que los 16 skills existan localmente
python build.py --check

# Construir dist/bstack-0.1.0.zip con MANIFEST.json
python build.py
```

### 2. Instalar en tu agente

Podés instalar desde tus skills locales o desde un bundle con `--zip dist/bstack-0.1.0.zip`:

```powershell
# Windows (PowerShell)
.\install.ps1 -Agent antigravity
.\install.ps1 -Agent claude
.\install.ps1 -Agent codex
.\install.ps1 -Agent all -DryRun
```

```bash
# Linux / macOS (Bash)
./install.sh --agent claude
./install.sh --agent codex
./install.sh --agent antigravity
./install.sh --agent all --dry-run
```

Rutas destino por defecto:

- **Antigravity**: `~/.gemini/config/skills/<skill>`
- **Claude Code**: `~/.claude/skills/<skill>`
- **Codex**: `~/.codex/skills/<skill>` (o `~/.agents/skills/<skill>` si no existe `~/.codex`)
- **Hermes**: `~/AppData/Local/hermes/skills/<etapa>/<skill>` (Windows) o `~/.hermes/skills/<etapa>/<skill>` (Unix)

Flags útiles: `--force` para sobrescribir existentes, `--target <ruta>` para una carpeta custom, `--layout flat|layered` para elegir estructura plana o por etapa, y `--dry-run` para previsualizar.

## Licencia

[MIT](./LICENSE) — Leonel Baltazar Bravo
