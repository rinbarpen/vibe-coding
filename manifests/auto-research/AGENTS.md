# Agent Instructions for Auto-Research

## 全生命周期主流程

权威阶段树为 `lifecycle/defaults.json`：startup → literature → idea → design → execution → analysis → writing → internal-review → submission → revision → acceptance。以下旧 Phase 名称仅作 aris 能力分组，执行记录一律用阶段树稳定 ID。

每个大/小/小小阶段进入、结束、失败、暂停、恢复和计划修订都使用 research_workflow.py checkpoint 留档并本地 Git 提交。阶段完成不等于假设成立。详见 references/lifecycle-runtime.md。

### 模型职责（项目默认）
- 科研问题与科学判断：GPT-6 Pro。
- 规划：GPT-6 medium。
- 执行与统计、归档：GPT-5.6-Luna high。
- 写作：GPT-5.5 high。
宿主验证 binding 后调用；记录实际模型和 effort。Pro 不映射为 effort；不静默降级。审查使用独立上下文并标明实际身份。

### Plan 前置规则
研究、实验、写作等规划前先使用 grill-me 压力测试并确认目标、约束与验收标准；现有已确认计划直接复用。

### Phase 1: Discover
文献调研 → 想法生成 → 新颖性检查

0. 调用 `grill-me`，明确研究计划后再开始本阶段
1. 使用 `aris/research-lit "query"` 进行文献检索和综述
2. 使用 `aris/idea-discovery "brief"` 生成研究想法
3. 使用 `aris/novelty-check` 进行新颖性验证
4. 产出：研究纲要 + 新颖性报告

### Phase 2: Design, Execute and Analyze

1. researcher 拆解 idea、claims、组件及混杂因素；planner 使用 experiment-plan 先规划。
2. executor 联网查找最新 baseline（原始论文/官方代码/协议），researcher 筛选公平对比；保存 query、日期、来源与纳入/排除理由。
3. 执行前使用 ablation-planner 的设计能力形成完整覆盖矩阵，不等待主实验完成才首次设计消融。
4. 默认 seeds=[42]，可覆盖多 seed；调用 experiment_stats.py design-review/expand 冻结矩阵。
5. experiment-bridge 实现 → 独立代码审查 → smoke/sanity → 预算门 → run-experiment 或 SSH experiment-queue。
6. 付费云使用前和 full suite 前人工确认预算；审查缺席显式记录并请求确认。批准矩阵预算内自动推进。
7. monitor 只检查运行事实，采集所有 attempts、负结果和失败日志；analyze-results 配合 experiment_stats.py summarize 统计。
8. experiment-audit 后按 PASS/WARN/FAIL/REVIEW_UNAVAILABLE 分配 eligible/provisional/ineligible，不把失败审计结果当论文支持证据。
9. 提供原始结果、claim/run、配置和审计引用进入 Writing Plan。每个科研活动检查点提交 Git。

详细运行契约与统计接口：references/experiment-execution.md。此契约优先于上游 bridge 的静默降级或未审批自动扩展矩阵默认值。

### Phase 3: Plan, Write and Review
写作规划 → 节点写作 → 版本管理 → 自动评审 → 局部改进

1. 先调用 `grill-me`，再使用 `aris/paper-plan` 生成论文大纲
2. 若 `.auto-research/writing-plan.yaml` 不存在：已有大纲则 `writing_plan.py init`，否则先生成大纲；旧项目使用 `writing_plan.py migrate`
3. 按 `plan-writing → validate → resolve → render-plan` 创建事实源、resolved JSON 和 `WRITING_PLAN.md`
4. 只在 resolved 节点配置 `approval: before_write` 且审批状态不是 `approved` 时暂停；其他节点继续
5. writer 一次只接收并写作一个 resolved 节点，不读取原始 YAML
6. 运行 `writing_plan.py review`，只局部重写 `warning`、`fail` 或 `blocked_missing_evidence` 节点；结构变化后回到步骤 3
7. 使用 `mine/paper-version-manager init` 初始化版本追踪（v1）
8. 使用 `aris/auto-review-loop` 启动自动评审循环（最多 4 轮）
9. 根据评审意见修改论文，并使用 `mine/paper-version-manager bump --minor` 标记修改（v1 → v1.1 等）
10. 重复步骤 8-9 直到评审收敛（每轮评审后 bump --minor）
11. 使用 `mine/paperreview-ai-review` 提交 paperreview.ai 外部评审
12. 使用 `aris/paper-claim-audit` 校验数值声明一致性，并使用 `aris/citation-audit` 校验引用
13. 对重大改写使用 `mine/paper-version-manager bump --major`，并重新 validate/resolve/render/approval
14. 使用 `aris/auto-paper-improvement-loop` 深度改进论文
15. 产出：逐节点写作记录、Writing Review、评审意见、改进清单和版本历史

