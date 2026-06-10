# Vercel Deployment Guide

## Quick Start

```bash
npm i -g vercel
vercel login
vercel init
```

## Supported Services

| Service | Product | Use Case |
|---------|---------|----------|
| Compute | Serverless Functions | API routes, SSR, ISR |
| Edge | Edge Functions | Low-latency compute at edge |
| Static | Static Files | Frontend, Jamstack |
| Database | Vercel Postgres (Neon) | Relational data |
| Storage | Vercel Blob | File uploads, assets |
| KV | Vercel KV (Upstash) | Caching, session store |
| Cron | Cron Jobs | Scheduled tasks |
| Analytics | Web Analytics + Speed Insights | Performance monitoring |

## Language Support

| Language | Runtime | Deployment Method |
|----------|---------|-------------------|
| TypeScript | Node.js 20.x | `vercel deploy` |
| Go | Go 1.21+ | `vercel deploy` (with `vercel.json`) |
| Python | Python 3.12 | `vercel deploy` (with `requirements.txt`) |
| Rust | WASM via Node | `vercel deploy` |
| Java | — | Not natively supported |

## CI/CD Integration (GitHub Actions)

```yaml
name: Deploy to Vercel
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

## Environment Variables

- Set via Vercel Dashboard → Project → Settings → Environment Variables
- Or via CLI: `vercel env add <KEY> <environment>`
- Preview envs get separate variable values from Production
- Never check `.env` files into Git

## Project Config (`vercel.json`)

```json
{
  "buildCommand": "pnpm build",
  "outputDirectory": "dist",
  "installCommand": "pnpm install",
  "functions": {
    "api/**/*.ts": {
      "runtime": "@vercel/node@3"
    }
  }
}
```

## Monitoring & Logging

- **Analytics**: Vercel Analytics (Web Vitals + custom events)
- **Logs**: `vercel logs <deployment-url>`
- **Runtime Logs**: Dashboard → Deployments → Functions → Logs
- **Alerts**: Via Vercel Dashboard or webhook integrations

## Pricing

- **Free Tier**: 100 GB bandwidth, 100 GB-hours execution, 6,000 build minutes/month
- **Pro**: $20/mo per member — 1 TB bandwidth, 1,000 GB-hours

## Gotchas

- Serverless functions have 10s timeout (Hobby), 60s (Pro), 900s (Enterprise)
- Cold starts on Serverless Functions; use Edge Functions for low-latency
- Monorepos need `"rootDirectory"` set in `vercel.json`
- Environment variables are NOT available during build unless prefix is `NEXT_PUBLIC_`
