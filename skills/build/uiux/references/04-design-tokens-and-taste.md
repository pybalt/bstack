# Design Tokens (`DESIGN.md`), Palette Extraction & Taste Capture

Starter template: `templates/design-md-starter.md`. Accent extractor script: `scripts/extract_accent_colors.py`.

## Part 1 — Google `DESIGN.md` Spec & `@google/design.md` CLI

# DESIGN.md Skill

DESIGN.md is Google's open spec (Apache-2.0, `google-labs-code/design.md`) for
describing a visual identity to coding agents. One file combines:

- **YAML front matter** — machine-readable design tokens (normative values)
- **Markdown body** — human-readable rationale, organized into canonical sections

Tokens give exact values. Prose tells agents *why* those values exist and how to
apply them. The CLI (`npx @google/design.md`) lints structure + WCAG contrast,
diffs versions for regressions, and exports to Tailwind or W3C DTCG JSON.

## When to use this skill

- User asks for a DESIGN.md file, design tokens, or a design system spec
- User wants consistent UI/brand across multiple projects or tools
- User pastes an existing DESIGN.md and asks to lint, diff, export, or extend it
- User asks to port a style guide into a format agents can consume
- User wants contrast / WCAG accessibility validation on their color palette

For purely visual brand references, use `references/16-brand-references-index.md`.
For *process and taste* when designing a one-off HTML artifact from scratch
(prototype, deck, landing page, component lab), use `references/03-prototyping-and-variants.md`.
This reference covers the *formal `DESIGN.md` token spec* itself.

## File anatomy

```md
---
version: alpha
name: Heritage
description: Architectural minimalism meets journalistic gravitas.
colors:
  primary: "#1A1C1E"
  secondary: "#6C7278"
  tertiary: "#B8422E"
  neutral: "#F7F5F2"
typography:
  h1:
    fontFamily: Public Sans
    fontSize: 3rem
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  body-md:
    fontFamily: Public Sans
    fontSize: 1rem
rounded:
  sm: 4px
  md: 8px
  lg: 16px
spacing:
  sm: 8px
  md: 16px
  lg: 24px
components:
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "#FFFFFF"
    rounded: "{rounded.sm}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.primary}"
---

## Overview

Architectural Minimalism meets Journalistic Gravitas...

## Colors

- **Primary (#1A1C1E):** Deep ink for headlines and core text.
- **Tertiary (#B8422E):** "Boston Clay" — the sole driver for interaction.

## Typography

Public Sans for everything except small all-caps labels...

## Components

`button-primary` is the only high-emphasis action on a page...
```

## Token types

| Type | Format | Example |
|------|--------|---------|
| Color | any CSS color (hex, `rgb()`, `oklch()`, named) | `"#1A1C1E"`, `"oklch(62% 0.18 250)"` |
| Dimension | number + unit (`px`, `em`, `rem`) | `48px`, `-0.02em` |
| Token reference | `{path.to.token}` | `{colors.primary}` |
| Typography | object with `fontFamily`, `fontSize`, `fontWeight`, `lineHeight`, `letterSpacing`, `fontFeature`, `fontVariation` | see above |

Component property whitelist: `backgroundColor`, `textColor`, `typography`,
`rounded`, `padding`, `size`, `height`, `width`. Variants (hover, active,
pressed) are **separate component entries** with related key names
(`button-primary-hover`), not nested.

## Canonical section order

Sections are optional, but present ones should appear in this order. The
linter flags out-of-order sections (`section-order`, warning) and duplicate
headings — consumers per the spec reject duplicates, so fix both before
returning the file.

1. Overview (alias: Brand & Style)
2. Colors
3. Typography
4. Layout (alias: Layout & Spacing)
5. Elevation & Depth (alias: Elevation)
6. Shapes
7. Components
8. Do's and Don'ts

Unknown sections are preserved, not errored. Unknown token names are accepted
if the value type is valid. Unknown component properties produce a warning.

## Workflow: authoring a new DESIGN.md

1. **Ask the user** (or infer) the brand tone, accent color, and typography
   direction. If they provided a site, image, or vibe, translate it to the
   token shape above.
2. **Write `DESIGN.md`** in their project root using `write_file`. Always
   include `name:` and `colors:`; other sections optional but encouraged.
3. **Use token references** (`{colors.primary}`) in the `components:` section
   instead of re-typing hex values. Keeps the palette single-source.
4. **Lint it** (see below). Fix any broken references or WCAG failures
   before returning.
5. **If the user has an existing project**, also write Tailwind or DTCG
   exports next to the file (`tailwind.theme.json`, `tokens.json`).

