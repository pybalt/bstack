# Discovery, Visual Direction & Pattern Catalog

Load this reference for new projects, open redesigns, visual direction briefs, A–H exploration boards, or style selection.

## 1. Choose the path

Read the request and available context before acting. In an existing project, inspect its instructions, visual documentation, components, tokens, assets, and configuration. Inspect relevant references directly.

| Request | Path |
| --- | --- |
| New project or redesign with an open direction | Built-in discovery → direction → visual reference if requested → implementation if included in the request → verification. |
| References requested in the first message | Establish product, audience, and goal; offer the eight-direction board early and continue discovery from the selection. |
| Resolved direction or selected visual | Extract decisions and constraints; clarify only gaps that change the result. |
| Focused adjustment | Preserve direction, content, and behavior outside the adjustment. Change what is necessary and verify its impact. |
| Audit or read-only request | Inspect, capture, and report findings with evidence; do not modify files. |

Full discovery applies to open-ended creation and redesign. Do not restart discovery for a correction or reopen resolved decisions. If the user explicitly skips the interview or delegates all decisions, record that choice, state assumptions, and choose a coherent direction.

### Preserved branding and resolved direction

Preserving a logo, palette, dark identity, or stack establishes constraints; it does not resolve art direction. To use the resolved-direction path, composition, typographic language, visual material, hierarchy, and behavior must be clear through a reference or observable decisions. If they are missing, develop that direction within the affected scope.

A new request for visual language, prominence, or material reopens the corresponding decisions even when branding stays. Do not restart all discovery when the user has already supplied the new brief: make it concrete, state implementation decisions, and build what was requested.


## 3. Built-in discovery

For open-ended creation or redesign, ask at least **15 substantive questions** in rounds of **3 to 5**. Wait for a round's answers before asking about decisions that depend on them. Each question may offer 2–3 explained options and a contextual recommendation, without silently preselecting the answer.

Inspect what the project can answer on its own. Do not ask which libraries or files exist. If the prompt already answers a question, preserve that answer and use the space to deepen another decision: avoid repeated questions and irrelevant preferences added to fill the quota.

These fifteen questions are an adaptable foundation for discovery:

1. What must someone achieve by using this? Define a concrete outcome.
2. Who are we designing for, and what knowledge or difficulties do they bring?
3. What is the main action we want to make easier?
4. In what context and on which devices will they use it: first visit, frequent use, limited time, or long sessions?
5. What content is essential, and what should stay out?
6. What must they understand or trust before acting?
7. Which three qualities should it communicate? Explain options such as precise, warm, technical, editorial, restrained, or playful.
8. What exactly do you like about the selected references: structure, rhythm, typography, imagery, or behavior?
9. What do you want to avoid beyond the default restrictions?
10. What role should typography play: functional, prominent, compact, or editorial?
11. What character should color have, and what real constraints apply?
12. What will carry the visual weight: the real product, photography, illustration, data, or typographic composition?
13. What should motion explain or express, and which moments need calm?
14. What task must be just as clear to complete on mobile as on desktop?
15. Which situations would frustrate someone most, and how should they recover?

Follow-up questions should resolve ambiguity. For “minimal,” distinguish information quantity, decoration, and space. For “dynamic,” distinguish feedback, narrative, and ambient activity. Do not require the user to know design terminology.

Discovery ends when all fifteen questions have been addressed and the task, hierarchy, direction, and constraints are clear. If remaining decisions affect those foundations, investigate them before generating or building. Do not present all fifteen questions together as a rigid form.

## 4. Direction and visual reference

After discovery, or when direction is already defined, read [visual direction](01-discovery-and-direction.md). Produce a short direction brief covering goal, audience, primary action, content, dominant visual idea, typography, color, imagery, motion, mobile priority, and explicit exceptions. Separate user decisions from recommendations and assumptions.

When styles or alternatives are requested, consult the [style and visual language library](01-discovery-and-direction.md). Preserve the reference repertoire and select families for the brief; a style does not dictate an effect, component, or exception to restrictions.

Translate explicit requirements into a positive contract: request → observable outcome → validating evidence. Include visual character and the prominence of the material as well as functionality. A claim, font family, or isolated color does not establish direction. If the request calls for a prominent animated scene, a fixed portrait with minor variations does not satisfy that contract.

