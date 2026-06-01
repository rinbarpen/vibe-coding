# Document Creation Command Definitions

Defines the core commands for the docx manifest. AI agents should execute these commands following the specified logic and referencing the associated skills.

| Command | Description | Execution Logic | Referenced Skills |
|---------|-------------|-----------------|-------------------|
| `vibe-docx-merge <files>` | Merge multiple docx files | Uses python-docx to copy content between documents, preserving styles. Works on copies, not originals. | `skills/anthropics/skills/docx` |
| `vibe-docx-templating <template> <data>` | Apply variable substitution | Loads template .dotx, replaces placeholders with data dictionary, saves to new file. | `skills/anthropics/skills/docx` |
| `vibe-docx-convert <input> <format>` | Convert between formats | Uses pandoc for md-to-docx and docx-to-md; python-docx for structural transforms. | `skills/anthropics/skills/docx` |
| `vibe-docx-stats` | Document statistics | Analyzes docx for word count, paragraph count, style usage, section count. | `skills/anthropics/skills/docx` |
| `vibe-docx-validate <file>` | Validate document structure | Verifies sections, paragraphs, styles, images, and embedded objects are intact. | `skills/anthropics/skills/docx`, `manifests/docx/skills/docx-advanced/SKILL.md` |
