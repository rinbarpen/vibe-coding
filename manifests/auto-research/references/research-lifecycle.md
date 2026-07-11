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
                    ┌─────────┴────────────────────────────────────────────┐
                    │     Phase 5:          │                            │
                    │     Export            │                            │
                    │         │             │                            │
                    │  export-paper-zip ──► paper-submission_<venue>.zip │
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
| 版本追踪初始化 | mine/paper-version-manager init | 论文草稿 | .versions/v1/ |
| 自动评审 | aris/auto-review-loop | 论文草稿 | 评审报告（最多 4 轮） |
| 小版本升级 | mine/paper-version-manager bump --minor | 修改后论文 | .versions/v1.1/ |
| 声明校验 | aris/paper-claim-audit | 论文草稿 + 结果 | 声明一致性报告 |
| 引用校验 | aris/citation-audit | 论文草稿 | 引用验证报告 |
| 大版本升级（重大改写时） | mine/paper-version-manager bump --major | 改写后论文 | .versions/v2/ |

### Phase 4: Polish

| 步骤 | 工具 | 输入 | 产出 |
|------|------|------|------|
| 图表规格 | aris/figure-spec | 图描述 JSON | 确定性 SVG |
| AI 插图 | aris/paper-illustration | 插图描述 | 论文插图 |
| 论文编译 | aris/paper-compile | 论文 + 图表 | 终稿 PDF |

### Phase 5: Export

| 步骤 | 工具 | 输入 | 产出 |
|------|------|------|------|
| 投稿打包 | mine/export-paper-zip | 论文目录 + --venue | paper-submission_<venue>_YYYYMMDD.zip |
| 文件打包 | mine/export-paper-zip --mode bundle | 文件/目录路径列表 | paper-bundle_YYYYMMDD_HHMM.zip |

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

阶段值：`idea-discovery` / `implementation` / `review` / `paper` / `version` / `export`

## 文件版本化

每个产出同时保存两个版本：
- `IDEA_REPORT_20250615_143022.md` — 带时间戳副本（可追溯）
- `IDEA_REPORT.md` — 固定名称最新副本（方便引用）

## 论文化版本管理

使用 `mine/paper-version-manager` 追踪论文修改历史：

| 操作 | 命令 | 适用场景 |
|------|------|----------|
| 初始化 | `mine/paper-version-manager init <dir> "消息"` | 首次草稿完成后 |
| 小版本升级 | `mine/paper-version-manager bump --minor <dir> "消息"` | 评审修改、格式调整、图表替换 |
| 大版本升级 | `mine/paper-version-manager bump --major <dir> "消息"` | 结构重排、新增实验、方法论变更 |
| 查看历史 | `mine/paper-version-manager list <dir>` | 查看所有版本快照 |
| 比较版本 | `mine/paper-version-manager diff <dir> --from v1 --to v1.1` | 对比修改内容 |
| 回滚 | `mine/paper-version-manager rollback <dir> v1` | 恢复到历史版本 |

**版本规则**：
- v1/v2/v3 = 大版本（结构/方法论/核心贡献变化）
- v1.1/v1.2/v2.1 = 小版本（评审意见修改、润色、图表更新）
- bump --major 会重置小版本计数（v1.2 → v2）