#### Writing Plan 职责边界

- **planner**：创建、迁移和修改原始 `.auto-research/writing-plan.yaml`，大纲更新时优先复用稳定 ID。
- **resolver**：校验 schema/引用/父子关系，输出无继承、无 profile、无 `append`/`unset` 的最终节点配置。
- **writer**：一次只写一个节点；输入限于当前 resolved node、父目标摘要、必要证据、相邻标题/摘要、已批准术语表和插入位置。写后记录 node ID、路径、锚点、来源、字数、生成时间与 resolved plan hash。
- **reviewer**：仅依据 resolved node plan 审查，不自行添加要求；失败时指定需局部重写的 node ID。

目标、受众、风格、证据或其他 resolved 写作要求发生实质变化时，要求哈希改变，旧审批自动失效。标题改名、文件移动和节点重排不改变身份。

### Phase 4: Polish
图表生成 → 论文编译 → 终稿

1. 使用 `aris/figure-spec "desc"` 生成确定性图表（架构图/工作流图）
2. 使用 `aris/paper-illustration "desc"` 生成 AI 插图
3. 使用 `aris/paper-compile` 编译终稿
4. 产出：定稿论文 + 图表

### Phase 5: Export
论文导出 → 打包 → 投稿 ZIP

1. 使用 `mine/export-paper-zip "path" --mode submission --venue <venue>` 导出投稿 ZIP
2. 或使用 `mine/export-paper-zip "path" --mode bundle --include <files...>` 自定义打包
3. 产出：`paper-submission_<venue>_YYYYMMDD.zip` + 记录到 MANIFEST.md

## Subagent Dispatch

| Agent | When | Responsibility |
|-------|------|----------------|
| lit-reviewer | Phase 1 | 文献调研和综述 |
| idea-generator | Phase 1 | 研究想法生成 |
| experiment-designer | Phase 2 | 实验方案设计 |
| paper-reviewer | Phase 3 | 自动评审（调用 auto-review-loop） |
| figure-designer | Phase 4 | 图表规格和生成 |
| citation-auditor | Phase 3 | 引用校验 |
| version-manager | Phase 3 | 版本追踪和变更记录 |

## Output Manifest 协议

- 每个阶段产出记录到 `MANIFEST.md`
- 格式：`| Timestamp | Skill | File | Stage | Description |`
- 阶段值：`idea-discovery` / `implementation` / `review` / `paper` / `version`
- 文件版本化：带时间戳副本 + 固定名称最新副本并存；使用 `mine/paper-version-manager` 管理论文版本历史

## 评审者独立性协议

- 评审者必须从原始论文草稿直接形成评估意见
- 执行者不得在评审前预先消化或总结论文内容
- 每轮评审使用独立会话（fresh review threads）
- 不同轮次之间不共享上下文

## 投稿、外审、返修和录用

Export 只完成材料打包，不表示科研结束。按 submission/revision/acceptance 阶段继续：venue 要求 → 作者确认 → 正式提交 → 保存回执 → 审稿意见矩阵 → 修订/补实验/回复 → 再提交；拒稿建立新 submission_id。正式提交须用户确认。录用通知与终稿归档分别完成并保留证据。
