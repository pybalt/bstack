# Visual Formats & Mode Selector

Pick **one** primary format per artifact based on what the user needs to understand or decide. Never cram 4 formats into one cluttered page.

## 1. Format Selector (IF / THEN)

| User Situation | Format | Core Visual Primitives |
| :--- | :--- | :--- |
| **`grill` decisions, trade-offs, frameworks** | **Decision Board / 2×2 Matrix** | 4-axis Problem Profile + competing option cards (Baseline Simple highlighted) with score bars, totals, and breakpoint callout — plus 2×2 desirability matrices (**Green** = Quick Wins `Do First`, **Amber** = Big Bets `Spike / Stage`, **Neutral** = Fill-ins `Optional`, **Hatched Gray + Strikethrough** = Money Pits `Avoid`). Decisions are inspected visually here and answered directly in the main chat. |
| **Architecture, business flows, `onboarding`** | **System / Flow Explorer** | Interactive SVG canvas (pan/zoom, click-to-inspect dimming unrelated items) with 3 depth levels + open-question badges on nodes/edges. Follow *Process vs System* classification below. |
| **PRs, refactors, bug fixes, `review`** | **Change Walkthrough** | 10-second executive header + impacted module map + **Before vs After** visual diff/flow comparison + Verified vs Unverified checks semaphore + risks/rollback box. |
| **Proposals, pitches, complex explanations** | **Slide Deck** | One idea per slide, keyboard navigation (`←` / `→` / progress bar), visual diagrams/metrics over prose, expandable speaker/technical notes tucked behind a toggle. |
| **Frontend taste, pipelines, state machines, `evolve`** | **Interactive Stepper / Comparison** | Side-by-side visual UI directions (for Frontend *taste* decisions), step-through state simulator (`Step 1 → 2 → 3`), or Pareto frontier + lineage view (for `evolve` generations). |

## 2. Process vs System Classification (For Diagrams)

Before drawing any diagram, decide explicitly whether it is a **Process** or a **System** (first matching rule wins):

1. **Verbs vs Nouns:** Boxes are action steps (*"Validate payment"*, *"Emit event"*) → **Process**. Boxes are persistent parts (*"Web App"*, *"API"*, *"Orders DB"*) → **System**.
2. **Repeated actor/component:** Would the same person or platform appear in two boxes? → **System** (each participant appears **once**; arrows repeat, never boxes).
3. **Ends vs Runs Continuously:** Has a clear trigger and terminal state → **Process**. Ongoing back-and-forth while running → **System**.

### Diagram Structural Rules
- **Prune ruthlessly:** Target **6–10 nodes** (hard cap **12**). If removing a box and moving its detail into a neighbor's Level 3 loses no decision clarity, prune it. Larger sub-flows become a single `subprocess` node.
- **Orthogonal edges only:** Horizontal and vertical segments (straight or right-angle elbows) — no tangled diagonals or crossing edges over boxes/labels.
- **Process rules:** Single reading direction (left-to-right desktop, top-to-bottom mobile); every step has input + output; diamonds are closed questions (`"Stock available?"`) with ≥ 2 labeled exits (`"Yes"`, `"No"`).
- **System rules:** No artificial start/end; each component appears once; arrows are labeled with verbs (*"Queries"*, *"Publishes"*); use C4 zoom discipline (never mix high-level services with individual helper functions on the same map).
