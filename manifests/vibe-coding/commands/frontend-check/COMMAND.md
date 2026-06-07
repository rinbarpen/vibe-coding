# /frontend-check

Run frontend-specific quality checks: accessibility, performance, bundle analysis,
visual regression.

## Usage

```
/frontend-check <mode>
```

### Modes

| Mode | Tools | What it checks |
|------|-------|----------------|
| `accessibility` | axe-core, pa11y-ci, jsx-a11y | WCAG 2.1 AA violations |
| `performance` | Lighthouse CI, Web Vitals | LCP < 2.5s, INP < 200ms, CLS < 0.1 |
| `bundle` | vite-bundle-analyzer, @next/bundle-analyzer | JS < 150KB (landing) / 300KB (app), CSS < 30KB / 50KB |
| `visual` | Playwright screenshots, Chromatic | Visual regression vs baseline |
| `all` | All of the above | Full quality gate |

## Execution

1. Start dev server (`pnpm dev`) if not already running
2. Run the selected check tools
3. Compare against budget/threshold targets
4. Report pass/fail per check

## Check Details

### Accessibility (`accessibility`)
- `npx axe http://localhost:3000` or `npx pa11y-ci`
- ESLint `jsx-a11y` plugin — zero violations
- Keyboard navigation: Tab/Enter/Escape through all interactive elements
- Color contrast: AAA for text, AA for large text (>18pt)

### Performance (`performance`)
- Lighthouse CI with per-page budgets
- Core Web Vitals: LCP < 2.5s, INP < 200ms, CLS < 0.1, FCP < 1.5s
- Run on mobile (slow 4G) and desktop profiles

### Bundle (`bundle`)
- Landing page: JS < 150KB gzipped, CSS < 30KB
- App page: JS < 300KB gzipped, CSS < 50KB
- No duplicate dependencies. Tree-shaking verified by analyzer.

### Visual (`visual`)
- Screenshot states: default, hover, focus, active, disabled, error, loading, empty
- Compare against baseline screenshots
- Flag any pixel diff above 1% threshold
- Test both light and dark themes

## Exit Criteria

- [ ] Accessibility: zero violations
- [ ] Performance: all CWV budgets met
- [ ] Bundle: all size budgets met
- [ ] Visual: no regressions detected
