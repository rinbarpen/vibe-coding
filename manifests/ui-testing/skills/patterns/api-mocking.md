# API Mocking Pattern

**Category**: Integration Testing  
**When**: Testing components or features that make network requests  
**Framework**: MSW (Mock Service Worker), Playwright Route

## MSW (Preferred — Integration Tests)

For Vitest/jsdom tests, mock at the network level with MSW.

```typescript
// src/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/users', () => {
    return HttpResponse.json([
      { id: 1, name: 'Alice', email: 'alice@example.com' },
    ]);
  }),

  http.post('/api/login', async ({ request }) => {
    const { email } = await request.json();
    if (!email) {
      return HttpResponse.json({ error: 'Email required' }, { status: 400 });
    }
    return HttpResponse.json({ token: 'mock-jwt', user: { email } });
  }),
];
```

```typescript
// src/mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

```typescript
// vitest.setup.ts
import { server } from '@/mocks/server';
import { afterAll, afterEach, beforeAll } from 'vitest';

beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

## Rules

- **One set of handlers**: Define ALL handlers in one place. Override per-test with `server.use()`.
- **No partial mocks**: If a handler is registered, it MUST return realistic data for all fields the component uses.
- **Per-test overrides**: Use `server.use(http.get('/api/x', () => ...))` inside a test to override a global handler.
- **Error states**: Always test error responses (network failure, 4xx, 5xx) — they are as important as success paths.

## Playwright Route (E2E Tests)

For Playwright E2E tests, use `page.route()` to intercept API calls:

```typescript
test('shows empty state when no users exist', async ({ page }) => {
  await page.route('**/api/users', async (route) => {
    await route.fulfill({ json: [] });
  });
  await page.goto('/users');
  await expect(page.getByText(/no users found/i)).toBeVisible();
});
```
