# Anti-Slop Audit: 10-Tell Diagnostic, U1–U20 & Static Hygiene

Static pattern scanner: `scripts/audit_ui.py`.

## Part 1 — Compositional 10-Tell Slop Diagnostic (Diagnose First, Fix Second)

## Anti-Slop Rules

Avoid common AI design sludge:

- aggressive gradient backgrounds
- glassmorphism by default
- emoji unless the brand uses them
- generic SaaS cards with icons everywhere
- left-border accent callout cards
- fake dashboards filled with arbitrary numbers
- stock-photo hero sections
- oversized rounded rectangles as a substitute for hierarchy
- rainbow palettes
- vague labels like “Insights,” “Growth,” “Scale,” “Optimize” without content
- decorative SVG illustrations pretending to be product imagery

Minimal is not automatically good. Dense is not automatically cluttered. Choose intentionally.

## Slop Diagnostic: Score Before You Fix

AI design slop has a tiny, predictable failure distribution — designers asked to label AI UIs collapse the "this is AI" signal down to about ten tells. Before polishing or repairing an artifact, run this as an explicit self-audit and write a short report. **Diagnose first, treat second** — auditing and fixing in one breath fails, because the model's prior outweighs the instruction and it repeats the mistake (recolors when it needed re-layout, polishes type on a composition problem).

The ten tells (presence of each = one point of slop; lower is better):

