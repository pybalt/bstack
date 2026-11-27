# Web Animation Implementation, Recipes, Gestures & Frame-Budget Performance

## Part 1 — Web Animation Build Sequence (`animate`)

# Building Animations

## Operating Posture

You are a senior design engineer building the animation yourself. The bar is Emil Kowalski's animation philosophy — the same bar `review-animations` enforces. Write it so it passes that review the first time.

Two failure modes, and the first is worse:

1. **Animating something that shouldn't animate.** The gate below exists to produce zero lines of code sometimes. That's a success, not a dodge.
2. **Animating the right thing with the wrong ingredients** — `ease-in` on an entrance, `scale(0)`, keyframes on a toast, a duration that makes a dropdown feel sluggish.

Never present motion options as a menu. Make the call, state the reasoning in one line, write the code.

## Hard Rules

1. **Run the sequence in order.** Steps 1 and 2 gate everything. Don't reach for a curve before you know whether it animates at all.
2. **No approximated values.** Every curve, duration, and spring config comes from the tables below. Never invent `cubic-bezier(0.4, 0, 0.2, 1)` because it looks familiar.
3. **Extend the codebase's tokens, don't fork them.** If `--ease-out` or a duration scale already exists, use it. Adding a parallel system is a defect.
4. **Reduced motion and hover gating ship with the animation**, not as a follow-up.
5. **Cheapest tool that works.** Don't install a motion library for a fade.

## The Build Sequence

### 1. Should this animate at all?

| Frequency | Decision |
| --- | --- |
| 100+ times/day (keyboard shortcuts, command palette toggle) | **No animation. Ever.** Stop here. |
| Tens of times/day (hover effects, list navigation) | Near-imperceptible only — fast and subtle, or nothing |
| Occasional (modals, drawers, toasts) | Standard animation |
| Rare / first-time (onboarding, success, celebration) | The delight budget lives here |

**Keyboard-initiated actions are a disqualifier, not a judgment call.** Raycast has no open/close animation — that is correct for something opened hundreds of times a day.

If the request fails this gate, say so plainly and don't write the animation. Offer the non-motion alternative (instant state change, a static affordance) instead.

### 2. What is the purpose?

Name it in one of these words before continuing:

- **Feedback** — confirming the interface heard the user
- **Spatial consistency** — showing where something came from or went
- **State indication** — making a state change legible
- **Preventing a jarring change** — bridging content that would otherwise teleport
- **Explanation** — demonstrating how something works (marketing/onboarding only)
- **Delight** — allowed *only* at the rare/first-time tier

Can't name it? Don't build it. "It looks cool" on a frequently-seen element is a reason to stop.

Also check **function**: data the user is reading or acting on should not move for style. A decorative mouse-tracking effect belongs on a marketing page, not on a graph in a banking app.

### 3. Pick the tool — cheapest that works

Walk down; stop at the first that fits.

| Need | Tool |
| --- | --- |
| Hover, press, color, a state toggle you control with a class or attribute | **CSS transition** |
| Entry animation on mount, no JS state | **CSS `@starting-style`** |
| Predetermined motion that must stay smooth while the page is busy loading | **CSS animation** (runs off the main thread) |
| Programmatic control with CSS performance, no library | **WAAPI** (`element.animate()`) |
| Springs, layout animations, exit animations, gesture-driven values | **Motion** (`motion.dev`) |

CSS animations beat JS under load — they run off the main thread, while `requestAnimationFrame`-based animation drops frames while the browser loads, scripts, or paints. Use CSS for predetermined motion, JS for dynamic and interruptible motion.

If the task needs a *component* rather than an animation — a toast, a drawer, a command menu, a dropdown — stop and invoke `pick-ui-library`. Hand-rolling those is how you end up with a `<div>` dropdown and no focus management.

### 4. Pick the properties

