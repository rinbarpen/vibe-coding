# vibe-coding

本项目是一个集成了多种专业 AI 技能 (Skills) 的工具库，旨在将 Claude 转化为具备多领域专业知识的智能助手。通过集成科学研究、设计美学和开发者工具，您可以直接在对话中执行复杂的专业任务。

---

## 🚀 核心技能详细介绍

### 1. 🧬 科学研究与协同实验室 (Scientific Research)
基于 **[Claude Scientific Skills](skills/claude-scientific-skills)** (K-Dense AI)，包含 **140+** 个深度集成的科研技能。

*   **生物信息学与基因组学**: 序列分析、单细胞 RNA-seq 处理、基因调节网络、变异注释。
*   **化学信息学与药物发现**: 分子属性预测、虚拟筛选、ADMET 分析、分子对接 (Molecular Docking)。
*   **蛋白质组学**: LC-MS/MS 数据处理、肽段鉴定、蛋白质定量。
*   **临床研究与精准医疗**: 临床试验分析、药物安全评估、治疗方案规划。
*   **医疗影像**: DICOM 处理、全切片图像分析、数字化病理流。
*   **物理与材料科学**: 晶体结构分析、相图计算、天文数据转换。

### 2. 🎨 UI/UX 设计智能 (Design Intelligence)
结合 **[UI-UX Pro Max](skills/ui-ux-pro-max-skill)** 与 Anthropic 官方设计技能。

*   **智能设计系统生成**: 自动分析项目需求并生成完整的视觉规范。
*   **58+ UI 风格库**: 支持 Glassmorphism (毛玻璃), Neumorphism (新拟态), Minimalism 等流行风格。
*   **[Frontend Design](skills/anthropics/skills/frontend-design)**: 遵循专业设计美学的界面组件生成，告别“AI 味”十足的平庸设计。
*   **[Theme Factory](skills/anthropics/skills/theme-factory)**: 预设多种行业主题（如 Arctic Frost, Midnight Galaxy），一键切换视觉风格。
*   **[Algorithmic Art](skills/anthropics/skills/algorithmic-art)**: 基于 p5.js 的生成艺术创作。

### 3. 📄 生产力与办公自动化 (Enterprise Productivity)
深度集成 **[Anthropic Official Document Skills](skills/anthropics)**，包含 **16+** 个官方文档处理技能。

*   **[Word (docx)](skills/anthropics/skills/docx)**: 高级文档创建、修订追踪、复杂格式处理。
*   **[Excel (xlsx)](skills/anthropics/skills/xlsx)**: 自动化数据透视、公式生成与大规模表格分析。
*   **[PowerPoint (pptx)](skills/anthropics/skills/pptx)**: 结构化幻灯片生成、内容布局优化。
*   **[PDF Master](skills/anthropics/skills/pdf)**: 提取表单字段、PDF 标注填充、图像转换。
*   **[Internal Comms](skills/anthropics/skills/internal-comms)**: 企业新闻稿、状态报告、FAQ 编写模板。

### 4. 🛠️ 开发者增强工具 (Developer Empowerment)
专为程序员设计的自动化流，提升开发效率。

*   **[MCP Builder](skills/anthropics/skills/mcp-builder)**: 自动生成符合 Model Context Protocol 规范的服务器代码（Node/Python）。
*   **[Web Artifacts Builder](skills/anthropics/skills/web-artifacts-builder)**: 快速构建 React + Tailwind + Lucide 的交互式组件预览。
*   **[Webapp Testing](skills/anthropics/skills/webapp-testing)**: 使用 Playwright 自动编写并运行本地应用测试用例。
*   **[Skill Creator](skills/anthropics/skills/skill-creator)**: 遵循 Agent Skills 规范，辅助您开发和校验自定义技能。

---

## 📂 技能与 MCP 索引 (Index)

为了方便查找和使用，我们提供了详细的技能与 MCP 服务器标注索引：
- 🇨🇳 [中文标注索引](skills/ANNOTATIONS.md)
- 🇺🇸 [English Annotations Index](skills/ANNOTATIONS_EN.md)

## 🛠️ 如何使用

1.  **加载技能**: 在支持 Skills 的环境（如 Claude Code 或 Claude.ai）中引用对应目录。
2.  **直接触发**: 
    *   *“使用科学技能分析这段 DNA 序列...”*
    *   *“使用 UI-UX 技能为我的金融 App 生成一个设计系统...”*
    *   *“使用 Word 技能基于这个大纲生成一份季度报告...”*

## 📜 许可证

本项目集成的技能库分别遵循其原作者的开源许可：
- Anthropic Skills: Apache 2.0 / Source-available
- Scientific Skills: MIT
- UI-UX Pro Max: MIT
