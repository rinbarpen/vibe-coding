# docx — docx-polar Pipeline

Word document engineering via the docx-polar pipeline. Supports template extraction, structured document generation, and industry-specific rules.

## Architecture

docx-polar pipeline (`/home/rczx/workspace/rinbarpen/work/docx-polar`):

```
extract_template.py → YAML style spec → write_docx.py → formatted DOCX → review → PASS
```

## Commands

| Command | Description |
|---------|-------------|
| `office-cli docx polar init <name> --feat <feat>` | Initialize docx-polar project with industry feature |
| `office-cli docx polar pipeline <name>` | Run full pipeline (generate → extract → apply → review) |
| `office-cli docx polar extract <template>` | Extract formatting template from reference DOCX |
| `office-cli docx polar write <spec>` | Generate DOCX from YAML specification |
| `office-cli docx polar review <file>` | Run content + style + citation review |
| `office-cli docx polar humanize <file>` | Remove AI writing patterns (EN/CN) |
| `office-cli docx validate <file>` | Structural validation |

## Workflow

1. **Init** — `office-cli docx polar init <name> --feat <feat>`
2. **Extract** (if template available) — `extract_template.py <reference.docx>` → YAML
3. **Write** — `write_docx.py <spec.yaml> --output <output.docx>`
4. **Humanize** — Auto-called by write_docx.py (humanizer/humanizer-zh)
5. **Review** — `review_content.py` (images+tables) + style check + citation check
6. **Iterate** — If review fails, fix and re-run until PASS

## Supported Scenarios

| Scenario | Rules | Feature File |
|----------|-------|-------------|
| 中国专利 | `rules/patent.md` | Full CNIPA patent pipeline (invention/utility model/design) |

## CRITICAL Gotchas

- **Run from docx-polar root**: All scripts must run from `/home/rczx/workspace/rinbarpen/work/docx-polar`
- **Node.js required**: `docx` npm package must be installed globally for `write_docx.py`
- **Extract before write**: Always extract template first for format fidelity
- **Humanizer auto-called**: Do NOT manually run humanizer — `write_docx.py` handles it
- **Review gate mandatory**: Never deliver without passing review
- **Patent dispatch**: Set `type: patent` in YAML spec to auto-dispatch to patent-writer
- **Format**: Body 宋体 12pt, headings 黑体; all section order fixed per patent type