Set `DESIGN_VARIANCE`, `MOTION_INTENSITY`, and `VISUAL_DENSITY` for the case and explain their visible effects. These are design controls, not internal model weights or exact rendering parameters. A selected reference determines composition ahead of these controls.

When deciding how to present, organize, compare, explore, operate, or narrate content, consult the [visual decision catalog](01-discovery-and-direction.md). Choose for the brief's problem and check its mobile criterion; avoid accumulating patterns for variety. The eight-style board explores directions; the catalog helps turn the chosen direction into a concrete interface.

### References requested in the first prompt

Once product, audience, and goal are clear, create **an eight-direction board A–H** early, usually in one 4 × 2 image. Do not wait until all discovery is complete to help choose a visual language. If that minimum context is missing, ask only what is necessary first.

Keep the same brief and content across all eight cells. Substantially vary composition, hierarchy, and visual language. Every cell respects the restrictions. Use an available image-generation tool when generated proposals are requested; identify real references and their sources. Do not present a synthetic image as a real site.

The board compares direction; it does not approve readability at thumbnail size. Include an A–H legend and enlarge the chosen option. When combining options, define a dominant direction and coherent synthesis.

### Image of the selected result

When the brief is complete, offer once: “The selected direction is [summary]. Would you like me to generate a visual reference of how it would look, including desktop and mobile?”

- If the image was already requested, generate it when the brief is ready without asking again.
- If the user accepts the image, show it and wait for their selection or corrections before implementing from it. A generic image does not replace mobile composition.
- If they decline and implementation was requested, continue with the agreed direction; images are not a mandatory gate.
- If they supply a sufficient reference, analyze and use it; do not generate extra alternatives without a reason.
- If generation is unavailable, explain the limitation. Offer a wireframe or specification as an alternative and let the user choose; never claim to have generated an image.

---

# Visual direction and references

Read this document to define a direction, produce references, or evaluate whether a proposal has an identity. Restrictions and exceptions live exclusively in section 2 of `SKILL.md` and remain active throughout exploration.

## Direction brief

Return a brief that supports decisions throughout the work. Adapt its length to the project:

| Field | What it must resolve |
| --- | --- |
| Product, audience, and task | What the person uses, for what purpose, and in which context. |
| Surface | Promotional landing page, editor, catalog, or component; each one's function within the same brand. |
| Preserved constraints | Logo, palette, content, or integrations that stay; do not confuse them with a resolved direction. |
| Action and hierarchy | What is recognized first, what needs to be understood, and what happens next. |
| Content | What actually exists, what is missing, and which simulations were agreed. |
| Visual idea | A concrete sentence describing the relationship between content and composition. |
| System | Available type families, scale, flat palette, spacing, surfaces, and imagery. |
| Behavior | What motion explains and where the interface stays still. |
| Mobile | Reading, navigation, and action priorities on a small screen. |
| Controls | Effective `DESIGN_VARIANCE`, `MOTION_INTENSITY`, and `VISUAL_DENSITY` values, with their visible effects. |
| Provenance | User decisions, recommendations, assumptions, origins of values, and explicit exceptions. |

An idea such as “a collection archive with a side index and prominent photography” guides decisions. Adjectives such as “premium, modern, and clean” need to become concrete before guiding implementation.

## Positive contract and observable outcomes

For each requirement that determines the result, record:

| Request | Observable decision | Evidence of fulfillment |
| --- | --- | --- |
| Composition or prominence | Which element dominates, its relationship to text, and how it enters the initial frame. | Rendering in the viewport where the surface will be used. |
| Typographic language | Letter construction, width, weight, rhythm, and relationship to content. | Real text in the composition, not the name of a font. |
| Visual material | Which image, scene, medium, or geometry appears and why it represents the product or direction. | Actual asset or rendered scene; clear provenance and function. |
| Palette and materiality | Contrast, surfaces, texture, and depth compatible with restrictions. | Integrated result, not an isolated color swatch. |
| Requested motion | What changes, in which order, with what amplitude, and where it resolves. | Full playback; key frames as supporting material. |
| UX and primary action | What can be done and how its result is recognized. | Action walkthrough and relevant recovery. |

