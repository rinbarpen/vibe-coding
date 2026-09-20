# 投稿 venue 与图表要求

Writing Plan 将投稿要求作为版本化输入，而不是在写作过程中由 writer 临时猜测。内置快照位于：

- `writing/venue-profiles.yaml`：期刊、会议和审稿服务的要求 profile。
- `writing/figure-types.yaml`：图类型、renderer、输入、输出和验收规则。
- `writing/writing-plan.schema.json`：`venue` 和 `presentation.figures` 的结构约束。

## 1. 选择与冻结 venue

在 `.auto-research/writing-plan.yaml` 顶层声明目标 venue：

```yaml
venue:
  profile: neurips-2025-reference
  source_url: https://neurips.cc/Conferences/2025/CallForPapers
  checked_at: "2026-09-19"
  overrides:
    manuscript:
      track: main
```

profile 是要求快照，不是永久真理。每次 abstract deadline、投稿、camera-ready 或转投前都要重新打开 `source_url`，核对 CFP、官方模板、页数、文件大小、匿名、补充材料和作者声明，并更新 `checked_at`。若官方要求和快照不一致，以官方页面为准，然后在 YAML 中写显式 override 并重新审批。

当前内置参考快照覆盖：

| Profile | 用途 | 关键约束示例 |
|---|---|---|
| `generic-journal` | 通用期刊基线 | 图格式/分辨率/声明按期刊作者指南覆盖 |
| `generic-conference` | 通用会议基线 | 官方模板、匿名、正文页数和 supplement 按 CFP 覆盖 |
| `neurips-2025-reference` | NeurIPS 参考快照 | 9 页正文、单 PDF、checklist、50 MB、匿名 |
| `icml-2025-reference` | ICML 参考快照 | 8 页正文、单 PDF、匿名、50 MB/20 MB 文件限制 |
| `acl-arr-reference` | ACL Rolling Review 参考快照 | long/short 页数、ACL 双栏模板、limitations、匿名、补充包 |
| `nature-article-reference` | Nature Article 参考快照 | 典型正文/展示项、90/180 mm、图例 300 词、最终可编辑图 |

这些快照的官方依据直接记录在 YAML 的 `source_url` 中：

- [NeurIPS 2025 Call for Papers](https://neurips.cc/Conferences/2025/CallForPapers)
- [ICML 2025 Author Instructions](https://icml.cc/Conferences/2025/AuthorInstructions)
- [ACL Rolling Review CFP](https://aclrollingreview.org/cfp)
- [Nature formatting guide](https://www.nature.com/nature/for-authors/formatting-guide)
- [Nature research figure guide](https://research-figure-guide.nature.com/)

## 2. 图类型与生成器

每个 `figure` 节点在 `presentation.figures` 中声明一个稳定的图规格：

```yaml
presentation:
  figures:
    - id: fig-ablation-main
      type: ablation
      title: 组件消融
      renderer: paper-figure
      data_source: results/ablation-summary.csv
      input_files: [results/run-records.json]
      outputs: [figures/fig-ablation-main.pdf, figures/fig-ablation-main.svg]
      formats: [pdf, svg]
      caption: 移除各组件后主要指标的变化。
      alt_text: 完整模型与各消融模型的指标比较
      provenance:
        command: python scripts/plot_ablation.py --input results/ablation-summary.csv
        code_revision: 7b2c1d
```

### 确定性结构图：`figure-spec`

- `architecture`：模型/系统架构
- `flowchart`：决策流程
- `pipeline`：数据或实验管线
- `algorithm`：算法步骤和复杂度
- `timeline`：时间线和里程碑

输入是 JSON 图规格，输出优先使用 SVG/PDF；同一输入必须得到稳定输出。

### 数据驱动图：`paper-figure` / `plot`

- `comparison`：baseline 对比
- `ablation`：组件、交互项和替代实现消融
- `training_curve`：训练/验证曲线
- `scaling`：规模、成本、延迟和性能关系
- `distribution`：箱线图、小提琴图和样本分布
- `scatter`：相关性、回归和误差关系
- `heatmap`：矩阵、敏感性和超参数扫描
- `confusion_matrix`：分类结果和归一化规则
- `qualitative_grid`：定性样例网格
- `attention`：注意力或归因可视化
- `map`：地理或空间分布

这些类型必须声明数据来源；如果是多 seed 结果，图规格必须指定聚合方式和不确定性展示方式。

### 概念插图：`paper-illustration`

- `concept_illustration` 用于机制示意、直觉解释和非定量概念图。
- 必须同时声明 `alt_text`、素材来源和“示意图而非定量结果”的 caption 约束。
- 概念插图不得伪装成实验数据，也不得改变已审批的核心结论。

## 3. 自动校验

`writing_plan.py resolve` 会把每个图节点扩展为：

- 图类型要求和默认 renderer
- 输出格式、caption、alt text 和 provenance
- 目标 venue 的格式、分辨率、尺寸、颜色空间、图例和可访问性要求
- `resolved_plan_hash`

`writing_plan.py review` 会逐节点检查：

- 图文件是否存在且路径未越出项目根目录
- 图类型与 renderer 是否匹配
- caption、alt text、数据来源、生成命令和 code revision 是否齐全
- 声明格式是否被 venue 允许
- caption 是否超过 venue 限制
- 分辨率、颜色空间和最终尺寸是否已声明

缺少原始数据、生成命令或代码 revision 的图会进入 `blocked_missing_evidence`；格式或文件缺失进入 `fail`。受限自动修订只处理 caption、格式标记和遗漏说明，不替换数据、统计方法或核心图形含义。

## 4. 投稿前顺序

```text
选择 venue
  → 打开官方 CFP/author guide/figure guide
  → 更新 venue profile 与 checked_at
  → validate
  → resolve
  → 生成图规格与图文件
  → review 图节点和正文节点
  → 编译 PDF/投稿包
  → 对照官方 checklist
  → Git checkpoint 与归档
```

期刊和会议的页数、模板、匿名、图尺寸、文件格式、补充材料、数据/代码声明和截止时间均不能从旧快照静默推断；变化必须形成新的计划哈希和 Git 记录。
