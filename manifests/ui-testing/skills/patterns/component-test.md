# Component Test Pattern

**Category**: Component Testing  
**When**: Testing isolated UI components in a browser-like environment  
**Framework**: Vitest + Testing Library, Jest + Testing Library

## Rules

- **Test behavior, not implementation**: Query by role/label/testid, not CSS classes or component state
- **User-centric interactions**: Use `@testing-library/user-event` (simulates real keyboard/mouse), never `fireEvent`
- **Custom render**: Create a `test-utils.tsx` that wraps components with needed providers (router, context, i18n)
- **One assertion per meaningful behavior**: Prefer multiple small tests over one large test
- **No test-id for interactive elements**: Reserve `data-testid` for containers, not buttons/inputs

## Example

```typescript
// test-utils.tsx
import { render, type RenderOptions } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { ThemeProvider } from '@/contexts/ThemeContext';

function TestProviders({ children }: { children: React.ReactNode }) {
  return (
    <MemoryRouter>
      <ThemeProvider>
        {children}
      </ThemeProvider>
    </MemoryRouter>
  );
}

export function renderWithProviders(
  ui: React.ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>,
) {
  return render(ui, { wrapper: TestProviders, ...options });
}
```

```typescript
// LoginForm.test.tsx
import { renderWithProviders } from '@/test-utils';
import { LoginForm } from './LoginForm';
import userEvent from '@testing-library/user-event';

test('shows error on invalid email', async () => {
  const user = userEvent.setup();
  renderWithProviders(<LoginForm />);

  await user.type(screen.getByLabelText('Email'), 'bad-email');
  await user.click(screen.getByRole('button', { name: /submit/i }));

  expect(screen.getByText(/please enter a valid email/i)).toBeVisible();
});

test('calls onSubmit with valid form data', async () => {
  const onSubmit = vi.fn();
  const user = userEvent.setup();
  renderWithProviders(<LoginForm onSubmit={onSubmit} />);

  await user.type(screen.getByLabelText('Email'), 'user@example.com');
  await user.type(screen.getByLabelText('Password'), 'secure123');
  await user.click(screen.getByRole('button', { name: /submit/i }));

  expect(onSubmit).toHaveBeenCalledWith({
    email: 'user@example.com',
    password: 'secure123',
  });
});
```