- **`transform` and `opacity` only.** They skip layout and paint and run on the GPU. `width`/`height`/`margin`/`padding`/`top`/`left` trigger all three. (`clip-path` is the sanctioned fourth — see Part 2 (Web Recipes) below. `height` is tolerated only for accordions, where there's no transform equivalent.)
- **Never `scale(0)`.** Start from `scale(0.9–0.97)` + `opacity: 0`. Nothing in the real world appears from nothing.
- **`transform-origin` at the trigger** for popovers, dropdowns, menus, tooltips — `var(--transform-origin)` in Base UI. **Modals are exempt**; they're not anchored to a trigger, so they stay centered.
- **Percentages in `translate()`** are relative to the element's own size — `translateY(100%)` moves by its own height whatever the content. Prefer over hardcoded pixels.
- **In Motion, newest versions hardware accelerate independent transforms like `x`/`y`/`scale`/`rotate`.**

```jsx
<motion.div animate={{ x: 100 }} />                          // motion 14.2+: hardware accelerated
<motion.div animate={{ transform: "translateX(100px)" }} />  // hardware accelerated in every version
```

- **Never drive a child's transform from a CSS variable on the parent** — it recalculates styles for every child. Set `transform` on the element directly.

### 5. Easing and duration — or a spring

**Easing**, in decision order:

| Situation | Easing |
| --- | --- |
| Entering or exiting | `ease-out` |
| Moving / morphing on screen | `ease-in-out` |
| Hover / color change | `ease` |
| Constant motion (marquee, progress) | `linear` |
| Default | `ease-out` |

**Never `ease-in` on UI.** It starts slow, delaying the exact moment the user is watching. `ease-out` at 200ms *feels* faster than `ease-in` at 200ms.

Built-in CSS easings are too weak. Use these:

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);        /* strong ease-out for UI */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);    /* strong ease-in-out for on-screen movement */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);     /* iOS-like drawer curve (Ionic) */
```

Need a curve that isn't here? Take it from [easing.dev](https://easing.dev/) or [easings.co](https://easings.co/). Don't hand-roll one.

**Duration:**

| Element | Duration |
| --- | --- |
| Button press feedback | 100–160ms |
| Tooltips, small popovers | 125–200ms |
| Dropdowns, selects | 150–250ms |
| Modals, drawers | 200–500ms |
| Marketing / explanatory | Can be longer |

**UI animations stay under 300ms.** A 180ms dropdown feels more responsive than a 400ms one.

**Reach for a spring instead** when the motion is drag with momentum, an element that should feel alive, a gesture the user can interrupt or reverse, or decorative mouse-tracking:

```js
{ type: "spring", duration: 0.5, bounce: 0.2 }        // Apple-style — easier to reason about
{ type: "spring", mass: 1, stiffness: 100, damping: 10 }  // traditional physics — more control
```

Keep bounce at 0.1–0.3, and avoid bounce in most UI — reserve it for drag-to-dismiss and playful interactions.

### 6. Interruption and exit

- **Transitions, not keyframes, for anything triggered rapidly** — toasts, toggles, anything a user can fire twice in a second. Transitions retarget from the current value; keyframes restart from zero.
- **Springs for gestures**, because they carry velocity through an interruption.
- **Exit the way it entered.** A toast that slides in from the bottom leaves through the bottom. Symmetric paths are what make swipe-to-dismiss feel obvious.
- **Asymmetric timing where the user is deciding.** Slow on the deliberate phase (a hold-to-confirm press: 2s linear), snappy on the system response (release: 200ms ease-out).

### 7. Reduced motion and pointer gating

Ships with the animation, every time.

```css
@media (prefers-reduced-motion: reduce) {
  .element { animation: fade 0.2s ease; } /* keep opacity/color, drop transform-based motion */
}

