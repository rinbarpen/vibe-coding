# CLAUDE.md

Manifest for professional presentation creation using ppt-master for slide template management and python-pptx for programmatic presentation manipulation.

## Data Safety (CRITICAL)

1. **NEVER modify the original file directly.**
2. **ALWAYS copy**: `cp original.pptx working.pptx`
3. **ALWAYS validate** the working copy before replacing the original.
4. **ALWAYS keep a backup**: `mv original.pptx _backups/original-{date}.pptx`
5. **EVERY modification happens on a git branch.**
6. **MERGE only after validation passes.**

## Commands

| Command | Description |
|---------|-------------|
| `git checkout -b ppt/<task>` | Create a branch before any file modification |
| `cp original.pptx working.pptx` | Create a safe working copy |
| `ppt-master init <name>` | Initialize a new presentation with ppt-master template |
| `ppt-master apply <template>` | Apply a slide master/template to existing deck |
| `ppt-master export <format>` | Export presentation to PDF, images, or video |
| `vibe-ppt-create <title> <slides>` | Create a new presentation from slide outline |
| `vibe-ppt-template <file> <template>` | Apply ppt-master template to python-pptx generated deck |
| `vibe-ppt-animate <file>` | Add/reorganize slide transitions and animations |
| `vibe-ppt-notes <file>` | Extract or generate speaker notes |
| `vibe-ppt-export <file> <format>` | Export to PDF, video, or image sequence |
| `vibe-ppt-validate <file>` | Validate presentation: slide count, layouts, images, notes |

## Architecture

```
<root>/
  source/        # Slide content definitions (YAML/JSON/Markdown outlines)
  templates/     # ppt-master slide master files and theme configurations
  output/        # Generated presentations (.pptx, .pdf, images)
  assets/        # Images, icons, logos, and media files
  scripts/       # python-pptx automation and build scripts
  notes/         # Speaker notes and presentation scripts
  _backups/      # Timestamped backups of original files
```

## Key Files

- `templates/slide-master.potx` — ppt-master slide master template
- `source/outline.yaml` — Slide content outline in structured format
- `skills/anthropics/skills/pptx` — Anthropic official pptx manipulation skill

## Presentation Design Guidelines

- **Slide Density**: Maximum 6 bullet points or 30 words per slide. One key message per slide.
- **Visual Hierarchy**: Title (bold, 28-36pt), body (24-28pt), captions (18-20pt).
- **Consistency**: Use a single slide master throughout the deck. Avoid mixing templates.
- **White Space**: Maintain adequate margins (0.5in minimum) and spacing between elements.
- **Color Palette**: Maximum 3 colors per slide. Use high-contrast combinations for readability.
- **Typography**: Limit to 2 font families per deck (one for headings, one for body).

## Workflow

1. **Branch**: `git checkout -b ppt/<task>` to isolate changes.
2. **Outline**: Define slide structure in `source/outline.yaml` with title, content, and notes per slide.
3. **Template Select**: Choose or create a ppt-master template/slide master.
4. **Build**: Generate slides programmatically using python-pptx and the anthropics pptx skill.
5. **Style**: Apply slide master, consistent colors, fonts, and layouts via ppt-master.
6. **Enhance**: Add charts, tables, images, and diagrams to support content.
7. **Animate**: Apply transitions and animations (subtle, consistent).
8. **Review**: Validate slide timing, speaker notes, and visual consistency.
9. **Commit**: `git add -A && git commit -m "ppt: <description>"` to checkpoint.
10. **Merge**: Only after full validation passes, merge back to main.

## Workflow Example

```bash
# Start a task
git checkout -b ppt/apply-corporate-theme

# Safe copy
cp presentation.pptx presentation_working.pptx

# Apply ppt-master template
ppt-master apply templates/corporate-theme.potx presentation_working.pptx

# Fine-tune with python-pptx
python -c "
from pptx import Presentation
prs = Presentation('presentation_working.pptx')
# ... adjust layouts, content ...
prs.save('presentation_working.pptx')
"

# Validate
python -c "
from pptx import Presentation
prs = Presentation('presentation_working.pptx')
print('Slides:', len(prs.slides))
for i, slide in enumerate(prs.slides):
    print(f'  Slide {i+1}: {slide.slide_layout.name}')
"

# Backup and replace
mv presentation.pptx _backups/presentation-$(date +%Y%m%d-%H%M%S).pptx
mv presentation_working.pptx presentation.pptx

# Commit checkpoint
git add -A && git commit -m "ppt: apply corporate theme to all slides"

# Merge after validation
git checkout main && git merge ppt/apply-corporate-theme
```

## Content Architecture

- **Title Slide**: Project/conference name, presentation title, author, date.
- **Agenda Slide**: Outline of sections with time allocation.
- **Section Dividers**: Transition slides between major sections with section title.
- **Content Slides**: One key message per slide, supporting visuals, consistent layout.
- **Summary/Closing**: Key takeaways, next steps, call to action, Q&A.

## Gotchas

- **python-pptx Limitations**: python-pptx cannot fully replicate the PowerPoint UI experience. Complex animations, SmartArt, and embedded video may not survive round-trip editing.
- **Slide Masters**: Apply the slide master before adding content. Changing masters mid-stream can orphan placeholder references.
- **Image Embedding**: python-pptx embeds images by file path. Ensure image paths are stable or copy assets to a working directory.
- **Font Licensing**: Embedded fonts may have licensing restrictions. Prefer standard fonts (Arial, Calibri, Times New Roman) for distribution.
- **Animation Timing**: python-pptx animation support is basic. For complex animations, use PowerPoint or ppt-master after initial generation.
- **Template Management**: Slide master and template operations are handled by `skills/anthropics/skills/pptx` and python-pptx. No separate CLI tool needed.
- **Backward Compatibility**: Save as `.pptx` (Office Open XML), not `.ppt` (legacy binary), for python-pptx compatibility.
- **File Size**: Compress images before embedding. Target <5MB for standard decks, <20MB for image-heavy decks.