## Workflow: lint / diff / export

The CLI is `@google/design.md` (Node). Use `npx` — no global install needed.

```bash
# Validate structure + token references + WCAG contrast
npx -y @google/design.md lint DESIGN.md

# Compare two versions, fail on regression (exit 1 = regression)
npx -y @google/design.md diff DESIGN.md DESIGN-v2.md

# Export to Tailwind v3 theme JSON (`tailwind` is a back-compat alias)
npx -y @google/design.md export --format json-tailwind DESIGN.md > tailwind.theme.json

# Export to a Tailwind v4 CSS @theme block (--color-*, --text-*, --radius-*, ...)
npx -y @google/design.md export --format css-tailwind DESIGN.md > theme.css

# Export to W3C DTCG (Design Tokens Format Module) JSON
npx -y @google/design.md export --format dtcg DESIGN.md > tokens.json

# Print the spec itself — useful when injecting into an agent prompt
npx -y @google/design.md spec --rules-only --format json
```

All commands accept `-` for stdin. `lint` returns exit 1 on errors (warnings
alone exit 0). `export` exits 0 on a successful export regardless of lint
findings in the source — run `lint` separately to gate on those. Output is
JSON by default; parse it if you need to report findings structurally.

On Windows, the `design.md` bin name can collide with the `.md` file
association (silent no-op or the file opens in an editor). Use the dot-free
alias: `npx -y -p @google/design.md designmd lint DESIGN.md`.

### Lint rule reference (the 9 rules, as of CLI 0.3.0)

- `broken-ref` (error) — `{colors.missing}` points at a non-existent token
- `contrast-ratio` (warning) — component `textColor` vs `backgroundColor`
  below WCAG AA (4.5:1)
- `missing-primary` (warning) — colors defined but no `primary` token
- `missing-typography` (warning) — colors defined but no typography tokens
- `orphaned-tokens` (warning) — color tokens never referenced by a component
- `section-order` (warning) — sections out of the canonical order
- `unknown-key` (warning) — top-level YAML key that looks like a typo of a
  schema key (`colours:` → `colors:`); custom extension keys stay silent
- `token-summary`, `missing-sections` (info) — counts and absent optional
  sections

When the user cares about accessibility, call this out explicitly in your
summary — WCAG findings are the most load-bearing reason to use the CLI.

## Pitfalls

- **Don't nest component variants.** `button-primary.hover` is wrong;
  `button-primary-hover` as a sibling key is right.
- **Hex colors must be quoted strings.** YAML will otherwise choke on `#` or
  truncate values like `#1A1C1E` oddly.
- **Negative dimensions need quotes too.** `letterSpacing: -0.02em` parses as
  a YAML flow — write `letterSpacing: "-0.02em"`.
- **Section order matters even though the linter only warns.** If the user
  gives you prose in a random order, reorder it to match the canonical list
  before saving — spec-compliant consumers expect it.
- **Typography sub-property typos are silently dropped.** As of CLI 0.3.0 a
  typo like `fontwight:` produces no finding and the value vanishes from
  exports — double-check sub-property names against the schema
  (`fontFamily`, `fontSize`, `fontWeight`, `lineHeight`, `letterSpacing`,
  `fontFeature`, `fontVariation`).
- **`version: alpha` is the current spec version** (as of Jul 2026, CLI
  0.3.0). The spec is marked alpha — watch for breaking changes.
- **Token references resolve by dotted path.** `{colors.primary}` works;
  `{primary}` does not.

## CLI Tooling

- CLI: `npx @google/design.md` (lints structure + WCAG contrast, diffs versions, exports to Tailwind or W3C DTCG JSON).

---

## Part 2 — Measuring Color & Provenance From Visual References

Goal: every hex value in `DESIGN.md` has measured provenance — never guess *"sky blue"* from memory.

### 1. Surfaces: Area-Based Quantization

Run median-cut area quantization on the reference image to extract dominant surface families (paper, canvas, background, wood, dark chrome).

### 2. Accents: Chroma-Filtered Histogram

Real limitation: on a light/document UI, neutral background occupies 70–90% of pixels, so median-cut returns five shades of gray while deliberate accents (ink, highlight, badges) never enter the top-N. Filter by saturation and value first using `scripts/extract_accent_colors.py`:

```bash
python3 scripts/extract_accent_colors.py path/to/reference.png --min-sat 0.18 --min-val 0.30 --top 14
```

Read results by **hue**, not raw pixel percentage: e.g., ~225° blue-gray for ink, ~60° high-sat for highlighter, ~150° for status tags, ~30° for warm accents. An accent occupying only 0.5% of total area is still a real token when it is *recurrent* and *deliberate*.

