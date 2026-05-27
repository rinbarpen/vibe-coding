# Automated Research Lifecycle

## 端到端流水线

```
                        Auto-Research Pipeline
                                │
                    ┌───────────┴───────────┐
                    │     Phase 1:          │
                    │     Discover          │
                    │         │             │
                    │  research-lit ──► idea-discovery ──► novelty-check
                    │         │             │                  │
                    └─────────┼─────────────┼──────────────────┘
                              │             │
                    ┌─────────┴─────────────┴──────────────────┐
                    │     Phase 2:          │                  │
                    │     Produce           │                  │
                    │         │             │                  │
                    │  experiment-bridge ──► run-experiment ──► analyze-results
                    │         │                                      │
                    └─────────┼──────────────────────────────────────┘
                              │
                    ┌─────────┴──────────────────────────────────────┐
                    │     Phase 3:          │                        │
                    │     Review            │                        │
                    │         │             │                        │
                    │  paper-write ──► auto-review-loop (4 rounds) ──► citation-audit
                    │         │                  │                        │
                    └─────────┼──────────────────┼────────────────────────┘
                              │                  │
                    ┌─────────┴──────────────────┴────────────────────────┐
                    │     Phase 4:          │                            │
                    │     Polish            │                            │
                    │         │             │                            │
                    │  figure-spec ──► paper-illustration ──► paper-compile
                    │         │                                            │
                    └─────────┼────────────────────────────────────────────┘
                              │
                          MANIFEST.md  (每次产出自动记录)
```

## 各阶段详情

### Phase 1: Discover

| 步骤 | 工具 | 输入 | 产出 |
|------|------|------|------|
| 文献调研 | aris/research-lit | 研究方向/关键词 | 文献综述、相关工作 |
| 想法生成 | aris/idea-discovery | 研究简报 | 候选想法列表 |
| 新颖性检查 | aris/novelty-check | 候选想法 | 新颖性评估报告 |

**典型命令**：
```
aris/research-lit "attention mechanism in vision transformers"
aris/idea-discovery "improving ViT efficiency — problem: quadratic attention cost"
aris/novelty-check
```

### Phase 2: Produce

| 步骤 | 工具 | 输入 | 产出 |
|------|------|------|------|
| 实验规划 | aris/experiment-plan | 研究提纲 | 实验计划 |
| 实验执行 | aris/run-experiment | 实验计划 | 实验结果 |
| 结果分析 | aris/analyze-results | 实验结果 | 分析报告 + 图表数据 |

### Phase 3: Review

| 步骤 | 工具 | 输入 | 产出 |
|------|------|------|------|
| 论文写作 | aris/paper-write | 实验报告 | 论文草稿 |
| 自动评审 | aris/auto-review-loop | 论文草稿 | 评审报告（最多 4 轮） |
| 声明校验 | aris/paper-claim-audit | 论文草稿 + 结果 | 声明一致性报告 |
| 引用校验 | aris/citation-audit | 论文草稿 | 引用验证报告 |

### Phase 4: Polish

| 步骤 | 工具 | 输入 | 产出 |
|------|------|------|------|
| 图表规格 | aris/figure-spec | 图描述 JSON | 确定性 SVG |
| AI 插图 | aris/paper-illustration | 插图描述 | 论文插图 |
| 论文编译 | aris/paper-compile | 论文 + 图表 | 终稿 PDF |

## Effort 级别

| Level | 评审轮数 | 安全检查 | 适用范围 |
|-------|----------|----------|----------|
| lite | 1 | 无 | 快速调研、初步想法 |
| balanced | 2 | 引用校验 | 标准论文 |
| max | 4 | claim audit + citation audit | 重要投稿 |
| beast | 4 + 保证门控 | 全部 | 顶刊/顶会投稿 |

## Output Manifest

每次产出后自动向 `MANIFEST.md` 追加一行：

```
| 2025-06-15 14:30 | research-lit | LIT_REVIEW.md | idea-discovery | Survey on ViT attention |
```

阶段值：`idea-discovery` / `implementation` / `review` / `paper`

## 文件版本化

每个产出同时保存两个版本：
- `IDEA_REPORT_20250615_143022.md` — 带时间戳副本（可追溯）
- `IDEA_REPORT.md` — 固定名称最新副本（方便引用）
