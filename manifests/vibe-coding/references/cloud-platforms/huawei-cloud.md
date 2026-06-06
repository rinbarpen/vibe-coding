# Huawei Cloud (华为云) Deployment Guide

## Quick Start

```bash
# Install HCloud CLI
pip install hcloud
hcloud configure
# Or install FunctionGraph CLI
npm i -g @huawei/function-graph-cli
```

## Supported Services

| Service | Product Name | Use Case |
|---------|-------------|----------|
| Serverless Compute | FG (FunctionGraph) | API backends, event processing |
| Container | CCE (云容器引擎) | Kubernetes workloads |
| VM | ECS (弹性云服务器) | Custom server deployments |
| MySQL | GaussDB(for MySQL) | Relational database |
| PostgreSQL | GaussDB(for PostgreSQL) | Relational database |
| NoSQL | GaussDB(for Mongo) / Redis | Document/Cache |
| Object Storage | OBS (对象存储) | File storage, CDN origin |
| CDN | CDN (内容分发) | Global content delivery |
| API Gateway | APIG (API网关) | API management |
| Container Registry | SWR (容器镜像服务) | Docker image registry |
| Message Queue | DMS (分布式消息) | Kafka/RabbitMQ/RocketMQ |

## Language Support

| Language | Runtime | Deployment Method |
|----------|---------|-------------------|
| Go | FG Go 1.x runtime | `fgs deploy` or HCloud CLI |
| Python | FG Python 3.10 | `fgs deploy` or HCloud CLI |
| TypeScript | FG Node.js 20.x | `fgs deploy` or HCloud CLI |
| Java | FG Java 11 | `fgs deploy` or HCloud CLI |
| Rust | Custom runtime via CCE | Docker image in SWR |

## CI/CD Integration (GitHub Actions)

```yaml
name: Deploy to Huawei Cloud
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup HCloud CLI
        env:
          HUAWEI_ACCESS_KEY: ${{ secrets.HUAWEI_ACCESS_KEY_ID }}
          HUAWEI_SECRET_KEY: ${{ secrets.HUAWEI_ACCESS_KEY_SECRET }}
        run: |
          hcloud configure set --access-key="$HUAWEI_ACCESS_KEY" \
                               --secret-key="$HUAWEI_SECRET_KEY" \
                               --region="cn-north-4"
      - name: Deploy to FunctionGraph
        run: fgs deploy --region cn-north-4
```

## Environment Variables

- FG: Set via console (FunctionGraph → Configuration → Environment Variables)
- CCE: Via Kubernetes Secrets or ConfigMap
- Local dev: `.env` file (not committed), or FunctionGraph function config

## Project Config (FunctionGraph)

```yaml
# function-graph.yml
function:
  name: my-function
  runtime: Python3.10
  handler: index.handler
  memorySize: 256
  timeout: 30
  environment:
    LOG_LEVEL: info
  triggers:
    - triggerTypeCode: APIG
      status: ACTIVE
      eventData:
        name: my-api
        groupName: my-api-group
```

## Monitoring & Logging

- **Cloud Eye (云监控)**: Infrastructure and service metrics
- **LTS (日志服务)**: Centralized log collection and analysis
- **APM (应用性能管理)**: Distributed tracing and performance monitoring
- **Alerting**: Via Cloud Eye → Alarm Rules

## Pricing

- **FG**: Free tier: 1M invocations/month, 400,000 GB-seconds
- **CCE**: Pay for underlying ECS instances + cluster management fee
- **GaussDB**: Starts from ~¥60/month for basic instance
- **OBS**: ~¥0.099/GB/month storage, ¥0.5/GB egress (first 10TB)
- **SWR**: Free up to 500MB storage

## Gotchas

- FunctionGraph cold starts can be 100-500ms; use reserved instances for latency-sensitive apps
- OBS cross-region replication needs explicit configuration
- CCE requires VPC and subnet configuration before cluster creation
- Chinese mainland regions require ICP filing (ICP备案) for public-facing services
- API Gateway (APIG) has separate configuration from FunctionGraph triggers
- Some regions require real-name verification before using services
- SWR image tags must be fully qualified with region
