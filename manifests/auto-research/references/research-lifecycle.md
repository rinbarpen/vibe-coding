# 科研全生命周期

从科研启动到正式录用，按科研活动划分大阶段→小阶段→小小阶段，而不是按工具调用划分。

1. **startup 研究启动**：目标与约束 → 问题、资源；研究计划 → 里程碑、预算。
2. **literature 文献调研与问题定位**：检索 → query、筛选；定位 → 分类、空白、新颖性。
3. **idea 方法形成**：假设 → 候选、比较；方法 → 机制、组件、claims。
4. **design 实验设计**：baseline → 联网检索、筛选、协议；消融 → 分解、覆盖、矩阵；评估 → 指标、seed、预算。
5. **execution 实验执行**：准备 → 环境、数据、评估器；实现 → 代码、审查、sanity；运行 → 审批、baseline、main、ablation、采集。
6. **analysis 分析与论证**：统计 → 完整性、汇总、对比；解释 → 消融、失败、claims、审计。
7. **writing 写作**：叙事、大纲、Writing Plan；逐节点 methods/results/discussion/figures/citations。
8. **internal-review 内部评审**：科学性、证据与表达；补实验、局部重写、投稿检查。
9. **submission 投稿**：venue、材料、作者确认；正式提交确认和回执。
10. **revision 外审返修**：决定、意见矩阵、策略；补实验、改稿、回复、重投或转投。
11. **acceptance 录用定稿**：正式通知确认；camera-ready、校样、最终归档。

阶段 ID 与 execution/cycle 分离；失败假设可完成研究活动。回退和转投创建新轮次，不覆盖旧结果。录用与终稿完成分开，录用必须有实际通知。

每个层级进入、结束、失败、暂停、恢复和规划变化都留档并 Git 提交。固定文件是当前计划，检查点快照和 Git 保存中间版本。完整契约见 [lifecycle-runtime.md](lifecycle-runtime.md)。

大阶段的细化目标、输入、输出、门禁与回退关系见 [lifecycle-stage-details.md](lifecycle-stage-details.md)。

实验先 plan 后 bridge，设计阶段就覆盖对比和消融；默认一个 seed=42，多 seed 可配置。联网 baseline 记录原始来源和冻结版本。执行、预算与统计见 [experiment-execution.md](experiment-execution.md)。

写作继续遵循 research → outline → plan-writing → validate → resolve → render-plan → approval-gates → write → review → revise；writer 只接收 resolved node。见 [Writing Plan](../writing/README.md)。

论文各版本使用 paper-version-manager；生命周期 Git 管理包括规划、失败日志、评审、投稿、返修和录用。每次产物登记 MANIFEST.md，关联阶段 checkpoint。
