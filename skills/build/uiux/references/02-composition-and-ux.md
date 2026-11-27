# Composition, UX States, Foundations & Optical Craft

## Design Principle: Start From Context, Not Vibes

Good high-fidelity design does not start from scratch.

Before designing, look for source context:

1. brand docs
2. existing product screenshots
3. current repo components
4. design tokens
5. UI kits
6. prior mockups
7. reference models
8. copy docs
9. constraints from legal, product, or engineering

If a repo is available, inspect actual source files before inventing UI:

- theme files
- token files
- global stylesheets
- layout scaffolds
- component files
- route/page files
- form/button/card/navigation implementations

The file tree is only the menu. Read the files that define the visual vocabulary before designing.

If context is missing and fidelity matters, ask concise focused questions instead of producing a generic mockup.

## Surface-First: Commit to a Composition Before Touching Tokens

The single highest-leverage anti-slop rule. Most AI design slop is **compositional, not cosmetic** — the model reaches for a centered hero + three equal-weight feature cards for *every* surface, then decorates. Recoloring or restyling that layout never fixes it, because the layout was wrong before a single color was chosen.

Before you write any colors, type scale, or components, **commit out loud to exactly one surface archetype.** This conditions generation on a high-level plan first, which collapses the entropy of what gets produced — the same reason a chain-of-thought step improves reasoning.

The seven surfaces:

1. **Monitor** — the user is watching state change (dashboards, status pages, observability). Density, glanceable hierarchy, no marketing framing.
2. **Operate** — the user is taking action on things (consoles, admin panels, queues, inboxes). Action affordances and selection state dominate.
3. **Compare** — the user is weighing options against each other (pricing, plans, spec tables, search results). Aligned columns, parity of structure, one differentiator emphasized.
4. **Configure** — the user is setting things up (settings, forms, wizards, onboarding). Progressive disclosure, clear save/validation states, low decoration.
5. **Decide / Learn** — the user is being convinced or taught (landing pages, docs, marketing). One idea lands per section; this is the ONLY surface where a hero is usually correct.
6. **Explore** — the user is browsing an open space (galleries, maps, search-and-filter, catalogs). Filters, result grids, and zoom/peek are the composition.
7. **Command / Inspect** — the user is driving by keyboard or drilling into one object (command bars, inspectors, detail panes, property editors). Speed and focus over breadth.

Rules:

- State the surface in one line before designing (e.g. "This is a **Monitor** surface, so density and glanceability beat a hero").
- A dashboard is a Monitor surface, not a Decide surface — do not give it a centered hero and three feature cards.
- If a screen genuinely spans two surfaces, name the **primary** one and treat the other as secondary; do not average them into mush.
- The hero-plus-three-cards composition is correct for **Decide/Learn only**. Reaching for it anywhere else is the #1 tell.

This one constraint eliminates more generic-looking UI than any aesthetic rule below.

---

# UX: from task to behavior

Read this document when designing, implementing, or auditing a flow. Match the depth to the task; a spacing adjustment does not require redesigning navigation.

## Task and hierarchy

Describe who arrives, what they need, what information they require before acting, and how they recognize the result. Choose one priority per screen or decision block. Supporting actions have less visual weight while remaining accessible.

Organize by frequency, sequence, and meaning. Use progressive disclosure when complexity can wait. Avoid hiding essential information behind exploratory interaction. Preserve recognizable terms and patterns in navigation, filtering, search, and editing.

Test a quick reading of the render: what am I looking at, what is it for, and what can I do? If the screen needs a verbal explanation, revise content and hierarchy.

## States relevant to the product

For each affected interaction, consider only states that exist:

| State | Criterion |
| --- | --- |
| Initial | Helps recognize the task and start. |
| Loading | Explains a real wait; reserves space and preserves useful context. |
| Initial empty state | Shows what is missing and how to begin. |
| No results | Preserves filters or the query and allows correction. |
| Error | Identifies the problem and offers concrete recovery. |
| Success | Confirms an outcome that happened, in the relevant location. |
| Disabled | Explains the prerequisite when it is not evident. |
| Selection or editing | Makes the affected content recognizable and shows how to finish or undo. |

Do not introduce loaders for instant operations or artificial delays to display animations. A skeleton is useful only when it represents an expected structure; a brief, accessible indicator may be better for an indeterminate wait.

In prototypes, disclose which states are simulated and which actions are not connected. A visual response does not establish persistence or real execution.

## Forms and recovery

- Use visible, associated labels; placeholders do not replace them.
- Group related fields, identify required information, and explain requirements before an error.
- Use input types, autocomplete, and inputmode suited to the data.
- Validate at a useful moment, preserve values, and place errors next to the field.
- Associate messages and fields for assistive technologies; avoid relying only on color.
- Prevent duplicate submissions during a real operation and allow retry when it fails.
- Keep the person in context when completing or correcting. Consider undo for reversible actions and proportionate protection for destructive ones.