“Keep it dark” resolves only part of the palette. “Cyberpunk” or “hacker” requires a coherent combination of composition, typography, material, and behavior. Black, green, uppercase letters, and a thematic claim do not establish that language.

When the user requests an ethereal, unusual, or audiovisual piece, propose and specify how it will be perceived: for example, geometry losing and regaining structure, material changes, layers with depth, or visible reconstruction. These are possibilities according to the brief, not a recipe for every brand or implicit permission for blocked decoration.

Make the hypothesis refutable: describe what will be visible and which result would fall short. If prominent animation was requested, a fixed image with minor interference can fail even when rendering changes some pixels. If an image was rejected, reusing it in a card does not satisfy the correction either.

## Surfaces within one brand

A landing page needs to express value and may use a central audiovisual piece. An editor needs to support repeated work with stable controls. A catalog needs comparable samples. Keep brand coherence and adapt composition, density, and motion to those functions.

Define the prominent piece and check it before extending the language to other sections. If the hero does not communicate the direction, repeating its font, palette, and asset across the site amplifies the problem.

The brief may live in the conversation. Save it in the project if that is part of the request or the work needs a persistent document; do not create auxiliary documentation for every adjustment.

## Direction controls and levels

Starting values are defined in `SKILL.md`; that is the only place that configures the starting point. Keep all three explicit controls in the brief even when the user answers in natural language. Adjust effective values to the product and record whether they come from the brief, a reference, a user choice, or the starting profile.

| Control | 1–3 | 4–7 | 8–10 |
| --- | --- | --- | --- |
| `DESIGN_VARIANCE` | Stable grids, consistent alignments, and repeated proportions. | Controlled offsets, changes in proportion, and rhythm between text and images. | Expressive composition: differently sized masses, marked asymmetry, and a distinct visual sequence. |
| `MOTION_INTENSITY` | Immediate feedback and discreet transitions, usually without automatic entrances. | Spatial continuity, perceptible state changes, and a bounded expressive gesture. | Prominent choreography, spatial transitions, or sequences tied to content and justified by the product. |
| `VISUAL_DENSITY` | Few units, controlled reading width, and generous separation. | Balanced everyday reading and grouping by task. | Frequent, compact information, precise rows or columns, and controls that remain legible. |

High variance does not require masonry, overlap, or huge empty spaces. High intensity does not enable blocked decoration or loops. High density does not justify tiny controls. Record the reason for each choice rather than fictitious numerical precision.

Intensity and impact are different. A minimal effect can score highly because it runs constantly while still failing to deliver a prominent transformation. Justify values through observable outcomes and distinguish the hero profile from a working surface's profile.

In the A–H board, each direction can explore a different profile; record differences when they help selection. In the chosen direction, keep a coherent profile and adapt its expression to each device: mobile does not inherit overlaps that prevent operation.

## Type scale and weights

Define a scale and concrete roles instead of relying on “premium typography.” Adjustable starting references include body text at 16 px relative to root size, long text at roughly 45–65 characters per line, and headings at 32–40 px on mobile and 48–64 px on desktop when content allows. These are composition references, not mandatory sizes for every product.

| Role | Weight reference | Criterion |
| --- | --- | --- |
| Reading text | 400 | Preserve comfortable reading and sufficient contrast. |
| Labels and actions | 500–600 | Distinguish function without making every control prominent. |
| Headings | 500–700 | Build hierarchy together with size, space, and proportion. |
| Data | Consistent weight and tabular figures when useful | Support comparison; use monospace only if it serves the direction. |

Check which weights and characters the actual family provides. An editorial family may resolve hierarchy with other weights; do not force synthetic bold or an ornamental mixture of styles within a word. Preserve the core typography restrictions.

## Eight-direction board

Use it when references or an eight-style exploration are requested. Keep product, audience, content, and primary action consistent so comparison is meaningful.

These eight families remain available as a starting point. To broaden or deepen styles for the brief, consult the [style and visual language library](01-discovery-and-direction.md):

