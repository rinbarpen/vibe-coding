# Auto-Figure Generation Guide

## 概述

图生成不再只由一句自然语言描述驱动。写作阶段先在 Writing Plan 中创建稳定 figure node，再从 `writing/figure-types.yaml` 选择图类型和 renderer，最后按目标投稿 venue 的要求进行尺寸、格式、分辨率、可访问性和 provenance 校验。期刊/会议规则见 [`venue-requirements.md`](venue-requirements.md)。

自动图表生成能力由 aris 中的三个技能构成：

| 技能 | 用途 | 生成方式 | 适用图表 |
|------|------|----------|----------|
| figure-spec | 确定性图表 | JSON → SVG | 架构图、流程图、工作流图 |
| paper-illustration | AI 插图 | 多阶段 AI 生成 | 概念图、原理图、模型架构图 |
| paper-figure | 数据驱动图表 | 实验数据 → 发行级图表 | 实验结果图、比较图 |

完整类型库包括：architecture、flowchart、pipeline、algorithm、comparison、ablation、training_curve、scaling、distribution、scatter、heatmap、confusion_matrix、qualitative_grid、attention、timeline、map 和 concept_illustration。每种类型的输入、输出、caption 模板和验收条件记录在 `writing/figure-types.yaml`，未知类型由 schema 拒绝。

## figure-spec（确定性图表）

### 原理
基于 FigureSpec v2 规范：JSON 描述 → 确定性 SVG 渲染。

### 输入格式
```json
{
  "type": "architecture",
  "title": "Model Architecture",
  "nodes": [
    {"id": "input", "label": "Input", "type": "rect", "pos": [0, 0]},
    {"id": "encoder", "label": "Encoder", "type": "rect", "pos": [0, 1]},
    {"id": "decoder", "label": "Decoder", "type": "rect", "pos": [0, 2]}
  ],
  "edges": [
    {"from": "input", "to": "encoder", "label": "features"},
    {"from": "encoder", "to": "decoder", "label": "latent"}
  ]
}
```

### 特点
- 完全确定性：相同输入总是相同输出
- 形状感知边缘裁剪（shape-aware edge cropping）
- 支持曲线路径、CJK 文本
- SVG 格式，可直接嵌入论文

### 适用场景
- 模型架构图
- 算法工作流图
- 数据处理 pipeline 图
- 系统架构图

### 使用方式
```
aris/figure-spec "描述需要生成的图表内容和结构"
```

## paper-illustration（AI 插图）

### 流程
```
Claude 监督阶段:
  1. 分析论文内容，确定插图需求
  2. 生成插图描述（composition, color palette, style）
  3. 质量检查

Gemini 渲染阶段:
  4. 根据描述生成图像
  5. 后处理（裁剪、调色）
```

### 适用场景
- 概念图（Concept illustration）
- 原理示意图
- 方法对比图
- 结果展示图

### 使用方式
```
aris/paper-illustration "描述需要的插图内容和风格"
```

## paper-figure（数据驱动图表）

### 流程
```
实验结果 → 图表规格 → 发行级渲染
```

### 适用场景
- 折线图（训练曲线）
- 柱状图（对比实验）
- 热力图（消融实验）
- 散点图（相关性分析）

### 使用方式
paper-writing 管线中自动调用，也可单独使用：
```
aris/paper-figure "实验结果的路径和图表要求"
```

## 生成记录与写后审查

每个图规格必须记录 `data_source` 或 `input_files`、`outputs`、`formats`、`caption`、`alt_text` 和 `provenance.command/code_revision`。`writing_plan.py resolve` 会将 `type_requirements` 和 `generation_defaults` 注入 resolved node；`review` 检查生成文件、venue 允许格式、caption 上限、来源和可复现命令。图文件和规格随当前阶段的 Git checkpoint 一起归档。

## GPT 双版本路线（覆盖上述五类旧后端）

Architecture、Flow、Pipeline、Algorithm、Concept 使用 `gpt-image` 生成视觉稿；可编辑版本交给 GPT 根据同一已批准语义规格设计 SVG，使用 ppt-master 原生形状导出器生成 PPTX。SVG 留档为中间源码，不以整页 SVG 图片或位图冒充可编辑 PPTX。文字、模块、箭头、图例应分别可编辑；保留调色板与字体设置。逐页审查标签、连线方向、分支和循环，与视觉稿分别核对事实，不要求逐像素一致。

记录提示词、实际模型身份、输入规格、SVG、PPTX、预览及审查日志；缺少宿主模型绑定时标记 `blocked_backend_unavailable`。此 scaffold 定义编排契约，不内置模型 API 客户端。数据图仍由真实数据和绘图代码生成，禁止图像模型代画数值结果。