Do not add fields the product does not need. In stepped flows, make progress recognizable and allow returning without losing data when feasible.

## Accessibility and predictability

Use semantic HTML before recreating controls. Review accessible names, tab order, keyboard activation, visible focus, and text/control contrast. Check contrast with a tool or calculation; looking at the color does not verify it.

Informative images need alternative text based on their observed content. Reserve `alt=""` for actual decoration. If an image is still missing, record that integration as pending; do not present empty alt text on a prominent photograph as resolved accessibility.

Reading and focus order must remain meaningful in every composition. Do not change visual order alone so keyboard and screen-reader users encounter a different story.

In dialogs, move focus to the appropriate context, contain it within a real modal, and restore it on close. Provide keyboard dismissal and a visible control. Prevent banners, fixed bars, or the keyboard from hiding the active element.

Important state changes must be perceivable without watching one point or interpreting an animation. Use proportionate accessible announcements when the change is not otherwise communicated.

## Content and complexity

Use concrete verbs for actions and consistent names for the same entities. Error messages should explain what happened and what can be done. Avoid spatial language such as “on the left” when the mobile composition changes.

Test long titles and names, accented characters, different quantities, large lists, empty lists, and missing content. Translation or real text should not dismantle a composition prepared only for short phrases.

Do not add search, tabs, filters, notifications, dark mode, or sections merely because they look typical of an application. Each element needs a task or requirement that justifies it.

## Completion evidence

Walk through the main task and at least its relevant recovery. Report observed states, simulated states, and what could not be executed. A screenshot establishes appearance; the walkthrough provides behavioral evidence.

---

## Typography

Use the existing type system if one exists.

If not, choose type deliberately based on the artifact:

- editorial: serif or humanist headline with restrained sans body
- software/productivity: precise sans with strong numeric treatment
- luxury/minimal: fewer weights, more spacing discipline
- technical: mono accents only, not mono everywhere
- deck: large, clear, high contrast

Avoid overused defaults when a stronger choice is appropriate.

If using web fonts, keep the number of families and weights low.

Use type as hierarchy before adding boxes, icons, or color.

## Color

Use brand/design-system colors first.

If no palette exists:

- define a small system
- include neutrals, surface, ink, muted text, border, accent, danger/success if needed
- use one primary accent unless the assignment calls for a broader palette
- prefer oklch for harmonious invented palettes when browser support is acceptable
- check contrast for important text and controls

Do not invent lots of colors from scratch.

## Layout and Composition

Design with rhythm:

- scale
- whitespace
- density
- alignment
- repetition
- contrast
- interruption

Avoid making every section the same card grid.

For product UIs, prioritize speed of comprehension over decoration.

For marketing surfaces, make one idea land per section.

For dashboards, avoid “data slop.” Only show data that helps the user decide or act.

## Images and Icons

Use real supplied imagery when available.

If an asset is missing:

- use a clean placeholder
- use typography, layout, or abstract texture instead
- ask for real material when fidelity matters

Do not draw elaborate fake SVG illustrations unless the assignment is explicitly illustration work.

Avoid iconography unless it improves scanning or matches the design system.

## Source-Code Fidelity

When recreating or extending a UI from a repo:

1. inspect the repo tree
2. identify the actual UI source files
3. read theme/token/global style/component files
4. lift exact values where appropriate
5. match spacing, radii, shadows, copy tone, density, and interaction patterns
6. only then design or modify

Do not build from memory when source files are available.

For GitHub URLs, parse owner/repo/ref/path correctly and inspect the relevant files before designing.

## Reading Documents and Assets

Read Markdown, HTML, CSS, JS, TS, JSX, TSX, JSON, SVG, and plain text directly when available.

For DOCX/PPTX/PDF, use available local extraction tools if present. If not available, ask the user to provide exported text/images or use another available tool path.

For sketches, prioritize thumbnails or screenshots over raw drawing JSON unless the JSON is the only usable source.

## Copyright and Reference Models

Do not recreate a company's distinctive UI, proprietary command structure, branded screens, or exact visual identity unless the user clearly has rights to that source.

It is acceptable to extract general design principles:

- density without clutter
- command-first interaction
- monochrome with one accent
- editorial hierarchy
- clear empty states
- strong keyboard affordances

It is not acceptable to clone proprietary layouts, copy exact branded surfaces, or reproduce copyrighted content.

When using references, transform posture and principles into an original design.

---

# UI Cheatsheet

