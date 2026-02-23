---
name: scientific-data-visualization
description: 专注于使用 Python/Matplotlib/R 进行科学绘图。遵循英语字体规则，提供美观、规范的学术图表。
---

# Scientific Data Visualization: 科学绘图

## 绘图分类与实现方法

针对学术论文与基金申报，图表分为以下四类，需采用不同的实现策略：

### 1. 数据图 (Data Plots)
- **定义**：展示实验数据、模拟结果、统计分布。
- **工具**：Python (Matplotlib, Seaborn), R (ggplot2)。
- **实现要点**：
    - **强制英语字体**：使用 `plt.rcParams` 设置 Times New Roman。
    - **矢量导出**：优先导出为 `.pdf` 或 `.svg` 以保证无限缩放。
    - **多子图布局**：利用 `plt.subplots(nrows, ncols)` 构建复合图。

### 2. 流程图与架构图 (Flowcharts & Architecture)
- **定义**：展示算法流程、系统架构、逻辑关系。
- **工具**：Mermaid (快速迭代), Draw.io (精细美化)。
- **实现要点**：
    - **Mermaid 语法**：直接在 Markdown 中编写，适合展示逻辑流。参考 [Pretty-mermaid-skills](../Pretty-mermaid-skills/SKILL.md) 进行美化渲染（支持 SVG/ASCII）。
    - **Draw.io 整合**：参考 [drawio-skills](../drawio-skills/skills/drawio/SKILL.md) 进行交互式绘图。
        - **实时预览**：调用 `start_session` 开启浏览器实时预览与编辑。
        - **数学公式**：支持 LaTeX `$$...$$` 或 `\(...\)` 渲染，需开启 `Mathematical Typesetting`。
        - **学术规范**：使用 IEEE 风格预设（黑白、正交线、标准符号）。
        - **导出规范**：导出为高分辨率 PNG 或嵌入式 SVG。

### 3. 技术路线图 (Technical Route)
- **定义**：基金申报书的核心，展示研究内容的逻辑递进。
- **工具**：Draw.io, PowerPoint (配合插件), Canvas Design (艺术化呈现)。
- **实现要点**：
    - **逻辑闭环**：输入 -> 执行 -> 关联 -> 输出。参考 [technical-route.md](references/technical-route.md)。
    - **Canvas Design 整合**：参考 [canvas-design](../anthropics/skills/canvas-design/SKILL.md) 创建具有“设计哲学”的视觉稿。
        - **设计宣言**：先定义视觉哲学（如 "Brutalist Joy"），再进行画布创作。
        - **极简文字**：文字仅作为视觉点缀，通过空间、色彩和构图传达思想。
    - **配色规范**：使用学术色系（如浅蓝、淡绿、浅灰）。

### 4. 科学示意图 (Scientific Illustrations)
- **定义**：展示生物结构、物理模型、实验装置。
- **工具**：BioRender (生物医学), Inkscape (通用矢量), Canvas Design (艺术化示意图)。
- **实现要点**：
    - **比例准确**：示意图需符合基本的物理/生物比例。
    - **标注清晰**：所有关键组件需有清晰的英语标注。
    - **艺术化提升**：利用 Canvas Design 的设计原则，提升示意图的“大师感”与“独特性”。

## 核心任务
1. **绘图代码生成**：根据数据生成 Matplotlib, Seaborn, ggplot2 等绘图代码。
2. **图表美化**：调整颜色、字体、布局，符合学术期刊规范。
3. **英语字体规则**：确保图表中的所有文字（标题、标签、图例）均为英语。

## 工作流
- **Step 1**: 识别绘图类型（数据图/流程图/路线图/示意图）。
- **Step 2**: 选择工具链并生成初步方案（参考 [references/plotting-config.md](references/plotting-config.md)）。
- **Step 3**: 运行代码或生成模板，进行可视化。
- **Step 4**: 根据反馈微调，导出最终格式。

## 技巧
- **Matplotlib**: 使用 `plt.rcParams` 设置字体。
- **颜色**: 使用颜色盲友好的配色方案。
- **格式**: 优先生成矢量图（PDF, EPS）。