| Direction | Decision to explore |
| --- | --- |
| Editorial typography | Reading rhythm and typography as structure. |
| Technical utility | Density, precision, and repeated operation. |
| Warm modernism | Proportion, space, and approachability. |
| Industrial | Structure, signage, contrast, and materials. |
| Restrained brutalism | Direct hierarchy and deliberately raw composition. |
| Cultural archive | Classification, indexes, and relationships between pieces. |
| Photography | Framing, image sequencing, and dialogue with text. |
| Playful geometry | Shape, flat color, and expressive behavior. |

Adapt or replace these families for the product; this is not a mandatory list for every board. Differences must extend beyond palette and font. Each proposal should change at least one relevant structural decision: hierarchy, composition, imagery, or how content is explored.

For a 4 × 2 image, reserve a consistent cell per direction and accompany it with an A–H legend. Check the generated board: eight distinct cells, clear correspondence with the legend, and compliance with restrictions. If a cell violates the brief, correct it before offering it as an option. Image generation can produce imperfect text; do not present it as approved copy.

For real references, inspect screens before citing them and link their sources. Explain what is adopted and what is discarded. Do not attribute a generated proposal to a real product.

Then select resources from the [visual decision catalog](01-discovery-and-direction.md) for the task they solve. A family such as “industrial” can use a product record, comparison, or narrative scene; it does not require a particular component. If combining references, record which visual relationship each contributes and preserve a dominant direction.

## Adaptable generation prompt

Attach the real images available to you; do not claim they were attached when only a description was provided. Build the prompt with:

1. Agreed product, audience, task, and content.
2. Output type: A–H board or detailed screen of a selected direction.
3. Dimensions and aspect ratio. For a detailed screen, define desktop and mobile separately or in two clearly separated frames.
4. Agreed composition, typography, color, imagery, and density.
5. All applicable restrictions from section 2 of `SKILL.md` and explicit exceptions.
6. Readable content, clear hierarchy, and one primary action; no invented feature inventory to fill space.

Request interface content without a device frame or browser chrome unless expressly requested. Do not stretch a desktop composition to fill a mobile frame. Recompose for its priorities.

If product imagery is missing, ask about its use when decisive or propose a direction supported by actual material. Do not automatically substitute random photographs or decorative illustrations for relevant imagery.

## Visual evaluation and feedback

Compare the selected reference with the render, not with a description of how it should look. Review relationships between elements and the full frame alongside isolated details.

Use these acceptance criteria:

- The screen communicates product, task, and next step without an external explanation.
- The visual idea is recognizable through connected typography, composition, imagery, and behavior decisions.
- The piece works with its specific content; it does not depend on filler metrics or decoration.
- Hierarchy keeps working with real text and on mobile.
- Spaces, alignments, line breaks, crops, and states show intent and coherence.
- The result respects the reference and agreed corrections.

Check every explicit request through the independent [acceptance](09-acceptance-and-render.md) review. Respected restrictions and an orderly screen cannot compensate for the wrong visual language.

When someone says “this doesn't feel right,” locate the affected dimension before regenerating everything. In a reference mix, choose a dominant direction and explain how the secondary gesture will fit.

---

# Styles and visual languages

Consult this library when someone asks for styles, references, or alternative directions. Use the names as an exploration vocabulary; always make composition, typography, imagery, material, and behavior concrete. A style name alone leaves too many decisions open.

The A–H board contains eight proposals selected for the brief, not eight universal styles. This library preserves familiar families, supports deeper exploration, and allows combining references without limiting every project to the same board. Direction controls and type weights are defined in [visual direction](01-discovery-and-direction.md).

## Reference families

