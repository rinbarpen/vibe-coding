# Auto-Figure Generation Guide

## 概述

自动图表生成能力由 aris 中的三个技能构成：

| 技能 | 用途 | 生成方式 | 适用图表 |
|------|------|----------|----------|
| figure-spec | 确定性图表 | JSON → SVG | 架构图、流程图、工作流图 |
| paper-illustration | AI 插图 | 多阶段 AI 生成 | 概念图、原理图、模型架构图 |
| paper-figure | 数据驱动图表 | 实验数据 → 发行级图表 | 实验结果图、比较图 |

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
