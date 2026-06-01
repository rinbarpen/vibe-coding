# Presentation Creation Command Definitions

Defines the core commands for the ppt manifest. AI agents should execute these commands following the specified logic and referencing the associated skills.

| Command | Description | Execution Logic | Referenced Skills |
|---------|-------------|-----------------|-------------------|
| `vibe-ppt-create <title> <slides>` | Create new presentation | Parses slide outline, generates slides via python-pptx, applies template. Works on new file, not existing. | `skills/anthropics/skills/pptx`, `manifests/ppt/skills/ppt-content/SKILL.md` |
| `vibe-ppt-template <file> <template>` | Apply slide master | Loads template .potx via ppt-master, applies to all slides. Always works on a copy first. | `manifests/ppt/skills/ppt-master-integration/SKILL.md`, `skills/anthropics/skills/pptx` |
| `vibe-ppt-animate <file>` | Standardize animations | Applies consistent transitions and entry animations via python-pptx. | `skills/anthropics/skills/pptx` |
| `vibe-ppt-notes <file>` | Manage speaker notes | Extracts all notes for review, or appends narrative to each slide. | `skills/anthropics/skills/pptx` |
| `vibe-ppt-export <file> <format>` | Export presentation | Converts to PDF/images via python-pptx save or ppt-master export. | `manifests/ppt/skills/ppt-master-integration/SKILL.md`, `skills/anthropics/skills/pptx` |
| `vibe-ppt-validate <file>` | Validate presentation structure | Verifies slides, layouts, images, notes are intact and consistent. | `skills/anthropics/skills/pptx`, `manifests/ppt/skills/ppt-content/SKILL.md` |
