# AGENTS.md

Instructions for AI agents working on document creation and Word manipulation projects.

## Repository Overview

Document authoring project using PreTeXt XML for source content and python-docx for programmatic Word document generation and manipulation.

## Iron Rule: Data Safety First

Every file modification follows this mandatory sequence:

1. **Branch**: Create a git branch for the operation (`docx/<task>`).
2. **Copy**: Work on a copy, never the original.
3. **Validate**: Verify structural integrity after every modification.
4. **Backup**: Timestamp the original before replacing it.
5. **Commit**: Checkpoint after each successful replacement.
6. **Merge**: Only merge after full validation.

## Core Flow (Document Creation)

1. **Plan**: Define document structure, audience, and output formats.
2. **Author (PreTeXt XML)**: Write structured content in `source/` using PreTeXt elements.
3. **Design**: Configure publisher settings, styles, and templates.
4. **Compile**: Build outputs and validate all cross-references.
5. **Review**: Use python-docx to inspect, validate, and polish the generated DOCX.
6. **Export**: Deliver final files in required formats (DOCX, PDF, HTML).

## Subagent Dispatching

Actively suggest and launch subagents based on task complexity:

- **`pretext-author`**: Expert in PreTeXt XML schema, element usage, and best practices for academic/professional publishing. Handles `pretext build`, cross-reference resolution, and publisher configuration.
- **`docx-engineer`**: Proficient in python-docx API for programmatic document creation, style application, and template processing.
- **`template-designer`**: Designs Word templates (.dotx) with proper styles, headers/footers, and formatting conventions.
- **`format-converter`**: Handles cross-format conversion (docx-to-md, md-to-docx, latex-to-docx) using pandoc and auxiliary tools.
- **`content-reviewer`**: Audits documents for structure consistency, style adherence, and reference integrity.

## Document Creation Standards

- **Source of Truth**: PreTeXt XML is the authoritative source; generated DOCX/PDF/HTML are derived outputs.
- **Style Separation**: Keep content (XML) separate from presentation (XSL/CSS/publisher config).
- **Modularity**: Split large documents into chapter-level XML files using `<xi:include>`.
- **Validation**: Always run `pretext build` to validate XML structure before final output.
- **Accessibility**: Ensure figures have `<description>` text, tables have headers, and color is not the sole differentiator.

## PreTeXt Cross-References

- Use `<xref ref="label"/>` for internal references to elements with `xml:id`.
- Use `<cite ref="bibkey"/>` for bibliography citations.
- Define labels with `xml:id` attributes on sections, figures, tables, and equations.
- Run `pretext build` to resolve all references; broken refs produce build warnings.

## Git Branch Workflow

- **Branch naming**: `docx/<task-description>` (e.g., `docx/add-appendix-b`, `docx/fix-cross-refs-ch4`)
- **Commit frequency**: After each successful validate→backup→replace cycle
- **Rollback**: `git checkout main && git branch -D docx/<task>` to abandon; `git revert <commit>` to undo one step
- **Never work on main**: All modifications start from and merge back to main only after validation

## Maintenance

- Keep `CLAUDE.md` updated with new commands and gotchas for document manipulation.
- When adding new PreTeXt elements or output targets, document usage patterns.
- Use `vibe-docx-stats` periodically to track document health.
