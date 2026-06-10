---
name: omnidraw
description: Unified drawing and diagram command center. Routes user requests to the best tool skill based on intent and scenario (patent figures, academic papers, technical architecture, presentations, UML modeling, creative design, and more). Covers Draw.io, Mermaid, Visio, GPT-Image-2, Nano Banana Pro v1/v2, PlantUML, Excalidraw, matplotlib, canvas-design, and scientific-schematics.
---

# Omnidraw — Unified Drawing & Diagram Router

Routes drawing requests to the best tool skill based on **what you need** and **what scenario you're in**.

## Tool Skills at a Glance

| Skill | Best For | Dependency |
|-------|----------|------------|
| [drawio](../drawio/SKILL.md) | Flowcharts, architecture, network, cloud, patent/academic figures | drawio MCP server |
| [mermaid](../mermaid/SKILL.md) | Sequence, ERD, Gantt, git, mindmap, state, quick markdown diagrams | None (inline code) |
| [visio](../visio/SKILL.md) | VSDX format deliverables, BPMN, enterprise diagrams | Draw.io bridge |
| [gpt-image-2](../gpt-image-2/SKILL.md) | Illustrations, concept art, logos, photo-realistic via OpenAI | `OPENAI_API_KEY` |
| [nano-banana](../nano-banana/SKILL.md) | Photos, concept art, quick iterations via fal-ai v1/v2 | fal-ai MCP server |
| [other-draw-tools](../other-draw-tools/SKILL.md) | PlantUML (UML), Excalidraw (hand-drawn), matplotlib (data charts), canvas-design, scientific-schematics | None |

## Scenario Dispatch

**What scenario are you in? Start here:**

### 专利附图 (Patent Figures)
→ [drawio](../drawio/SKILL.md) for structure/flow/connection diagrams (A–H format, 15px text, B&W)
→ [other-draw-tools](../other-draw-tools/SKILL.md) (matplotlib) for data charts

### 学术论文图 — English Journals (IEEE/ACM/Elsevier/Springer)
→ [drawio](../drawio/SKILL.md) for architecture/pipeline (grayscale, EPS/PDF, LaTeX)
→ [mermaid](../mermaid/SKILL.md) for sequence diagrams
→ [other-draw-tools](../other-draw-tools/SKILL.md) (matplotlib) for results/data charts (300 DPI, serif)

### 学术论文图 — 中文期刊 (中国科学/计算机学报/软件学报)
→ [drawio](../drawio/SKILL.md) for 架构图/流程图 (宋体, 中英双语图注)
→ [other-draw-tools](../other-draw-tools/SKILL.md) (matplotlib) for 数据图 (中文标签)

### 技术架构图 (Technical Architecture)
→ [drawio](../drawio/SKILL.md) for system/cloud/network architecture (precise layout, icons)
→ [mermaid](../mermaid/SKILL.md) (C4) for quick context/container diagrams

### 流程/逻辑图 (Flowcharts & Process)
→ [mermaid](../mermaid/SKILL.md) for quick markdown-embedded flows
→ [drawio](../drawio/SKILL.md) for publishable, precisely laid-out flows

### 数据图表 (Data Charts)
→ [other-draw-tools](../other-draw-tools/SKILL.md) (matplotlib) for programmatic, publication-quality charts
→ [mermaid](../mermaid/SKILL.md) for quick inline pie/bar charts

### 演示文稿 (Presentations / Pitch Decks)
→ [nano-banana](../nano-banana/SKILL.md) (v2, 16:9) for hero images
→ [gpt-image-2](../gpt-image-2/SKILL.md) for concept illustrations
→ [drawio](../drawio/SKILL.md) for architecture slides
→ [other-draw-tools](../other-draw-tools/SKILL.md) (matplotlib) for data chart slides

### 照片/真实感图片 (Photos & Realistic Images)
→ [nano-banana](../nano-banana/SKILL.md) (v2) for best quality
→ [gpt-image-2](../gpt-image-2/SKILL.md) for detailed prompt following

