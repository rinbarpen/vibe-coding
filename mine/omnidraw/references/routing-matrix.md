# Omnidraw Routing Matrix

Full decision table mapping user intent to the best tool skill. Use this as the definitive reference for tool dispatch.

## How to Use

1. Identify the user's **intent** (what kind of diagram/image they need)
2. Check the **scenario** (patent, paper, presentation, etc.)
3. Dispatch to the **primary tool skill**
4. If primary is unavailable or unsuitable, use the **fallback**

## Routing Matrix: Intent → Tool

### Diagrams (Structured Visual Logic)

| Intent | Primary Skill | Fallback | Notes |
|--------|--------------|----------|-------|
| Flowchart / process flow | [drawio](../drawio/SKILL.md) | [mermaid](../mermaid/SKILL.md) | Draw.io for publishable; Mermaid for quick/embedded |
| System architecture | [drawio](../drawio/SKILL.md) | [mermaid](../mermaid/SKILL.md) (C4) | Draw.io for precise layout with icons |
| Network topology | [drawio](../drawio/SKILL.md) | — | Only Draw.io has proper network shapes |
| Cloud architecture (AWS/GCP/Azure) | [drawio](../drawio/SKILL.md) | — | Only Draw.io has official cloud icon sets |
| Sequence diagram | [mermaid](../mermaid/SKILL.md) | [drawio](../drawio/SKILL.md) | Mermaid is faster; use Draw.io for complex sequences |
| Class diagram | [other-draw-tools](../other-draw-tools/SKILL.md) (PlantUML) | [mermaid](../mermaid/SKILL.md) | PlantUML has best UML class support |
| Use case diagram | [other-draw-tools](../other-draw-tools/SKILL.md) (PlantUML) | [drawio](../drawio/SKILL.md) | Only PlantUML has native use case syntax |
| Activity diagram | [other-draw-tools](../other-draw-tools/SKILL.md) (PlantUML) | [drawio](../drawio/SKILL.md) | PlantUML activity syntax is most expressive |
| Component diagram | [other-draw-tools](../other-draw-tools/SKILL.md) (PlantUML) | [drawio](../drawio/SKILL.md) | — |
| Deployment diagram | [other-draw-tools](../other-draw-tools/SKILL.md) (PlantUML) | [drawio](../drawio/SKILL.md) | — |
| State machine | [mermaid](../mermaid/SKILL.md) | [other-draw-tools](../other-draw-tools/SKILL.md) (PlantUML) | Mermaid stateDiagram-v2 is very clean |
| ER diagram / data model | [mermaid](../mermaid/SKILL.md) (ERD) | [other-draw-tools](../other-draw-tools/SKILL.md) (PlantUML) | Mermaid for quick; PlantUML for detailed |
| Database schema (detailed) | [drawio](../drawio/SKILL.md) | [mermaid](../mermaid/SKILL.md) | Draw.io for production schemas |
| Gantt chart | [mermaid](../mermaid/SKILL.md) | [drawio](../drawio/SKILL.md) | Mermaid Gantt syntax is very readable |
| Timeline | [mermaid](../mermaid/SKILL.md) | [drawio](../drawio/SKILL.md) | — |
| Pie / donut chart | [mermaid](../mermaid/SKILL.md) | [other-draw-tools](../other-draw-tools/SKILL.md) (matplotlib) | Mermaid for markdown; matplotlib for publication |
| Bar / line / scatter / heatmap | [other-draw-tools](../other-draw-tools/SKILL.md) (matplotlib) | [mermaid](../mermaid/SKILL.md) | matplotlib for precise data control |
| Git branch graph | [mermaid](../mermaid/SKILL.md) (git) | — | Mermaid is the only tool with gitGraph |
| Mind map | [mermaid](../mermaid/SKILL.md) (mindmap) | [drawio](../drawio/SKILL.md) | — |
| UML (general) | [other-draw-tools](../other-draw-tools/SKILL.md) (PlantUML) | [mermaid](../mermaid/SKILL.md) | PlantUML has broadest UML coverage |
| BPMN | [visio](../visio/SKILL.md) | [drawio](../drawio/SKILL.md) | Visio has best BPMN stencils; draw.io has BPMN shapes |
| Org chart | [drawio](../drawio/SKILL.md) | [visio](../visio/SKILL.md) | Draw.io is faster; Visio has data-linked org charts |
| Wireframe / UI mockup | [other-draw-tools](../other-draw-tools/SKILL.md) (Excalidraw) | [drawio](../drawio/SKILL.md) | Excalidraw's hand-drawn style fits wireframes |
| Whiteboard / sketch | [other-draw-tools](../other-draw-tools/SKILL.md) (Excalidraw) | [drawio](../drawio/SKILL.md) | — |
| Infographic | [drawio](../drawio/SKILL.md) | [other-draw-tools](../other-draw-tools/SKILL.md) (canvas-design) | — |

### Images (Raster / Generative)

