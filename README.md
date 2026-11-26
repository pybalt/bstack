# bstack

Stack de desarrollo para agentes de código: el ciclo completo de un cambio de software, desde preparar el repositorio hasta verificar el resultado y hacer merge.

Está ordenado **por etapa del flujo de trabajo**, no por herramienta, para que el agente sepa qué skill cargar según el punto del cambio en el que está trabajando.

## Etapas del stack

| # | Etapa (`id`) | Qué resuelve | Skills |
| - | ------------ | ------------ | ------ |
| 1 | **Entorno y repositorio** (`entorno`) | Autenticación, clonado y trabajo cuando otro agente toca el mismo repo. | `github-auth`, `github-repo-management`, `repos-con-sesiones-paralelas`, `codebase-inspection` |
| 2 | **Entender antes de escribir** (`plan`) | Leer el terreno y acordar el cambio antes de la primera línea. | `plan`, `spike`, `systematic-debugging` |
| 3 | **Construir** (`construir`) | Test primero, port fiel y skills que se puedan mantener. | `test-driven-development`, `portado-fiel-de-libreria`, `hermes-agent-skill-authoring` |
| 4 | **Delegar a CLIs de codigo** (`delegar`) | Cuando el volumen no lo hace el agente principal: qué CLI, con qué encargo. | `claude-code`, `codex`, `opencode`, `cursor-orchestration` |
| 5 | **Revisar** (`revisar`) | Antes del PR: seguridad, calidad y simplificación. | `requesting-code-review`, `github-code-review`, `simplify-code`, `ui-anti-slop` |
| 6 | **Depurar** (`depurar`) | Cuando algo no cierra: causa raíz antes que parche. | `node-inspect-debugger`, `python-debugpy`, `rea-reverse-engineering` |
| 7 | **Entregar** (`entregar`) | Del issue al PR con CI verde, y el deploy cuando corresponde. | `github-issues`, `github-issue-to-pr`, `github-pr-workflow`, `cloudflare-workers-deploy` |
| 8 | **Verificar** (`verificar`) | Nada se declara terminado sin prueba ejecutada. | `verification-before-completion`, `dogfood` |

La definición canónica del stack vive en [`bstack.yaml`](./bstack.yaml) (8 etapas, 27 skills).

## Estructura del repositorio

Este repositorio versiona **la definición del stack, el builder y el instalador** (sin redistribuir archivos de skills de terceros):

- `bstack.yaml`: manifiesto de etapas y skills.
- `build.py`: valida los skills declarados contra el árbol local de Hermes y empaqueta `dist/bstack-<version>.zip` con `MANIFEST.json` (hashes `sha256`).
- `install.py` / `install.ps1` / `install.sh`: instala el stack en Hermes, Claude Code, Codex o Antigravity desde un bundle `.zip` o desde el árbol local de Hermes.

## Uso

### 1. Validar y empaquetar

Requiere Python 3.10+ (sin dependencias externas) y tener los skills disponibles en el directorio local de Hermes (`~/AppData/Local/hermes/skills` en Windows o `~/.hermes/skills` en Linux/macOS, configurable con `BSTACK_SKILLS_DIR`, `HERMES_HOME` o `--skills-dir`).

```bash
# Verificar que los 27 skills existan localmente
python build.py --check

# Construir dist/bstack-0.1.0.zip con MANIFEST.json
python build.py
```

### 2. Instalar en tu agente

Podés instalar desde el árbol local de Hermes o pasando `--zip dist/bstack-0.1.0.zip`:

```powershell
# Windows (PowerShell)
.\install.ps1 -Agent antigravity
.\install.ps1 -Agent claude
.\install.ps1 -Agent codex
.\install.ps1 -Agent hermes
.\install.ps1 -Agent all -DryRun
```

```bash
# Linux / macOS (Bash)
./install.sh --agent claude
./install.sh --agent codex
./install.sh --agent antigravity
./install.sh --agent hermes
./install.sh --agent all --dry-run
```

Rutas destino por defecto:

- **Hermes**: `~/AppData/Local/hermes/skills/<etapa>/<skill>` (Windows) o `~/.hermes/skills/<etapa>/<skill>` (Unix)
- **Claude Code**: `~/.claude/skills/<skill>`
- **Codex**: `~/.codex/skills/<skill>` (o `~/.agents/skills/<skill>` si no existe `~/.codex`)
- **Antigravity**: `~/.gemini/config/skills/<skill>`

Flags útiles: `--force` para sobrescribir skills ya instalados, `--target <ruta>` para elegir una carpeta custom, `--layout flat|layered` para forzar la estructura y `--dry-run` para previsualizar cambios.

## Licencia

[MIT](./LICENSE) — Leonel Baltazar Bravo
