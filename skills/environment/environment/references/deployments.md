# Deployments (3-Plane Architecture, Idempotency & Verification)

Load this reference when provisioning infrastructure, shipping platform updates, or deploying services/workers.

## 1. Three-Plane Separation (Never Collapse Them)

| Plane | Owns | Hard rule |
| :--- | :--- | :--- |
| **Control Plane** (IaC: Terraform/OpenTofu) | Networks, IAM, service accounts, disks, buckets, firewall/tunnel rules | Branch + review required; ad-hoc runs allowed **only** for read-only (`plan`, `describe`, `list`) |
| **Install Plane** (pack + copy + bootstrap) | Bundle packaging, private tunnel copy, root bootstrap | Atomic directory swap; **never** hand-edit platform files inside a running host |
| **Runtime Plane** (target services/CLIs) | Agent CLIs, local proxies, systemd units, config contracts | Reads single env/YAML contract (e.g., `/etc/sandbox/dev.env`); provider-neutral core |

## 2. Idempotent, Version-Pinned Installs

1. **Idempotency gate:** Running `bootstrap` twice on the same host must converge cleanly — zero duplicate users, crons, systemd units, or firewall rules.
2. **Commit pinning (`.origin`):** Write deployed git SHA to an `.origin` file on target so `--verify` detects repo-to-host drift immediately.
3. **Feature flags & provider abstraction:** Gate cloud-specific features (`git-proxy`, `model-token`, `cloud-logging`, `board`) behind explicit flags or `$CLOUD` branches with a neutral default so core runs on any Ubuntu/Linux host.

## 3. Secrets, Triggers & Edge Deploy Traps

- **No long-lived secrets in app/agent env:** Pipe secrets via `stdin` to secret stores, or hold them inside a root-owned local proxy that attaches auth only on allowlisted requests.
- **Semantic secret verification:** A generic `401` cannot separate "missing key" from "invalid key". Confirm with a non-destructive call where a provider-specific response proves the key decoded and authenticated.
- **Separate state for triggers & migrations:** Code uploads often leave cron schedules, routes, or DB migrations untouched. Explicitly verify schedules (`GET .../schedules`), export names (`scheduled` handler), and strip one-time initial migrations (e.g., Durable Object / SQL init) on redeploys.
- **Auth on mutating public endpoints:** Enforce token gating from deploy #1 and verify all three cases: **missing token → 401**, **invalid token → 401**, **valid token → 200**. Check downstream IP allowlists before choosing dynamic-IP edge runtimes.

## 4. Non-Mutating External Verification (`--verify`) — Completion Checklist

Never declare a deploy "done" on exit code `0` or HTTP `200` alone. Complete every applicable check:

- [ ] Read-only `--verify` passed (units active, permissions/UIDs intact, proxy healthy, `.origin` matches `HEAD`).
- [ ] Compiled/bundled artifact was smoke-tested (not just unbundled source).
- [ ] Live streaming logs (`tail`) observed during a real request or trigger.
- [ ] Post-deploy side effect confirmed (DB row, event, or job output timestamped **after** deploy time; non-zero app error codes inside HTTP 200 JSON checked).
- [ ] `dist/` and local secret files remain gitignored (`git status -sb` clean).
