# CLAUDE.md

## Architecture
- **Document Source**: LaTeX (`.tex`), Markdown (`.md`), or Typst (`.typ`)
- **Bibliography**: BibTeX (`.bib`) or CSL
- **Assets**: Figures (PDF/PNG/SVG), Tables (CSV/TeX)
- **Output**: PDF, HTML, or DOCX

## Academic Commands
| Command | Description |
|---------|-------------|
| `latexmk -pdf main.tex` | Compile LaTeX to PDF |
| `typst compile main.typ` | Compile Typst to PDF |
| `vibe-check citations` | Verify all citations exist in .bib file |
| `vibe-check cross-refs` | Check for broken \ref or \cite links |
| `vibe-spell-check` | Run academic spell and grammar check |
| `vibe-gen-stats` | Generate word count and figure/table stats |

## Writing Guidelines
- **Academic Tone**: Use formal, objective language. Avoid contractions and slang.
- **Citation Consistency**: Ensure all claims are backed by citations in the required format (APA, IEEE, etc.).
- **Logical Flow**: Each paragraph should have a clear topic sentence and transition.
- **Mathematical Rigor**: Use standard notation and ensure all variables are defined.