| Style | Visual relationships to explore | Decision the brief must resolve |
| --- | --- | --- |
| Editorial typography | Contrasting scale, margins, columns, and rhythm between headings, body text, and captions. | Which content deserves prominence and how reading works in a single mobile column. |
| Swiss / international | Rigorous grids, shared alignments, typographic hierarchy, and structural space. | Which order makes content understandable; a precise grid can be asymmetric. |
| Functional minimalism | Few visible elements, clear groups, and attention directed through proportion. | What can be removed while preserving information, discoverability, and operation. |
| Warm modernism | Simple geometry, human proportions, flat color, and approachable materials. | How to express warmth through content and scale without relying on beige and large radii. |
| Industrial | Exposed structure, modules, signage, joints, and contrast between parts. | Which product relationships justify that structure and which signage helps operation. |
| Technical utility | Indexes, aligned data, stable controls, and a clear distinction between state and action. | What must remain visible during repeated work and which complexity can wait. |
| Restrained brutalism | Direct hierarchy, frank borders, forceful typography, and deliberately raw composition. | How to preserve orientation and reading within a raw expression. |
| Neobrutalism | Flat color planes, defined outlines, offsets, and contrasting masses. | Which element dominates; borders and shadows should not give every block equal weight. |
| Cultural archive | Numbering, records, relationships, timelines, and diverse materials coexisting. | How to explore by author, date, or subject without turning metadata into decorative noise. |
| Photography | Framing, scale, sequencing, image editing, and the relationship with text. | What the real images communicate and which crop preserves that meaning on mobile. |
| Playful geometry | Simple shapes, flat color, scale changes, and expressive responses. | Which visual play helps recognize or use the product while controls remain easy to hit. |
| Retro digital | Raster graphics, windows, screen typography, and the constraints of a specific era. | Which era and traits to recover while preserving accessible text and current capabilities. |
| Retrofuturism | Historical visions of the future, diagrams, typography, and objects from a recognizable period. | Which vision is being reinterpreted and how it relates to current content. |
| Cyberpunk / hacker | Tension between systems and disruption, fragmented information, signals, codes, and contrasts of scale. | Which material and transformation build that world; black, green, and monospace alone leave direction incomplete. |
| Organic / ethereal | Continuous contours, voids, changing matter, depth, and shape transitions. | Which form or material supports the idea; flat surfaces and requested animation can achieve it without automatic gradients. |
| Handcrafted / tactile | Traces of process, specific illustration, paper, printing, or controlled irregularity. | Which real material to use and how to preserve detail, contrast, and loading cost. |
| Collage / montage | Cutouts, disparate scales, layers, and relationships between visual sources. | What connects the pieces and establishes reading order; mobile needs an edited composition. |
| Art Deco / ornamental geometry | Symmetry or stepped rhythms, vertical proportions, and geometric motifs. | Which motifs fit the brand; requested ornament does not enable other blocked effects. |
| Spatial / three-dimensional | Perspective, volume, depth, lighting, and the relationship between object and interface. | Whether volume communicates a property or is the requested expressive piece; plan an accessible and viable mobile version. |
| Controlled maximalism | Layers, abundant content, scale contrasts, and multiple levels of reading. | Which anchors support orientation and which hierarchy survives reduced width. |

The initial eight families—editorial, technical utility, warm modernism, industrial, restrained brutalism, cultural archive, photography, and playful geometry—remain available. Select each board's eight proposals for the differences that help decide that project.

## Common materials and techniques

A material or technique can appear in different styles. The decision catalog linked below helps choose its function; core restrictions determine whether an explicit request is necessary.

| Reference | What to evaluate before using it |
| --- | --- |
| Glassmorphism / glass | Transparency, blur, and readability over real content. This ornamental material is blocked by default; a concrete request defines where to use it. |
| Paper, grain, and printing | Relationship to content, contrast, and texture at different scales. Apply where it contributes to the agreed material and check its cost during scrolling. |
| Volume, relief, and perspective | Which spatial property they communicate; distinguish a product scene from controls whose relief only adds decoration. |
| Masonry, modular grids, and bento | Nature and hierarchy of units, reading order, and loading stability. These are organization options; filler bento remains blocked. |
| Masks, cropping, and overlap | Which content they reveal and how its meaning is preserved. Respect selectable text, focus, and a readable mobile composition. |
| Scroll narratives, parallax, and sequences | Relationship between progress and content, exit, and access to the action. Keep native scrolling; scroll hijacking needs an explicit request. |
| Glitch, distortion, and kinetic text | Which expressive transformation was requested, on which element, and for how long. The style name does not automatically enable these ornamental effects. |
| Gradients, iridescence, glow, and liquid effects | Record the explicit request and its scope before incorporating them. A reference image does not constitute that authorization by itself. |

