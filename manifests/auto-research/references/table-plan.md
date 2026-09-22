# Benchmark Table Plan: statistical evidence to native LaTeX

## Scope

Version 1 implements the audited numeric benchmark matrix: datasets × explicitly selected experiment/configuration rows × metrics. It is a production path for local statistics, not a substitute for running experiments. It does not yet implement every ablation/text/longtable layout in the style gallery. The default seed count remains one.

Resources: `writing/table-plan.schema.json` (Draft 2020-12), `writing/table-plan.example.yaml`. Internal scaffold command only; no new public vibe command.

## Pipeline

1. Freeze experiment settings; generate matrix; execute runs and collect records.
2. Use `experiment_stats.py summarize` to create `results/EXPERIMENT_STATISTICS.json`. A failed audit remains in the report; do not delete it to get a passing table.
3. Copy the example Table Plan. Explicitly select each experiment ID and parameter object, shared protocol, comparison group, source kind and expected seeds. Do not mix paper-reported values with reproduced runs.
4. Validate, resolve against actual raw result files, render, then review the output and explicit manuscript value references:

```bash
uv run scripts/table_plan.py validate .auto-research/table-main.yaml
uv run scripts/table_plan.py resolve .auto-research/table-main.yaml --content-root . --output .auto-research/table-main.resolved.json
uv run scripts/table_plan.py render .auto-research/table-main.resolved.json --content-root . --output-dir paper/tables
uv run scripts/table_plan.py review .auto-research/table-main.resolved.json --content-root . --output-dir paper/tables --manuscript paper/results.tex --output .auto-research/table-main.review.json
```

Exit 0: ready/pass; 1: invalid configuration, stale provenance, blocked evidence or failed review; 2: file/tool I/O error. JSON goes to stdout; resolve and review additionally write their output files atomically. Fixed input gives stable output. Rendering regenerates the two generated files; edit the plan, not generated TeX. Review rejects manual changes. Register plan/resolved/review/TeX files in the existing lifecycle checkpoint; use archive indices for binary PDFs.

## Evidence and aggregation

Each cell has a stable `table:row:dataset:metric` ID and all contributing run IDs, seeds, attempts, configuration hashes, source paths and hashes. The statistics file itself is hashed. Raw JSON/one-row CSV is re-read, hashed and checked against recorded metrics. Means and sample SD are recomputed from those verified values; the summary supplies metric direction metadata, not trusted numeric values.

All expected seeds must be present exactly once, completed, audited PASS and eligible. Incomplete, failed, provisional or hash-mismatched cells are retained as blocked with provenance and reasons; no partial mean is passed off as a complete result, no zero imputation, no cherry-picking. CLI render refuses blocked input. The pure renderer's dash representation is for diagnostics, not a way around the completion gate.

Scale is explicit and positive (e.g. fraction × 100); precision is 0–6. The plan author must ensure labels/units describe that conversion. `mean_sd` shows sample SD only with multiple seeds. Best-value emphasis compares displayed means, respects minimize/maximize, and includes rounded ties; it is not significance. No p-values/CI are synthesized.

## Native LaTeX and manuscript linkage

```tex
% Preamble
\usepackage{booktabs}
% After begin{document}, before the table or references:
\input{paper/tables/table-main-values}
\input{paper/tables/table-main}
% Traceable numeric statement (unit is supplied by the author):
Accuracy was \ResearchValue{table-main:candidate:dataset-a:accuracy}\%.
```

`table` / `table*` follows the plan's single/double-column layout. The host document class retains fonts/caption rules; no resizebox or geometry override. Matrix columns are right-aligned; decimal alignment across arbitrary precision/SD formats and automatic width-driven layout selection remain future work. Compilation must be performed in the actual target template; this tool never certifies a venue merely because generic TeX compiled.

The review checks generated TeX exactly and explicit `ResearchValue` IDs. It does not prove prose claims, inspect arbitrary hand-typed numbers, recursively traverse TeX includes, or detect hostile macro redefinitions. Review each source file containing statements; the host must include the generated values file. Audit identity and raw-result authenticity remain upstream responsibilities.

## Writing Plan integration

In a node's existing `presentation.tables` list, add:

```yaml
- table_plan: .auto-research/table-main.yaml
  resolved: .auto-research/table-main.resolved.json
  output_dir: paper/tables
```

`writing_plan.py review` revalidates the linked plan, evidence and generated files. Legacy free-form table entries still work. A LaTeX node can use comment anchors:

```tex
% auto-research:node sec-results start
\begin{table} ... \end{table}
% auto-research:node sec-results end
```

Native table/table*/longtable environments are recognized by the basic presence check. An external `\input` alone is not proof of table presence; verify linked artifacts and review the appropriate node/file. This is initial LaTeX integration, not a complete TeX parser.
