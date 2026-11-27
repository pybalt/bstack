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

## 3. Desirability Color Coding for 2×2 Matrices (`matrix2x2`)

Encode strategic desirability directly into the four quadrants so priority reads in under a second (light and dark WCAG-compliant):

| Quadrant | `tone` | Visual Encoding | Badge |
| :--- | :---: | :--- | :--- |
| **Quick Wins** *(High Impact · High Feasibility)* | `win` | Soft green surface & border, green heading/dot | `Do First` |
| **Big Bets** *(High Impact · Lower Feasibility)* | `bet` | Soft warm amber surface & border, amber heading/dot | `Spike / Stage` |
| **Fill-ins** *(Low Impact · High Feasibility)* | `fill` | Quiet neutral surface (`--zone`), low prominence | `Optional` |
| **Money Pits** *(Low Impact · High Effort)* | `cut` | Muted gray surface with diagonal SVG hatch + strikethrough titles | `Avoid` |

## 4. Chat-First Decision Flow (Zero Copy-Paste Friction)

1. Attach open items (`open`) to relevant nodes/cards AND expose an **"Open decisions"** summary drawer in the header showing each question + options (with the recommended option highlighted) so the user can inspect context visually.
2. Never put form radios or "Copy responses" buttons inside the HTML — **ask the actual decision in the main agent chat** (`ask_question` / `AskUserQuestion` / direct prompt) right alongside the artifact link so the user explores the visual brief and clicks/replies once in chat.
