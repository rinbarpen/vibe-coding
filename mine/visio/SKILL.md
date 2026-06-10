---
name: visio
description: Microsoft Visio diagram creation guidance via Draw.io bridge workflow. Since Visio has no API or MCP server, this skill documents the recommended Draw.io→VSDX export pipeline, manual Visio conventions, and template recommendations for users who must deliver in Visio format.
---

# Visio Diagram Skill

Microsoft Visio format support via Draw.io bridge. Since Visio has no programmatic API or MCP server, the recommended workflow is: draw in Draw.io (MCP) → export to VSDX.

## When to Use

- Deliverable requires `.vsdx` format
- Enterprise/client mandates Visio
- Need Visio-specific stencils or templates
- Integration with Microsoft Office ecosystem
- Visio-specific features (data-linked shapes, org charts from Excel)

**If VSDX is not required**: prefer [Draw.io](../drawio/SKILL.md) or [Mermaid](../mermaid/SKILL.md) for faster iteration and programmatic control.

## Recommended Workflow: Draw.io → VSDX

### Step 1: Create in Draw.io (MCP)

Use the [drawio skill](../drawio/SKILL.md) to generate the diagram:

```
Create a system architecture diagram showing load balancer → web servers → app servers → database cluster
```

### Step 2: Export from Draw.io

Via MCP:
```
export_diagram to my-diagram.drawio
```

Or use the Draw.io MCP tools:
1. `get_diagram` to retrieve current diagram XML
2. `export_diagram` to save as `.drawio`

### Step 3: Convert to VSDX

**Option A — draw.io Desktop App (free)**:
1. Download draw.io desktop from https://github.com/jgraph/drawio-desktop/releases
2. Open the `.drawio` file
3. File → Export as → VSDX
4. Choose VSDX (Visio Drawing)

**Option B — drawio.com online**:
1. Go to https://app.diagrams.net
2. File → Open from → Device → select `.drawio` file
3. File → Export as → VSDX

**Option C — Automated (headless)**:
```bash
drawio --export --format vsdx --output output.vsdx input.drawio
```

### Step 4: Polish in Visio (if needed)

After conversion, open the VSDX in Visio to:
- Apply Visio themes and variants
- Add data-linked shapes
- Insert Visio-specific stencils
- Adjust page setup for printing

## Direct Visio Authoring

When you must work directly in Visio:

### Visio Template Selection

| Purpose | Template | Tab |
|---------|----------|-----|
| Software architecture | UML Component | Software |
| Database schema | Crow's Foot Database Notation | Software |
| Network diagram | Detailed Network Diagram | Network |
| Flowchart | Basic Flowchart | Flowchart |
| Org chart | Organization Chart | Business |
| Floor plan | Floor Plan | Maps & Floor Plans |
| Timeline | Timeline | Schedule |
| BPMN | BPMN Diagram | Flowchart |

### Visio Conventions

- **Font**: Segoe UI 10-12pt for labels, Calibri 14-16pt for titles
- **Connectors**: Right-angle (orthogonal) for architecture, curved for workflows
- **Layers**: Use layers to organize (background, main, annotations)
- **Page size**: Default to A4 (210×297mm) or Letter (8.5×11")
- **Export for sharing**: PDF (vector) for review, PNG (300 DPI) for embedding

### Visio Stencils

- Built-in: File → Shapes → choose category
- Download additional stencils from Microsoft, vendor sites (AWS, Azure, GCP)
- Custom stencils: Create via Shapes → My Shapes → New Stencil

## Diagram Type Mapping

| Diagram Type | Visio Template | Draw.io Equivalent |
|-------------|---------------|-------------------|
| Flowchart | Basic Flowchart | Flowchart |
| Org chart | Organization Chart | Org chart shapes |
| Network | Detailed Network Diagram | Network shapes |
| UML Class | UML Class | UML section |
| Database ERD | Crow's Foot Database Notation | ERD section |
| BPMN | BPMN Diagram | BPMN shapes |
| Floor plan | Floor Plan | Floor plan shapes |
| Timeline | Timeline | Timeline shapes |
| Cloud architecture | AWS/Azure/GCP stencils | Cloud shapes |

## Limitations

- **No programmatic API** — Visio has no public API or MCP server
- **No real-time collaboration** — Visio requires desktop app or SharePoint
- **Conversion fidelity** — Draw.io→VSDX may need minor adjustments (line routing, font substitution)
- **Stencil differences** — Some Draw.io shapes have no direct Visio equivalent
- **No live preview** — Unlike Draw.io MCP, no browser-based preview during creation

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Draw.io→VSDX shapes misplaced | Re-apply Visio auto-layout after import |
| Fonts different after export | Set Visio default font to match before import |
| Connectors become straight lines | Re-route in Visio or use orthogonal connectors in Draw.io |
| Cloud icons missing | Download official icon sets as Visio stencils |
| File size too large | Remove unused shapes and masters in Visio |
