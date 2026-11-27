# Existing Repository Onboarding (Read-Only)

Load this reference when entering an unfamiliar repository or resuming a codebase that may have changed since your last session.

## 1. Parallel Ground-Truth Sweep (Batch 1 — Read-Only)

Run these lookups in parallel; never inspect `.git/objects`, `node_modules`, `.venv`, `dist`, or `build`:

1. **Git truth:** `git status -sb`, `git log --oneline -12`, `git worktree list`.
2. **Project contracts & persistent memory:** Check for `AGENTS.md`, `CLAUDE.md`, `DESIGN.md`, `.cursor/rules`, `README.md` — and query cross-session engineering memory (e.g., Engram MCP, if configured) for prior decisions, conventions, and known pitfalls in this repo.
3. **Runtime & manifests:** Read `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, `Dockerfile`, `.env.example`, and CI workflows (`.github/workflows/*`, `.gitlab-ci.yml`).
4. **Top-level map:** List depth 1–2 directories to locate source, tests, scripts, and configs.

## 2. Entrypoint & Verification Probe (Batch 2)

Do not stop at the directory tree:

1. **Read the real entrypoint(s)** + **1 core module** (CLI bin, server bootstrap, router root, worker handler, or package exports).
2. **Identify boundaries:** External APIs, databases, queues, auth middleware, and env/config validation schemas.
3. **Probe verification surface:** Identify exact `dev`, `build`, `typecheck`, `lint`, and `test` commands. Run the fastest non-destructive check (e.g. unit test subset or `--check`) if safe; if you do not run it, mark it `Not run`.

## 3. Drift & Hazard Check

- **Doc drift:** Flag any file paths, scripts, or test counts in `README.md`/`AGENTS.md` that disagree with the live tree.
- **Dirty tree / parallel WIP:** If `git status` shows foreign modifications, inspect `git diff` and defer to `environment/references/versioning.md` before staging or editing.
- **Missing prereqs:** Flag absent `.env`, unbuilt codegen, or mismatched runtime versions (`.nvmrc`, `.python-version`).

## 4. Required Output Schema (Completion Criterion)

Deliver **one screen** with zero filler and strict separation between observed facts and unexecuted commands:

```markdown
### Onboarding Brief — <repo>
- **Purpose & Stack:** <1 sentence> | <runtime/framework + lockfile manager>
- **Entrypoints & Core Map:** `<path>` (entrypoint), `<dir>` (core logic), `<dir>` (tests)
- **Commands:**
  - Verified: `<cmd>` -> <exact observed result>
  - Read from config (not run): `<cmd>`
- **Drift & Hazards:** <doc mismatches, dirty WIP, missing .env, or "None observed">
- **Ready for:** <next step — `grill`, `spike`, `odd-build`, or `systematic-debugging`>
```

*(If a cross-session memory tool like Engram is active, persist newly discovered verified commands, entrypoints, and repo hazards so future sessions skip re-discovery.)*
