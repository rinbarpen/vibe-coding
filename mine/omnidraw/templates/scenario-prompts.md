# Omnidraw Scenario Prompt Templates

Copy-paste dispatch prompts organized by scenario. Each template includes the tool skill to invoke and a ready-to-use prompt for the user's specific content.

---

## Patent Figures (专利附图)

### Structure Diagram (结构示意图)
**Tool**: [drawio](../drawio/SKILL.md)
```
Draw a patent structure diagram (中国专利结构示意图) for [device/system name]:
- Show modules: [module A], [module B], [module C], [module D]
- Use orthogonal connectors, clean lines
- Font: 15px, black text
- Black-and-white only, no grayscale shading
- A–H format: A. Structure Diagram, B. [title], C. [nodes], D. [edges], E. Top-down, F. Patent, G. PNG 300dpi
- Caption outside image: 图[N] [title]结构示意图
```

### Flowchart (方法流程图)
**Tool**: [drawio](../drawio/SKILL.md)
```
Draw a patent method flowchart (中国专利方法流程图) for [method name]:
- Steps: [step1] → [step2] → [step3] → [decision step] → [branch A] / [branch B]
- Diamond for decision, rounded rect for steps, circle for start/end
- Font: 15px, Chinese labels
- Black-and-white, orthogonal lines
- Caption outside image: 图[N] [title]方法流程图
```

### Circuit / Connection Diagram (电路/连接图)
**Tool**: [drawio](../drawio/SKILL.md)
```
Draw a patent connection diagram for [circuit/system]:
- Components: [component 1] connected to [component 2] via [connection type]
- Show ports/interfaces between components
- Black-and-white, no shading
- Orthogonal lines, consistent spacing
- 15px labels inside components
```

---

## Academic Paper Figures (English)

### Architecture Diagram (IEEE)
**Tool**: [drawio](../drawio/SKILL.md)
```
Draw an IEEE-compliant architecture diagram for [system]:
- Show [N] main components with clear boundaries
- Grayscale only, no color
- LaTeX math for any formulas
- 300 DPI minimum
- Export as EPS/PDF
- Caption style: Fig. N. [Title].
- Use sans-serif font for labels, consistent spacing
```

### Pipeline / Training Flow
**Tool**: [mermaid](../mermaid/SKILL.md) or [drawio](../drawio/SKILL.md)
```
Create a pipeline diagram showing [process]:
- Stages: [stage1] → [stage2] → [stage3] → [stage4]
- Show data flow between stages
- Label dimensions of data at each stage
- Suitable for [conference — CVPR/NeurIPS/ICML/ACL]
- Single-column or dual-column layout as appropriate
```

### Results Comparison Chart
**Tool**: [other-draw-tools](../other-draw-tools/SKILL.md) (matplotlib)
```
Generate a matplotlib bar chart comparing [method] against [N] baselines:
- Metrics: [metric1], [metric2], [metric3]
- Baselines: [method A], [method B], [method C], [method D], Ours
- Include error bars (std dev over 5 runs)
- Use distinguishable grayscale patterns
- Font: serif, 12pt labels, 14pt title
- Save as PDF, 300 DPI
```

---

## Academic Paper Figures (Chinese, 中文期刊)

### 系统架构图
**Tool**: [drawio](../drawio/SKILL.md)
```
绘制用于[期刊名称]的系统架构图：
- [N]个主要模块：[模块A]、[模块B]、[模块C]、[模块D]
- 模块间用箭头标注数据流向
- 宋体 10-12pt 标注，图题为黑体 14pt
- 中英双语图注（如有缩写）
- 灰度图，300 DPI
- 导出为 EPS/PDF
- 图题：图N [系统名称]系统架构图
```

### 实验结果对比图
**Tool**: [other-draw-tools](../other-draw-tools/SKILL.md) (matplotlib)
```
用 matplotlib 绘制实验结果对比图：
- 对比指标：[指标1]、[指标2]
- 对比方法：[方法A]、[方法B]、[方法C]、本文方法
- 柱状图，灰度区分，添加误差棒
- 字体：宋体/SimSun，12pt
- 保存为 PDF，300 DPI
- 图题：图N [实验名称]结果对比
```

