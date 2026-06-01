# Page Object Pattern

**Category**: E2E Testing  
**When**: E2E tests with multiple specs sharing page interactions  
**Framework**: Playwright, Cypress

## Structure

```
tests/e2e/pages/
├── LoginPage.ts
├── DashboardPage.ts
├── SettingsPage.ts
└── fragments/
    ├── NavigationBar.ts
    └── UserMenu.ts
```

## Rules

- **Locators only**: NO assertions inside page objects
- **Intent methods**: Name methods after user intent (`login()`, not `fillUsername().clickSubmit()`)
- **Composable**: Extract shared UI fragments (nav, modals) into separate files
- **No page objects for simple interactions**: One-off tests can use direct locators
- **Lazy locators**: Define as getters/arrow functions, not pre-resolved elements

## Example

```typescript
// LoginPage.ts
import { type Page } from '@playwright/test';

export class LoginPage {
  // Lazy locators — resolved on each access
  readonly usernameInput = () => this.page.getByLabel('Username');
  readonly passwordInput = () => this.page.getByLabel('Password');
  readonly submitButton = () => this.page.getByRole('button', { name: /log in/i });
  readonly errorMessage = () => this.page.getByTestId('login-error');

  constructor(private readonly page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async login(username: string, password: string) {
    await this.usernameInput().fill(username);
    await this.passwordInput().fill(password);
    await this.submitButton().click();
    await this.page.waitForURL('/dashboard');
  }
}
```

```typescript
// login.spec.ts — usage in test
test('successful login redirects to dashboard', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('admin', 'password123');
  await expect(page).toHaveURL('/dashboard');
});
```
