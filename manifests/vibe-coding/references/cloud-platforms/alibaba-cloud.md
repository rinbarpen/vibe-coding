# Alibaba Cloud (阿里云) Deployment Guide

## Quick Start

```bash
# Install Aliyun CLI
pip install aliyun-cli
aliyun configure
# Or use Fun (Function Compute CLI)
npm i -g @alicloud/fun
```

## Supported Services

| Service | Product Name | Use Case |
|---------|-------------|----------|
| Serverless Compute | FC (函数计算) | API backends, event processing |
| Serverless App Engine | SAE | Full-managed Spring Boot/Dubbo |
| Container | ACK (容器服务) | Kubernetes workloads |
| VM | ECS (云服务器) | Custom server deployments |
| MySQL | RDS MySQL | Relational database |
| PostgreSQL | RDS PostgreSQL | Relational database |
| Redis | Redis (云数据库) | Caching, session store |
| Object Storage | OSS (对象存储) | File storage, CDN origin |
| CDN | CDN (内容分发) | Global content delivery |
| API Gateway | API Gateway | API management |
| Message Queue | MNS / RocketMQ | Async messaging |

## Language Support

| Language | Runtime | Deployment Method |
|----------|---------|-------------------|
| Go | FC Go 1.x runtime | `fun deploy` or Aliyun CLI |
| Python | FC Python 3.10 | `fun deploy` or Aliyun CLI |
| TypeScript | FC Node.js 20.x | `fun deploy` or Aliyun CLI |
| Java | FC Java 11 / SAE | `fun deploy` or SAE console |
| Rust | Custom runtime via ACK | Docker image |

## CI/CD Integration (GitHub Actions)

```yaml
name: Deploy to Alibaba Cloud
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Aliyun CLI
        uses: aliyun-actions/setup-aliyun-cli@v1
        with:
          access-key-id: ${{ secrets.ALIBABA_ACCESS_KEY_ID }}
          access-key-secret: ${{ secrets.ALIBABA_ACCESS_KEY_SECRET }}
      - name: Deploy to FC
        run: fun deploy --stage prod
```

## Environment Variables

- FC: Set via console (Function → Configuration → Environment Variables)
- SAE/ACK: Via Kubernetes Secrets or console
- Local dev: `.env` file (not committed), or `template.yml` `EnvironmentVariables:` block

## Project Config (`template.yml`)

```yaml
ROSTemplateFormatVersion: '2015-09-01'
Transform: 'Aliyun::Serverless-2018-04-03'
Resources:
  my-service:
    Type: 'Aliyun::Serverless::Service'
    Properties:
      Description: 'My service'
    my-function:
      Type: 'Aliyun::Serverless::Function'
      Properties:
        Handler: index.handler
        Runtime: python3
        CodeUri: './src'
```

## Monitoring & Logging

- **Cloud Monitor (云监控)**: Infrastructure and application metrics
- **SLS (日志服务)**: Centralized log collection, search, and analysis
- **ARMS (应用实时监控)**: Application performance monitoring, tracing
- **Alerting**: Via Cloud Monitor → Alert Rules

## Pricing

- **FC**: Free tier: 1M invocations/month, 400,000 CU-seconds
- **SAE**: Pay per vCPU/memory per minute, ~¥0.0024/vCPU/min
- **ACK**: Pay for underlying ECS instances + management fee
- **RDS**: Starts from ~¥50/month for basic instance
- **OSS**: ~¥0.12/GB/month storage, ¥0.5/GB egress (first 10TB)

## Gotchas

- FC HTTP trigger requires API Gateway binding for external access
- OSS cross-region replication has eventual consistency
- ACK clusters need VPC and vSwitch configured before creation
- Chinese mainland regions require ICP filing (ICP备案) for public-facing services
- RAM (Resource Access Management) roles required for cross-service access
- Some regions require real-name verification before using any service
