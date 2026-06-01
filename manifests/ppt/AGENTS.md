# AGENTS.md

Instructions for AI agents working on presentation creation and slide deck automation.

## Repository Overview

Presentation automation project using ppt-master for slide master/template management and python-pptx for programmatic presentation generation.

## Iron Rule: Data Safety First

Every file modification follows this mandatory sequence:

1. **Branch**: Create a git branch for the operation (`ppt/<task>`).
2. **Copy**: Work on a copy, never the original.
3. **Validate**: Verify structural integrity after every modification.
4. **Backup**: Timestamp the original before replacing it.
5. **Commit**: Checkpoint after each successful replacement.
6. **Merge**: Only merge after full validation.

## Core Flow (Presentation Creation)

1. **Structure**: Define slide outline (title, content, speaker notes per slide).
2. **Theme**: Select or design slide master/template via ppt-master.
3. **Generate**: Build slide content programmatically using python-pptx.
4. **Enhance**: Add supporting visuals (charts, tables, images, diagrams).
5. **Polish**: Apply consistent formatting, animations, and transitions.
6. **Review**: Validate content, timing, and speaker notes alignment.
7. **Deliver**: Export to final format (pptx, pdf, images).

## Subagent Dispatching

Actively suggest and launch subagents based on task complexity:

- **`slide-designer`**: Expert in visual layout, typography, color theory, and slide composition. Ensures design consistency and visual hierarchy.
- **`content-organizer`**: Structures narrative flow, optimizes information density, and writes speaker notes. One key message per slide.
- **`animation-engineer`**: Applies transitions, animations, and timing with consistency and restraint. No decorative-only animations.
- **`template-master`**: Manages ppt-master configurations, slide masters (.potx), theme inheritance, and export settings.
- **`visual-editor`**: Creates and embeds charts, diagrams, tables, and images from source data.

## Content Architecture

- **Title Slide**: Project/conference name, presentation title, author, date.
- **Agenda Slide**: Outline of sections with time allocation.
- **Section Dividers**: Transition slides between major sections with section title.
- **Content Slides**: One key message per slide, supporting visuals, consistent layout.
- **Summary/Closing**: Key takeaways, next steps, call to action, Q&A.

## Design Standards

- **Grid System**: Align all elements to a consistent grid (4-column or 6-column).
- **Consistency**: Same fonts, colors, and layouts throughout the deck. One slide master.
- **Dual Encoding**: Support textual content with visual elements (charts, icons, diagrams).
- **Accessibility**: Ensure color contrast meets WCAG AA standards. Provide alt text for images.
- **Speaker Notes**: Every slide should have speaker notes (1-3 sentences per slide).

## Git Branch Workflow

- **Branch naming**: `ppt/<task-description>` (e.g., `ppt/create-investor-deck`, `ppt/apply-brand-theme`)
- **Commit frequency**: After each successful validate→backup→replace cycle
- **Rollback**: `git checkout main && git branch -D ppt/<task>` to abandon; `git revert <commit>` to undo one step
- **Never work on main**: All modifications start from and merge back to main only after validation

## Maintenance

- Keep `CLAUDE.md` updated with new commands and gotchas for presentation manipulation.
- When adding new ppt-master templates or themes, document them in `templates/README.md`.
- Periodically audit `_backups/` and prune old backups.
