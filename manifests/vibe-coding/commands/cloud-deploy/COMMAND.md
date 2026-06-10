# /cloud-deploy

Deploy the project to a cloud platform.

## Usage

```
/cloud-deploy <target> <platform> [options]
```

### Platforms

| Platform | Target | Description |
|----------|--------|-------------|
| `vercel` | production / preview | Deploy to Vercel |
| `cloudflare` | production / preview | Deploy to Cloudflare Workers/Pages |
| `tencent` | production / staging | Deploy to Tencent Cloud SCF/TKE |
| `alibaba` | production / staging | Deploy to Alibaba Cloud FC/ACK |
| `huawei` | production / staging | Deploy to Huawei Cloud FG/CCE |

### Options

| Option | Description |
|--------|-------------|
| `--region=<region>` | Cloud region (platform-specific) |
| `--env=<env>` | Environment name for env variables |
| `--dry-run` | Preview deployment without executing |

## Pre-Flight Checklist

Before deploying:
- [ ] All 5 quality gates passed (`/quality-gate`)
- [ ] CI/CD pipeline green
- [ ] Database migration tested and reversible
- [ ] Environment variables configured in target platform
- [ ] Rollback plan documented
- [ ] `/deploy-check` passed

## Post-Deploy Verification

1. Health check endpoint returns 200
2. Monitoring dashboards show normal metrics
3. Logs show no unexpected errors
4. Load test passes (for production)

## References

- `references/cloud-platforms/vercel.md`
- `references/cloud-platforms/cloudflare.md`
- `references/cloud-platforms/tencent-cloud.md`
- `references/cloud-platforms/alibaba-cloud.md`
- `references/cloud-platforms/huawei-cloud.md`