---

## Technical Architecture

### Microservices Architecture
**Tool**: [drawio](../drawio/SKILL.md)
```
Draw a microservices architecture diagram for [system name]:
- API Gateway → [Service A], [Service B], [Service C]
- Each service has its own database
- Shared Redis cache layer
- Message queue (RabbitMQ/Kafka) between [Service X] and [Service Y]
- Service discovery and config server
- Use layered layout: gateway layer → service layer → data layer
- Professional style with blue/green/gray palette
```

### Cloud Infrastructure (AWS)
**Tool**: [drawio](../drawio/SKILL.md)
```
Draw an AWS architecture diagram:
- Route 53 → CloudFront → ALB → ECS Fargate (2 AZs)
- RDS Multi-AZ with read replica
- ElastiCache Redis cluster
- S3 for static assets and backups
- CloudWatch for monitoring
- Use official AWS icons
- Group by VPC with public/private subnet boundaries
```

### System Context (C4)
**Tool**: [mermaid](../mermaid/SKILL.md) (C4Context)
```
Create a C4 system context diagram for [system]:
- Users/Actors: [list user types]
- Internal systems: [list internal systems]
- External systems: [list external dependencies]
- Show data flow direction on each relationship
```

---

## Presentation / Pitch Deck

### Hero Image (16:9)
**Tool**: [nano-banana](../nano-banana/SKILL.md) (v2)
```
Generate a 16:9 hero image for a presentation about [topic]:
[Subject description matching the talk theme], professional yet modern, [color palette matching brand], clean composition with space for title text overlay, cinematic lighting, 4k quality, abstract-tech style.
```

### Architecture Slide
**Tool**: [drawio](../drawio/SKILL.md)
```
Draw a presentation-ready architecture diagram for [system]:
- Keep it simple — max 6-8 components
- Use high-contrast colors for projector visibility
- Large font (18pt+), bold labels
- Include company/product logo area
- Export as high-res PNG (1920x1080)
- Dark or light theme depending on slide deck
```

### Data Chart Slide
**Tool**: [other-draw-tools](../other-draw-tools/SKILL.md) (matplotlib)
```
Generate presentation-ready data chart:
- [Chart type] showing [data]
- Large fonts (16pt+), high contrast
- Simple legend, minimal grid lines
- Slide aspect ratio (16:9)
- Save as PNG 1920x1080
- [Color palette — match brand]
```

---

## Quick / Embedded (Markdown)

### Quick Flowchart
**Tool**: [mermaid](../mermaid/SKILL.md)
```
````mermaid
graph TD
    A[[Start]] --> B[Process 1]
    B --> C{Decision?}
    C -->|Yes| D[Path A]
    C -->|No| E[Path B]
    D --> F[[End]]
    E --> F
````
```

### Quick API Sequence
**Tool**: [mermaid](../mermaid/SKILL.md)
```
````mermaid
sequenceDiagram
    Client->>API: POST /endpoint
    API->>DB: Query
    DB-->>API: Result
    API-->>Client: Response
````
```

### Quick ERD
**Tool**: [mermaid](../mermaid/SKILL.md)
```
````mermaid
erDiagram
    [Entity A] ||--o{ [Entity B] : has
    [Entity A] {
        string id PK
        string name
    }
    [Entity B] {
        string id PK
        string foreign_key FK
    }
````
```

---

## Visio Format Delivery

### Diagram for Visio Export
**Tool**: [drawio](../drawio/SKILL.md) → [visio](../visio/SKILL.md)
```
Step 1 — Draw in Draw.io:
"Draw a [diagram type] for [purpose]: [details]. Use standard shapes, orthogonal connectors, clear labels. Export as .drawio."

Step 2 — Convert:
"Open the .drawio file in draw.io desktop, File → Export as → VSDX."

Step 3 — Polish in Visio (optional):
"Open the VSDX in Visio. Apply [theme/template], adjust page setup for [A4/Letter], add any Visio-specific stencils."
```
