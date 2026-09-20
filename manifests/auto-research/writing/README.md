# Writing Plan 子系统

Writing Plan 用稳定节点 ID 把写作要求、审批状态、正文和审查结果连接起来。人工与 agent 共同维护 `.auto-research/writing-plan.yaml`；writer 只读取解析后的 `.auto-research/resolved-writing-plan.json`。`WRITING_PLAN.md` 是生成视图，人工修改不会被读取。

投稿 venue 与图生成也属于计划事实源：`venue` 选择 `venue-profiles.yaml` 中的要求快照；`presentation.figures` 选择 `figure-types.yaml` 中的图类型和 renderer。resolver 会把 venue 要求和图类型要求注入每个 resolved node，reviewer 据此检查格式、尺寸、caption、alt text、来源和生成命令。

## 命令

```bash
uv run scripts/writing_plan.py init --outline PAPER_OUTLINE.md --output .auto-research/writing-plan.yaml
uv run scripts/writing_plan.py validate .auto-research/writing-plan.yaml
uv run scripts/writing_plan.py resolve .auto-research/writing-plan.yaml --output .auto-research/resolved-writing-plan.json
uv run scripts/writing_plan.py render .auto-research/resolved-writing-plan.json --output WRITING_PLAN.md
uv run scripts/writing_plan.py review .auto-research/resolved-writing-plan.json --content-root . --json-output .auto-research/writing-review.json --markdown-output WRITING_REVIEW.md
uv run scripts/writing_plan.py migrate --project-root . --output .auto-research/writing-plan.yaml
```

返回码：成功为 `0`；schema、语义或内容验收失败为 `1`；I/O、依赖或工具内部错误为 `2`。`validate` 和 `review` 把机器可读 JSON 写到 stdout，把短摘要写到 stderr。`init` 与 `migrate` 只有显式传入 `--force` 才覆盖现有计划。

使用 `init --force` 从更新后的大纲同步节点时，工具只对“节点类型与标题均唯一且一致”的可靠匹配复用现有 ID，并保留该节点的局部配置；无法可靠匹配的条目获得新 ID。若删除导致交叉引用或审批记录孤立，同步会以配置失败退出且保留旧文件，等待 planner 先处理引用。

## 字段与节点

- `document`：文档身份、目的、语言、成功标准及文档级默认值。
- `profiles`：项目局部 profile；会覆盖同名内置 profile。
- `defaults`：整个文档的受众、风格、篇幅、证据、呈现与审批默认值。
- `workflow`：写后审查、受限自动修订和失败类别。
- `approvals`：以 node ID 为键的审批记录；记录中的 `resolved_plan_hash` 必须与当前节点要求哈希相同。
- `nodes`：文件、章节、标题、段落、图表、引用、参考文献、附录、术语表等内容节点。
- `venue`：投稿类型、官方要求快照、来源 URL、核验日期和项目级覆盖。每次投稿或 camera-ready 前刷新官方页面并更新 `checked_at`。

### 图节点

图节点使用 `presentation.figures` 声明可复现图规格。支持 `architecture`、`flowchart`、`pipeline`、`algorithm`、`comparison`、`ablation`、`training_curve`、`scaling`、`distribution`、`scatter`、`heatmap`、`confusion_matrix`、`qualitative_grid`、`attention`、`timeline`、`map` 和 `concept_illustration`。数据驱动图必须给出 `data_source`/`input_files`；所有图必须给出 `caption`、`alt_text`、输出格式和 `provenance.command/code_revision`。

图的具体 renderer、输入、输出和验收项见 [`figure-types.yaml`](figure-types.yaml)，投稿快照和官方来源见 [`venue-profiles.yaml`](venue-profiles.yaml)。完整运行规则见 [`references/venue-requirements.md`](../references/venue-requirements.md)。

节点 ID 必须匹配 `^[a-z][a-z0-9-]{2,63}$`，且在计划中唯一。改标题、次序和输出路径时保留 ID；删除节点前先清理交叉引用与审批记录。正文推荐使用下列锚点，以便逐节点审查：

```markdown
<!-- node:sec-methodology:start -->
正文……
<!-- node:sec-methodology:end -->
```

## 继承

优先级为：内置默认值 → 引用 profile → document/defaults → file 节点 → 祖先节点 → 当前节点。每一层先应用该层引用的 profile，再应用局部字段。

- 标量由子级覆盖。
- 对象递归合并。
- 列表默认整体替换。
- `{append: [...]}` 在继承列表末尾追加并保序。
- `{unset: true}` 删除继承值。
- `id`、`type`、`parent_id`、`output_path`、`anchor` 不从 profile 或父节点继承；只有 `output_path` 会从最近的 file 祖先复制给后代。
- resolved JSON 不包含 `profile`、`append` 或 `unset`。

示例：

```yaml
defaults:
  style: {profile: academic}
  content: {keywords: [可复现]}
nodes:
  - id: sec-methods
    type: section
    title: 方法
    order: 10
    content:
      keywords: {append: [透明度]}
      optional: {unset: true}
```

## 审批语义

`approval: auto` 直接进入写作；`approval: before_write` 仅在该节点边界暂停。resolver 为每个节点输出 `resolved_plan_hash` 和 `approval_state`。当目标、受众、风格、证据或其他 resolved 要求改变时，哈希改变，旧审批自动变为 `stale`。标题、次序和输出路径不参与要求哈希，因此不会无故使内容审批失效。

