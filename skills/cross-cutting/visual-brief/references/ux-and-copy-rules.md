# Anti-Wall-of-Text UX, Visual Grammar & Feedback Loop

## 1. Visual Grammar (One Meaning Per Visual Channel)

Never overload color, border, and shape with conflicting meanings:

| Channel | Encodes ONLY | Standard Values |
| :--- | :--- | :--- |
| **Shape** *(ISO 5807)* | Element type | Rectangle = step/component · Pill = person / start / end · Diamond = decision · Cylinder = database/store · Parallelogram = I/O · Wave-bottom = doc/artifact · Side-bars = subprocess |
| **Stroke / Border** | Lifecycle / certainty status | Solid normal = existing/verified (`base`) · Thick solid = focus / to-build / key change (`focus`) · Dashed = open question / unconfirmed (`open`) |
| **Accent Color** | Actor or comparison track | Max **2 semantic accents** (e.g., Agent/Automated vs Human, or Before vs After). Everything else stays in tinted neutral ink. |
| **Container** | Grouping / boundary | Shaded dashed frame = runtime zone / trust boundary · Unshaded dashed frame = logical group |

Generate the legend dynamically from only the shapes, statuses, and actors actually used in the artifact.

## 2. Copy Discipline (Write Each Fact Once)

- **Canvas / Card title (Level 1):** 1–3 words on mobile, concise title + optional short subtitle on desktop.
- **Inspector lead (Level 2):** **1 sentence, ≤ 14 words**, starting with a verb and naming concrete behavior (*"Validates payment and queues dispatch; retries twice on timeout"* — never vague filler like *"A service that handles things"*).
- **Expandable detail (Level 3):** Grouped short headings (*Decided*, *Measured*, *Constraints*, *Trade-offs*) with bullet items **≤ 12 words**, one fact per bullet.
- **Zero duplication:** Never repeat in prose what the layout, container zone, arrow direction, or score bar already communicates.

## 3. Interactive "Decisions Back to Chat" Loop

Whenever the artifact contains open questions, `grill` branches, or review approvals:

1. Attach open items (`open`) directly to the relevant node, card, or option — **plus** expose a unified **"Pending (answered/total)"** drawer button in the control bar.
2. Each item offers **2–4 concrete radio options** (recommended option first with measured reason) **plus "Other"** with a free-text input.
3. Persist selections in `localStorage` keyed by a unique artifact ID (`visual-brief:<slug>-<hash>`, never bare `document.title`) so reloads don't lose progress.
4. Provide a **"Copy responses"** button outputting clean numbered markdown:
   ```text
   Responses for "<Artifact Title>":
   1. [Section/Node] <Question> -> <Chosen Option or Custom Note>
   ```
5. If `navigator.clipboard.writeText` fails (sandboxed iframe / file URL), automatically reveal and select a read-only `<textarea>` so the user can copy with `Ctrl+C` / `Cmd+C`.
