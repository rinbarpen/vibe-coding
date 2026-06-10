# CLAUDE.md — Fullstack Web Scenario

## Architecture
- **Frontend**: TypeScript + React (Next.js 14+ with App Router)
- **Backend**: Go (chi router) or TypeScript (Hono/Express)
- **Database**: PostgreSQL via Prisma (TS) or sqlc (Go)
- **Auth**: JWT with refresh token rotation
- **API**: REST with OpenAPI 3.x spec in `api/openapi.yaml`

## Commands
| Command | Description |
|---------|-------------|
| `pnpm dev` | Start frontend dev server (Next.js) |
| `pnpm test` | Run frontend tests |
| `pnpm lint` | Lint frontend code |
| `go run ./cmd/server` | Start Go backend |
| `go test ./...` | Run Go backend tests |
| `docker compose up` | Start all services locally |

## Key Rules
- API-First: OpenAPI spec defined before implementation
- Type-Safe: Generate TS types from OpenAPI spec using `openapi-typescript`
- E2E: Playwright tests for all critical user flows
- Database: Migrations via Prisma Migrate or golang-migrate
- Deployment: Docker Compose for local, CI/CD pipeline for staging/prod

## Environment Variables
```
DATABASE_URL=postgres://user:pass@localhost:5432/db
API_URL=http://localhost:8080
JWT_SECRET=<generated-secret>
```