@media (hover: hover) and (pointer: fine) {
  .element:hover { transform: scale(1.05); } /* touch fires false hovers on tap */
}
```

```jsx
const reduce = useReducedMotion();
const closedX = reduce ? 0 : '-100%';
```

Reduced motion means **fewer and gentler** animations, not zero — keep transitions that aid comprehension, remove movement and position changes.

## Recipes

For ready-to-build implementations of the common cases — button press, dropdown, tooltip, modal, drawer, toast, accordion, stagger, hold-to-confirm, tab indicator, scroll reveal, drag-to-dismiss — see [Part 2 (Web Recipes) below](Part 2 (Web Recipes) below). Load it whenever the request matches one of those components; start from the recipe rather than from a blank file.

## Never Ship

Self-check before you finish. Each of these is an automatic block in `review-animations`:

| Never | Instead |
| --- | --- |
| `transition: all` | Name the exact properties |
| `transform: scale(0)` entrance | `scale(0.95)` + `opacity: 0` |
| `ease-in` on a UI element | `ease-out` or a strong custom curve |
| Built-in `ease-out` on a deliberate animation | `cubic-bezier(0.23, 1, 0.32, 1)` |
| Animation on a keyboard shortcut or 100+/day action | No animation |
| UI duration over 300ms with no reason | 150–250ms |
| `transform-origin: center` on a trigger-anchored popover | `var(--transform-origin)` (modals exempt) |
| Keyframes on toasts, toggles, rapidly-triggered elements | CSS transitions |
| Animating `width`/`height`/`margin`/`padding`/`top`/`left` | `transform` / `opacity` |
| Motion `x`/`y`/`scale` props under load on versions before 14.2 | Upgrade to 14.2+, or a full `transform` string |
| Ungated `:hover` motion | `@media (hover: hover) and (pointer: fine)` |
| Missing `prefers-reduced-motion` | Gentler variant, not zero |
| Everything entering at once | 30–80ms stagger |

## Output

Write the code. Then, in at most a few lines:

- **The gate result** — frequency tier and the named purpose. If something in the request was rejected, say which and why.
- **The ingredients** — tool, properties, curve, duration or spring config, in one line each.
- **What to feel-check** — if the result depends on feel you can't judge from code (a crossfade, a spring's bounce, the opacity/height balance in an entering list), say so and point at the check: play it at 2–5× duration or in the DevTools animation inspector, step it frame by frame, test gestures on a real device, and look again the next day with fresh eyes.

Don't pad this into a report. The code is the deliverable.

## Tone

Opinionated and brief. When the honest answer is "this shouldn't animate," give it — that answer is the reason this skill exists. When feel genuinely can't be settled from code, say so instead of guessing at a value.

---

## Part 2 — 14 Web Animation Recipes

# Animation Recipes

Ready-to-build implementations for the cases that come up most. Start from the recipe, then adapt — don't rebuild from scratch.

Curves are the `--ease-out`, `--ease-in-out`, and `--ease-drawer` tokens defined in SKILL.md.

---

## Button press

Any pressable element. Instant feedback that the interface heard the user.

```css
.button {
  transition: transform 160ms var(--ease-out);
}

.button:active {
  transform: scale(0.97);
}
```

`scale()` scales children too — the label and icons come along, which is what makes it read as a physical press.

No hover gating needed here: `:active` is a real press on touch. Gate any `:hover` styling separately.

---

## Dropdown, popover, menu, select

Scales out of its trigger, not out of thin air.

```css
.popover {
  transform-origin: var(--transform-origin); /* Base UI supplies this */
  transition:
    opacity 200ms var(--ease-out),
    transform 200ms var(--ease-out);
}

.popover[data-starting-style],
.popover[data-ending-style] {
  opacity: 0;
  transform: scale(0.95);
}
```

The `transform-origin` is the whole point — the panel should look like it came out of the thing you clicked.

---

## Tooltip

Same shape as a popover, faster, plus the detail most implementations miss.

```css
.tooltip {
  transform-origin: var(--transform-origin);
  transition:
    transform 125ms var(--ease-out),
    opacity 125ms var(--ease-out);
}

.tooltip[data-starting-style],
.tooltip[data-ending-style] {
  opacity: 0;
  transform: scale(0.97);
}

/* Once one tooltip is open, neighbours open instantly */
.tooltip[data-instant] {
  transition-duration: 0ms;
}
```

The initial delay prevents accidental activation. After that, skipping both the delay and the animation makes the whole toolbar feel faster.

---

## Modal

The one popover that stays centered.

```css
.modal {
  transform-origin: center; /* exempt — not anchored to a trigger */
  transition:
    opacity 250ms var(--ease-out),
    transform 250ms var(--ease-out);
}

.modal[data-starting-style],
.modal[data-ending-style] {
  opacity: 0;
  transform: scale(0.96);
}

.backdrop {
  transition: opacity 250ms var(--ease-out);
}
```

Animate the backdrop's opacity alongside it so they read as one surface.

---

## Drawer / sheet

```css
.drawer {
  transform: translateY(0);
  transition: transform 500ms var(--ease-drawer);
}

.drawer[data-closed] {
  transform: translateY(100%);
}
```

This is how Vaul hides a drawer before animating it in.

Add drag and it becomes a gesture problem — see **Drag to dismiss** below.

---

## Toast

```css
.toast {
  opacity: 1;
  transform: translateY(0);
  transition:
    opacity 400ms ease,
    transform 400ms ease;

  @starting-style {
    opacity: 0;
    transform: translateY(100%);
  }
}
```

- `ease` rather than `ease-out`, slightly slower than typical UI: Sonner reads as elegant partly because its motion is tuned to the component's personality rather than to the generic UI budget.
- If `@starting-style` isn't available, fall back to the mount flag:

```jsx
useEffect(() => { setMounted(true); }, []);
// <div data-mounted={mounted}>
```

When toasts stack and the list reflows, the opacity change has to work against the height change. There's no formula for that pair — adjust until it feels right, then check it again the next day.

---

## Accordion / collapse

```css
.content {
  overflow: hidden;
  transition:
    height 200ms var(--ease-out),
    opacity 200ms var(--ease-out);
}
```

Keep it short — this is one of the few animations that costs layout on every frame, so a long duration is expensive as well as sluggish. Measure the content height in JS (or use a headless primitive that supplies it) rather than animating to `auto`.

---

## Stagger a group entrance

For a list or grid the user sees occasionally — not for a list they scroll past all day.

```css
.item {
  opacity: 0;
  transform: translateY(8px);
  animation: fadeIn 300ms var(--ease-out) forwards;
}

