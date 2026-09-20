# Auto-Research Manifest

面向自动化学术研究的独立 manifest 包。

## 场景

整合三条 AI 驱动的研究自动化能力线，并用版本化 Writing Plan 连接研究结果与节点级写作：
- **aris** — 研究编排框架（文献调研、想法发现、实验规划、论文写作）
- **paperreview** — 自动论文评审（4 轮自主评审循环、数值声明校验、引用校验）
- **autofigure** — 自动图表生成（确定性 SVG 架构图、AI 插图、数据驱动图表）

## 使用方式

```bash
# 初始化到目标研究项目
./scripts/init-auto-research.sh /path/to/your/research-project
```

## 快速开始

1. 在每次制定研究、实验或论文计划前调用 `grill-me`；也可在任意阶段直接调用
2. 创建一个研究方向 issue
3. 运行 `aris/research-pipeline "topic"` 启动全流程
4. 大纲确定后初始化计划：`uv run scripts/writing_plan.py init --outline PAPER_OUTLINE.md --output .auto-research/writing-plan.yaml`
5. 依次运行 `validate`、`resolve`、`render`，仅将 resolved node plan 交给 writer
6. 在计划中选择 `venue.profile`，刷新官方 author guide/CFP 和 `checked_at`
7. 按 `writing/figure-types.yaml` 为架构图、流程图、对比图、消融图、曲线、热力图、定性图和概念图创建 figure node
8. 写作后运行 `review`，只局部修订未通过节点，再运行 `aris/auto-review-loop`
9. 使用 `aris/figure-spec`、`aris/paper-figure` 或 `aris/paper-illustration` 生成论文图表

完整写作顺序：

`research → outline → plan-writing → validate → resolve → render-plan → approval-gates → write → review → revise`

字段、继承、稳定 ID、审批哈希和迁移说明见 [`writing/README.md`](writing/README.md)。
投稿要求和图生成规则见 [`references/venue-requirements.md`](references/venue-requirements.md)。

## 全生命周期运行契约

从启动到录用使用三层科研阶段树，而非仅实验阶段。权威流程见 `references/research-lifecycle.md`，检查点/Git/模型规则见 `references/lifecycle-runtime.md`，实验设计与自动统计见 `references/experiment-execution.md`。这三份契约优先于简化流水线示意。

项目首次启用：`python3 scripts/research_workflow.py init`。模型角色默认：研究 GPT-6 Pro、规划 GPT-6 medium、执行 GPT-5.6-Luna high、写作 GPT-5.5 high；显式核验实际宿主绑定。实验默认 seeds=[42]。baseline 必须联网检索；消融在执行前完成覆盖矩阵；预算审批后由已有 aris 后端自动执行。

内部工具：research_workflow.py 的 init/status/route/checkpoint/resume；experiment_stats.py 的 design-review/expand/gate/summarize。不新增 vibe 公共命令。每个阶段事件 Git 留档，中间规划与日志持续保存；投稿回执、评审、返修、转投及录用记录纳入同一周期。初始化只安装资源，不启动云资源、模型或正式投稿。