审批记录示例：

```yaml
approvals:
  sec-methodology:
    status: approved
    resolved_plan_hash: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
    approved_by: reviewer
    approved_at: 2026-09-19T10:00:00+08:00
```

## Review 与受限修订

review 按节点检查目标、受众、风格、篇幅、必含/禁用内容、证据、呈现和交叉引用，状态固定为 `pass`、`warning`、`fail` 或 `blocked_missing_evidence`。`auto_fix: constrained` 只允许修复篇幅、格式、措辞和遗漏说明；核心结论、证据标准、章节结构与已审批目标需要重新规划/审批。报告中的 `allowed_auto_fixes` 明确列出可局部修订项，writer 只重写不合格节点。

## 常见错误

- 重复 ID、缺失父节点或父子循环。
- profile 名称不存在或 profile 自引用。
- 两个 file 节点使用同一个 `output_path`。
- 交叉引用、审批记录指向已删除 ID。
- `length.min > target`、`target > max` 或 `min > max`。
- 直接编辑 `WRITING_PLAN.md`，而未修改 YAML 后重新 validate/resolve/render。

## 图实现配方与可配置审美

17 类图分别使用 `figure-types.yaml` 的 `implementation` 配方，详见
[`逐类实现方法`](../references/figure-implementation-recipes.md)。配色见 `figure-palettes.yaml`。

```yaml
defaults:
  presentation:
    figure_style:
      palette: editorial     # editorial / contrast / earth / monochrome
      font_size_pt: 9
      series_colors:         # 按稳定方法名映射，避免图间颜色漂移
        ours: "#31688E"
        baseline: "#6D7885"
# 在任意 figure spec 中局部覆盖：
# visual:
#   palette: earth
#   mode: diverging
#   colors: ["#276582", "#F5F3ED", "#A74732"]
```

优先级：视觉默认值 → 文档/文件/祖先的 figure_style → 当前节点 figure_style → 单图 visual。
`colors` 整组替换，`series_colors` 按方法名合并；改 palette 后若已有自定义 colors，仍以自定义 colors 为准。
resolver 输出 `resolved_visual`（实际颜色、字号、线宽、画布尺寸和色彩语义），renderer 必须消费它。
图数据、布局或配色改变后重跑 resolve/review；变化计入审批哈希。自定义组合仍需灰度、色觉与最终尺寸视觉复核。
数据类型允许使用 `plot` 指定本地绘图脚本。此功能提供可执行规划解析和逐类生成契约；渲染由已安装 skill/项目脚本完成。

## 图完整性与合成冒烟测试

review 拒绝零字节图文件、非法 SVG XML、没有图形元素的 SVG、非法 PDF/EPS 文件头尾、损坏光栅文件、未声明输出和格式后缀不匹配。输入文件必须存在且非空；远程来源需先下载留档。光栅验证使用 Pillow，未安装时给出失败而非跳过。PDF/EPS 目前只检查 envelope，返回 warning 并要求完整渲染检查；SVG 的结构检查不等于可见性或科学性证明。

运行 `uv run scripts/figure_smoke.py --output /tmp/figure-smoke --palette editorial`，可生成 17 类明确标为 SYNTHETIC 的布局样例，每类输出 SVG/PDF/PNG、输入 JSON 和哈希清单。支持四套预设。它是布局回归夹具，不是生产科研数据后端，不调用付费模型；地图是虚构局部坐标网格，概念图是程序化机制草图。

可复现方法：固定 seed=42，同一环境重跑；PNG/SVG 内容可比较。PDF 元数据可能包含时间，不宣称跨次字节相同。最终还需按实际数据、目标期刊尺寸和色觉检查验收。

## GPT 图像与可编辑 PPTX 双交付（优先于旧生成路线）

architecture / flowchart / pipeline / algorithm / concept_illustration 的 renderer 改为 `gpt-image`，其 `type_requirements.editable_renderer` 为 `gpt-pptx`。前者负责视觉稿，后者由 GPT 编排可编辑 SVG/原生对象，通过 ppt-master 导出 PPTX。它们是编排契约，不是 writing_plan.py 内置的网络调用接口；宿主必须配置实际模型绑定与执行工具并记录实际身份。缺少绑定应阻塞，禁止退回旧方框图冒充完成。

PPTX 必须保留独立文本和形状，禁止整页位图充当可编辑图；连线可编辑不代表移动节点后自动重路由。共享语义规格是事实源，两版均需逐项检查标签、节点、分支、循环和输入输出。SVG 是中间格式；PNG 是图像版；PPTX 是编辑源。图像生成不承诺确定性，PPTX 不承诺与位图逐像素一致。

`figure_file_error` 新增 PPTX ZIP/XML 及每页原生形状/文本检查，但这仅是最低门禁，不证明全部对象都可编辑或与语义规格一致。

其余数据图保留代码绘图；样例采用 Liberation Sans，轴标签 11 pt、刻度 9.5 pt、图例 9 pt，统计定义下移到图注，减少大标题和轴标签拥挤。文字与科研图几何须在目标输出尺寸重新验收。`figure_smoke.py` 仅渲染剩余 12 类，另写出五类 GPT 待生成请求，不虚构外部调用成功。
