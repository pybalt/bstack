# Standalone HTML Contract & Pre-Delivery QA

## 1. Portable Single-File HTML Contract

Every `visual-brief` HTML file must work identically when opened directly in any browser, local server, or agent viewer:

- **Mandatory document shell:** Always start with `<!doctype html>`, `<html lang="en">` (or matching user language), `<meta charset="utf-8">`, and `<meta name="viewport" content="width=device-width,initial-scale=1">`. Never omit doctype or viewport.
- **Zero build & offline-safe:** Inline `<style>` and `<script>` inside one `.html` file. Use crisp system font stacks (`system-ui, -apple-system, "Segoe UI", sans-serif` and `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`) — optional web fonts must never block layout or fail ugly offline.
- **Data separated from engine:** Keep diagram/board/deck data cleanly isolated inside `// <DATA> ... // </DATA>` so iterative edits only touch structured data without breaking layout/interaction JS.
- **Light + Dark tokens (explicit + `prefers-color-scheme`):** Define semantic CSS variables (`--bg`, `--zone`, `--surface`, `--raised`, `--ink`, `--muted`, `--line`, `--accent-a`, `--accent-b`) with a manual light/dark toggle that stays in sync with system preference. Use tinted neutrals (never pure `#000000` on `#FFFFFF`).
- **XSS-safe DOM rendering:** Build all dynamic labels, cards, bullets, and user-entered notes with `document.createTextNode` / `.textContent` — **never `innerHTML`** with data or user input.

## 2. Responsive Layout Rules (Desktop + Mobile)

- **Desktop (`>= 1000px`):**
  - Full-width canvas/board/deck; clicking a node opens a fixed side inspector (right, or left if it would cover the clicked target) **without shifting or re-zooming the canvas**.
  - Full keyboard support (`Tab`, `Enter`/`Space`, `Esc` to close inspector, `←`/`→` in slide decks or steppers).
- **Mobile (`< 780px`):**
  - Vertical reading flow (or cleanly stacked cards/slides); touch targets **`>= 44×44 px`**.
  - Controls live in a dedicated bottom dock strip (never floating on top of canvas nodes).
  - Inspector opens as a bottom sheet above the dock and smoothly scrolls/pans the selected node into view if covered.
- **Accessibility:** Respect `prefers-reduced-motion`, keep browser zoom enabled, never require hover to reveal essential data, and ensure visible focus states.

## 3. Pre-Delivery Verification Checklist

Verify before delivering the artifact (programmatically via headless Chrome/Playwright if available, or by inspecting rendered views):

- [ ] Valid standalone `<!doctype html>` + viewport tag + zero console/JS errors.
- [ ] Light and dark themes pass WCAG contrast (`>= 4.5:1` for text, `>= 3:1` for strokes/controls).
- [ ] Zero overlapping cards, labels, or clipped text at both desktop (`1280×800`) and mobile (`390×844`) viewports.
- [ ] Every interactive control (cards/nodes, expand detail, theme toggle, slide nav, "Copy responses" + clipboard fallback) works cleanly.
- [ ] Copy respects 3-level disclosure (no walls of text visible upfront).
