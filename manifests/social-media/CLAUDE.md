# CLAUDE.md

Dedicated manifest for social media content creation, polishing, and distribution.

## Commands

| Command | Description |
|---------|-------------|
| `vibe-draft <topic>` | Generate a content draft for a specific topic |
| `vibe-polish` | Apply Chinese copywriting guidelines and beautiful prose style |
| `vibe-lint-text` | Check for common Chinese typesetting issues |
| `vibe-gen-image-prompt` | Generate DALL-E/Midjourney prompts for content illustrations |
| `vibe-summarize` | Generate social media snippets (TL;DR, Twitter thread, etc.) |
| `vibe-export <format>` | Export content to Markdown, PDF, or HTML |

## Content Standards

- **Typesetting**: Follow `skills/chinese-copywriting-guidelines/SKILL.md`.
- **Style**: Use `skills/beautiful_prose/SKILL.md` for high-quality English/Chinese prose.
- **Tone**: Professional, engaging, and authentic. Avoid AI-sounding filler.
- **Visuals**: Matplotlib charts must use English labels (as per core rules).

## Architecture

```
<root>/
  content/      # Raw drafts and final posts
  assets/       # Images, diagrams, and media
  templates/    # Platform-specific templates (WeChat, Red, X)
  scripts/      # Automation scripts for distribution
```

## Workflow

1. **Ideation**: Research and brainstorm topics using `SemanticSearch`.
2. **Drafting**: Create initial content structure.
3. **Refining**: Use `vibe-polish` to enhance readability and impact.
4. **Reviewing**: Self-audit using `vibe-lint-text`.
5. **Finalizing**: Generate metadata and export.

## Gotchas

- Always run `proxy_on` before fetching external research data.
- Ensure all Chinese-English mixed text has proper spacing.
- Use `Beautiful Prose` skill for any formal announcements or long-form articles.