### 3. Contrast Pairs

Before writing `DESIGN.md`, check every planned text/surface pair against WCAG ratios (`>= 4.5:1` normal text, `>= 3:1` large text & UI graphics) and interpret findings directly in the spec:

- A failing pair can be valid when the color is a **background fill** (e.g. a ~1.4:1 highlight) or **decoration** (~1.7:1 border): document what foreground color must sit on top of it rather than discarding the swatch.
- A failing pair used for **real body text** (e.g. mid-gray on black) becomes an explicit **Don't** rule.
- A pair passing **AA Large Only** (3.0–4.49:1) is restricted to large headings or thick UI elements: state that explicitly.

### 4. Confidence Markers in `DESIGN.md`

- ✅ **High** — measured programmatically from the reference image (hex, area, WCAG ratio).
- ⚠️ **Medium** — grounded visual inference (font family identified visually, spacing estimated from render).
- ❓ **Low** — element absent from reference material (interactive states, focus rings, mobile layout).

List every ❓ item under **Open Questions** noting what source material would close it. Presenting ❓ guesses as measured facts is worse than an honest incomplete spec.

---

## Part 3 — `/learn-taste` Session Rule Extraction (EXPLICIT INVOCATION ONLY)

> Gate: Only run Part 3 when explicitly invoked by the user (`/learn-taste` or asking to save design taste/rules from this session). Never edit component code under this mode.

# Learning Taste

Every correction a user makes is taste the agent didn't have. If it isn't written down, the next session makes the same mistake and the user corrects it again. This skill finds those corrections, turns each one into a rule with its reason, and writes it where the next agent will read it.

It does ONE thing: write rules. It never changes component code, and it never adds a rule the user didn't express.

## Hard Rules

1. **Only the user's taste.** Every rule traces back to something the user said, edited, or confirmed. Never add a rule because it seems like good practice. That's your taste, and your taste is what the user was correcting.
2. **Never invent a why.** If the user gave no reason, propose one marked *inferred* and get it confirmed before writing. A wrong why is worse than none: the next agent extends the reasoning to cases it doesn't fit.
3. **Propose, then stop.** Present every candidate and write only what the user approves. A wrong rule repeats in every future session, exactly like the mistake would have.
4. **A check beats a sentence.** If a violation can be found by matching code (a banned value, a raw hex instead of a token, a forbidden property), propose a lint rule, a token restriction, or a test. A check runs every time. A sentence in a long file gets skipped when the agent's context is full.
5. **Write for an agent that wasn't here.** No "like we discussed" or "the card from earlier". Name the class of component, the value, the token, the file.

## Workflow

### Phase 1: Collect corrections

Read the current conversation from the first turn. If the user names earlier sessions and you can read their transcripts (Claude Code stores them as JSONL under `~/.claude/projects/<project>/`), read those too.

Explicit corrections are the minority. Look for all five signals:

| Signal | Example | What it tells you |
| --- | --- | --- |
| Explicit correction | "No, semi-transparent shadow, not a border" | The rule, often with the why |
| Silent edit | User changed `duration: 400` to `200` in a file you wrote | Your default was wrong and their value is the rule. Find these through notices that a file changed outside your edits, or by diffing a file against what you last wrote |
| Repeated nudge | "Smaller." → "Still too big." → "Ok" | Your default was off by the total distance. Record where they landed, not the steps |
| Revert or rejection | "Undo that", picking variant B over A, deleting something you added | What not to do. The why is usually missing, so it goes to Phase 3's questions |
| Confirmed non-obvious choice | "Yes, keep the icon outside the button" | A choice a fresh agent might not repeat. Record it only if a fresh agent would plausibly do otherwise |

For each one, capture the user's exact words (or the diff), what you had done, what they wanted instead, and any reason they gave.

Skip what isn't taste: functional bugs, content specific to one screen ("the headline should say Pricing"), and corrections to your understanding of the task.

**Completion criterion:** every turn has been read, and every correction is listed with its source quote or diff.

### Phase 2: Filter

Walk every correction through this tree:

```
Would a fresh agent building a DIFFERENT component in this repo make the same mistake?
├── No (a one-off: this campaign's color, this page's layout) → Skipped
└── Yes
    ├── Does an existing rule cover it? Check DESIGN.md, CLAUDE.md / AGENTS.md, project skills.
    │   ├── Yes, and it says the same thing → The rule failed. Rewrite it stricter
    │   │   (a number, a token, "never") instead of adding a duplicate.
    │   ├── Yes, and it contradicts → Conflict. Show both; the user picks.
    │   └── No → continue
    ├── Can a violation be found by matching code? → Check candidate.
    │   Keep a one-line rule too, so the why is recorded somewhere.
    └── Did the user say it applies everywhere, not just here? → Ask where their global rules live.
        Otherwise it's a project rule.
```

