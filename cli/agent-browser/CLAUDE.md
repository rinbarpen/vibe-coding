# CLAUDE.md (Agent Browser)

Manifest for AI-powered browser automation using [agent-browser](https://github.com/vercel-labs/agent-browser) — a headless browser control library for AI agents. Supports navigation, interaction, extraction, and screenshot capture.

## Data Safety

1. **Sandbox first**: Test browser automation on non-production URLs.
2. **Rate limit**: Respect robots.txt and avoid aggressive scraping.
3. **Session isolation**: Use separate browser contexts for unrelated tasks.
4. **Screenshot validation**: Always verify visual output after complex interactions.

## Commands

| Command | Description |
|---------|-------------|
| `npx agent-browser goto <url>` | Navigate to a URL |
| `npx agent-browser click <selector>` | Click an element matching selector |
| `npx agent-browser type <selector> <text>` | Type text into an input field |
| `npx agent-browser extract <selector>` | Extract text content from elements |
| `npx agent-browser screenshot [path]` | Take a screenshot of the current page |
| `npx agent-browser evaluate <script>` | Run arbitrary JavaScript in the page |
| `npx agent-browser wait <selector>` | Wait for element to appear |
| `npx agent-browser form <json>` | Fill and submit a form from JSON |
| `npx agent-browser trace [path]` | Start/stop tracing for debugging |

## Architecture

```
<root>/
  scripts/            # Automation script repository
  sessions/           # Saved browser sessions (replayable)
  fixtures/           # Test data, form inputs, mock responses
  screenshots/        # Captured screenshots
  traces/             # Browser traces for debugging
  reports/            # Automation run reports
```

## Key Files

- `skills/agent-skills` — Agent browser skill definitions (submodule)
- `manifests/agent-browser` — This manifest configuration

## Workflow

1. **Plan**: Define the browser automation goal (scrape, test, fill form).
2. **Script**: Write or compose agent-browser commands in a script file.
3. **Sandbox**: Run in a sandbox/non-production environment first.
4. **Verify**: Check screenshots and extracted data for correctness.
5. **Production**: Deploy with rate limiting and error handling.

## Gotchas

- **Headless detection**: Some sites block headless browsers. Use stealth options if needed.
- **Dynamic content**: SPAs may require explicit `wait` calls after navigation.
- **Selector fragility**: Prefer data-testid or semantic selectors over fragile CSS class chains.
- **Session reuse**: Use session saving to avoid re-login in multi-step workflows.
- **Rate limiting**: Add delays between requests for public websites.
