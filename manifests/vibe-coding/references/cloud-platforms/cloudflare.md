# Cloudflare Deployment Guide

## Quick Start

```bash
npm i -g wrangler
wrangler login
wrangler init my-project
```

## Supported Services

| Service | Product | Use Case |
|---------|---------|----------|
| Compute | Workers | Serverless edge functions |
| Static | Pages | Full-stack web apps, Jamstack |
| KV Store | Workers KV | Key-value storage, config, cache |
| Object Storage | R2 | S3-compatible, no egress fees |
| SQL Database | D1 | SQLite at the edge |
| Durable Objects | Durable Objects | Stateful, strongly consistent storage |
| Queues | Queues | Async message delivery |
| Pub/Sub | Pub/Sub | Real-time messaging |
| AI | Workers AI | Run LLMs at edge (Llama, Mistral, etc.) |

## Language Support

| Language | Runtime | Deployment Method |
|----------|---------|-------------------|
| TypeScript | Workers / Pages | `wrangler deploy` |
| Go | Workers (via WASM) | `wrangler deploy` |
| Rust | Workers (via wasm-bindgen) | `wrangler deploy` |
| Python | Workers (Pyodide) | `wrangler deploy` |
| Java | — | Not supported |

## CI/CD Integration (GitHub Actions)

```yaml
name: Deploy to Cloudflare
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CF_API_TOKEN }}
          accountId: ${{ secrets.CF_ACCOUNT_ID }}
          command: deploy
```

## Environment Variables

- Set via Dashboard → Workers & Pages → Settings → Variables
- Or via CLI: `wrangler secret put <KEY>`
- Variables available in `env.<KEY>` in Worker code
- `.dev.vars` for local development (not committed)

## Project Config (`wrangler.toml`)

```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-12-01"

[[kv_namespaces]]
binding = "KV"
id = "abc123"

[[d1_databases]]
binding = "DB"
database_name = "my-db"
database_id = "def456"

[[r2_buckets]]
binding = "BUCKET"
bucket_name = "my-bucket"
```

## Monitoring & Logging

- **Logs**: `wrangler tail` (live), Dashboard → Workers → Logs
- **Metrics**: Workers Analytics (requests, CPU time, errors, duration)
- **Alerts**: Via Cloudflare Dashboard → Notifications

## Pricing

- **Free Tier**: 100,000 requests/day, 10ms CPU time per request
- **Paid**: $5/mo + usage ($0.30/million requests)
- **KV**: $0.50/GB-month storage, $0.50/million reads
- **R2**: $0.015/GB-month storage, no egress fees
- **D1**: $0.75/million reads, $1.00/million writes

## Gotchas

- Worker CPU time limits: 10ms (Free), 50ms (Bundled), 30s (Unbound + Cron)
- No TCP connections from Workers (HTTP/WebSocket only)
- KV is eventually consistent (up to 60s replication delay); use Durable Objects for strong consistency
- R2 has eventual consistency on overwrites
- WASM-based language support (Go, Rust) has larger bundle sizes and cold-start overhead
