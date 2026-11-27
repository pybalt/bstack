# Engineering & Product Frameworks (Selective Toolbox)

**Strict Rule:** Never apply more than **1–2 frameworks** in a single grill session. Pick only the framework that resolves the active uncertainty — using frameworks for ceremony is overkill.

## Framework Selector (IF / THEN)

| Active Question | Pick 1 Framework | How to apply it concisely |
| :--- | :--- | :--- |
| *"Why build this at all? What business value moves?"* | **4 Value Levers** | Map to **Revenue · Cost · Efficiency · Risk**. If none move measurably, challenge the task. |
| *"Too many ideas — what is in vs out?"* | **Impact × Feasibility (2×2)** or **MoSCoW** | Cut to Quick Wins / Must-haves; push Won'ts out explicitly. |
| *"How do we rank competing backlog items?"* | **RICE** or **WSJF / Cost of Delay** | `RICE = (Reach × Impact × Confidence) / Effort`; use **WSJF** when delay cost / urgency dominates. |
| *"How do we stop scope creep & overkill?"* | **Appetite / Timebox (Shape Up)** | Fix *"how much time is this problem worth?"* first, then design the simplest solid solution that fits. |
| *"Are we jumping to solutions before validating the pain?"* | **Opportunity Solution Tree** | `Outcome → User/System Pain → Candidate Solutions → Spike`. |
| *"What is the end-to-end user or system flow?"* | **CUJ (Blocks & Outputs)** or **Walking Skeleton** | Break the Critical User Journey into blocks with verifiable outputs; ship a thin end-to-end slice first. |
| *"What is the user really trying to achieve?"* | **JTBD (Jobs To Be Done)** | *"When [situation], I want to [motivation], so I can [outcome]."* Essential for Frontend/Product taste. |
| *"How do domain rules & services interact?"* | **Lightweight Event Storming** | `Command → Domain Event → Policy/Rule → System/Read Model`. |
| *"Which technical option wins objectively?"* | **Pugh Matrix** + **One-Way / Two-Way Doors** | Score candidates against Baseline Simple (`references/scoring-and-brief.md`); match rigor to irreversibility. |
| *"Should we build this custom or use off-the-shelf?"* | **Build vs Buy vs Commodity (Wardley)** | Build custom **only** for core differentiators; use boring standard tools/SaaS for commodities. |
| *"How do we document a system at the right zoom?"* | **C4 Model** | Keep one abstraction level per view: Context → Container → Component. Pair with `visual-brief`. |
| *"What could make this blow up in production?"* | **Pre-Mortem** | *"It is 6 months later and this failed badly — why?"* Surfaces hidden risks better than generic checklists. |
| *"What are the security threats by design?"* | **Lightweight STRIDE** | Check **S**poofing, **T**ampering, **R**epudiation, **I**nfo Disclosure, **D**oS, **E**levation of Privilege on each trust boundary. |
| *"Which failures are silent and need telemetry?"* | **Lightweight FMEA** + **SLI/SLO (RED/USE)** | Rate *Severity × Likelihood × Detectability*. Low detectability mandates logs/metrics before coding. Tie SLIs to CUJ outputs using **RED** (services) or **USE** (infra). |
| *"How do we record a permanent architectural call?"* | **Compact ADR** | 4 blocks: Context → Options Considered → Decision → Consequences & Breakpoint. |

## Visual Rendering Rule
Whenever a 2×2 matrix, Pugh comparison, CUJ flow, C4 diagram, or Pre-Mortem grows past a small table and increases cognitive load, delegate rendering to **`visual-brief`** so the user can inspect and decide visually.
