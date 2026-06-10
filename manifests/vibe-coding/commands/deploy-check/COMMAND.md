# /deploy-check

Pre-deployment verification checklist.

## Execution

Run through each check before deploying. If any check fails, deployment is blocked.

### Infrastructure
- [ ] Quality gates passed on latest commit
- [ ] CI/CD pipeline is green (all jobs pass)
- [ ] Docker image built and pushed (multi-stage, non-root user)

### Database
- [ ] Migration files reviewed and tested
- [ ] Down/rollback migration exists and is tested
- [ ] Migration applied to staging — no issues

### Environment
- [ ] Environment variables configured for target environment
- [ ] Secrets loaded from secret manager, not hardcoded
- [ ] Required services are reachable (database, cache, message queue)

### Rollback
- [ ] Rollback plan exists
- [ ] Previous working Docker image tag is known
- [ ] Database rollback migration is ready

### Observability
- [ ] Health check endpoints return 200
- [ ] Monitoring dashboard covers RED metrics
- [ ] Alerts configured for error rate and latency spikes

### Release
- [ ] Release notes drafted
- [ ] Version tag created (if applicable)