| Problem                            | Solution                                                     |
| ---------------------------------- | ------------------------------------------------------------ |
| Old timestamps read "340 days ago" | Switch to an absolute date after a week                      |
| Numbers jitter when they change    | `font-variant-numeric: tabular-nums`                         |
| Large headings look off            | Tighter tracking like `-0.02em`                              |
| Body text looks awkward            | Cap the line at about 65 characters with `max-width: 65ch`   |
| Button feels unresponsive          | `transform: scale(0.97)` on `:active`                        |
| Avatar squished into an oval       | `flex-shrink: 0` on the avatar                               |
| Gradient fade has a visible edge   | Use an eased gradient: extra color stops along an ease curve |
| Transition still feels off         | Add `filter: blur(2px)` during the transition                |
| Dropdown feels sluggish            | `ease-out` under 300ms, never `ease-in`                      |
| Popover grows from the wrong spot  | `transform-origin` at the trigger (modals stay centered)     |
| Count reads "1 members"            | Pluralize with `Intl.PluralRules`                            |

---

# Apple Design Foundations, Optical Typography & Multimodal Craft

## The Core Idea

> "When we align the interface to the way we think and move, something magical happens — it stops feeling like a computer and starts feeling like a seamless extension of us."

An interface is fluid when it behaves like the physical world: things respond instantly, move continuously, carry momentum, resist at boundaries, and can be redirected mid-motion. Everything below is a way to get closer to that.

Apple frames design as serving four human needs: **safety/predictability, understanding, achievement, and joy.** Every rule here serves one of them.

## 13. Multimodal feedback — motion + sound + haptics

Three rules for combining senses (from *Designing Audio-Haptic Experiences*):

1. **Causality** — it must be obvious what caused the feedback. Trigger it on the actual causal event (the toggle flipping, the item snapping home), and match its character to the action's physicality.
2. **Harmony** — the visual, the sound, and the haptic must fire on the **same frame**. Latency between them destroys the illusion. Don't let a CSS transition lag the audio/haptic (Vibration API).
3. **Utility** — add feedback only where it earns its place. Reserve haptics/sound for meaningful moments (success, error, commit, snap). Over-feedback trains users to ignore all of it.

## 14. Reduced motion & accessibility

Reduced motion doesn't mean *no* feedback — it means a gentler, non-vestibular equivalent. Respond to three independent signals and bake them into your components:

- **`prefers-reduced-motion: reduce`** — replace slides/springs/parallax with short opacity **cross-fades or static transitions**. Drop elastic/overshoot. Keep opacity/color changes that aid comprehension.
- **`prefers-reduced-transparency: reduce`** — make translucent surfaces frostier/solid: raise background opacity, drop the blur.
- **`prefers-contrast: more`** — near-solid backgrounds with a defined, contrasting border.

Also: avoid full-viewport moving backgrounds, slow looping oscillations (near 0.2 Hz / one cycle per 5s), and abrupt brightness jumps (ease dark↔light theme changes). Make large moving objects semi-transparent while they travel, and fade big surfaces out during a large reposition and back in once settled.

```css
@media (prefers-reduced-motion: reduce) {
  .sheet { transition: opacity 200ms ease; transform: none !important; }
}
@media (prefers-reduced-transparency: reduce) {
  .toolbar { background: white; backdrop-filter: none; }
}
```

## 15. Typography — optical sizing, tracking, leading

Apple designs type to change shape with size; the same discipline applies on the web. (From *The Details of UI Typography*, WWDC 2020.)

- **Tracking (letter-spacing) is size-specific — never one value for all sizes.** Large display text wants *negative* tracking (letters read too far apart as they grow); small text wants slightly *positive* tracking for legibility. A fixed `letter-spacing` is wrong somewhere. Tighten headings, leave body near `0`.
- **Leading (line-height) tracks size inversely.** Tight on large headings, looser on body copy. Increase it for scripts with tall ascenders/descenders; tighten it for dense, information-heavy UI.
- **Build hierarchy from weight + size + leading as a set,** not size alone. Emphasize with weight — it adds presence without taking more space.
- **Respect the user's text-size setting** (Dynamic Type). Scale layout *with* the text — spacing in `rem`/`em`, not fixed px — so a larger font doesn't break the layout.
- **Default to the platform's system font** before a custom face; it already ships optical sizing, tracking tables, and legibility tuning. Override only with a reason.

```css
:root { font: 100%/1.5 system-ui, sans-serif; } /* body: system font, comfortable leading */

.display {
  font-size: clamp(2rem, 5vw, 4rem);
  line-height: 1.05;        /* tight leading for large text */
  letter-spacing: -0.02em;  /* negative tracking as it grows */
  font-optical-sizing: auto;
}
```

## 16. Design foundations — the eight principles

The motion and craft above serve Apple's eight design principles (*Principles of Great Design*, WWDC 2026). Use these as the names you reason with:

1. **Purpose.** Make with intention; decide what *not* to build. Every feature asks for the user's time, attention, and trust — spend that budget only where it pays off.
2. **Agency.** Keep people in control: offer choices, don't force a single path. Back it with forgiveness — easy undo for slips, a confirmation dialog only for genuinely destructive, irreversible actions (use sparingly; overusing it trains people to click through).
3. **Responsibility.** Act in the user's interest. Privacy: ask at the right moment, only for what's needed, transparently. Safety: anticipate misuse and harm — especially with AI (an allergy-aware recipe app must not suggest a harmful ingredient). Add previews, confirmations, disclaimers; cut a feature whose risk outweighs its value.
4. **Familiarity.** Build on what people already know. Use metaphors that are neither too literal nor too abstract (a trash can means delete), and honor their physics. Be consistent: things that look the same must behave the same and live in the same place (close is always top-left on macOS) so people can predict what happens next. Only break a familiar pattern if you can prove it's better — then test it, don't assume.
5. **Flexibility.** Design for different contexts, devices, and the full range of abilities. Adapt to the platform (iPhone = quick touch; desktop = deep workflows with precise pointer control) and to the situation. Design inclusively (age, language, expertise, accessibility). When no single layout fits everyone, let people personalize — rearrange controls, hide what they don't use.
6. **Simplicity — not minimalism.** Strip the unnecessary so the core purpose shines; burying everything in one place looks minimal but isn't simple. Be concise (plain language, no jargon, fewer steps) and clear (use hierarchy — order, spacing, contrast — so the most important thing is the most obvious). Every element earns its place; sometimes *adding* context simplifies (a video scrubber that shows time remaining). Show the common path first, advanced options one level deeper.
7. **Craft.** Uncompromising attention to detail builds trust. Beautiful typography, colors that adapt to light/dark, clear iconography, and responsive animations that give immediate, natural feedback. Nothing is random — every spacing, timing, and alignment value is a deliberate choice you can defend. Jittery scroll, misaligned icons, and layouts that break on rotation read as carelessness. Craft needs iteration and longevity — keep evolving the design as features and hardware change.
8. **Delight.** The result of getting the other seven right, not confetti tacked on top. Decide the emotion you want people to feel (calm, confident, excited) and reinforce it in every decision.

Tactical rules that serve these:

- **Feedback comes in four kinds:** status, completion, warning, error. Confirm meaningful actions, expose ongoing status, warn before problems, validate inline (not on submit).
- **Wayfinding.** Every screen should answer: Where am I? Where can I go? What's there? How do I get out? Never trap the user.
- **Grouping & mapping.** Proximity implies relationship; place a control near what it affects and arrange controls to mirror what they change. If you need a label to explain a control, the mapping is weak.
- **Direct, specific labels beat safe generic ones.** Name nav items for their contents ("Progress", "Library"), not vague umbrellas ("Home"). Specificity creates predictability.

## 17. Process

- **Prototype interactively — an interactive demo is worth "a million static designs."** You discover the interface by building and playing with it; a working prototype also sets a concrete bar that prevents a mediocre final implementation.
- **Design interaction and visuals together.** "You shouldn't be able to tell where one ends and the other begins." Motion is not a layer added after the pixels.
- **Test with real people in real context**, and review motion with fresh eyes — play it in slow motion / frame-by-frame to catch what's invisible at full speed.

## Quick Reference

| Need | Technique | Concrete value |
| --- | --- | --- |
| Default UI spring | Critically damped, no overshoot | `damping 1.0`, `response 0.3–0.4` |
| Momentum / flick spring | Under-damped, slight bounce | `damping ~0.8`, `response 0.3–0.4` |
| Gesture → spring velocity | Hand off release velocity | `gestureVelocity / (target − current)` if normalized |
| Flick landing point | Project momentum | `current + (v/1000)·d/(1−d)`, `d ≈ 0.998` |
| Interrupt cleanly | Start from presentation (live) value | read the on-screen transform |
| Avoid reversal "brick wall" | Carry velocity through re-target | spring that blends velocity |
| Reversible transition | Mirror the easing curve | inverse cubic-bézier |
| Decide reverse vs. commit | Use velocity **sign**, not position | at release |
| 1:1 drag | Pointer Events + capture | respect the grab offset |
| Feedback | On pointer-down, continuous | never only at the end |
| Boundary | Rubber-band, don't hard-stop | progressive resistance |
| Translucent chrome | `backdrop-filter` layer | content scrolls under |
| Type tracking | Size-specific, never fixed | tighten large text (`-0.02em`), body near `0` |
| Reduced motion | Cross-fade, not slide/spring | `@media (prefers-reduced-motion)` |