## Turn references into a distinct direction

For each real reference, inspect the screen or sequence and record what you take: for example, a photograph's proportion, an index's rhythm, or an object's transformation. Link the source and distinguish observed qualities from proposals. Identify a generated image as a proposal without attributing it to a real site.

When mixing references, choose a dominant one and define the secondary one's concrete contribution. “Editorial with technical records” resolves more than adding labels; check that both contribute to the same task. Preserve typography, content, mobile reading, and the primary action during comparison.

Consult the [visual decision catalog](01-discovery-and-direction.md) to turn style into composition and interaction. Generate the board and detailed reference using the [visual direction](01-discovery-and-direction.md) procedure; when images have already been requested, honor that request rather than replacing it with this written list.

---

# Visual decision catalog

Consult this catalog to resolve a relationship between content, composition, and use. Start with the brief's problem; choose a resource that changes a visible decision and explain how it will be checked. Combine resources only when they address different needs on the same surface.

[Styles and visual languages](01-discovery-and-direction.md) provide character; this catalog contains 36 resources grouped into seven design problems. A composition can be editorial, industrial, or playful through its proportions, typography, materials, and behavior. Style and resource serve different functions and are selected together.

## Selection criteria

For the chosen resource, resolve these questions in the direction brief or conversation:

1. **Need:** what must the person understand, find, compare, or do?
2. **Visible relationship:** what dominates and which elements must be read together?
3. **Available content:** which real text, images, data, or behavior support that relationship?
4. **Direction profile:** which decisions express the effective composition, motion, and density controls?
5. **Mobile and evidence:** how is it recomposed, and which render or walkthrough will allow evaluating the result?

Restrictions and exceptions are determined in section 2 of `SKILL.md`. When a selected technique requires a blocked resource, record the explicit request and scope or address the same need with another treatment. A high intensity setting preserves this boundary.

## 1. Communicate a proposition

| Resource | Relationship that should be visible | Mobile and verification |
| --- | --- | --- |
| Proposition and visual evidence | A concrete statement next to the piece that makes it understandable: a result, object, or interaction. Proportion depends on which contributes more information. | Order statement, evidence, and action for the necessary understanding. Check that the evidence retains useful size and detail during the initial walkthrough. |
| Visible working surface | The actual workspace explains the product through a recognizable task, with relevant content and controls. | Reframe the task, show a detail, or allow exploring the tool. A desktop screenshot reduced until controls are illegible does not fulfill the function. |
| Object in context | A product, piece, or document takes the primary role; its attributes connect to visible details instead of being distributed across independent boxes. | Preserve scale, orientation, and access to detail. Test the crop with the actual image and place annotations where they remain readable without overlap. |
| Human process | Photographs or work materials explain how a result is produced. The sequence preserves a concrete relationship between person, action, and product. | Edit images for what they communicate rather than to fill width. Check that cropping preserves the action and that captions and names do not suggest invented social proof. |
| Cover with an index | A featured piece introduces a collection while the index makes its breadth, classification, or cadence understandable. | Separate the primary entry from archive access. Selecting a piece and returning to the collection should preserve orientation. |
| Prominent narrative scene | A requested scene expresses the central idea through visible transformation; heading and action have stable positions within the frame. | Design scale, crop, and sequence for the viewport. Observe the full cycle at normal speed; a thumbnail or noisy image does not establish prominence. |

## 2. Organize information and density

| Resource | Relationship that should be visible | Mobile and verification |
| --- | --- | --- |
| Reading column with references | Text preserves its rhythm while notes, sources, or examples connect to a concrete point. | Insert references near their mention when moving to one column. Test long text and return to the reading position after opening a reference. |
| Index and content | Sections form an understandable map and content retains its position during navigation. | The index may become a recognizable expandable control. Check direct links, visible headings, and that fixed bars do not cover destinations. |
| Summary and depth | A summary supports deciding whether to open data, explanation, or detail. Expansion addresses an information need. | Preserve context and the close control during expansion. Information essential to acting remains available before expansion. |
| Activity record | Events, states, or documents follow a real sequence and show what changed. | Prioritize date, entity, and consequence. Test extensive events, groups, and relevant time zones without inventing activity to animate the screen. |
| Dense operations panel | The workspace groups information by frequency and dependency; tables, rows, or dividers express relationships without a box per datum. | Decide which columns are essential, which move to detail, and when local scrolling is needed. Check that each row retains its identity and actions. |