### 概念艺术/插画 (Concept Art & Illustration)
→ [gpt-image-2](../gpt-image-2/SKILL.md) for detailed, prompt-adherent illustrations
→ [nano-banana](../nano-banana/SKILL.md) (v2) for faster visual exploration

### UML 建模 (Software Design — UML)
→ [other-draw-tools](../other-draw-tools/SKILL.md) (PlantUML) for class, use case, component, deployment
→ [mermaid](../mermaid/SKILL.md) for sequence and state

### Visio 格式交付 (Enterprise / VSDX Required)
→ [visio](../visio/SKILL.md) for Draw.io→VSDX bridge workflow
→ [drawio](../drawio/SKILL.md) as the creation tool (export to VSDX)

### 手绘/白板风格 (Sketch / Whiteboard)
→ [other-draw-tools](../other-draw-tools/SKILL.md) (Excalidraw) for hand-drawn aesthetics

### 海报/设计 (Posters & Design Artifacts)
→ [other-draw-tools](../other-draw-tools/SKILL.md) (canvas-design) for design-focused posters
→ [gpt-image-2](../gpt-image-2/SKILL.md) for visual concept generation

### 科研示意图 (Scientific Schematics)
→ [other-draw-tools](../other-draw-tools/SKILL.md) (scientific-schematics) for publication-quality
→ [drawio](../drawio/SKILL.md) for fallback

### 快速内联 (Quick Markdown-Embedded)
→ [mermaid](../mermaid/SKILL.md) for zero-setup code fence diagrams (GitHub/Notion/Obsidian)

## Routing Matrix (Quick Reference)

### Diagrams

| Intent | Primary | Fallback |
|--------|---------|----------|
| Flowchart / process | [drawio](../drawio/SKILL.md) | [mermaid](../mermaid/SKILL.md) |
| System architecture | [drawio](../drawio/SKILL.md) | [mermaid](../mermaid/SKILL.md) (C4) |
| Network topology | [drawio](../drawio/SKILL.md) | — |
| Cloud architecture (AWS/GCP/Azure) | [drawio](../drawio/SKILL.md) | — |
| Sequence diagram | [mermaid](../mermaid/SKILL.md) | [drawio](../drawio/SKILL.md) |
| UML class / use case / component | [other-draw-tools](../other-draw-tools/SKILL.md) (PlantUML) | [drawio](../drawio/SKILL.md) |
| State machine | [mermaid](../mermaid/SKILL.md) | [other-draw-tools](../other-draw-tools/SKILL.md) (PlantUML) |
| ER diagram | [mermaid](../mermaid/SKILL.md) (ERD) | [drawio](../drawio/SKILL.md) |
| Gantt / timeline | [mermaid](../mermaid/SKILL.md) | [drawio](../drawio/SKILL.md) |
| Pie / simple chart | [mermaid](../mermaid/SKILL.md) | [other-draw-tools](../other-draw-tools/SKILL.md) (matplotlib) |
| Bar / line / scatter / heatmap | [other-draw-tools](../other-draw-tools/SKILL.md) (matplotlib) | [mermaid](../mermaid/SKILL.md) |
| Git branch graph | [mermaid](../mermaid/SKILL.md) (git) | — |
| Mind map | [mermaid](../mermaid/SKILL.md) (mindmap) | [drawio](../drawio/SKILL.md) |
| BPMN | [visio](../visio/SKILL.md) | [drawio](../drawio/SKILL.md) |
| Org chart | [drawio](../drawio/SKILL.md) | [visio](../visio/SKILL.md) |
| Wireframe / sketch | [other-draw-tools](../other-draw-tools/SKILL.md) (Excalidraw) | [drawio](../drawio/SKILL.md) |
| Infographic | [drawio](../drawio/SKILL.md) | [other-draw-tools](../other-draw-tools/SKILL.md) (canvas-design) |

### Images

