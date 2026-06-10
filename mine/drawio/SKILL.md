---
name: drawio
description: AI-powered Draw.io diagram generation via MCP server. Create flowcharts, architecture diagrams, network topologies, cloud infrastructure diagrams (AWS/GCP/Azure), sequence diagrams, and more using natural language. Supports real-time browser preview, structured A–H format extraction, LaTeX math in labels, and export to .drawio files.
---

# Draw.io Diagram Skill

AI-powered Draw.io diagram generation with real-time browser preview via MCP server.

## When to Use

- Flowcharts, process diagrams, decision trees
- System/software architecture diagrams
- Network topology and infrastructure diagrams
- Cloud architecture (AWS, GCP, Azure)
- Sequence diagrams, UML diagrams
- Patent structure/relationship figures
- Academic paper figures (IEEE, ACM, Elsevier)
- Infographics and technical illustrations

## MCP Server

This skill uses the Draw.io MCP server configured in the project root `mcp.json`:

```json
{
    "drawio": {
        "command": "npx",
        "args": ["-y", "drawio-mcp-server"]
    }
}
```

**Alternative**: `mine/chinese-patent/drawio/` uses `@next-ai-drawio/mcp-server@0.1.15` with additional features (browser preview, version history).

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `start_session` | Opens browser with real-time diagram preview |
| `create_new_diagram` | Create a new diagram from XML |
| `edit_diagram` | Edit diagram by ID-based operations |
| `get_diagram` | Get the current diagram XML |
| `export_diagram` | Save diagram to a `.drawio` file |

## Quick Start

### Flowchart

```
Create a flowchart showing user registration: sign up form → email validation → create account → send welcome email. Use decision diamond for email validation.
```

### System Architecture

```
Draw a microservices architecture: API Gateway → Auth Service, User Service, Order Service → each with its own DB. Add Redis cache layer and message queue between services.
```

### Cloud Architecture (AWS)

```
Generate an AWS architecture diagram with Lambda, API Gateway, DynamoDB, S3, and CloudFront for a serverless web app.
```

### Sequence Diagram

```
Create a sequence diagram showing OAuth 2.0 authorization code flow between user, client app, authorization server, and resource server.
```

## Diagram Types & Guidance

| Type | Best For | Style Tips |
|------|----------|------------|
| Flowchart | Process, decision logic | Orthogonal connectors, diamonds for decisions |
| Architecture | System design, microservices | Layered layout, clear service boundaries |
| Network | Infrastructure, topology | Icon-based, subnets as containers |
| Cloud | AWS/GCP/Azure | Use official cloud icons |
| Sequence | API flows, protocols | Lifelines, activation bars |
| UML | Class, component, deployment | Standard UML notation |
| ERD | Database schema | Crow's foot notation |
| Infographic | Visual explanation | Rich styling, icons, grouping |

## Style Presets

See [`mine/chinese-patent/drawio/references/style-presets.md`](../chinese-patent/drawio/references/style-presets.md) for copy-paste style strings.

Quick reference:
- **Primary node**: `rounded=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=15`
- **Success/Data node**: `rounded=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=15`
- **Warning/Constraint node**: `rounded=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=15`
- **Container**: `rounded=1;fillColor=#f5f5f5;strokeColor=#999999;fontSize=14`

## A–H Structured Format

For complex diagrams, use the A–H extraction format (see [`mine/chinese-patent/drawio/references/ah-to-xml.md`](../chinese-patent/drawio/references/ah-to-xml.md)):

```
A. Diagram Type: Architecture / Flowchart / Network / ...
B. Title: [Diagram title]
C. Nodes: [List of nodes with labels and types]
D. Edges: [List of connections with labels]
E. Layout: Top-down / Left-right / Layered
F. Style: Professional / Patent / Academic / Cloud
G. Export: .drawio / .png / .svg
H. Notes: [Additional constraints or requirements]
```

## Patent Figure Conventions

When drawing for Chinese patents:
- Use 15px font size for in-figure text
- Keep figure captions outside the image (e.g., `图1 系统结构示意图`)
- Black-and-white preferred, clean orthogonal lines
- No grayscale shading unless essential
- LaTeX for mathematical expressions

See [`mine/chinese-patent/drawio/references/ieee-network-diagrams.md`](../chinese-patent/drawio/references/ieee-network-diagrams.md).

## Academic Paper Figures

See [`mine/chinese-patent/drawio/references/ieee-network-diagrams.md`](../chinese-patent/drawio/references/ieee-network-diagrams.md) for IEEE/academic publication standards.

Key conventions:
- IEEE: EPS/PDF, grayscale, 300 DPI minimum
- ACM: PDF/PNG, LaTeX math
- Elsevier: TIFF/EPS/PDF
- Export as vector format (SVG/PDF) when possible

## Troubleshooting

| Issue | Solution |
|-------|----------|
| MCP server won't start | Run `npx -y drawio-mcp-server` manually to check |
| Diagram not rendering | Verify XML is valid; check `get_diagram` output |
| Math not displaying | Wrap in `$$` for LaTeX; use AsciiMath for simple formulas |
| Export fails | Ensure `.drawio` extension in file path |
| Style not applying | Use semicolons as separators in style string |

## Resources

- [style-presets.md](../chinese-patent/drawio/references/style-presets.md) — Copy-paste style strings
- [ah-to-xml.md](../chinese-patent/drawio/references/ah-to-xml.md) — A–H to XML converter
- [structured-diagram-prompts.md](../chinese-patent/drawio/references/structured-diagram-prompts.md) — Domain-specific prompt configs
- [ieee-network-diagrams.md](../chinese-patent/drawio/references/ieee-network-diagrams.md) — Academic publication standards
- [math-typesetting.md](../chinese-patent/drawio/references/math-typesetting.md) — LaTeX/AsciiMath in diagrams
- [drawio-aesthetic-guide.md](../chinese-patent/drawio/references/drawio-aesthetic-guide.md) — Visual design guide
- [mcp-tools.md](../chinese-patent/drawio/references/mcp-tools.md) — Full MCP tool API reference
