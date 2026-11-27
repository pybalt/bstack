# VM & Ephemeral Sandboxes (Private-by-Default Isolation)

Load this reference when provisioning agent VMs, configuring private access, choosing a host, or designing sandboxed execution.

## 1. Choosing the Runtime Host (Decision Gate)

Evaluate the workload against **multi-role OS isolation, VPN/DB parity, background agent persistence, and ops cost**:

| Option | Choose when | Strengths | Deal-breaker limitations |
| :--- | :--- | :--- | :--- |
| **Private VM + Tailscale / IAP / SSM** | Multi-agent workstations, VPN/read-only DB parity, credential proxies, persistent daemons | Full Linux kernel control (`uid`/role, `nftables`, `auditd`, `chattr +a`), persistent `/srv`, native VPC/VPN, uninterrupted background loops | You own IaC/patching (`terraform`, `bootstrap.sh`, idle shutdown) |
| **GitHub Codespaces** ([Overview](https://docs.github.com/en/codespaces/about-codespaces/what-are-codespaces)) | Lightweight single-dev GitHub repos, quick PR sandboxes without VPN/PII | Instant DevContainer + prebuilds, ephemeral `GITHUB_TOKEN`, Tailscale bridge possible ([Private Network](https://docs.github.com/en/codespaces/developing-in-a-codespace/connecting-to-a-private-network)) | Single-user container (no multi-role UID/`nftables`/auditd boundary), suspends on terminal/UI idle even while background agents work ([Idle Timeout](https://docs.github.com/en/codespaces/setting-your-user-preferences/setting-your-timeout-period-for-github-codespaces)), GitHub lock-in |
| **Self-Hosted CDE** (e.g. [Coder](https://coder.com/docs) / DevPod on your VPC) | Team-scale self-service DevContainers inside your own cloud | Terraform templates + DevContainer ergonomics inside private VPC/VPN | Extra control-plane server ops if you only need 1 VM per engineer |

## 2. Private-by-Default Agent VM Contract

Treat agents on a real VM as an **untrusted execution layer**:

- **Zero public IP; tunnel or mesh-only ingress:** Keep port 22 closed to the internet. Connect team machines exclusively via identity-aware tunnels (GCP IAP, AWS SSM) or **Tailscale**:
  - Enable **Tailscale SSH** (`tailscale set --ssh`) to authenticate via identity/WireGuard instead of static `~/.ssh/authorized_keys`.
  - Tag VMs (`tag:private-vm`) and scope reachability via **ACLs** (`check` re-auth mode + SSH session recording for sensitive hosts).
  - Use **Subnet Routers** (`--advertise-routes=...` + `--stateful-filtering`) only for legacy VPC/LAN targets unable to run Tailscale, locked down by ACLs.
  - Docs: [Tailscale SSH](https://tailscale.com/docs/features/tailscale-ssh) · [ACLs](https://tailscale.com/docs/features/access-control/acls) · [Tags](https://tailscale.com/docs/features/tags) · [Subnet Routers](https://tailscale.com/docs/features/subnet-routers)
- **Federated identity:** Prefer OS Login / Tailscale identity / SSM; block project-wide static SSH keys.
- **Persistent `/srv` vs ephemeral boot disk:** Store worktrees, bus/mailboxes, skills, and role memory on a separate data disk so OS rebuilds preserve state.
- **1 OS user per role, zero general `sudo`:** Enforce boundaries via UID/GID ownership (`0700`/`0750`) and single-command `sudoers.d` rules only where strictly required.

## 3. Credential Proxies, Metadata Guard & Live Debug Access

- **Block cloud metadata servers for `uid >= 1000`:** Enforce via `nftables`/`iptables` so agents cannot self-mint tokens for other roles.
- **Loopback proxies (`127.0.0.1`) with short-lived tokens:** Root-owned proxies gated by UID/GID (`nftables` / Unix socket perms) mint short-TTL tokens (~15m) for model APIs, git PATs, **cross-env real-time logs/diagnostics**, and DB queries — agents use the proxy CLI, never read raw credentials.
- **VPN DB boundary:** Restrict direct VPN DB access to a dedicated `db-query` proxy/user enforcing `references/devex.md` Tier A (read-only + shadow write) or Tier B (metadata-only).

## 4. Ephemeral Sandboxes & Cost Control

- **Kill the idle:** Auto-shutdown VMs after an idle window (counting SSH, active agent sessions, containers, pending tasks, CPU) and wake on demand.
- **True isolation runtimes:** Plain pods share the host kernel; untrusted execution requires `gVisor`, `Kata Containers`, or microVMs (Firecracker) via `RuntimeClass` (test `io_uring`/GPU compatibility first).
- **Per-task lifecycle:** 1 sandbox per task, pre-baked snapshots (cut cold start), hard execution timeouts, default-deny egress allowlist, and volume cleanup on exit.

## 5. Escalation Gate & Remote Safety

- Always pass `-o BatchMode=yes -o ConnectTimeout=10` over SSH and verify `whoami && hostname && pwd` before stateful commands.
- **Escalate to human before:** opening public ingress, adding IAM permissions/network routes, disabling metadata/audit rules, or deleting a persistent disk/VM.
