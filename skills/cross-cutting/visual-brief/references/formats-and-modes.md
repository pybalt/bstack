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

## 2. Composable Block Engine & Pure-SVG Chart Catalog (`brief-shell.html`)

`assets/brief-shell.html` is a **Block Composer**, not a rigid template. Each tab in `BRIEF.views` takes `blocks: [...]` (or a single block object for backward compatibility) and can place any two blocks side-by-side using `{"type": "grid", "cols": 2, "blocks": [ ... ]}` (collapses to 1 column below `920px`).

All **19 quantitative charts** render as **pure inline SVG** with **zero external CDN scripts** — guaranteeing instant load, Retina crispness, Light/Dark theme token sync, keyboard + inspector interactivity, and strict CSP compliance inside IDE artifact panes.

| Category | Block `type` | Visual Output | Key Data Fields |
| :--- | :--- | :--- | :--- |
| **Strategy / 2D** | `quadrant-plot` | Continuous 2×2 X vs Y over a 10×10 desirability field (Green → Amber → Neutral → Hatched Gray) | `xLabel`, `yLabel`, `xLowGood`, `points: [{id, title, x, y, size, lead}]` |
| **Strategy / 2D** | `scatter` | Multi-series X vs Y scatter plot + optional dashed **Pareto frontier** | `xLabel`, `yLabel`, `points: [{id, title, x, y, series, pareto, winner, dominated}]` |
| **Strategy / 2D** | `radar` | Multi-axis spider/radar polygon comparison | `max`, `axes: [...]`, `series: [{label, values: [...], color}]` |
| **Strategy / 2D** | `heatmap` | Clickable X × Y color-intensity grid (`risk`, `win`, `info`, or `diverging` `-1..+1` correlation) | `scale`, `min`, `max`, `cols: [...]`, `rows: [{label, values: [...], notes}]` |
| **Distributions** | `bell` | Gaussian normal curves (Before vs After) with `p50`/`p95`/`p99` + red SLO threshold | `unit`, `xLabel`, `slo`, `minZero`, `curves: [{label, mean, sd, color, dashed}]` |
| **Distributions** | `boxplot` | Horizontal 5-number Box & Whisker plot (`min`, `Q1`, `median`, `Q3`, `max`) + outlier dots | `unit`, `xLabel`, `groups: [{label, min, q1, median, q3, max, outliers}]` |
| **Distributions** | `histogram` | Binned frequency bars + smooth density envelope + optional vertical reference line | `xLabel`, `showCurve`, `refIndex`, `refLabel`, `bins: [{label, count, highlight}]` |
| **Trends / Deltas** | `kpi` | Executive metric cards (2–4 across) with tabular headline, delta pill, and inline SVG sparkline | `items: [{id, label, value, delta, deltaTone, spark: [...], lead}]` |
| **Trends / Deltas** | `line` | Multi-series line/area chart + optional shaded confidence band (`low`/`high`) + SLO threshold | `labels: [...]`, `area`, `band`, `threshold`, `series: [{label, values, dashed}]` |
| **Trends / Deltas** | `slope` | Before → After dumbbell delta chart color-coded green (improved) vs red (regressed) | `beforeLabel`, `afterLabel`, `unit`, `lowerIsBetter`, `items: [{label, before, after}]` |
| **Trends / Deltas** | `waterfall` | Additive bridge chart (`start` → `delta` steps → `total`) with dotted connectors | `unit`, `lowerIsBetter`, `items: [{label, value, kind: "start"\|"delta"\|"total"}]` |
| **Composition** | `pareto` | Sorted bars (vital 80% highlighted) + cumulative curve + 80% guide | `items: [{label, value, lead}]` |
| **Composition** | `bar` | Vertical or horizontal, grouped or stacked bar comparison | `orientation`, `stacked`, `unit`, `categories: [...]`, `series: [{label, values}]` |
| **Composition** | `donut` | Composition ring with centered KPI total + interactive percentage legend | `unit`, `centerValue`, `centerLabel`, `items: [{label, value, color}]` |
| **Composition** | `treemap` | Proportional balanced-split rectangles colored by group with labels & share | `unit`, `items: [{label, value, group, color, lead}]` |
| **Flow / Funnel** | `funnel` | Centered tapered conversion funnel with top-% and step-to-step drop-off badges | `stages: [{label, value, color, lead}]` |
| **Flow / Funnel** | `sankey` | Multi-column weighted cubic Bézier alluvial flow diagram | `unit`, `nodes: [{id, label, col, color}]`, `links: [{source, target, value}]` |
| **Plan / Health** | `timeline` | Horizontal Gantt / roadmap / postmortem bars with progress fill and `today` line | `axis: [...]`, `today`, `todayLabel`, `tasks: [{label, start, end, progress, tone}]` |
| **Plan / Health** | `bullet` | Compact Stephen Few SLO/KPI bullet gauges with qualitative bands + target tick | `items: [{label, value, target, max, ranges, unit, lowerIsBetter}]` |
| **Structure** | `grid` / `profile` / `flow` / `pugh` / `matrix2x2` / `table` / `walkthrough` / `checks` / `callout` / `slides` | Composable 2-col layout, problem profile, swimlanes, Pugh cards, discrete 2×2, numeric tables, Before/After diffs, RDD receipts, callouts, slide decks | See legacy/structural schemas above |

**Composition Discipline:** Cap each tab at **2–3 cohesive blocks** (e.g., `kpi` + 2-column `grid` of charts + 1 `callout` or `table`). Never pile 6 charts into one scrolling wall.

## 3. Process vs System Classification (For Diagrams)

Before drawing any diagram, decide explicitly whether it is a **Process** or a **System** (first matching rule wins):

1. **Verbs vs Nouns:** Boxes are action steps (*"Validate payment"*, *"Emit event"*) → **Process**. Boxes are persistent parts (*"Web App"*, *"API"*, *"Orders DB"*) → **System**.
2. **Repeated actor/component:** Would the same person or platform appear in two boxes? → **System** (each participant appears **once**; arrows repeat, never boxes).
3. **Ends vs Runs Continuously:** Has a clear trigger and terminal state → **Process**. Ongoing back-and-forth while running → **System**.

### Diagram Structural Rules
- **Prune ruthlessly:** Target **6–10 nodes** (hard cap **12**). If removing a box and moving its detail into a neighbor's Level 3 loses no decision clarity, prune it. Larger sub-flows become a single `subprocess` node.
- **Orthogonal edges only:** Horizontal and vertical segments (straight or right-angle elbows) — no tangled diagonals or crossing edges over boxes/labels.
- **Process rules:** Single reading direction (left-to-right desktop, top-to-bottom mobile); every step has input + output; diamonds are closed questions (`"Stock available?"`) with ≥ 2 labeled exits (`"Yes"`, `"No"`).
- **System rules:** No artificial start/end; each component appears once; arrows are labeled with verbs (*"Queries"*, *"Publishes"*); use C4 zoom discipline (never mix high-level services with individual helper functions on the same map).
