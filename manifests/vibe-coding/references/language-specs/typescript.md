# TypeScript / JavaScript Language Specification

## Overview
Typed superset of JavaScript. The dominant language for web frontends and a strong choice for full-stack development with Node.js. TypeScript adds static types to JavaScript's flexible runtime, catching errors at compile time rather than runtime.

## Strengths
- Only language that runs natively in browsers (JavaScript) — TypeScript compiles to JavaScript
- Excellent type system with structural typing (interfaces, generics, discriminated unions, template literal types)
- Full-stack capability: use the same language for frontend (React/Vue/Svelte) and backend (Node.js)
- Massive ecosystem (npm is the largest package registry — 2M+ packages)
- Fast iteration cycle with hot module replacement (instant feedback during development)
- Rich framework ecosystem (React, Next.js, Svelte, Vue, Angular, Express, Hono)
- Excellent developer tooling (VS Code, TypeScript compiler, ESLint, Prettier)
- Serverless-friendly (fast cold start with Node.js)
- TypeScript adoption is industry standard for new web projects

## Weaknesses
- Node.js event loop is single-threaded (CPU-intensive tasks block the event loop)
- npm dependency bloat and supply chain risk (left-pad incidents, protestware)
- TypeScript configuration complexity (tsconfig.json, strict mode adoption)
- Runtime performance lower than Go/Rust (JIT-compiled, not AOT)
- Memory usage higher than compiled languages (V8 heap)
- JavaScript ecosystem churn (framework churn, tooling churn)
- `node_modules` disk usage (mitigated by pnpm with content-addressable storage)

## Best For
- Web frontends (React, Next.js, Svelte, Vue, Angular)
- Full-stack web applications (Next.js, Remix, Nuxt, SvelteKit)
- Node.js backend services with moderate throughput
- CLI and developer tools (npm ecosystem, wide distribution)
- Real-time applications (WebSocket via Socket.io, WebRTC)
- Serverless functions (fast cold start, wide platform support)
- Cross-platform desktop apps (Electron, Tauri with web frontend)

## Not Ideal For
- CPU-intensive backend services (use Go or Rust for compute-heavy workloads)
- Systems programming (use Rust — no memory management in JS)
- Data science / ML training (use Python — though TensorFlow.js exists)
- Native mobile development (use Kotlin/Swift — React Native/Expo as alternative)
- Safety-critical systems (dynamic features + GC make behavior harder to predict)
- High-frequency trading or ultra-low-latency systems

## Testing
- Unit/Integration: `Vitest` (fast, Vite-native, Jest-compatible API) or `Jest`
- E2E: `Playwright` (browser automation, cross-browser, visual regression)
- Component: `@testing-library/react` (behavioral testing, avoid implementation details)
- API mocking: `MSW` (Mock Service Worker — intercept at network level)
- Coverage: Built-in via `vitest --coverage` or `jest --coverage` (80%+ threshold)
- Property-based: `fast-check` (generative testing)
- Visual regression: Playwright screenshot comparison or Chromatic
- Lint: `eslint` with `@typescript-eslint`, Prettier for formatting
- Type check: `tsc --noEmit` (in CI)
- Skills: `e2e-testing` (Playwright specialist)

## Key Libraries
- Frontend: `React` + `Next.js` (app router, server components, server actions)
- State management: `Zustand` (lightweight), `Jotai` (atomic), `TanStack Query` (server state)
- Validation: `Zod` (runtime validation with TypeScript inference)
- Database: `Prisma` (ORM, type-safe), `Drizzle` (SQL-like, lightweight)
- End-to-end types: `tRPC` (type-safe API calls without code generation)
- HTTP server: `Hono` (lightweight, multi-runtime), `Express` (mature standard)
- Schema-first API: `zod` + `openapi-typescript` for OpenAPI type generation
- Testing: `Vitest`, `Playwright`, `Testing Library`
- Package management: `pnpm` (preferred — fast, disk-efficient), `bun` (runtime + package manager)

## Type System (Recommended Config)
- `tsconfig.json`: `strict: true`, `noUncheckedIndexedAccess: true`, `exactOptionalPropertyTypes: true`
- `interface` for object shapes that can be extended
- `type` for unions, intersections, and mapped types
- `unknown` instead of `any` (unknown forces type narrowing before use)
- Discriminated unions for state machines: `type State = { kind: 'loading' } | { kind: 'loaded'; data: T } | { kind: 'error'; error: Error }`
- `satisfies` operator for type validation without widening (TS 4.9+)
- `as const` for literal types and readonly tuples

## References
- Skills: `frontend-patterns`, `e2e-testing`
- Agents: `typescript-reviewer`, `e2e-runner`, `build-error-resolver`
- Rules: `~/.claude/rules/typescript/`, `~/.claude/rules/web/`
