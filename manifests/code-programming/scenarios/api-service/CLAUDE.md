# CLAUDE.md — API Service Scenario

## Architecture
- **Language**: Go (preferred) or Python (FastAPI) or TypeScript (Hono)
- **Database**: PostgreSQL
- **Cache**: Redis
- **Message Queue**: Optional — NATS or RabbitMQ
- **API**: REST with OpenAPI 3.x or gRPC with Protobuf

## Commands
| Command | Description |
|---------|-------------|
| `go run ./cmd/server` | Start Go server |
| `uv run fastapi dev` | Start Python server |
| `pnpm dev` | Start TypeScript server |
| `go test ./...` | Run Go tests |
| `pytest` | Run Python tests |
| `pnpm test` | Run TypeScript tests |

## Key Rules
- Health check: `GET /healthz` (liveness) and `GET /readyz` (readiness)
- OpenAPI spec: `api/openapi.yaml` is source of truth
- Middleware: logging, recovery, CORS, auth, rate limiting (in that order)
- All mutation endpoints support idempotency keys
- Rate limiting on all public endpoints
- Structured JSON logging (not plain text)

## Environment Variables
```
DATABASE_URL=postgres://user:pass@localhost:5432/db
REDIS_URL=redis://localhost:6379
API_PORT=8080
LOG_LEVEL=info
```
