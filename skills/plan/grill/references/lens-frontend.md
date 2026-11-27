# Domain Lens: Frontend & Product UI

Load this lens when grilling user interfaces, web/mobile flows, visual direction, interaction models, or client state.

## 1. Taste Rule: Show Visually — Do Not Fake Numeric Scores for Aesthetics

Visual direction, hierarchy, and interaction feel depend on **taste and user clarity**, not arbitrary 1–5 formulas in walls of text:
- For **visual/interaction decisions**, compare **2–3 concrete directions or layouts** via `visual-brief` (or hand off to `uiux` discovery) and grill the user on *what feels right and why*.
- Reserve numeric scoring (`references/scoring-and-brief.md`) for **engineering trade-offs** (state architecture, data fetching, bundle weight, caching, rendering strategy).

## 2. High-Leverage Decision Branches

1. **User Intent & Journey First (`JTBD` + `CUJ`):**
   - What is the single primary action on this screen? What cognitive load can be removed instead of added?
   - Cut scope with `Walking Skeleton`: nail the primary happy path before secondary chrome.
2. **Complete State Matrix (Zero Half-Built UI):**
   - Explicitly decide all 5 states before coding: **Default**, **Loading** (skeleton/perceived speed), **Empty** (actionable guidance), **Error** (recoverable, human copy), and **Extreme/Edge** (long text, 0 items, 1000 items, slow network).
3. **State & Architecture Simplicity:**
   - Keep state as local and derived as possible; avoid global stores, premature abstractions, or duplicate client caches when URL state or server state suffices.
   - Challenge unnecessary client libraries — check bundle impact and native platform capabilities first.
4. **Responsive, Input & Accessibility:**
   - Desktop vs mobile behavior (touch targets `>= 44px`, keyboard navigation, focus states, contrast, `prefers-reduced-motion`).

## 3. Frontend Observability & Security Baseline

- **Logs & Error Visibility:** Unhandled error boundaries + structured client error reporting (route, action, correlation ID linking to backend logs — zero PII/tokens).
- **Metrics:** Core user-facing signals — perceived latency (LCP/INP or key interaction completion time), CUJ completion/drop-off, and client-side error rate.
- **Security:** Zero secrets in client bundles, safe DOM rendering (no raw `innerHTML` with untrusted content), strict CSRF/CORS/cookie hygiene, and never rely on client-side validation as an authorization boundary.

## 4. Recommended Frameworks
`JTBD` · `CUJ Blocks & Outputs` · `Walking Skeleton` · `Impact × Feasibility`.
