# CLAUDE.md

## Architecture
- Frontend: React/Vue (Independent)
- Backend: API-First (FastAPI/Node.js)
- Database: Multi-tenant (Tenant Isolation)

## SaaS Commands
| Command | Description |
|---------|-------------|
| `uv run manage.py migrate` | Database migration |
| `pnpm dev` | Frontend development |
| `vibe-check saas` | Verify tenant isolation |

## Tenant Isolation
- All queries must include `tenant_id`.
- Use Feature Flags for subscription levels.
