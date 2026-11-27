# Engineering & Product Frameworks — Copy-Ready Templates

Pick **1–2 templates max** per `grill` session based on `references/frameworks.md`. Never run all templates together.

---

## 1. Four Value Levers
```markdown
### Value Check (4 Value Levers)
| Lever | Impact (None / Low / Med / High) | Concrete Measurable Signal |
| :--- | :---: | :--- |
| **Revenue** | ... | ... |
| **Cost** | ... | ... |
| **Efficiency** | ... | ... |
| **Risk** | ... | ... |
**Verdict:** Proceed / Cut scope / Challenge priority
```

## 2. Impact × Feasibility (2×2)
```markdown
### Impact × Feasibility
- **Quick Wins (High Impact, High Feasibility — Do First):** ...
- **Big Bets (High Impact, Low Feasibility — Spike / Stage):** ...
- **Fill-ins (Low Impact, High Feasibility — Only If Free):** ...
- **Money Pits (Low Impact, Low Feasibility — Cut):** ...
```

## 3. RICE & MoSCoW Scope Cut
```markdown
### RICE Prioritization (`(Reach × Impact × Confidence) / Effort`)
| Item | Reach | Impact (0.25–3) | Confidence (%) | Effort (person-days) | RICE | MoSCoW |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| ... | ... | ... | ... | ... | ... | Must / Should / Could / Won't |
```

## 4. Appetite & Timebox (Shape Up)
```markdown
### Appetite
- **Problem Worth (Fixed Timebox):** <e.g., 2 days / 1 week>
- **Fixed Time, Variable Scope:** What MUST ship inside appetite vs what gets cut first.
- **Rabbit Holes / No-Gos:** <explicit traps we will not enter>
```

## 5. CUJ (Critical User Journey) — Blocks & Outputs
```markdown
### CUJ: <Journey Name>
| Block | Trigger / Input | System Action | Verifiable Output | SLI / Metric |
| :--- | :--- | :--- | :--- | :--- |
| 1. <Block> | ... | ... | ... | `<latency / error rate / completion>` |
| 2. <Block> | ... | ... | ... | ... |
```

## 6. JTBD (Jobs To Be Done)
```markdown
### JTBD
- **When** `<triggering context/situation>`,
- **I want to** `<core motivation/action>`,
- **So I can** `<measurable desired outcome>`.
```

## 7. Lightweight Event Storming
```markdown
### Domain Flow
`[Actor / Trigger]` -> **Command:** `<DoX>` -> **Policy / Rule:** `<Invariant>` -> **Event:** `<XHappened>` -> **Downstream System / Read Model:** `<Consumer>`
```

## 8. Pugh Competition Matrix (Against Baseline Simple)
```markdown
### Decision: <Branch Name> (Profile: <Magnitude · Blast Radius · Reversibility>)
| Criterion (1–5) | A: Baseline Simple | B: <Alternative> | C: <Hybrid / Alt> |
| :--- | :---: | :---: | :---: |
| Problem Fit (No-Overkill) | ... | ... | ... |
| Low Friction | ... | ... | ... |
| Zero Tech Debt (target 0) | ... | ... | ... |
| Technical Solidity (+ Obs/Sec) | ... | ... | ... |
| Evolutionary Exit | ... | ... | ... |
**Winner:** `<Option>` · **Breakpoint:** switch only if `<concrete threshold>`.
```

## 9. Pre-Mortem & Lightweight FMEA
```markdown
### Pre-Mortem ("6 months later, this failed in production — why?")
| Failure Mode | Severity (1–5) | Likelihood (1–5) | Detectability (1=easy, 5=blind) | Preventive Guardrail or Telemetry Added |
| :--- | :---: | :---: | :---: | :--- |
| ... | ... | ... | ... | ... |
```

## 10. Lightweight STRIDE Threat Check
```markdown
### STRIDE Boundary Check: <Component / Trust Boundary>
- **S**poofing (identity/authn): `<control>`
- **T**ampering (integrity/input validation): `<control>`
- **R**epudiation (audit trail/logs): `<control>`
- **I**nfo Disclosure (PII/secrets redaction, least privilege): `<control>`
- **D**enial of Service (rate limits, bounds, timeouts): `<control>`
- **E**levation of Privilege (server-side authz check): `<control>`
```

## 11. SLI / SLO + RED / USE Telemetry Contract
```markdown
### Telemetry Contract
- **Service (RED):** Rate `<req/s>` · Errors `<4xx vs 5xx threshold>` · Duration `<p95/p99 target>`
- **Infra (USE):** Utilization `<CPU/RAM/disk>` · Saturation `<queue/conn pool>` · Errors `<hardware/OS>`
- **SLI / SLO:** `<e.g., 99.5% of checkout CUJ completes < 800ms>`
```
