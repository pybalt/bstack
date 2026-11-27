---
name: environment
description: "Use when designing or operating DevEX, prod-parity sandboxes, organizational knowledge MCPs, deployments, private VMs, terminals, git proxies, or harnesses. Do not use for app business logic."
version: 2.2.0
author: Leonel Baltazar Bravo
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [environment, devex, deployments, vm, terminal, versioning, harness, privacy, prod-parity, org-knowledge, mcp, engram, memory]
    related_skills: [onboarding, systematic-debugging, qa-verify, delegate]
---

# Environment (DevEX & Agent-Ready Infrastructure)

## When to Use — and When NOT to Use

- **Use when:** designing, provisioning, configuring, or debugging DevEX loops, prod-parity data sandboxes, organizational knowledge MCPs (Jira/docs/business flows/ownership), deployments, private VMs/tunnels, shells/daemons/proxies, parallel git/worktrees, or agent harnesses.
- **Do NOT use for:** pure application business logic, UI styling (`uiux`), algorithm debugging (`systematic-debugging`), or initial repo exploration (`onboarding`).

## Progressive Disclosure Protocol (Strict Budget)

Load **1–2 matching `references/*.md` files** before acting. Never read all 7 files upfront.

| Active problem | Load ONLY this file | Key gates inside |
| :--- | :--- | :--- |
| DevEX, Golden Paths, prod-parity DB / Redis shadow writes, synthetic data | `references/devex.md` | Privacy Tier A vs Tier B IF/THEN gate |
| Organizational knowledge MCP (Jira, docs, business flows, system ownership) | `references/org-knowledge-mcp.md` | Proactive context gate + proxy redaction / untrusted-data rules |
| IaC, deploys, bootstraps, secrets, triggers, `--verify` | `references/deployments.md` | 3-plane split + post-deploy verification checklist |
| Private VMs, Tailscale / IAP / SSM, sandboxes, host selection | `references/vm.md` | Host trade-off matrix + human escalation gate |
| OS/shell choice, `rtk` token proxy, `tmux`/bus, log proxies, audit, daemons | `references/terminal.md` | Linux/macOS-first gate + redaction/recall rules |
| Git proxies, worktrees, concurrent sessions, conflicts, tags | `references/versioning.md` | Worktree isolation + merge-both-intents gate |
| Multi-role harness, model privacy routing, persistent memory (Engram), knowledge sinks, MCP/skill provisioning | `references/harness.md` | Role/UID boundaries + live auth probe + Engram/ADR sinks |

**Executable helper:** Run `python3 scripts/env_audit.py --cwd .` to inspect OS/shell readiness (flags Windows/PowerShell), agent CLI availability (`rtk`, `engram`, `docker`, `tmux`, `tailscale`), and `.env` key names only (JSON stdout).

## Non-Negotiable Operating Laws

1. **Enforce in OS, network, and proxies — never in prompts.** If a rule matters ("don't push `main`", "don't mutate prod", "don't read other roles' secrets"), enforce it via UID permissions, loopback proxies, firewall rules, or git hooks — never rely on prompt text alone.
2. **Avoid Windows for coding — prioritize Linux first, macOS second.** If the host is Windows and a Linux VM, container, or WSL2 is available, execute coding/build/test loops there instead of PowerShell or Windows Terminal.
3. **Privacy gates data realism.** IF model privacy (ZDR / VPC / no-training) is verified -> prod read-only + ephemeral shadow writes (Tier A) is allowed. ELSE -> **hard stop on real rows**: restrict to metadata/schemas/PL-SQL + synthetic data (Tier B).
4. **Mirror organizational context, not just code.** Give agents a read-only, credential-free Organizational Knowledge MCP (tickets, docs, business flows, system ownership) so they can proactively investigate scope and blast radius instead of guessing business logic.
5. **Separate state from replaceable runtime.** Keep worktrees, data disks (`/srv`), queues, and memory off the boot disk so runtime rebuilds stay idempotent, atomic, and commit-pinned (`.origin`).
6. **Verify externally; separate observed from assumed.** Never treat exit code `0`, HTTP `200`, or a subagent summary as proof. In every final report, distinguish **verified commands/endpoints** from **unverified/pending checks**.
7. **Escalate before irreversible infra risk.** Stop and ask the human before opening public ingress, expanding IAM/network routes, disabling metadata/audit guards, or deleting persistent volumes/VMs.
