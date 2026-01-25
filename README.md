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
*   **[Frontend Design](skills/anthropics/skills/frontend-design)**: 遵循专业设计美学的界面组件生成，告别"AI 味"十足的平庸设计。
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

---

## 🚀 快速开始

### 1. 克隆仓库并初始化子模块

本项目使用 Git Submodules 管理技能库，首次克隆后需要初始化子模块：

```bash
# 克隆仓库
git clone <repository-url>
cd vibe-coding

# 初始化并更新所有子模块
git submodule update --init --recursive
```

项目包含以下子模块：
- `skills/claude-scientific-skills` - K-Dense AI 科学技能库（140+ 技能）
- `skills/ui-ux-pro-max-skill` - UI/UX 设计技能库
- `skills/anthropics` - Anthropic 官方技能库
- `skills/superpowers` - Superpowers 开发工作流技能

### 2. 更新技能索引

运行标注脚本以生成或更新技能索引：

```bash
# 使用 Python 脚本更新索引
python3 scripts/annotate_skills_mcp.py
```

或者在 Cursor 中使用命令：
```
/annotate-skills-mcp
```

这将生成：
- `skills/ANNOTATIONS.md` - 中文技能索引
- `skills/ANNOTATIONS_EN.md` - 英文技能索引
- `README.md` - 更新项目 README（包含最新统计数据）

### 3. 配置 MCP 服务器（可选）

如果您使用 Cursor IDE 或其他支持 MCP 的客户端，可以配置 `mcp.json` 中定义的 MCP 服务器：

- **promptx-alpha** - Prompt 管理工具
- **pdf-reader-mcp** - PDF 阅读器
- **chrome-devtools** - Chrome 开发者工具集成
- **drawio** - 图表绘制工具
- **claude-scientific-skills** - 科学技能 MCP 服务器（云端）
- **windows-mcp** - Windows 系统集成（Windows 系统）

配置方法请参考您使用的 IDE 的 MCP 设置文档。

### 4. 在 Cursor/Claude Code 中使用技能

**Cursor IDE:**
- 技能会自动从 `skills/` 目录加载
- 确保项目根目录包含 `.cursor/rules/` 中的规则文件

**Claude Code:**
- 通过插件市场安装相关技能插件
- 或直接引用 `skills/` 目录中的技能

---

## 🛠️ 如何使用

1.  **加载技能**: 在支持 Skills 的环境（如 Claude Code 或 Claude.ai）中引用对应目录。
2.  **直接触发**: 
    *   *"使用科学技能分析这段 DNA 序列..."*
    *   *"使用 UI-UX 技能为我的金融 App 生成一个设计系统..."*
    *   *"使用 Word 技能基于这个大纲生成一份季度报告..."*

---

## 📁 项目结构

```
vibe-coding/
├── skills/                    # 技能库目录（包含子模块）
│   ├── claude-scientific-skills/  # 科学技能库（140+ 技能）
│   ├── ui-ux-pro-max-skill/       # UI/UX 设计技能
│   ├── anthropics/                # Anthropic 官方技能
│   ├── superpowers/               # Superpowers 工作流技能
│   ├── agent-skills/              # Agent 技能集合
│   ├── agent-browser/             # 浏览器自动化技能
│   ├── Khazix-Skills/             # 技能演进管理器
│   ├── skills/                    # 其他技能集合
│   ├── ANNOTATIONS.md             # 中文技能索引（自动生成）
│   └── ANNOTATIONS_EN.md          # 英文技能索引（自动生成）
├── .cursor/                   # Cursor IDE 配置
│   ├── rules/                 # 代码规范和规则
│   │   ├── python-uv-standards.mdc
│   │   ├── nextjs-fullstack-standards.mdc
│   │   ├── go-backend-standards.mdc
│   │   └── ...                 # 其他语言/框架规范
│   └── commands/               # 自定义命令
│       └── skill-mcp-annotation.md
├── scripts/                    # 工具脚本
│   └── annotate_skills_mcp.py  # 技能索引生成脚本
├── prompts/                    # 提示词模板
│   ├── creative.md
│   ├── programming.md
│   └── writing.md
├── mcp.json                    # MCP 服务器配置
├── .gitmodules                 # Git 子模块配置
└── README.md                   # 项目说明文档（本文件）
```

### 主要目录说明

- **`skills/`** - 所有技能库的根目录，包含通过 Git Submodules 管理的技能集合
- **`.cursor/rules/`** - Cursor IDE 的代码规范文件，定义了不同语言和框架的开发标准
- **`.cursor/commands/`** - Cursor 自定义命令定义，如 `/annotate-skills-mcp`
- **`scripts/`** - 项目维护脚本，主要用于生成和更新技能索引
- **`prompts/`** - 提示词模板库，用于不同场景的 AI 对话

---

## 🔧 维护与更新

### 更新技能索引

当您添加、修改或删除技能时，需要更新索引以保持同步：

```bash
# 方法 1: 直接运行脚本
python3 scripts/annotate_skills_mcp.py

# 方法 2: 在 Cursor 中使用命令
/annotate-skills-mcp
```

脚本会自动：
- 扫描 `skills/` 目录中的所有 `SKILL.md` 和 `AGENTS.md` 文件
- 提取技能名称、路径和描述信息
- 生成中英文索引文件
- 更新 README.md 中的统计数据

### 更新子模块

当技能库有更新时，可以更新对应的子模块：

```bash
# 更新所有子模块到最新版本
git submodule update --remote

# 更新特定子模块
git submodule update --remote skills/claude-scientific-skills
```

### 添加新的技能

1. 在 `skills/` 目录下创建新的技能目录
2. 添加 `SKILL.md` 或 `AGENTS.md` 文件（遵循 Agent Skills 规范）
3. 运行 `/annotate-skills-mcp` 命令更新索引

### 添加新的 MCP 服务器

1. 在 `mcp.json` 中添加服务器配置
2. 确保服务器符合 MCP 协议规范
3. 在 Cursor 中重新加载 MCP 配置

---

## 📜 许可证

本项目集成的技能库分别遵循其原作者的开源许可：
- Anthropic Skills: Apache 2.0 / Source-available
- Scientific Skills: MIT
- UI-UX Pro Max: MIT
