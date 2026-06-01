# CLAUDE.md

Manifest for professional Word document creation using PreTeXt XML authoring for text layout/typesetting and python-docx for programmatic document manipulation.

## Data Safety (CRITICAL)

1. **NEVER modify the original file directly.**
2. **ALWAYS copy**: `cp original.docx working.docx`
3. **ALWAYS validate** the working copy before replacing the original.
4. **ALWAYS keep a backup**: `mv original.docx _backups/original-{date}.docx`
5. **EVERY modification happens on a git branch.**
6. **MERGE only after validation passes.**

## Commands

| Command | Description |
|---------|-------------|
| `git checkout -b docx/<task>` | Create a branch before any file modification |
| `cp original.docx working.docx` | Create a safe working copy |
| `pretext build` | Compile PreTeXt source to all output formats (HTML, PDF, DOCX) |
| `pretext build html` | Generate HTML output for preview |
| `pretext build pdf` | Generate PDF via LaTeX |
| `pretext view` | Start local preview server for PreTeXt output |
| `pretext generate --stringparam publisher target` | Generate specific output format via publisher config |
| `vibe-docx-merge <files>` | Merge multiple docx files using python-docx |
| `vibe-docx-templating <template> <data>` | Apply Jinja2-style templating to docx |
| `vibe-docx-convert <input> <format>` | Convert between docx, markdown, latex using pandoc |
| `vibe-docx-stats` | Report document statistics (word count, style usage, revision count) |
| `vibe-docx-validate <file>` | Validate document structure: sections, styles, references, images |

## Architecture

```
<root>/
  source/              # PreTeXt XML source files (*.ptx)
    main.ptx           # Root document (includes chapters via <xi:include>)
    chapters/          # Chapter-level XML files
    frontmatter/       # Title page, abstract, TOC configuration
    backmatter/        # Appendices, bibliography, index
  assets/              # Images, figures, external resources
  output/              # Generated outputs (HTML, PDF, DOCX)
  styles/              # Custom CSS, XSL, or publisher configuration
  templates/           # Reference docx templates for style inheritance
  scripts/             # python-docx automation scripts
  _backups/            # Timestamped backups of original files
```

## Key Files

- `source/main.ptx` — Root PreTeXt document entry point
- `publication.ptx` — PreTeXt output format configuration
- `skills/anthropics/skills/docx` — Anthropic official docx manipulation skill

## PreTeXt XML Authoring Guidelines

- Use `<section>`, `<subsection>`, `<title>` for document hierarchy.
- Use `<p>` for paragraphs, `<em>` and `<bold>` for inline emphasis.
- Use `<list>` with `<li>` for bulleted/numbered lists.
- Use `<table>` with `<row>` and `<cell>` for tabular data.
- Use `<figure>` with `<image>` for figures and diagrams; add `<description>` for accessibility.
- Use `<xref ref="label"/>` for internal cross-references, `<cite ref="bibkey"/>` for citations.
- Define bibliography in `<bibliography>` with `<biblio>` entries.
- Use `<xi:include href="chapters/file.ptx"/>` to split large documents into modular files.
- Define `xml:id` on all major elements for cross-referencing.
- Run `pretext build` to validate XML structure before final output.

## PreTeXt Output Targets

| Target | Command | Use Case |
|--------|---------|----------|
| HTML   | `pretext build html` | Web publication, online reading, quick review |
| PDF    | `pretext build pdf`  | Print, submission, formal distribution |
| DOCX   | Via LaTeX intermediary | Word format for collaborators |

## Workflow

1. **Branch**: `git checkout -b docx/<task>` to isolate changes.
2. **Plan**: Outline document structure in `source/main.ptx` with skeleton sections.
3. **Author**: Write content in modular `source/chapters/*.ptx` files using PreTeXt XML.
4. **Compile**: Run `pretext build` to validate and generate outputs.
5. **Review**: Inspect generated HTML/PDF/DOCX for formatting issues.
6. **Refine**: Adjust XML structure, styles, or templates as needed.
7. **Polish**: Use python-docx (via anthropics/docx skill) for fine-tuning DOCX output.
8. **Commit**: `git add -A && git commit -m "docx: <description>"` to checkpoint.
9. **Merge**: Only after full validation passes, merge back to main.

## Workflow Example

```bash
# Start a task
git checkout -b docx/reformat-chapter-3

# Author in PreTeXt XML
vim source/chapters/chapter-3.ptx

# Compile and validate
pretext build
pretext view  # Preview in browser

# For docx-specific fine-tuning, use the copy-first safety workflow
cp output/manuscript.docx output/manuscript_working.docx
python -c "
from docx import Document
doc = Document('output/manuscript_working.docx')
# ... modify styles, formatting ...
doc.save('output/manuscript_working.docx')
"

# Validate structure
python -c "
from docx import Document
doc = Document('output/manuscript_working.docx')
print('Sections:', len(doc.sections))
print('Paragraphs:', len(doc.paragraphs))
"

# Backup and replace
mv output/manuscript.docx _backups/manuscript-$(date +%Y%m%d-%H%M%S).docx
mv output/manuscript_working.docx output/manuscript.docx

# Commit checkpoint
git add -A && git commit -m "docx: reformat chapter 3 with consistent heading styles"

# Merge after validation
git checkout main && git merge docx/reformat-chapter-3
```

## Gotchas

- **PreTeXt Installation**: Requires Python 3 and a LaTeX distribution (TeX Live). Run `pip install pretext` to install. TeX Live is ~4GB; for HTML-only workflows, LaTeX is optional.
- **Font Embedding**: DOCX output depends on system fonts. Explicitly specify fonts in the publisher file.
- **Cross-Reference Stability**: PreTeXt cross-references resolve at compile time; always `pretext build` before final delivery.
- **Image Paths**: Use relative paths in `<image>` elements; PreTeXt resolves from source directory.
- **Chinese Content**: PreTeXt supports UTF-8; ensure the LaTeX engine is configured for CJK fonts when outputting PDF with Chinese text.
- **python-docx Limitations**: python-docx cannot preserve all native Word features (some advanced formatting, tracked changes, embedded OLE objects). Use it for template-based generation, not round-trip editing.
- **Section Numbering**: PreTeXt handles section numbering automatically; do not manually number section titles in XML.
- **Large Documents**: Split into chapter-level `<xi:include>` files. Compiling a single 100K-line .ptx is slow.
