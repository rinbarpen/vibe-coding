# Tencent Cloud (腾讯云) Deployment Guide

## Quick Start

```bash
# Install TCCLI
pip install tccli
tccli configure
# Or use Serverless Framework
npm i -g serverless
```

## Supported Services

| Service | Product Name | Use Case |
|---------|-------------|----------|
| Serverless Compute | SCF (云函数) | API backends, event processing |
| Container | TKE (容器服务) | Kubernetes workloads |
| VM | CVM (云服务器) | Custom server deployments |
| MySQL | CDB (云数据库) | Relational database |
| PostgreSQL | PostgreSQL | Relational database |
| Object Storage | COS (对象存储) | File storage, CDN origin |
| CDN | CDN (内容分发) | Global content delivery |
| API Gateway | API Gateway | API management, rate limiting |
| Message Queue | CMQ (消息队列) / CKafka | Async messaging |

## Language Support

| Language | Runtime | Deployment Method |
|----------|---------|-------------------|
| Go | SCF Go runtime | `serverless deploy` or TCCLI |
| Python | SCF Python 3.10 | `serverless deploy` or TCCLI |
| TypeScript | SCF Node.js 20.x | `serverless deploy` or TCCLI |
| Java | SCF Java 11 | `serverless deploy` or TCCLI |
| Rust | Custom runtime via TKE | Docker image |

## CI/CD Integration (GitHub Actions)

```yaml
name: Deploy to Tencent Cloud
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Serverless Framework
        run: npm i -g serverless
      - name: Deploy
        env:
          TENCENT_SECRET_ID: ${{ secrets.TENCENT_SECRET_ID }}
          TENCENT_SECRET_KEY: ${{ secrets.TENCENT_SECRET_KEY }}
        run: serverless deploy --stage prod
```

## Environment Variables

- SCF: Set via console (Function → Configuration → Environment Variables)
- TKE: Set via Kubernetes Secrets or ConfigMap
- Local dev: `.env` file (not committed), or Serverless Framework `serverless.yml` `environment:` block

## Project Config (`serverless.yml`)

```yaml
service: my-service
provider:
  name: tencent
  runtime: Python3.10
  region: ap-guangzhou
  credentials: ~/.tencent/credentials

functions:
  api:
    handler: index.main_handler
    events:
      - apigw:
          name: my-api
          parameters:
            protocols:
              - http
              - https
```

## Monitoring & Logging

- **Cloud Monitor (云监控)**: Metrics dashboard, custom metrics
- **CLS (日志服务)**: Centralized log collection and search
- **APM (应用性能监控)**: Distributed tracing, performance analysis
- **Alerting**: Via Cloud Monitor → Alarm Policies

## Pricing

- **SCF**: Free tier: 1M invocations/month, 400,000 GB-seconds
- **TKE**: Pay for underlying CVM instances + small management fee
- **CDB**: Starts from ~¥50/month for basic instance
- **COS**: ~¥0.118/GB/month storage, ¥0.5/GB egress

## Gotchas

- SCF function timeout: max 900s; default 3s — adjust for long-running tasks
- COS event triggers have eventual consistency delays
- Cross-region deployment requires explicit region specification
- TKE requires VPC network configuration before deployment
- Chinese mainland regions have ICP filing (备案) requirements for public-facing services
- Some services require real-name verification (实名认证)
