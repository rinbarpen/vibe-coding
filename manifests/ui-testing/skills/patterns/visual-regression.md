# Visual Regression Pattern

**Category**: Visual Testing  
**When**: UI has intentional visual design that should not regress  
**Tools**: Percy, Chromatic, Playwright Snapshots, Loki

## Approach Selection

| Approach | Best For | Pros | Cons |
|----------|----------|------|------|
| Playwright Snapshots | Inline visual checks | Zero setup, in-repo | Large repo size, browser-specific diffs |
| Percy | CI-focused visual review | Cloud review UI, cross-browser | Paid, external dependency |
| Chromatic | Storybook integration | Component-level diffs, team review | Requires Storybook |
| Loki | Screenshot-based | Self-hosted, simple | Manual diff review |

## Playwright Snapshots

```typescript
test('homepage matches baseline', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png', {
    maxDiffPixelRatio: 0.02,   // Allow 2% pixel difference
    fullPage: true,              // Capture full scrollable page
  });
});
```

Configuration in `playwright.config.ts`:

```typescript
snapshotPathTemplate: '__screenshots__/{projectName}/{arg}{ext}',
```

Update snapshots intentionally: `npx playwright test --update-snapshots`

## Rules

- **Commit snapshots to repo**: Snapshots ARE code. Review them in PRs.
- **Max 2% diff threshold**: Adjust per component, document exceptions.
- **Isolate visual tests**: Use dedicated test files (e.g., `homepage.visual.spec.ts`).
- **CI-first**: Visual approvals happen in CI, not locally. Local diff means environment mismatch.
- **No dynamic content**: Freeze dates, random data, and animations in visual tests.
