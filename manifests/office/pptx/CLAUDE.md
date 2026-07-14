# pptx — ppt-master + Aesthetic Design

PowerPoint creation via the ppt-master SVG-to-PPTX pipeline, combined with curated aesthetic design presets.

## Commands

| Command | Description |
|---------|-------------|
| `office-cli ppt master init <name> --style <preset>` | Initialize project with style preset |
| `office-cli ppt master strategist` | Execute 8 Strategist confirmations |
| `office-cli ppt master execute` | Generate SVGs and run quality checks |
| `office-cli ppt master export` | Export PPTX |
| `office-cli ppt master qa <file>` | Run QA verification |

## Workflow (Strict Serial Pipeline)

### Step 1: Source → Markdown
| Source | Command |
|--------|---------|
| PDF | `python3 skills/ppt-master/scripts/source_to_md/pdf_to_md.py <file>` |
| DOCX | `python3 skills/ppt-master/scripts/source_to_md/doc_to_md.py <file>` |
| XLSX | `python3 skills/ppt-master/scripts/source_to_md/excel_to_md.py <file>` |
| PPTX | `python3 skills/ppt-master/scripts/source_to_md/ppt_to_md.py <file>` |
| URL | `python3 skills/ppt-master/scripts/source_to_md/web_to_md.py <URL>` |
| Markdown | Read directly |

### Step 2: Project Init
```bash
python3 skills/ppt-master/scripts/project_manager.py init <name> --format ppt169
python3 skills/ppt-master/scripts/project_manager.py import-sources <path> <files...> --move
```

### Step 3: Template Option
Default = free design. Opt-in if user names a template.

### Step 4: Strategist Phase ⛔ BLOCKING
Read `references/strategist.md`. Present 8 Confirmations (bundled):
1. Canvas format
2. Page count range
3. Target audience
4. Style objective
5. Color scheme
6. Icon usage
7. Typography plan
8. Image usage

Output: `design_spec.md` + `spec_lock.md`

### Step 5: Image_Generator (Conditional)
Only if image approach includes "AI generation".

### Step 6: Executor Phase
- Read `executor-base.md` + `shared-standards.md` + one style file
- Generate SVGs **sequentially, one page at a time** — NO batching
- Before each page: `read_file <project_path>/spec_lock.md`
- Quality check: `svg_quality_checker.py` — fix all errors before proceeding
- Chart calibration: `svg_position_calculator.py` — MANDATORY gate

### Step 7: Post-processing & Export (sequential, one at a time)
```bash
python3 skills/ppt-master/scripts/total_md_split.py <project_path>
python3 skills/ppt-master/scripts/finalize_svg.py <project_path>
python3 skills/ppt-master/scripts/svg_to_pptx.py <project_path> -s final
```

## Aesthetic Design Presets

### 12 Style Presets (from frontend-slides)

| # | Preset | Vibe | Fonts | Palette |
|---|--------|------|-------|---------|
| 1 | **Bold Signal** | confident, high-impact | Archivo Black + Space Grotesk | Charcoal, hot orange, white |
| 2 | **Electric Studio** | clean, agency-polished | Manrope | Black, white, cobalt |
| 3 | **Creative Voltage** | energetic, retro-modern | Syne + Space Mono | Electric blue, neon yellow, navy |
| 4 | **Dark Botanical** | elegant, premium | Cormorant + IBM Plex Sans | Near-black, ivory, blush, gold |
| 5 | **Notebook Tabs** | editorial, organized | Bodoni Moda + DM Sans | Cream paper on charcoal |
| 6 | **Pastel Geometry** | approachable, friendly | Plus Jakarta Sans | Pale blue, cream, soft pink/mint |
| 7 | **Split Pastel** | playful, creative | Outfit | Peach + lavender split |
| 8 | **Vintage Editorial** | witty, magazine-inspired | Fraunces + Work Sans | Cream, charcoal, dusty warm |
| 9 | **Neon Cyber** | futuristic, techy | Clash Display + Satoshi | Midnight navy, cyan, magenta |
| 10 | **Terminal Green** | developer-focused | JetBrains Mono | GitHub dark + terminal green |
| 11 | **Swiss Modern** | minimal, precise | Archivo + Nunito | White, black, signal red |
| 12 | **Paper & Ink** | literary, thoughtful | Cormorant Garamond + Source Serif 4 | Warm cream, charcoal, crimson |

### Mood → Preset Mapping

| Mood | Presets |
|------|---------|
| Impressed / Confident | Bold Signal, Electric Studio, Dark Botanical |
| Excited / Energized | Creative Voltage, Neon Cyber, Split Pastel |
| Calm / Focused | Notebook Tabs, Paper & Ink, Swiss Modern |
| Inspired / Moved | Dark Botanical, Vintage Editorial, Pastel Geometry |

### 10 ppt-master Curated Color Schemes
Midnight Executive, Forest & Moss, Coral Energy, Warm Terracotta, Ocean Gradient, Charcoal Minimal, Teal Trust, Berry & Cream, Sage Calm, Cherry Bold

### Design Density Limits

| Slide Type | Max Content |
|------------|-------------|
| Title | 1 heading + 1 subtitle + optional tagline |
| Content | 1 heading + 4-6 bullets or 2 short paragraphs |
| Feature grid | 6 cards max |
| Code | 8-10 lines max |
| Quote | 1 quote + attribution |
| Image | 1 image, ideally under 60vh |

## CRITICAL Gotchas

- **NEVER use `#` with hex colors** — `color: "FF0000"` correct, `color: "#FF0000"` corrupts the file
- **NEVER encode opacity in hex** — use `opacity` property instead
- **NEVER use unicode `•` for bullets** — use `bullet: true`
- **NEVER reuse option objects across pptxgenjs calls** — PptxGenJS mutates objects in-place
- **SERIAL EXECUTION** — Steps MUST execute in order; no cross-phase bundling
- **NO sub-agent SVG generation** — Executor must generate all SVGs in main agent
- **Spec_lock re-read per page** — Before each SVG, read `spec_lock.md` again; resist context drift
- **Every slide needs a visual element** — never create text-only slides
- **shadow `offset` must be non-negative** — negative values corrupt the file
- **QA cycle mandatory** — convert to PDF → images → visual inspect → fix → re-verify; at least one complete cycle before declaring done