.item:nth-child(2) { animation-delay: 50ms; }
.item:nth-child(3) { animation-delay: 100ms; }
.item:nth-child(4) { animation-delay: 150ms; }

@keyframes fadeIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

Stagger is decorative — it must never block interaction while it plays.

---

## Hold to confirm

For destructive actions where a plain click is too easy to fire by accident.

```css
.overlay {
  clip-path: inset(0 100% 0 0);
  transition: clip-path 200ms var(--ease-out); /* release: snappy */
}

.button:active .overlay {
  clip-path: inset(0 0 0 0);
  transition: clip-path 2s linear;             /* press: slow and deliberate */
}

.button:active {
  transform: scale(0.97);
}
```

`linear` is correct here — the fill is a progress indicator, and progress shouldn't ease.

---

## Tab indicator with a color transition

Timing individual color transitions across a tab list never quite lands. Clip instead.

Duplicate the tab list. Style the copy as the active state — different background, different text color. Clip the copy so only the active tab shows, and animate the clip on change:

```css
.tabs-active-copy {
  clip-path: inset(0 60% 0 20%); /* driven by the active tab's position */
  transition: clip-path 250ms var(--ease-in-out);
}
```

The text and background change together, in perfect sync, because they're one element being revealed rather than two colors being interpolated.

---

## Scroll reveal

Marketing surfaces only. Don't do this to functional UI a user visits daily.

```css
.reveal {
  clip-path: inset(0 0 100% 0);
  transition: clip-path 600ms var(--ease-in-out);
}

.reveal[data-visible] {
  clip-path: inset(0 0 0 0);
}
```

Trigger with `IntersectionObserver`, or Motion's `useInView` with `{ once: true, margin: "-100px" }`. Fire it once — re-animating on every scroll-by is an interface fighting its reader.

---

## Drag to dismiss

The gesture recipe. Springs, not durations, because the user can reverse mid-motion.

```js
// Dismiss on a flick, not just on distance
const timeTaken = Date.now() - dragStartTime.current;
const velocity = Math.abs(swipeAmount) / timeTaken;

if (Math.abs(swipeAmount) >= SWIPE_THRESHOLD || velocity > 0.11) {
  dismiss();
}
```

```js
// Set transform on the dragged element directly.
// Driving it through a CSS variable on the parent recalcs styles for every child.
element.style.transform = `translateY(${distance}px)`;
```

Four details that separate a good drag from a bad one:

- **Pointer capture** once the drag starts, so it continues when the pointer leaves the element's bounds.
- **Multi-touch protection** — `if (isDragging) return` on new touch points, or switching fingers mid-drag makes the element jump.
- **Damping past boundaries** — dragging beyond a natural edge moves the element less the further it goes. Real things slow before they stop.
- **Friction, not a wall** — allow the over-drag with rising resistance rather than refusing it.

Settle with a spring so an interrupted drag keeps its velocity:

```js
{ type: "spring", duration: 0.5, bounce: 0.2 }
```

---

## Masking a crossfade that won't settle

When two states overlap visibly during a transition and no amount of easing or duration tuning fixes it, blur the seam:

```css
.content {
  transition:
    filter 200ms ease,
    opacity 200ms ease;
}

.content.transitioning {
  filter: blur(2px);
  opacity: 0.7;
}
```

Without blur the eye reads two distinct objects swapping. Blur blends them into one perceived transformation. Keep it under 20px — heavy blur is expensive, especially in Safari.

---

## Programmatic, without a library

When the motion needs JS control but not a dependency, WAAPI gives you CSS-grade performance:

```js
element.animate(
  [{ clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0 0)' }],
  { duration: 1000, fill: 'forwards', easing: 'cubic-bezier(0.77, 0, 0.175, 1)' }
);
```

Hardware-accelerated, interruptible, no bundle cost.

---

## Part 3 — Direct Manipulation, Vaul & Touch Gestures (`gestures`)

# Gesture-Driven UI

How to build gestures that feel physical. A gesture is direct manipulation: while the finger is down, the UI is the finger; the moment it lifts, physics takes over. Every rule below follows from that split.