| Intent | Primary Skill | Fallback | Notes |
|--------|--------------|----------|-------|
| Photo-realistic image | [nano-banana](../nano-banana/SKILL.md) (v2) | [gpt-image-2](../gpt-image-2/SKILL.md) | v2 for quality; GPT-Image-2 for prompt adherence |
| Quick concept iteration | [nano-banana](../nano-banana/SKILL.md) (v1) | [nano-banana](../nano-banana/SKILL.md) (v2) | v1 is faster and cheaper |
| Illustration / concept art | [gpt-image-2](../gpt-image-2/SKILL.md) | [nano-banana](../nano-banana/SKILL.md) (v2) | GPT-Image-2 follows detailed prompts better |
| Logo / icon design | [gpt-image-2](../gpt-image-2/SKILL.md) | [nano-banana](../nano-banana/SKILL.md) (v2) | — |
| Poster / design artifact | [other-draw-tools](../other-draw-tools/SKILL.md) (canvas-design) | [gpt-image-2](../gpt-image-2/SKILL.md) | canvas-design for design-focused output |
| Product mockup | [nano-banana](../nano-banana/SKILL.md) (v2) | [gpt-image-2](../gpt-image-2/SKILL.md) | — |
| Abstract / texture / background | [nano-banana](../nano-banana/SKILL.md) (v2) | [gpt-image-2](../gpt-image-2/SKILL.md) | — |
| Scientific schematic | [other-draw-tools](../other-draw-tools/SKILL.md) (scientific-schematics) | [drawio](../drawio/SKILL.md) | scientific-schematics for publication standards |

## Scenario-Based Dispatch

### Patent Figures (专利附图)
- Structure/relationship diagrams → [drawio](../drawio/SKILL.md) (A–H format, 15px text, B&W)
- Flowcharts → [drawio](../drawio/SKILL.md)
- Data charts → [other-draw-tools](../other-draw-tools/SKILL.md) (matplotlib)

### Academic Paper (English)
- Architecture/pipeline diagrams → [drawio](../drawio/SKILL.md) (IEEE: EPS/PDF, grayscale)
- Sequence diagrams → [mermaid](../mermaid/SKILL.md)
- Data/results charts → [other-draw-tools](../other-draw-tools/SKILL.md) (matplotlib, 300 DPI, serif font)
- Scientific schematics → [other-draw-tools](../other-draw-tools/SKILL.md) (scientific-schematics)

### Academic Paper (Chinese, 中文期刊)
- Architecture/pipeline diagrams → [drawio](../drawio/SKILL.md) (宋体, 中英双语图注)
- Data charts → [other-draw-tools](../other-draw-tools/SKILL.md) (matplotlib with Chinese font)
- Flowcharts → [drawio](../drawio/SKILL.md) or [mermaid](../mermaid/SKILL.md)

### Technical Documentation
- Architecture diagrams → [drawio](../drawio/SKILL.md)
- Sequence/API flows → [mermaid](../mermaid/SKILL.md) (renders natively in GitHub)
- ER diagrams → [mermaid](../mermaid/SKILL.md)
- Git graphs → [mermaid](../mermaid/SKILL.md)

### Presentation / Pitch Deck
- Architecture slides → [drawio](../drawio/SKILL.md)
- Hero images → [nano-banana](../nano-banana/SKILL.md) (v2, 16:9)
- Concept illustrations → [gpt-image-2](../gpt-image-2/SKILL.md)
- Data charts → [other-draw-tools](../other-draw-tools/SKILL.md) (matplotlib)

### Software Design (UML)
- Class/use case/component/deployment → [other-draw-tools](../other-draw-tools/SKILL.md) (PlantUML)
- Sequence → [mermaid](../mermaid/SKILL.md)
- State → [mermaid](../mermaid/SKILL.md)

### Enterprise / Client Deliverable
- Visio format required → [visio](../visio/SKILL.md) (Draw.io→VSDX bridge)
- Cloud architecture → [drawio](../drawio/SKILL.md)
- BPMN → [visio](../visio/SKILL.md)

### Creative / Design
- Poster → [other-draw-tools](../other-draw-tools/SKILL.md) (canvas-design)
- Logo → [gpt-image-2](../gpt-image-2/SKILL.md)
- Mood board imagery → [nano-banana](../nano-banana/SKILL.md) (v1, multiple images)

## Tool Capability Comparison

| Capability | drawio | mermaid | visio | gpt-image-2 | nano-banana | other-draw-tools |
|-----------|--------|---------|-------|-------------|-------------|-----------------|
| Zero deps | ✗ (needs MCP) | ✓ | ✗ (needs desktop) | ✗ (needs API key) | ✗ (needs MCP) | ✓ |
| Inline code fences | ✗ | ✓ | ✗ | ✗ | ✗ | PlantUML only |
| Real-time preview | ✓ (MCP) | ✓ (live editor) | ✗ | ✗ | ✗ | ✗ |
| Vector export | ✓ (SVG, PDF) | ✓ (SVG via live) | ✓ (VSDX) | ✗ | ✗ | matplotlib: ✓ |
| Raster export | ✓ (PNG) | ✓ (PNG via live) | ✓ (PNG) | ✓ (PNG, WebP) | ✓ (PNG, WebP) | matplotlib: ✓ |
| Cloud icons | ✓ | ✗ | ✓ (stencils) | ✗ | ✗ | ✗ |
| LaTeX math | ✓ (MathJax) | ✗ | ✗ | ✗ | ✗ | matplotlib: ✓ |
| Text in images | ✓ | ✓ | ✓ | ✗ (unreliable) | ✗ (unreliable) | ✓ |
| Precise layout | ✓ | ✗ (auto-layout) | ✓ | ✗ | ✗ | matplotlib: ✓ |
| Photo-realistic | ✗ | ✗ | ✗ | ✓ | ✓ | ✗ |
| Hand-drawn style | ✗ | ✗ | ✗ | ✗ | ✗ | Excalidraw: ✓ |
| Free / open source | ✓ | ✓ | ✗ | ✗ | ✗ (paid MCP) | ✓ |