### Phase 3: Generalize and find the why

Pick the narrowest level that would have prevented the mistake on the next, different component:

| Level | Example | Verdict |
| --- | --- | --- |
| Instance | "The pricing card gets a shadow, not a border" | Too narrow: it only protects this card |
| Class | "Raised surfaces (cards, popovers, menus) separate from the background with `shadow-raised`, never a solid border" | Write this |
| Universal | "Never use borders" | Too broad: breaks inputs, dividers, tables |

If the same correction came up on two or more different components, that's evidence for the class level. If two levels both seem right, ask.

Write the rule strictly: values and token names from this codebase, "always" or "never", no "prefer" or "try to". Use softer wording only when the user framed it as a preference.

Then the why. Use the user's reason, in their words, when they gave one. Otherwise write your best candidate, mark it *inferred*, and put it in the questions for the user.

**Self-test before proposing:** read only the rule and its why, then picture the original task. Would an agent that knows nothing else produce what the user wanted? If it could still produce the wrong version, the rule is too vague. Add the value, the token, or the exception.

### Phase 4: Decide where it goes

```
Check candidate?
├── Yes → lint rule, token restriction, or test, plus a one-line rule in DESIGN.md
└── No
    ├── Is DESIGN.md's section for this aspect over ~40 lines, AND relevant to only some tasks
    │   (motion rules don't matter when building a settings form)?
    │   └── Yes → move the whole section into a project skill and leave a one-line pointer in DESIGN.md
    └── Default → DESIGN.md at the repo root, under the matching section:
        Surfaces · Color · Typography · Spacing & layout · Motion · Interaction · Copy
```

Create DESIGN.md or the section if it's missing.

**Make sure it gets read.** A DESIGN.md that no agent loads changes nothing. If neither CLAUDE.md nor AGENTS.md points to it, propose adding this line to whichever one the project uses: `Before building or changing UI, read DESIGN.md.`

Entry format:

```md
## Surfaces

- **Raised surfaces (cards, popovers, menus) use `shadow-raised`, never a solid border.**
  Why: a solid border makes a raised surface look flat and heavy; a semi-transparent shadow separates it from the background and adapts to both themes.
  <!-- 2026-11-12: "no, semi-transparent shadow, not a border" -->
```

The comment holds the date and the user's words. When a later correction conflicts, it shows which rule is newer and what the user actually said.

### Phase 5: Report and stop

Present the report below, then stop.

### Phase 6: Write on approval

Write only the approved items. Show the resulting diff of DESIGN.md (and any skill or config file). For a check, implement it and run it across the codebase. If it flags existing code, report the count and ask whether to make it a warning or fix the violations. Never fix them without asking, because that changes component code.

## Required Output Format

### Rules to add

| # | You said | Rule | Why | Where |
| --- | --- | --- | --- | --- |
| 1 | "no, semi-transparent shadow, not a border" | Raised surfaces use `shadow-raised`, never a solid border | Solid borders look flat and heavy; shadows adapt to both themes | DESIGN.md › Surfaces |
| 2 | Changed `duration: 400` → `200` in `Dropdown.tsx` | Dropdowns and popovers open in 150–200ms | *inferred:* 400ms felt sluggish on a surface opened many times a day | DESIGN.md › Motion |

### Needs your answer

Each *inferred* why, each ambiguous generalization level, and each global-or-project question. One line each, with your recommendation.

### Conflicts

The existing rule, the new correction, and which one you'd keep.

### Make it a check

Each check candidate with its exact implementation (the rule config or test), and what it would flag in the current codebase.

### Skipped

One line per skipped correction and why, so the user can override.

Close with: "Say `write all` or `write 1, 3`, and answer the questions above."

If the session had no taste corrections, say so in one line. That's a good result, not a failure.

## Invocation Variants

| Invocation | Behavior |
| --- | --- |
| `/learn-taste` | Current session, full workflow, stop at the report |
| `/learn-taste <sessions>` | Also read the named or most recent N session transcripts |
| `write all` / `write 1, 3` | Write the approved items from the last report |
| `/learn-taste prune` | Read DESIGN.md and propose merges for duplicates, fixes for contradictions, and stricter wording for vague rules. Same propose-then-stop rule |