1. **Tech gradient** — blue/violet/indigo glossy gradient on everything.
2. **Generic tech hue** — the default accent is indigo/violet (not chosen for the brand, just the model's favorite).
3. **Feature-tile grid** — icon + heading + sentence × 3, all equal weight, nothing prioritized.
4. **Accent rail** — a colored left strip on cards: decoration pretending to be organization.
5. **Unearned blur** — glassmorphism with no real depth/elevation system behind it.
6. **Monument stat** — oversized numbers filling space that should carry product story.
7. **Icon topper** — a rounded-square icon centered above every heading (Tailwind-template filler).
8. **Center stack** — everything centered because no real composition was committed to.
9. **Default type** — Inter (or system-ui) used by default rather than chosen.
10. **Wrong surface** — the composition doesn't match the surface (e.g. a hero on a Monitor surface). This is the root cause behind most of the others.

How to run it:

- Score the artifact out of 10 (10 = maximum slop). State the score and list which tells fired, in one short report.
- Treat the report as **context, not a to-do list** — it tells you *where* to spend repair effort, it does not dictate edits.
- Then repair, matched to the diagnosis:
  - tells 3, 8, 10 → **re-layout / re-compose** (revisit the surface choice — do not recolor).
  - tells 1, 2, 9 → **recolor / re-typeset** (palette and type are genuinely the problem here).
  - tells 4, 5, 6, 7 → **remove the decoration**; replace it with real hierarchy (scale, weight, spacing).
- Re-score after repairing. Do not declare done while compositional tells (3, 8, 10) are still firing — those are causes, the rest are usually symptoms.

The point of separating diagnosis from treatment: let the audit complain first, then fix only what it complained about, in the register the complaint calls for.

---

## Part 2 — Surgical Copy, Chart & Surface Cleanup (`U1–U20`)

A good interface is **used**, not read. Cut filler words and decorative chrome; keep what the user needs to act.

**Root rule:** deletion is the default. If you rewrite, state **only** what the code already proves. Never invent a metric, speed claim, integration, or benefit you cannot point to in code. If there is nothing true left to say, delete the line.

### When to Use

- The user says a UI *"feels AI-generated"*, *"looks generic"*, or asks to make it look human-designed.
- Before shipping any screen, dashboard, chart, or landing page authored by an agent.
- Whenever uppercase eyebrows, decorative `01/02/03` numbering, fake `LIVE`/`NEW`/`AI` badges, pulsing dots, decorative title emojis, glossy gradients/glows, or `font-black` appear.
- When auditing any web app, dashboard, or standalone HTML artifact prior to delivery.

### The 20 Rules (Citable as `U1–U20`)

**Copy**
- **U1 Eyebrows:** Tiny uppercase/tracked kicker above a heading (`PASSPORT`, `FEATURES`) or pill with dot (`● POLAR`). Delete — the heading already states it.
- **U2 Decorative numbering:** `01 02 03`, `§`, `//` prefixes. Delete unless sequence is genuinely ordered (checkout, step-by-step wizard).
- **U3 Echo subtitle:** Subtitle under every title. Keep only if it adds a fact the title does not (*"Analytics / Understand your data better"* → cut line 2). Same for nav menu blurbs: keep only when labels alone are ambiguous.
- **U4 Botsplaining:** Copy narrating what a visible control already does (*"Click the button below"*, *"This chart shows revenue over time"*). Delete. Do **not** delete empty states or errors — edit them to 1–2 plain sentences without *"Oops!"* or exclamation marks.
- **U5 Leaked design notes:** `(updates in real time)`, `(powered by AI)`, long parentheticals. Delete or move to a tooltip.
- **U6 Status chains:** Facts joined with `·` or `|` (*"12 items · Updated 2m · Synced · v2.1"*). Keep the actionable fact. Any live state (`Synced`) must pass the Real State Test below.
- **U7 Labeling everything:** Label duplicating the placeholder, icon, or title. One cue only: in forms, the visible `<label>` wins. Format-hint placeholders (`name@company.com`) and non-obvious constraints (`minimum 12 characters`) may stay.
- **U8 Staccato & empty slogans:** *"One. Big. Thing."*, *"Built different."* → replace with one concrete sentence naming the thing and what it does, or delete.
- **Length cap:** Section, card, and caption titles ≤ 5 words. Hero may be one sentence.

**Decoration**
- **Real State Test:** An element is legitimate only if rendered from real state/data (`{isLive && ...}`, `status === "online"`, prop, or query). Hardcoded static text is decoration.
- **U9 Badges without real state:** `LIVE`, `NEW`, `AI`, `Beta`, `Pro`, `🔥 Popular`. Keep only if backed by tracked app data.
- **U10 Status dots:** Pulsing or colored dots next to text. Keep only if tied to live state (a loading skeleton pulse is not a status dot).
- **U11 Decorative emojis & icons:** In headings, buttons, KPIs, feature lists, and tinted icon boxes atop every card. Delete. Keep only when the icon IS the control (icon button with `aria-label`), conveys meaning text lacks, or lives in an action toolbar/menu.

**Charts & Dashboards**
- **U12 Chart-type titles:** *"Bar chart of monthly revenue"* → *"Monthly revenue"*. Static reports may headline the takeaway; live dashboards keep neutral titles (takeaways go stale).
- **U13 Reading instructions:** *"Each bar represents one month"*, *"Hover for details"*. Delete.
- **U14 Double encoding:** One encoding per quantity. Bar + value label + gridline + axis tick = three too many. KPI: number + one direction cue + period (`▲ 12% vs last month`).
- **U15 Competing scaffolding:** Box around the plot, dense gridlines, minor ticks, heavy borders, 3D, shadows/glows, tinted plot backgrounds. Remove or soften to light gray hairlines. Data first, labels second, scaffolding last.
- **U16 Legend where direct labels belong:** Label series directly at line/bar ends with their latest value and drop the legend. Keep a legend only for `> 4` series or tightly colliding lines.

**Surface**
- **U17 Gradients & glows:** Hue-to-hue gradients on surfaces/buttons/active items, gradient text, colored glows, blurred blobs. Fix: solid neutral surface, neutral hairline or subtle shadow (`<= 0 1px 2px rgb(0 0 0 / .05)`). Same-hue tonal subtle fades may stay when justified.
- **U18 Off-scale spacing:** `mt-[13px]`, `gap: 7px`. Fix to scale `4/8/12/16/20/24/32/40/48/64` (inside controls: `2/6/10/14`). Siblings with the same role share the same spacing.
- **U19 Extra-heavy weights:** `font-black`, `800/900` → `500/600`. Let size and contrast carry hierarchy.
- **U20 Decorative motion:** `transition-all`, `hover:scale-*` on cards, `animate-bounce`. Fix: `transition-colors 150ms ease-out`; subtle press scale (`0.97–0.98`) only if the control already had press feedback.

### Guardrails

- Touch **only** visible copy and decoration (plus `U15` chart scaffolding and `U17–U20` surface polish). Do not alter logic, data, brand colors, spacing tokens, or layout structure.
- Always align fixes toward the project's existing tokens (Tailwind theme, CSS vars, design system), never fallback values.
- When removing an element, clean up what existed solely for it: empty wrappers, single-child wrappers, orphan margins, unused imports.
- Never remove `aria-label`, `alt`, `title` on icon buttons, or screen-reader-only text. If trimmed visible text was the sole accessible name, move it to `aria-label`.
- Inputs always keep a visible `<label>` bound via `for`/`id` or wrapping — never swap a label for a placeholder.
- Edit i18n/CMS strings at their source or report them; never hardcode over i18n keys.
- Unverifiable claims (customer counts, uptime, ratings, testimonials): never delete or fabricate — list them as open tasks.
- Never delete legitimate UI elements just to chase a zero count. A clean screen is a success.

### Procedure

1. **Scan:** Search for eyebrows, `01`, `·`, `animate-pulse`, `font-black`, gradients (`scripts/audit_ui.py`).
2. **Read:** Inspect every visible string and decorative element; tag with `U1–U20`.
3. **Verdict:** `heavy` (widespread tells) / `light` (few isolated tells) / `none` (edit nothing; note up to 2 optional refinements).
4. **Edit** surgically.
5. **Re-read diff:** Check for empty wrappers, unlabeled inputs, or unnamed icon buttons.
6. **Report:** Summary table (rule / before / after / intentionally kept) + rewrites (`old -> new`) + pending unverifiable claims.

### Pitfalls

- Confusing *"less text"* with *"prettier"*: the goal is usability, not editorial minimalism.
- Deleting a genuine live indicator (e.g., `Synced` backed by a real WebSocket state) because it looks decorative.
- Applying `U17–U20` without respecting existing `--surface` tokens, inadvertently breaking palette or layout.
- Inventing fake data to backfill a rewritten sentence.

---

## Part 3 — Static Source Pattern Audit (`DP001–DP003`)

# Static pattern audit

The `scripts/audit_ui.py` script uses only Python 3 and the standard library. It reads code and returns JSON on stdout; it does not modify the project, install dependencies, or access the network.

## Run

Resolve `SKILL_DIR` to the folder from which you read this skill. Do not assume a personal path or a directory specific to one assistant.

```sh
python3 "$SKILL_DIR/scripts/audit_ui.py" "/path/to/project" --file src/hero.tsx --file src/styles.css
```

Repeat `--file` to limit review to affected code. Without that argument, the script scans interface files in the project and excludes common dependencies and build outputs; it may report existing issues outside the change. Do not expand the work scope to remove them automatically.

## Rules and results

| Rule | Detects | Treatment |
| --- | --- | --- |
| DP001 | CSS gradient functions, SVG gradients, and common Tailwind utilities | Review the restriction and any explicit exception. |
| DP002 | Common Inter declarations and imports, web fonts, and common utilities | Review the restriction and any explicit exception. |
| DP003 | Common infinite-repeat syntax and pulse, bounce, or spin utilities | Contextual review: it may be decorative activity or a functional indicator. |

The script preserves line numbers and skips common comment syntax. It is not a complete parser: computed names, escaped CSS, variables, raster assets, and other constructions may be missed. Example strings or content can produce false positives. Inspect each finding in context.

- Exit code **0**: no unresolved patterns within scope; this does **not** mean “design approved.”
- Exit code **1**: blocked patterns or contextual reviews remain unresolved.
- Exit code **2**: input, reading, or configuration error; the audit did not complete.

The JSON always declares `scope: "static_source_patterns_only"` and `creative_verdict: "not_assessed"`. Reducing many findings to zero closes only that pattern review. It does not justify declaring that the brief, identity, or animation has been achieved.

It does not semantically detect eyebrows, generic copy, filler cards, competing CTAs, hierarchy, contrast, cropping, behavior, or motion quality. These require inspecting the render and walking through the experience.

Keep its results as source hygiene and use the separate [acceptance](09-acceptance-and-render.md) reviews for completion. Do not average the auditor's count with a visual or temporal assessment or remove an expressly requested effect solely to reduce DP003: review and record the scope of the request.

## Scoped exceptions

When appropriate, pass `--exceptions /path/to/exceptions.json`. Each entry must name the rule, relative file, and line range. This list records decisions; it does not grant permission or establish that a request is authentic. Link it to the actual request in the conversation; do not invent an exception to obtain exit code 0.

Example format for a gradient expressly requested in a specific region:

```json
[
  {
    "rule": "DP001",
    "path": "src/hero.css",
    "start_line": 12,
    "end_line": 12,
    "basis": "user-request",
    "reason": "The user enabled the gradient only in this background.",
    "user_request": "I want a gradient in the hero background."
  }
]
```

For DP003, `basis: "functional"` records a real processing indicator with a `reason` explaining what it represents, when it ends, and how it adapts to reduced motion. It does not enable gradients or Inter.

For a real false positive in an example string or other syntax outside visual use, explain the finding in the delivery. Keep the result pending if the script cannot express it; do not invent a human request or functional purpose.

Recheck ranges after editing: lines may change. The report includes unused exceptions to identify stale configuration. Keep proportionate evidence in temporary work or the existing review system.
