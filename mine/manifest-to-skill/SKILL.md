---
name: manifest-to-skill
description: "Convert a manifest (CLAUDE.md + AGENTS.md + supporting assets under manifests/<name>/) into an installable skill under mine/<name>/. Use when the user says 'convert manifest X to skill', 'make X into a skill', or wants to repackage a project template as a reusable agent skill. Also triggers on 'manifest-to-skill', 'mts', 'convert manifest', 'manifest to skill'."
---

# Manifest → Skill Converter

Converts one or all manifests from `manifests/<name>/` into a standalone agent skill under `mine/<name>/` with a proper `SKILL.md` and supporting asset directories.

## Input / Output Contract

| Aspect | Value |
|--------|-------|
| **Source** | `manifests/<name>/` (must contain `CLAUDE.md` + `AGENTS.md`) |
| **Output root** | `mine/<name>/` |
| **Primary output** | `mine/<name>/SKILL.md` (YAML frontmatter + markdown body) |
| **Asset dirs** | Copied: `references/`, `scripts/`, `templates/`, `commands/`, `rules/`, `agents/`, `.github/`, `skills/` |
| **Traceability** | Original `CLAUDE.md` + `AGENTS.md` saved to `mine/<name>/source/` |
| **Validation** | Frontmatter regex-checked, all relative paths resolved |

## Workflow

### Phase 1: Analysis

1. If user specified a name, target `manifests/<name>/`. If user said "all" or listed nothing, iterate all 9 manifests.
2. Read `manifests/<name>/CLAUDE.md` and `manifests/<name>/AGENTS.md` in full.
3. List directory contents to discover: `references/`, `scripts/`, `templates/`, `commands/`, `rules/`, `agents/`, `.claude/agents/`, `.codex/agents/`, `.github/`, `skills/`.
4. Extract key metadata:
   - **Name**: the manifest directory name
   - **Description**: first sentence/paragraph from CLAUDE.md
   - **Commands**: all rows from the Commands table
   - **Workflow phases**: from AGENTS.md core flow
   - **Subagent dispatch**: from AGENTS.md dispatch table
   - **Gotchas**: any Gotchas section in CLAUDE.md

### Phase 2: Synthesis (generate SKILL.md)

Generate a single `SKILL.md` with this structure:

```yaml
---
name: <manifest-name>
description: "<first-sentence-of-CLAUDE.md>"
---
```

Then the markdown body:

```
# <Manifest Title>
## Overview
<1-2 paragraphs from CLAUDE.md>

## Commands
<Commands table from CLAUDE.md, paths converted to relative `<name>/commands/...`>

## Workflow
<Core flow from AGENTS.md, preserving phases, exit criteria>

### Subagent Dispatch
<Dispatch table from AGENTS.md; if none exists, omit>

## Sub-Skills
<Only if manifest has skills/ dir. For each sub-skill directory:
 read its SKILL.md, inline as an H3 section: name, description, key capabilities>

## Resources
<For each supporting dir found in Phase 1, list it with a one-line description>

## Gotchas
<If CLAUDE.md has a Gotchas section, copy it verbatim>
```

**Rules:**
- Keep it concise. Aim for 80-150 lines. Don't dump raw AGENTS.md text — summarize and structure.
- Preserve all commands from the manifest's Commands table verbatim (don't drop rows).
- For `skills/` subdirectories: read each sub-skill's `SKILL.md` frontmatter, extract `name` and `description`, and list them as H3 sections with a short summary of their key capabilities.
- For `agents/`, `.claude/agents/`, `.codex/agents/`: add a section pointing to the agent files, don't inline them.
- Do NOT copy `.gitignore`, `.editorconfig`, `CONTRIBUTING.md`, `README.md`.

### Phase 3: Asset Copy

Create `mine/<name>/` if it doesn't exist. Copy these directories from `manifests/<name>/`:

| Source | Destination | Condition |
|--------|-------------|-----------|
| `references/` | `mine/<name>/references/` | If exists |
| `scripts/` | `mine/<name>/scripts/` | If exists |
| `templates/` | `mine/<name>/templates/` | If exists |
| `commands/` | `mine/<name>/commands/` | If exists |
| `rules/` | `mine/<name>/rules/` | If exists |
| `.github/` | `mine/<name>/github/` | If exists (rename to avoid dot-prefix issues) |
| `skills/` | **DO NOT COPY** | Inlined in Phase 2 instead |

Use `cp -r` for each. Verify each copy with `ls`.

### Phase 4: Agent Definitions (if present)

If `.claude/agents/` and/or `.codex/agents/` exist in the manifest:

1. Create `mine/<name>/agents/`.
2. Copy `.claude/agents/*` → `mine/<name>/agents/claude/`.
3. Copy `.codex/agents/*` → `mine/<name>/agents/codex/`.
4. Add a section in SKILL.md: `## Agent Definitions` listing the copied agent files.

### Phase 5: Traceability

Save originals for reference:

```bash
mkdir -p mine/<name>/source
cp manifests/<name>/CLAUDE.md mine/<name>/source/
cp manifests/<name>/AGENTS.md mine/<name>/source/
```

### Phase 6: Validation

Check that:
1. `mine/<name>/SKILL.md` exists and has valid YAML frontmatter (starts with `---`, has `name:` and `description:`).
2. All relative paths used in SKILL.md (`commands/`, `references/`, etc.) point to existing directories/files under `mine/<name>/`.
3. For each sub-skill referenced in the Sub-Skills section, verify it was correctly summarized.

If validation fails, fix the issue before reporting completion.

## Conversion Template (per manifest)

Use this template for each manifest conversion. Replace `{{NAME}}` and `{{FIELDS}}`:

```markdown
---
name: {{NAME}}
description: "{{FIRST_SENTENCE}}"
---

# {{TITLE}}

{{OVERVIEW_PARAGRAPH}}

## Commands

{{COMMANDS_TABLE}}

## Workflow

{{WORKFLOW_SECTIONS}}

{{SUBAGENT_DISPATCH_TABLE}}

{{SUB_SKILLS_SECTION}}

## Resources

{{RESOURCE_LIST}}

{{GOTCHAS_SECTION}}
```

## Batch Mode ("all")

When converting all 9 manifests:

1. Run Phase 1-6 for each manifest sequentially.
2. Keep a checklist and mark each one `✅` or `❌` as you go.
3. Report a summary table at the end.

## Gotchas

- `skills/` dir in a manifest means sub-skills — inline them, don't copy the directory.
- `.claude/` and `.codex/` are dot-prefixed hidden dirs — rename to `agents/claude/` and `agents/codex/` when copying.
- After conversion, verify the output skill can stand alone: `SKILL.md` should not reference paths outside `mine/<name>/`.
- Some manifests (market-analysis, social-media) are minimal — their SKILL.md will be shorter. That's fine.
- If the manifest's AGENTS.md has an extremely long dispatch table, prioritize the top 3-5 entries and note "see source/AGENTS.md for full table".
