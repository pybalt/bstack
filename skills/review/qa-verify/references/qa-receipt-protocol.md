# RDD Verification Receipt & Domain QA Protocol

Load this reference when executing final verification and issuing an RDD Receipt.

## 1. Fingerprint Freezing (Invalidate on 1-Byte Drift)

Capture a deterministic fingerprint of the exact workspace candidate before running QA checks, and verify it is **unchanged** right before issuing the receipt:

```bash
# Compute candidate fingerprint (HEAD + tracked diff + untracked status)
git rev-parse --short HEAD
(git status --porcelain; git diff HEAD) | sha256sum | cut -c1-12
```
*(On macOS use `shasum -a 256`; on Windows use Python `hashlib.sha256`.)*

**Invalidation rule:** If the post-QA fingerprint differs from the pre-QA fingerprint by even 1 byte, **mark the receipt INVALID** and re-run all checks affected by the edit.

## 2. Fail-Closed Verification Pyramid

Run layers in order — stop and fix if Layer 1 fails:

### Layer 1 — Mechanical Gates (Mandatory)
- **Typecheck & Build:** clean compilation / packaging with zero new warnings/errors.
- **Lint & Format:** project linter passes on changed files.
- **Secret & Hygiene Scan:** zero API keys, tokens, `.env` values, private paths, debug `[DEBUG-*]` logs, or leftover `spikes/` files in the diff.
- **Automated Test Suite:** targeted tests + relevant regression suite pass cleanly.

### Layer 2 — Real Behavioral & E2E QA (Matched to Domain)

| Domain | Required Live Behavioral Checks |
| :--- | :--- |
| **Backend / API / Worker** | Invoke real endpoints/jobs (local parity lab or Tier A/B sandbox per `environment`): verify valid payload, invalid input rejection (4xx), authz denial, idempotency/retry behavior, and actual persisted/shadow state. |
| **Frontend / UI** | Open real rendered app (browser / headless): test primary CUJ flow end-to-end, inspect **Loading / Empty / Error / Edge** states, verify zero console/network errors, check desktop (`1280×800`) + mobile (`390×844`) layout & a11y (`uiux`). |
| **CLI / Scripts** | Execute real CLI with valid fixtures, bad args, missing files, and `--dry-run`/`--check`; verify stdout/stderr format and exact exit codes. |
| **AI / Prompts / Agents** | Run golden eval suite + adversarial/edge inputs; verify schema compliance, fallback behavior on error/timeout, token/cost budget, and prompt-injection containment. |
| **Infra / Deployments** | Dry-run / plan diff (`terraform plan`, IaC check), post-deploy `--verify` health/endpoint probes, rollback readiness, and least-privilege check (`environment/references/deployments.md`). |

### Layer 3 — Live Observability & Security Audit
During Layer 2 execution, inspect the actual emitted output:
- Confirm expected structured log events and `correlation_id` / context keys appear.
- Confirm health/error/business metrics increment as designed.
- Confirm **zero** tokens, passwords, auth headers, or raw PII appear in logs, stack traces, or client-visible error payloads.

### Layer 4 — Mandatory Post-QA Knowledge Closure (Final Step)
Before marking any non-trivial feature, architectural change, refactor, or resolved incident complete, document **what was decided, designed, and shipped** using `assets/adr-and-closure-template.md` into the workspace's configured **Knowledge Sink(s)**:
1. **Architecture / Design Board or Repo Docs:** Update the project's visual architecture board (via MCP, if configured) and/or write a compact ADR (`docs/adr/ADR-NNN-*.md`) + architecture/contract docs.
2. **Cross-Session Memory (e.g., Engram):** Persist architectural decisions, newly verified commands, known hazards, and root-cause lessons so future sessions start informed.
3. *(Exception:)* Trivial single-file inline edits with zero architectural or behavioral contract impact may record `N/A (trivial inline)` explicitly in the receipt.

## 3. RDD Verification Receipt (Required Closing Output)

Copy `assets/receipt-template.md` and populate every row with real observed outputs and the verified post-QA fingerprint from `python3 scripts/fingerprint.py --compare <pre-qa-fp>`.
