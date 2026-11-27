---
name: onboarding
description: "Use when entering an unfamiliar repo or starting a new project. Progressive disclosure for codebase mapping and guided project setup. Skip for mid-session focused edits."
version: 1.1.0
author: Leonel Baltazar Bravo
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [onboarding, codebase, architecture, workspace, setup, handoff]
    related_skills: [environment, grill, spike, odd-build]
---

# Onboarding

## When to Use — and When NOT to Use

- **Use when:** opening an unfamiliar repository, resuming a repo after parallel/external changes, or starting a brand-new project from an empty directory (`/onboarding`).
- **Do NOT use for:** focused edits inside a repository you already mapped in this session, or pure debugging (`systematic-debugging`).

## Mode Router (Load Exactly ONE File)

| Workspace state | Load ONLY this file | Output / Exit gate |
| :--- | :--- | :--- |
| **Code exists** (existing repo) | `references/repo-onboarding.md` | Run `python3 scripts/repo_snapshot.py --cwd .` first → Verified 1-screen Onboarding Brief (**read-only**) |
| **Empty dir or explicit `/onboarding`** | `references/new-project.md` | 1-question-at-a-time intake → Project Seed → **stop & wait** before scaffolding |

## Non-Negotiable Rules

1. **Tree beats docs.** Never trust `README.md`, `AGENTS.md`, or old comments over live manifests, lockfiles, and `git log`. Report every mismatch explicitly.
2. **Never invent command results.** Separate commands you **executed** from commands only **read in config** (`Verified` vs `Not run`).
3. **Zero production edits during onboarding.** Onboarding ends at the verified brief or approved Project Seed — hand off to `grill`, `spike`, or `odd-build` afterward.
4. **Stay inside the read budget.** Run `scripts/repo_snapshot.py` for Batch 1 instead of running 6 separate shell commands; never crawl `node_modules`, `.venv`, `dist`, or giant lockfiles.
