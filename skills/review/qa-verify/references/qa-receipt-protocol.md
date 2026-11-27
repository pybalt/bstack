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

## 3. RDD Verification Receipt (Required Closing Output)

```markdown
# Verification Receipt (RDD) — <branch / feature>
- **Status:** VERIFIED | PARTIAL (unverified items listed) | BLOCKED
- **Fingerprint:** `HEAD <sha>` · `diff <12-char-hash>` (Unchanged post-QA: Yes)
- **Adversarial Review:** `<APPROVED / N/A (inline low-risk)>` (Blocking remaining: 0)

## Executed Checks (Verified)
| Gate | Command / Probe | Observed Result |
| :--- | :--- | :--- |
| Mechanical (build/lint/tests) | `<exact cmd>` | PASS (`<exact counts / exit 0>`) |
| Behavioral / E2E QA | `<exact probe / flow>` | PASS (`<observed state / output>`) |
| Observability & Security | `<log/metric/secret check>` | PASS (structured events present, 0 leaks) |

## Not Verified / Environment Limits
- <Explicit list of anything not executed and why — or "None">

## Artifacts & Memory
- Optional `visual-brief` walkthrough: `<path or N/A>`
- Durable lessons / new commands persisted (e.g., Engram): `<yes/no>`
```
