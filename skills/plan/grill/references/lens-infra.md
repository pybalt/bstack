# Domain Lens: Infrastructure, Cloud & Platform

Load this lens when grilling cloud resources, networking, deployments, VMs/containers, IAM, scaling, storage, or platform architecture.

## 1. High-Leverage Decision Branches (Risk, Cost & Ops First)

1. **Blast Radius & Failure Modes (`Pre-Mortem` + `FMEA`):**
   - What breaks if this component dies, misconfigures, or gets compromised?
   - Prefer isolated, replaceable runtimes separated from persistent state (`environment`).
2. **Real Scalability vs Hypothetical Scale:**
   - Challenge Kubernetes, multi-region active-active, or custom autoscaling when a single managed service or vertical scaling covers 5x current load cleanly.
   - State the exact **scaling trigger** (CPU/RPS/storage threshold) that would justify graduating later.
3. **Cost Model (Fixed + Variable + Surprises):**
   - Estimate compute, storage, network egress, managed service minimums, and log/metric ingestion costs.
   - Enforce hard budget alerts, lifecycle TTLs, and auto-stop/scale-to-zero for non-prod environments.
4. **Connectivity, Identity & Zero-Trust:**
   - Private-by-default (Tailscale / IAP / SSM / private VPC; avoid public ingress unless strictly required).
   - Least-privilege IAM, short-lived credentials, credential-free proxies for agents/tooling, and encrypted transit/rest.
5. **Rollback, Reproducibility & Operational Burden (*The 3 AM Test*):**
   - Can a clean deploy AND a clean rollback run in minutes via IaC/code (no artisanal console clicks)?
   - Who maintains upgrades, patches, certs, and incidents? Penalize architectures that create high ongoing ops toil.

## 2. Infra Observability & Security Baseline

- **Logs:** Centralized, queryable structured runtime + audit logs across environments (dev/staging/prod), reachable via read-only redacted proxies with bounded retention.
- **Metrics (USE + Cost):** Resource **U**tilization, **S**aturation, **E**rrors (CPU, RAM, disk, connections, queue depth), deploy/health status, and spend anomaly alerts.
- **Security:** Least-privilege IAM, network segmentation, automated secret management (zero hardcoded creds), immutable audit trails, and explicit human escalation before opening ingress or deleting persistent state.

## 3. Recommended Frameworks
`Pre-Mortem` · `Lightweight STRIDE` · `Build vs Buy vs Commodity` · `USE Metrics` · `FMEA` · `ADR`.