## 3. Compare, decide, and establish trust

| Resource | Relationship that should be visible | Mobile and verification |
| --- | --- | --- |
| Comparison with shared attributes | Options use the same criteria, units, and order so differences remain legible. | Keep each option's name associated with its attributes when stacking or scrolling. Test selection and return without losing selected criteria. |
| Verifiable before and after | Two states of the same content show a change under comparable conditions. The comparison control reveals rather than exaggerates the difference. | Use a touch- and keyboard-operable control or two complete views. Preserve framing, scale, and labels; a transition does not establish a nonexistent result. |
| Traceable detail | A claim or figure leads to its source, scope, or method where it affects the decision. | Check reading the explanation and returning. Detail must contribute substance and provenance without logos, numbers, or quotes added as decoration. |
| Configuration and consequence | Selecting an option changes a related summary, representation, or calculation and makes the relevant consequence visible. | Place the change near the control or clearly connect it. Test cost, availability, pending states, and correction; disclose simulations in delivery. |
| Selection and review | A selected set is reviewed with its constraints before the next step; corrective actions preserve completed work. | Maintain access to the set and relevant total with the keyboard open. Verify removing, returning, and continuing; fixed bars must not cover the active element. |

## 4. Explore collections

| Resource | Relationship that should be visible | Mobile and verification |
| --- | --- | --- |
| Metadata archive | Images, documents, or pieces can be found through classification meaningful to the content. | Test long names, active filters, no results, and return from detail. Reading order must match the visible classification. |
| Variable-rhythm gallery | Piece proportions guide a visual sequence. Modular grids or masonry are chosen for the actual material. | Adjust columns for necessary detail, reserve loading space, and preserve semantic order. Review extreme aspect ratios and pieces without an image. |
| Detail browsing | Someone moves between related pieces while retaining position, selection, and collection context. | Ensure return to the original element and navigation independent of hover. Test direct links and orientation changes. |
| Relationship map | Position, proximity, or connections help explain a spatial or conceptual set. | Offer search, a list, or equivalent access if the canvas requires pan and zoom. Check orientation, exit, and selection without dragging as the only method. |
| Meaningful collection groups | Chapters or groups explain relationships between pieces with different priorities. Size and space reflect those priorities. | Recompose groups while retaining headings and order. If using bento-like modules, each unit needs real autonomous content and a reason for its proportions. |

## 5. Operate, edit, and recover

| Resource | Relationship that should be visible | Mobile and verification |
| --- | --- | --- |
| Work and contextual detail | Selection reveals properties or tools near the task while keeping the modified content clear. | The inspector can become a sheet or dedicated view. Preserve selection, focus, and values when opening and closing; check that the keyboard does not hide confirmation. |
| Consequence preview | Parameter changes update a readable representation of the outcome. The relationship between control and output remains visible. | Alternate or bring controls and outcome together without losing settings. Test latency, quick changes, and error; distinguish previewing from saving or executing. |
| Useful capture stages | Fields follow real dependencies or decisions, and the person recognizes progress, requirements, and the ability to return. | Check suitable input, autocomplete, errors, and value retention. Dividing into steps must reduce effort rather than hide how much data is requested. |
| Multiple selection and shared action | Selection makes scope, quantity, and available actions visible without confusingly replacing normal navigation. | Keep clear touch targets and a recognizable exit. Verify partial selection, offscreen elements, and recovery from the action where relevant. |
| Local result and recovery | An operation confirms what happened beside the affected element and supports correction or retry according to the actual result. | Preserve space and context when displaying messages. Check failures and rapid consecutive actions; animation must never announce confirmation before it arrives. |

## 6. Tell a story through motion

Also read [motion](10-motion-principles.md) when selecting one of these resources. An expressive request is valid; specify material, phases, amplitude, rhythm, and resolution so the result can be evaluated.