## First decision: build it, or use a solution that exists?

Doing a drawer gesture *right* means momentum-based dragging, overlay opacity matched to drag progress, velocity-aware dismissal, focus trapping, and Escape-to-close. That is weeks of edge cases, not an afternoon. **For a bottom sheet / drawer, default to [Vaul](https://vaul.emilkowal.ski/)** — it exists precisely because this is hard to hand-roll. Build the gesture yourself only when no library covers the interaction (custom swipe cards, bespoke drag interactions). Use the `pick-ui-library` skill when unsure.

## The two phases of every gesture

Walk this split for any gesture you build. Mixing the phases up is the #1 cause of gestures that feel wrong.

```
Is the pointer currently down?
├── Yes → TRACK phase: position maps 1:1 to the pointer.
│         No easing. No duration. No spring. The element IS the finger.
└── No  → RELEASE phase: physics finishes the motion.
          A spring seeded with the release velocity. Never a keyframe.
```

### Track phase rules

- **1:1 means 1:1.** Drive position from a `useMotionValue` (or direct `transform` writes), never a spring or a transition — a spring during tracking makes the element trail the finger and feel disconnected, like dragging something through syrup.
- **Write `transform` directly on the dragged element.** Never update a CSS variable on a parent to move children: CSS variables are inheritable, so every change recalculates styles for all descendants. This exact bug made Vaul's drag laggy past ~20 list items; setting `transform` on the element fixed it.
- **No React state per move event.** A re-render every pointermove drops frames. Motion values and direct style writes bypass the render cycle.
- **Rubber-band at the edges.** Dragging past a boundary should move the element a fraction of the distance (Motion: `dragElastic` ≈ 0.2), not stop dead — hard stops feel like hitting a wall; resistance communicates "there's nothing further" physically.

### Release phase rules

- **Finish with a spring, seeded with the gesture's velocity.** The element should leave the finger at the speed it was moving. A fixed-duration ease here makes every fling land identically, which reads as fake.
- **Dismiss on distance OR velocity.** Passing a distance threshold (~40–50% of travel) dismisses, but so does a fast flick over a short distance. In Motion, read both from `onDragEnd`'s `info.offset` and `info.velocity`. Distance-only thresholds make flicks feel ignored.
- **Bounce belongs only at the end of a drag.** A drag applies force — like throwing a ball at a wall — so a slight bounce on release feels physical. The same element closed by a button press gets **zero** bounce: no force was applied. Keep the value small, and remember bounce scales inversely with element size (smaller elements need more bounce to read the same).
- **Snap-back is fast.** If the gesture doesn't pass the threshold, return quickly with the spring — a slow snap-back feels like the UI is disagreeing with the user in slow motion.

## Interruptibility is non-negotiable

The user must be able to catch a sheet mid-close and drag it back. Springs allow this: when retargeted mid-flight they keep their current velocity, so the redirect is seamless. CSS `@keyframes` restart from zero and cannot be caught — this is why Sonner's early CSS enter animation made toasts jump when a second toast arrived. **Never use a keyframe animation on anything a gesture can touch.** CSS transitions and springs only.

## Linked values

The dragged element is rarely alone — an overlay fades, the page behind scales. Derive these from drag progress, don't animate them separately:

```jsx
const y = useMotionValue(0);
const overlayOpacity = useTransform(y, [0, drawerHeight], [1, 0]);
```

One source of truth means the overlay is always exactly as faded as the drawer is dismissed — including mid-gesture, including when the user reverses. Two separate animations drift apart the moment a gesture is interrupted.

## Motion drag props

```jsx
<motion.div
  drag="y"
  dragConstraints={{ top: 0 }}
  dragElastic={0.2}
  onDragEnd={(e, info) => {
    if (info.offset.y > threshold || info.velocity.y > 500) dismiss();
  }}
/>
```

`dragMomentum` is on by default — right for a flung card, wrong for a simple reposition; disable it when the element should stop where the finger stops. `dragConstraints` takes a ref or bounds object.

## Sheets without springs: the Vaul curve

Vaul mimics the iOS sheet with pure CSS to stay small: `cubic-bezier(0.32, 0.72, 0, 1)` over **500ms**. The curve is extremely steep at the start — that's what lets a 500ms duration still feel snappy while landing with a spring-like gentle settle. Two rules from it:

- A **small floating drawer** (not touching the screen edge) should override to ~200ms — the 500ms iOS timing only reads right on a full-width edge-attached sheet:
  ```css
  [vaul-drawer]  { transition: transform 0.2s cubic-bezier(0.165, 0.84, 0.44, 1); }
  [vaul-overlay] { transition: opacity  0.2s cubic-bezier(0.165, 0.84, 0.44, 1); }
  ```
- **The component must feel like a single entity.** If the drawer opens in 200ms, its height changes and content crossfades must live in the same timing family — one slow sub-animation makes the whole thing feel broken.

Mark interactive children with `data-vaul-no-drag` so pressing a button inside the drawer doesn't start a drag.

## Spatial consistency

**An element dismisses in the direction it entered.** Sonner's toast slides up from the bottom, so swipe-down dismisses it — enter and exit share one axis, which is what makes the gesture feel discoverable and intuitive without instruction. A gesture that dismisses along an axis the element never moved on has to be learned; one that reverses the entrance is *felt*.

## Hold gestures are asymmetric

Hold-to-delete and similar press-and-hold interactions use **`linear`** during the hold — the animation visualizes time passing, and time passes linearly; any other curve lies about how long is left. On release before completion, snap back fast with `ease-out`. The deliberate phase is slow and honest; the cancel is instant. Symmetric timing here is a bug.

## Touch checklist

Run through this for every gesture you ship:

- **Test on a real phone** — hit the dev server by local IP. Trackpad simulation lies about touch, and a 60Hz desktop monitor hides opacity-transition roughness that a 120Hz phone shows.
- **Hit targets ≥ 44×44px.** Enlarge small visual targets with an invisible `::before` hitbox instead of growing the layout.
- **`touch-action`** on the drag axis (`touch-action: pan-x` for a vertical drag, etc.) so the browser doesn't fight the gesture with native scrolling.
- **Gate hover effects** behind `@media (hover: hover) and (pointer: fine)` — touch fires phantom hovers on tap.

## Reduced motion

Tracking is direct manipulation — the user is producing the motion — so it stays. What reduces: momentum flings, bounce, and any decorative motion around the gesture. On release under `prefers-reduced-motion`, settle with a short opacity/position change instead of a bouncy spring.

## When it still feels wrong

A "weird" spring is usually fixed by increasing `damping`. A gesture that stutters is a performance problem — check the track-phase rules above first, then use the `animation-performance` skill. To diagnose a feeling you can't name, record the gesture and scrub it frame by frame.

---

## Part 4 — Frame-Budget & Main-Thread Performance Diagnostics (`animation-performance`)

# Animation Performance

## Why This Matters

Imagine [Sonner](https://sonner.emilkowal.ski/) running at 30fps. Same easing, same durations, same code. Nobody would have cared. Performance isn't a polish pass applied after the motion is good; it's what lets good motion register at all.

## Operating Posture

You are a design engineer who has shipped drawers, toasts, and dashboards to real devices and has had each of the traps below bite in production. You know the developer's MacBook is the least representative device the animation will ever run on.

Two failure modes, and the first is worse:

1. **"It's smooth on my machine."** A fast laptop hides almost every problem in this skill. The bar is a mid-range phone, and on a 120Hz screen the budget is half what you think.
2. **Sprinkling `will-change` and calling it fixed.** It's the last step, not the first. Most jank is the wrong property or a busy main thread, and `will-change` fixes neither.

## Hard Rules

1. **`transform` and `opacity` by default.** Anything else needs a reason. If a cheaper property produces the same visual, use it, even when the expensive one "seems fine".
2. **Name the cause before changing code.** Every fix you propose names which of the causes below it addresses. "Added `will-change`, seems smoother" is not a diagnosis.
3. **Never conclude "it's fine" from a fast machine.** Say which findings you verified from code and which need a recording on a real device.
4. **Never `transition: all`.** List the exact properties. `all` animates whatever changes next, including layout properties nobody intended to animate.
5. **Don't trade correctness for a best-effort optimization.** Hardware acceleration is something the browser may grant. Which properties you animate is something you control. Spend effort on the second.

## The Symptom Table

Start here. Match what the user is seeing, then read the matching section.

| Problem | Solution |
| --- | --- |
| Animation stutters | Animate `transform`/`opacity`, not `width`/`height`/`top`/`margin` |
| Shadow animation is choppy | `filter: drop-shadow()` |
| Jank only during navigation or loading | Move the animation to CSS or WAAPI so it runs off the main thread |
| Motion `x`/`y` drops frames | Upgrade to `motion` 14.2+, or animate the full `transform` string |
| Hand-rolled animation drops frames in React | Write to `ref.current.style`, not state |
| Drag gets laggier as the list grows | Stop animating an inherited CSS variable; set `transform` directly |
| Blur transition lags (especially Safari) | Keep animated `blur()` under 20px |
| Unexpected properties animate | Replace `transition: all` with explicit properties |
| Element shifts 1px when motion starts or ends | `will-change: transform`, only once you see it |

## The Frame Budget

60fps is what the brain reads as fluid motion and matches most refresh rates. It gives the browser **16.7ms** (1000/60) per frame. On a 120Hz screen, now most phones and many laptops, it's **8ms**. Design against the smaller number.

For scale: a layout recalculation on a complex page can take over 100ms. That isn't one missed frame, it's a dozen.

Two things decide whether you stay inside the budget:

1. **What you animate**: how much work each frame costs.
2. **Where it runs**: whether that work can be blocked by everything else the page is doing.

## What You Animate

To show a visual change, the browser runs up to three steps:

- **Layout**: calculate the size and position of every element.
- **Paint**: draw the page into layers.
- **Composite**: put those layers on screen.

Every property enters this pipeline at one of three points, and the cost differs by an order of magnitude:

| Tier | Properties | Cost |
| --- | --- | --- |
| Composite only | `transform`, `opacity`, and in current Chrome/Firefox also `filter`, `clip-path`, `background-color` | Cheapest. Browsers promote these to their own layer. |
| Paint + composite | `box-shadow`, `border-radius`, `color` | No re-measuring, but a redraw every frame. |
| Layout + paint + composite | `width`, `height`, `padding`, `margin`, `top`, `left`, `border-width` | Most expensive. One growing element can move everything around it. |

`transform` and `opacity` change how an element looks, not where it sits in the document flow, so nothing needs re-measuring. Anything else in the composite tier needs testing across browsers and devices; support is uneven.

**Swapping down a tier:**

| Instead of | Animate |
| --- | --- |
| `width` / `height` / `padding` to grow or shrink | `scale()` |
| `top` / `left` / `margin` to move | `translate()` (percentages are relative to the element's own size) |
| `display` / `visibility` swaps | `opacity` |
| `box-shadow` | `filter: drop-shadow(…)` |

The last one is the one people miss. An animated shadow looks harmless but repaints the element every frame.

Two things follow:

- **Layout animations don't always drop frames.** An absolutely positioned element, or one with few children, may animate `padding` without visible cost. But a `padding` animation and a `scale()` animation look the same, and only one of them can't regress on a slower device. Pick the one with no downside.
- **Layout properties also move the wrong things.** Animating a sidebar's `margin-left` pushes the content beside it on every frame; `translateX` doesn't. For a dashboard next to an opening sidebar, that's the whole page re-laid-out 60 times a second.

## Where It Runs

**JavaScript always runs on the main thread.** An animation driven by `requestAnimationFrame` competes with everything else the browser is doing. When the main thread is busy, the animation's code can't run and the frame is late.

| Driver | Thread |
| --- | --- |
| JS + `requestAnimationFrame` (GSAP, Motion layout animations) | Main thread, always |
| Web Animations API (`element.animate()`, Motion's `animate()` and `motion/react` components) | Can be hardware-accelerated |
| CSS transitions and keyframes | Can be hardware-accelerated |

Hardware acceleration means the animation runs off the main thread, so it stays smooth no matter what JavaScript is doing. "JS" and "main thread" aren't synonyms: a JS library that hands off to WAAPI can be accelerated, a rAF loop can't.

Reliably accelerated: `transform` and `opacity`. Gaining support: `filter`, `clip-path`, `background-color`.

**The pattern to watch for is motion that runs while the page is doing heavy work**: page transitions, tab indicators during navigation, anything that fires alongside data fetching or hydration. Vercel's dashboard animated its active tab indicator with a Framer Motion shared layout animation. The browser was loading the next page at exactly that moment, so it dropped frames. Moving it to a CSS animation fixed it.

Motion hands `opacity`, `transform`, `clip-path` and `filter` to WAAPI, so they can be accelerated. The `x`, `y`, `scale`, `rotate` shorthands depend on the version:

```jsx
<motion.div animate={{ x: 100 }} />                          // motion 14.2+: hardware-accelerated. Before: main thread, can jank
<motion.div animate={{ transform: "translateX(100px)" }} />  // hardware-accelerated in every version
```

From `motion` 14.2, the shorthands on an HTML element are combined into one accelerated `transform` animation, so keep them. On older versions, switch to the string form when the animation has to survive a busy main thread. In every version, these stay on the main thread: layout animations (`layout`, `layoutId`), `onUpdate`, `transformTemplate`, inertia, and values driven every frame by a motion value (drag, `useTransform`).

**Acceleration is progressive enhancement.** Browsers silently decline it under conditions that change between versions; Chrome, for example, historically didn't accelerate percentage-based transforms. That's not a reason to stop using `translateY(100%)`. Percentages are the right call for elements of unknown size (it's how Sonner and Vaul position toasts and drawers), and correctness beats a best-effort optimization.

## React: Don't Animate Through State

Animation libraries animate outside React's render cycle, so they're fine. The trap is a hand-rolled animation that calls `setState` every frame: the component re-renders every 16.7ms and the render alone blows the budget.

```jsx
// Drops frames: one re-render per frame
setY(nextY);

// Smooth: no re-render
ref.current.style.transform = `translateY(${nextY}px)`;
// or with a motion value: y.set(nextY)
```

Look for state updates inside `requestAnimationFrame`, `pointermove`, `scroll`, or drag handlers.

## Two Traps That Look Correct

Both of these use `transform` and still drop frames.

**Inherited CSS variables.** Vaul's drag got laggy once a drawer held more than ~20 items, with no re-renders involved. The drag distance was written to a CSS variable that `translateY()` read:

```js
// Recalculates styles for every descendant, every frame
const style = { "--swipe-amount": `${draggedDistance}px` };

// Only touches this element
const style = { transform: `translateY(${draggedDistance}px)` };
```

CSS variables inherit, so changing one on a parent triggers style recalculation for every child. The more content, the slower each frame. Suspect this whenever a `transform` animation degrades as content grows.

**Blur.** `filter: blur()` gets expensive fast, especially in Safari. Keep animated blur under 20px; 2–5px is enough to soften a crossfade.

## `will-change`

A browser can hand an animation from the CPU to the GPU mid-flight, and that hand-off can make the element shift by a pixel at the start or end. `will-change` promotes the element up front so no hand-off happens:

```css
.drawer {
  will-change: transform;
}
```

**Add it only once you see the shift or measured dropped frames.** Browsers already promote elements animating `transform` or `opacity`, so on the common path it does nothing, and every promoted layer costs GPU memory. Put it on the element that animates, never on `*` or large containers.

Where it earns its place is an expensive paint, like a large blurred or filtered element. Promote it and keep the layer small; a small layer is cheaper to composite than a full-screen one.

## Should You Avoid JS Animation?

No. Main-thread animation only suffers when the page is busy during it, which is rare, and now you know how to spot it.

Framer Motion gives you things CSS can't: real springs, shared layout animations, exit animations for unmounted components, momentum gestures. The question is whether you need those, not whether JS animation is allowed.

**The working split:** CSS for simple motion and anything that plays while the page is busy; Framer Motion for complex, interruptible, gesture-driven motion.

## Workflow

### Phase 1: Find what animates

List every animation in scope with its driver and properties:

| Element | Driver | Properties | Plays during |
| --- | --- | --- | --- |
| Tab indicator | `motion/react` `layoutId` | layout | route change |
| Drawer | CSS transition | `transform` | user drag |
| Card hover | CSS transition | `all` | hover |

Expand `transition: all` and Motion shorthands into what they actually animate.

### Phase 2: Diagnose

Work down this list. It's ordered by how often each one is the cause:

1. **Which properties animate?** Anything other than `transform`/`opacity` is the first suspect: layout properties first, then `box-shadow` and `border-radius`, which don't look like layout and are easy to miss.
2. **Does the jank coincide with the page being busy?** Navigation, fetching, hydration, a long task. Move the animation to CSS or WAAPI.
3. **Is React re-rendering per frame?** State updates in rAF, pointer, or scroll handlers.
4. **Does it get worse as content grows?** An inherited CSS variable, or too many nodes animating at once.
5. **Is a CSS variable animated at all?** Or Motion's `x`/`y`/`scale` on a version before 14.2?
6. **Any animated `blur()` above 20px?**
7. **Still shifting or stuttering?** Now add `will-change: transform` to the animating element.

Confirm with a recording, not by feel: the DevTools Performance panel for dropped frames and long tasks, the Animations panel to slow motion down. Profile on a real mid-range phone over remote debugging. CPU throttling on a desktop models a slow CPU, not a weak GPU or a small memory budget.

### Phase 3: Report

For each finding:

```
**[Element]**: `file.tsx:42`
Cause: [which of the causes above]
Before: `transition: all 200ms` (animates `padding`, triggers layout)
After: `transition: transform 200ms` with `scale(0.97)`
Verified: from code / needs a device recording
```

Order findings by cost: layout before paint, busy-main-thread before idle. Then stop. Apply fixes when asked.
