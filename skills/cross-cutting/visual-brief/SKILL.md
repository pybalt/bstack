---
name: visual-brief
description: "Use when replacing dense technical walls of text (grilling trade-offs, architecture debates, system/process diagrams, change reports, proposals, or UI taste comparisons) with a self-contained interactive visual HTML artifact responsive on both desktop and mobile. Do not use for production app UI (use uiux) or short answers where 5 lines of text suffice."
version: 1.0.0
author: Leonel Baltazar Bravo
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [visual-brief, diagrams, slides, decision-board, walkthrough, cognitive-load, interactive-html, responsive]
    related_skills: [grill, onboarding, evolve, systematic-debugging, uiux]
---

# Visual Brief (Cognitive-Load-Reducing Visual Artifacts)

Replace dense technical walls of text with **scannable, interactive, self-contained HTML interfaces** that work cleanly on both **desktop and mobile** — for grilling, architecture debates, change reports, engineering frameworks, and presentations.

## When to Use — and When NOT to Use

- **Use when:** explaining multi-part architectures or processes, running visual `grill` trade-offs (Pugh, 2×2, CUJ, taste comparisons), reporting complex diffs/PRs (*before vs after*), or walking through proposals/slides where prose creates high cognitive load.
- **Do NOT use for:** short explanations where 5 lines or a tiny markdown table suffice (anti-overkill), or building production application UIs (use `uiux`).

## Progressive Disclosure Protocol

Load **only** the reference(s) needed for the artifact being built:

| Need | Load ONLY this file | Inside |
| :--- | :--- | :--- |
| Pick the right visual format (Decision Board, Diagram, Walkthrough, Slides, Stepper) | `references/formats-and-modes.md` | Format selector + Process vs System rules |
| Copy density, 3-level disclosure, 2×2 desirability palette & chat-first decisions | `references/ux-and-copy-rules.md` | Anti-wall-of-text rules + artifact-to-chat workflow |
| Single-file HTML contract, desktop+mobile layout, WCAG contrast, XSS safety & QA | `references/html-contract-and-qa.md` | Standalone HTML spec + verification checklist |

**Reusable Shell & Validator (Preferred Workflow):**
1. Copy **`assets/brief-shell.html`** to the target `.html` path and edit **only** the `const BRIEF = { ... };` JSON between `// <DATA>` and `// </DATA>` (supports `flow`, `decision`, `matrix2x2`, `walkthrough`, and `slides` views out of the box).
2. Validate deterministically before delivery: `python3 scripts/validate_brief.py <output.html>` (checks doctype, viewport, light/dark WCAG contrast, zero `innerHTML`, and copy-density caps).

## Non-Negotiable Operating Laws

1. **Proportionality first (no visual bloat).** Never generate an HTML artifact when a concise chat answer communicates faster.
2. **Three levels of depth — zero upfront wall of text.**
   - *Level 1 (Map / Overview):* visual layout, labels of 1–3 words, scores or status badges at a glance.
   - *Level 2 (Card / Inspector):* one crisp sentence (≤ 14 words) explaining the selected element.
   - *Level 3 (Expandable Detail):* grouped bullet points (≤ 12 words each) revealed on demand.
3. **Desktop AND Mobile first-class.** Desktop (`>= 1000px`): wide layout, keyboard navigation, side inspector that never shifts the canvas. Mobile (`< 780px`): stacked/vertical layout, touch targets `>= 44px`, bottom sheet that never covers the active control bar.
4. **Artifact to build intuition, chat to decide (zero copy-paste friction).** Surface open questions and candidate options cleanly inside the brief so the user can inspect context and form judgment — then ask the actual decision directly in the main chat (`ask_question` / `AskUserQuestion` / chat prompt). Never force the user to fill forms in HTML and copy-paste answers back.
5. **Single standalone HTML, zero build, zero vendor lock-in.** Must include `<!doctype html>` and `<meta name="viewport" content="width=device-width,initial-scale=1">`, work offline with system font fallbacks, support light & dark themes with WCAG contrast, render untrusted strings via `textContent` (zero `innerHTML`), and never depend on proprietary IDE artifact wrappers.
6. **Verify before handing off.** Check light + dark rendering, zero overlaps/clipping on desktop and mobile viewports, zero JS errors, and working interactive controls before sharing the file path or link.
