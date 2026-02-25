# CLAUDE.md

## Architecture
- Hub: Centralized API Gateway
- Nodes: Independent microservices
- Sync: Event-driven (Redis/RabbitMQ)

## Distributed Commands
| Command | Description |
|---------|-------------|
| `vibe-hub-up` | Start Centralized Hub |
| `vibe-node-reg` | Register node to Hub |
| `vibe-sync-data` | Trigger manual data sync |

## Data Sync
- Event-driven eventual consistency.
- Idempotent writes.