| Intent | Primary | Fallback |
|--------|---------|----------|
| Photo-realistic image | [nano-banana](../nano-banana/SKILL.md) (v2) | [gpt-image-2](../gpt-image-2/SKILL.md) |
| Quick concept iteration | [nano-banana](../nano-banana/SKILL.md) (v1) | [nano-banana](../nano-banana/SKILL.md) (v2) |
| Illustration / concept art | [gpt-image-2](../gpt-image-2/SKILL.md) | [nano-banana](../nano-banana/SKILL.md) (v2) |
| Logo / icon design | [gpt-image-2](../gpt-image-2/SKILL.md) | [nano-banana](../nano-banana/SKILL.md) (v2) |
| Poster / design artifact | [other-draw-tools](../other-draw-tools/SKILL.md) (canvas-design) | [gpt-image-2](../gpt-image-2/SKILL.md) |
| Scientific schematic | [other-draw-tools](../other-draw-tools/SKILL.md) (scientific-schematics) | [drawio](../drawio/SKILL.md) |

> Full decision table with detailed notes: [references/routing-matrix.md](./references/routing-matrix.md)

## Per-Skill Quick Reference

### drawio — Diagrams via MCP

- **Best for**: flowcharts, architecture, network, cloud infra, patent figures, academic paper diagrams
- **Limitations**: needs MCP server running; not suitable for quick inline diagrams
- **Quick start**: `Create a flowchart showing [process] with [N] steps and [decision point]. Use orthogonal connectors.`
- **Resources**: [style-presets.md](../chinese-patent/drawio/references/style-presets.md), [ah-to-xml.md](../chinese-patent/drawio/references/ah-to-xml.md)

### mermaid — Text-to-Diagram

- **Best for**: sequence diagrams, ERDs, Gantt charts, state machines, git graphs, quick embedded diagrams in markdown
- **Limitations**: auto-layout only (no pixel-level control), limited UML support
- **Quick start**: 
  ````markdown
  ```mermaid
  graph TD
      A[Start] --> B{Decision?}
      B -->|Yes| C[Action]
  ```
  ````
- **Templates**: [../mermaid/templates/mermaid-prompts.md](../mermaid/templates/mermaid-prompts.md)

### visio — VSDX Format Bridge

- **Best for**: deliverables requiring .vsdx format, enterprise clients, BPMN with Visio stencils
- **Limitations**: no programmatic API; requires draw.io desktop for VSDX export
- **Quick start**: Draw in Draw.io → `export_diagram` → open in draw.io desktop → Export as VSDX → polish in Visio
- **Workflow**: see [visio SKILL.md](../visio/SKILL.md) for full bridge workflow

### gpt-image-2 — OpenAI Image Generation

- **Best for**: detailed prompt-following illustrations, concept art, logos, icons
- **Limitations**: needs `OPENAI_API_KEY`; unreliable text rendering; URL expires in 1 hour
- **Quick start**: `Generate an illustration of [subject], [style], [mood]. [Key details].`
- **Templates**: [../gpt-image-2/templates/gpt-image-prompts.md](../gpt-image-2/templates/gpt-image-prompts.md)

### nano-banana — fal-ai Image Generation (v1/v2)

- **Best for**: photo-realistic images, fast concept iteration (v1), final quality output (v2)
- **Limitations**: needs fal-ai MCP server; no inpainting/outpainting
- **Quick start (v2)**: `Generate a photorealistic [subject], [environment], [lighting], [mood]. Highly detailed, 8k.`
- **Quick start (v1)**: `[Subject], [style], [key details], [mood]. High quality.`
- **Templates**: [../nano-banana/templates/nano-banana-prompts.md](../nano-banana/templates/nano-banana-prompts.md)

### other-draw-tools — PlantUML, Excalidraw, matplotlib, canvas-design, scientific-schematics

- **Best for**: UML (PlantUML), hand-drawn sketches (Excalidraw), data charts (matplotlib), posters (canvas-design), publication schematics (scientific-schematics)
- **Limitations**: diverse set — pick the right sub-tool
- **Quick start**: see [other-draw-tools SKILL.md](../other-draw-tools/SKILL.md) for per-tool quick starts

## Multi-Tool Workflows

### Workflow 1: Architecture Diagram for Visio Delivery
```
1. [drawio] Create the architecture diagram with MCP
2. [drawio] Export as .drawio file
3. [visio] Open in draw.io desktop, Export → VSDX
4. [visio] Polish in Microsoft Visio (themes, stencils, page setup)
```