| Resource | Relationship that should be visible | Mobile and verification |
| --- | --- | --- |
| Material transformation | A material or object changes structure or properties in a way that expresses the brief. The main change is recognizable at normal speed. | Decide crop and scale to show the complete transformation. Observe beginning, development, and resolution; reduced motion preserves an understandable representation of the outcome. |
| Layered explanation | A piece separates, reveals, or recomposes to show parts and relationships that were not previously evident. | Recompose distances and annotations to keep detail legible. Allow access to information without waiting for or replaying the full sequence. |
| Continuous decision and result | A choice connects visibly to its consequence while preserving a spatial or content anchor. | Interrupt and repeat the interaction to test continuity. The destination must remain identifiable without relying on a large trajectory or following the pointer. |
| Chaptered narrative | Each stage develops an idea and progress reveals a new relationship. Native scrolling or explicit controls allow traversal. | Check heights, exit, return, and access to the action. An important chapter must not become compressed or skipped by a desktop-only sequence. |
| Complete-cycle demonstration | A task shows input, action, and result within an expressly requested sequence. If it repeats, the return has a comprehensible pause and transition. | Preserve enough time to read and recognize phases. Check pause and repetition; distinguish a conceptual demonstration from an actual product operation. |

## 7. Establish character through typography and material

| Resource | Relationship that should be visible | Mobile and verification |
| --- | --- | --- |
| Complete typographic composition | Scale, width, weight, alignment, and line breaks build a recognizable idea across the heading and its context. | Test real text and intermediate widths. Preserve reading unity; avoid expressing character by highlighting a word with a blocked treatment. |
| Document language | Records, numbering, annotations, or document structure serve the content and its classification. | Ensure reading order and data relationships. Labels have a concrete function; a promotional eyebrow does not become functional because it resembles a record. |
| Observed material | Specific photography, illustration, or texture contributes information about the product, its process, or its visual world. | Check source, detail, contrast, and media weight in the actual frame. The material retains meaning when the screen's proportions change. |
| Contrasting scales | A dominant piece and subordinate elements establish importance or relationships without giving everything equal visual weight. | Recompose sizes and order instead of proportionally reducing everything. Check that subordinate elements remain legible and operable. |
| Content-derived motif | A recognizable shape, cut, alignment, or behavior originates in project material and reappears where it contributes continuity. | Define where its use ends. Check that the motif retains character with less space and does not become a repeated ornamental layer across every block. |

## Relate resources, styles, and controls

Starting values are configured only in `SKILL.md`. These examples show how different tasks may need different profiles; the brief and selected reference determine effective values.

| Surface and possible direction | `DESIGN_VARIANCE` | `MOTION_INTENSITY` | `VISUAL_DENSITY` | Visible decision |
| --- | --- | --- | --- | --- |
| Landing page with a requested audiovisual scene | 8 | 8 | 3 | The scene and its transformation dominate the frame, with stable reading and action. |
| Frequently used editor, technical utility | 4 | 2 | 6 | Work and properties stay close; changes help preserve context. |
| Editorial photography archive | 7 | 3 | 4 | Image sequencing and the index provide character with calm navigation. |
| Technical comparison of options | 4 | 2 | 7 | Shared attributes and their differences take priority over decoration. |

For text, label, and heading weights, use the [visual direction](01-discovery-and-direction.md) scale; adjust to the family and available weights. Resource variety does not require adding fonts, engines, or components.

## Turn the decision into a reference

Example: an object archive can combine **cover with an index**, **metadata archive**, and **object in context** within a photographic direction with editorial structure. The reference shows a dominant piece, a legible index, and a concrete detail; mobile recomposes those three elements for the task. If the same project includes an editing tool, that surface may need a different density and motion profile.

For generated proposals, prepare the A–H board or desktop and mobile views using the [visual direction](01-discovery-and-direction.md) procedure. For real references, inspect and link sources; explain which visual relationship comes from each. The written catalog accompanies exploration without replacing images the user has requested.

Evaluate implementation through [acceptance](09-acceptance-and-render.md): functionality, brief fidelity, and temporal impact retain independent results. The catalog guides decisions; the outcome is verified in the medium where it will be used.
