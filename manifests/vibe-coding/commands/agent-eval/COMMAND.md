# /agent-eval

Run agent performance evaluation suite.

## Usage

```
/agent-eval <mode> [options]
```

### Modes

| Mode | Description |
|------|-------------|
| `regression` | Run eval suite against golden dataset, compare to baseline |
| `benchmark` | Measure performance metrics (latency, tokens, cost) |
| `adversarial` | Test agent against edge cases and adversarial inputs |

### Options

| Option | Description |
|--------|-------------|
| `--dataset=<path>` | Path to eval dataset (default: `data/eval/`) |
| `--limit=<n>` | Run only N test cases |
| `--output=<path>` | Report output path |

## Execution

1. Load eval dataset from `data/eval/`
2. Run agent against each test case
3. Collect metrics: task success, tool call success, latency, token usage
4. Compare to baseline thresholds
5. Generate eval report to `docs/eval/report-<date>.md`

## Metrics

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Task success rate | > 85% | < 70% |
| Tool call success rate | > 90% | < 80% |
| Avg latency | < 5s | > 10s |
| Tokens per run | < 10K | > 50K |
| Cost per run | < $0.05 | > $0.20 |

## Exit Criteria

- [ ] Eval suite completed cleanly
- [ ] All metrics pass thresholds
- [ ] Report generated at `docs/eval/report-<date>.md`
- [ ] If regression: no metric regression vs baseline