### Workflow 2: Paper Figure Pipeline
```
1. [drawio] Draw architecture/pipeline diagram (grayscale, LaTeX, 300 DPI)
2. [other-draw-tools] Generate results chart with matplotlib
3. Combine both figures for the paper
4. Export as EPS/PDF for journal submission
```

### Workflow 3: Presentation Deck Imagery
```
1. [nano-banana] Generate hero image (16:9, v2) for title slide
2. [drawio] Draw simplified architecture diagram for slide 3
3. [other-draw-tools] Generate data chart (matplotlib) for slide 5
4. [gpt-image-2] Generate concept illustration for slide 7
```

### Workflow 4: Quick Technical Documentation
```
1. [mermaid] Embed sequence diagram in API docs
2. [mermaid] Embed ERD in database docs
3. [mermaid] Embed git graph in release notes
4. [drawio] Create full architecture diagram for the overview page
```

### Workflow 5: Iterative Image Exploration
```
1. [nano-banana] Quick v1 iterations (2-3 prompt variations, fast)
2. [nano-banana] Refine best direction with v2 (higher quality)
3. [gpt-image-2] Generate alternative style if needed
```

## Template Index

### Diagram Templates
| File | Type | Count |
|------|------|-------|
| [mermaid/templates/mermaid-prompts.md](../mermaid/templates/mermaid-prompts.md) | Mermaid diagram prompts | 20+ templates |
| [omnidraw/templates/scenario-prompts.md](./templates/scenario-prompts.md) | Multi-scenario dispatch prompts | 15+ scenarios |

### Image Generation Templates
| File | Type | Count |
|------|------|-------|
| [gpt-image-2/templates/gpt-image-prompts.md](../gpt-image-2/templates/gpt-image-prompts.md) | GPT-Image-2 prompts by category | 15+ templates |
| [nano-banana/templates/nano-banana-prompts.md](../nano-banana/templates/nano-banana-prompts.md) | Nano Banana prompts by category | 15+ templates |

## Best Practices

### Tool Selection
1. **Start with the scenario** — are you writing a patent, paper, presentation, or documentation?
2. **Prefer zero-dependency tools** when quality is equivalent (Mermaid over Draw.io for quick flows)
3. **Use v1 for exploration, v2 for finals** (Nano Banana) — saves time and cost
4. **Draw.io for anything that needs precise layout** — Mermaid auto-layout can't be pixel-tuned
5. **Don't fight the tool** — if you need UML, use PlantUML not Mermaid; if you need photos, use Nano Banana not Draw.io

### Prompt Writing
1. **Be specific about the output format** (file type, resolution, color/B&W)
2. **Name the scenario** in your request ("for an IEEE paper", "for a Chinese patent")
3. **Specify constraints upfront** (grayscale, font size, export format)
4. **Use style keywords** from the respective tool's reference guides
5. **Iterate** — generate a draft, review, refine (especially for images)

### Cross-Tool Consistency
1. **Use the same color palette** across diagrams in the same document
2. **Match font sizes** — if Draw.io uses 15px, matplotlib should use ~12pt
3. **Consistent naming** — same component names across architecture diagram, sequence diagram, and ERD

## Troubleshooting

| Issue | Check |
|-------|-------|
| Draw.io MCP not responding | Verify `npx drawio-mcp-server` runs manually |
| Mermaid not rendering | Validate syntax at https://mermaid.live |
| Visio export missing shapes | Re-route connectors in Visio after import |
| GPT-Image-2 401 error | Check `OPENAI_API_KEY` is set and valid |
| Nano Banana poor quality | Switch to v2, increase inference steps, add quality boosters |
| matplotlib Chinese garbled | Set `plt.rcParams['font.sans-serif']` for Chinese font |
| Wrong tool selected | Describe your scenario and intent; re-dispatch from Scenario Dispatch table |

## Resources

- [routing-matrix.md](./references/routing-matrix.md) — Full decision table with 40+ rows and tool capability comparison
- [scenario-prompts.md](./templates/scenario-prompts.md) — Copy-paste dispatch prompts for 15+ scenarios
- Each tool skill's SKILL.md and templates/ for deep-dive guidance
