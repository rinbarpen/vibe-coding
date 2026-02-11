import os
import json
import re
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).parents[3]
SKILLS_DIR = WORKSPACE_ROOT / "skills"
# MCP 路径可能需要根据实际环境调整，这里使用之前探索到的路径
MCPS_DIR = Path("/home/rczx/.cursor/projects/home-rczx-workspace-rinbarpen-vibe-coding/mcps")

LANGS = {
    'cn': {
        'title': 'Skills & MCP 标注索引',
        'skills': '技能 (Skills)',
        'mcps': 'MCP 服务器 (MCP Servers)',
        'path': '路径',
        'desc': '简介',
        'usage': '使用场景',
        'see_desc': '见简介',
        'file_name': 'ANNOTATIONS.md'
    },
    'en': {
        'title': 'Skills & MCP Annotations Index',
        'skills': 'Skills',
        'mcps': 'MCP Servers',
        'path': 'Path',
        'desc': 'Description',
        'usage': 'Usage',
        'see_desc': 'See description',
        'file_name': 'ANNOTATIONS_EN.md'
    }
}

def extract_skill_info(skill_path):
    skill_md = skill_path / "SKILL.md"
    agents_md = skill_path / "AGENTS.md"
    
    target_file = None
    if skill_md.exists():
        target_file = skill_md
    elif agents_md.exists():
        target_file = agents_md
        
    if not target_file:
        return None
    
    content = target_file.read_text(encoding="utf-8")
    
    # Try to extract YAML frontmatter manually to avoid PyYAML dependency
    name = skill_path.name
    description = ""
    
    yaml_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if yaml_match:
        yaml_content = yaml_match.group(1)
        name_match = re.search(r"^name:\s*(.*)$", yaml_content, re.MULTILINE)
        desc_match = re.search(r"^description:\s*(.*)$", yaml_content, re.MULTILINE)
        if name_match:
            name = name_match.group(1).strip().strip('"').strip("'")
        if desc_match:
            description = desc_match.group(1).strip().strip('"').strip("'")
            
    if not description:
        # Fallback: find first # header and first paragraph
        header_match = re.search(r"^#\s+(.*)$", content, re.MULTILINE)
        if header_match:
            name = header_match.group(1).strip()
        
        # Find first non-empty line after header
        body = re.sub(r"^---.*?---\s*", "", content, flags=re.DOTALL)
        body = re.sub(r"^#.*$", "", body, flags=re.MULTILINE)
        paragraphs = [p.strip() for p in body.split("\n") if p.strip()]
        if paragraphs:
            description = paragraphs[0]

    return {
        "name": name,
        "path": str(skill_path.relative_to(WORKSPACE_ROOT)),
        "description": description
    }

def extract_mcp_info(mcp_path):
    metadata_file = mcp_path / "SERVER_METADATA.json"
    instructions_file = mcp_path / "INSTRUCTIONS.md"
    
    if not metadata_file.exists():
        return None
        
    try:
        metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
        name = metadata.get("serverName", mcp_path.name)
    except Exception:
        name = mcp_path.name
        
    description = ""
    if instructions_file.exists():
        content = instructions_file.read_text(encoding="utf-8")
        # Get first paragraph
        paragraphs = [p.strip() for p in content.split("\n") if p.strip()]
        if paragraphs:
            description = paragraphs[0]
            
    return {
        "name": name,
        "path": str(mcp_path),
        "description": description
    }

def generate_markdown(skills_data, mcps_data, lang='cn'):
    labels = LANGS[lang]
    output = [f"# {labels['title']}\n"]
    
    output.append(f"## {labels['skills']}\n")
    for s in sorted(skills_data, key=lambda x: x['name']):
        output.append(f"### {s['name']}")
        output.append(f"- **{labels['path']}**: `{s['path']}`")
        output.append(f"- **{labels['desc']}**: {s['description']}")
        
        usage = s['description'] if "Use" in s['description'] or "使用" in s['description'] else labels['see_desc']
        output.append(f"- **{labels['usage']}**: {usage}")
        output.append("")

    output.append(f"## {labels['mcps']}\n")
    for m in sorted(mcps_data, key=lambda x: x['name']):
        output.append(f"### {m['name']}")
        output.append(f"- **{labels['path']}**: `{m['path']}`")
        output.append(f"- **{labels['desc']}**: {m['description']}")
        
        usage = m['description'] if "Use" in m['description'] or "使用" in m['description'] else labels['see_desc']
        output.append(f"- **{labels['usage']}**: {usage}")
        output.append("")
    
    return "\n".join(output)

def get_counts():
    sci_count = 0
    sci_dir = SKILLS_DIR / "claude-scientific-skills" / "scientific-skills"
    if sci_dir.exists():
        sci_count = len([d for d in sci_dir.iterdir() if d.is_dir()])
        
    ui_styles_count = 0
    ui_styles_file = SKILLS_DIR / "ui-ux-pro-max-skill" / "skills" / "ui-ux-pro-max" / "data" / "styles.csv"
    if ui_styles_file.exists():
        try:
            with open(ui_styles_file, 'r', encoding='utf-8') as f:
                ui_styles_count = len(f.readlines()) - 1
        except Exception:
            ui_styles_count = 57 # Fallback
            
    anthropic_count = 0
    anth_dir = SKILLS_DIR / "anthropics" / "skills"
    if anth_dir.exists():
        anthropic_count = len([d for d in anth_dir.iterdir() if d.is_dir()])
        
    return {
        'scientific': sci_count,
        'ui_styles': ui_styles_count,
        'anthropic': anthropic_count
    }

def update_readmes(counts):
    # Chinese README
    readme_cn = f"""# vibe-coding

本项目是一个集成了多种专业 AI 技能 (Skills) 的工具库，旨在将 Claude 转化为具备多领域专业知识的智能助手。通过集成科学研究、设计美学和开发者工具，您可以直接在对话中执行复杂的专业任务。

---

## 🚀 核心技能详细介绍

### 1. 🧬 科学研究与协同实验室 (Scientific Research)
基于 **[Claude Scientific Skills](skills/claude-scientific-skills)** (K-Dense AI)，包含 **{counts['scientific']}+** 个深度集成的科研技能。

*   **生物信息学与基因组学**: 序列分析、单细胞 RNA-seq 处理、基因调节网络、变异注释。
*   **化学信息学与药物发现**: 分子属性预测、虚拟筛选、ADMET 分析、分子对接 (Molecular Docking)。
*   **蛋白质组学**: LC-MS/MS 数据处理、肽段鉴定、蛋白质定量。
*   **临床研究与精准医疗**: 临床试验分析、药物安全评估、治疗方案规划。
*   **医疗影像**: DICOM 处理、全切片图像分析、数字化病理流。
*   **物理与材料科学**: 晶体结构分析、相图计算、天文数据转换。

### 2. 🎨 UI/UX 设计智能 (Design Intelligence)
结合 **[UI-UX Pro Max](skills/ui-ux-pro-max-skill)** 与 Anthropic 官方设计技能。

*   **智能设计系统生成**: 自动分析项目需求并生成完整的视觉规范。
*   **{counts['ui_styles']}+ UI 风格库**: 支持 Glassmorphism (毛玻璃), Neumorphism (新拟态), Minimalism 等流行风格。
*   **[Frontend Design](skills/anthropics/skills/frontend-design)**: 遵循专业设计美学的界面组件生成，告别“AI 味”十足的平庸设计。
*   **[Theme Factory](skills/anthropics/skills/theme-factory)**: 预设多种行业主题（如 Arctic Frost, Midnight Galaxy），一键切换视觉风格。
*   **[Algorithmic Art](skills/anthropics/skills/algorithmic-art)**: 基于 p5.js 的生成艺术创作。

### 3. 📄 生产力与办公自动化 (Enterprise Productivity)
深度集成 **[Anthropic Official Document Skills](skills/anthropics)**，包含 **{counts['anthropic']}+** 个官方文档处理技能。

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

### 5. 📦 更多社区与专项技能 (More Community & Specialized Skills)

*   **[AI-Research-SKILLs](skills/AI-Research-SKILLs)**: 83+ AI/ML 研究工程技能（模型架构、训练、推理、评估、论文写作等）。
*   **[Humanizer-zh](skills/Humanizer-zh)**: 去除中文文本的 AI 写作痕迹，使表述更自然。
*   **[Pretty-mermaid-skills](skills/Pretty-mermaid-skills)**: 高质量 Mermaid 图表渲染，多主题、SVG/ASCII 输出。
*   **[chinese-novelist-skill](skills/chinese-novelist-skill)**: 分章节中文小说创作，支持长篇与多题材。

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
"""
    WORKSPACE_ROOT.joinpath("README.md").write_text(readme_cn, encoding="utf-8")

    # English README
    readme_en = f"""# vibe-coding

This project is a toolkit that integrates various professional AI Skills, aiming to transform Claude into an intelligent assistant with multi-domain professional knowledge. By integrating scientific research, design aesthetics, and developer tools, you can perform complex professional tasks directly in the conversation.

---

## 🚀 Core Skills Detailed Introduction

### 1. 🧬 Scientific Research & Collaborative Lab
Based on **[Claude Scientific Skills](skills/claude-scientific-skills)** (K-Dense AI), containing **{counts['scientific']}+** deeply integrated research skills.

*   **Bioinformatics & Genomics**: Sequence analysis, single-cell RNA-seq processing, gene regulatory networks, variant annotation.
*   **Cheminformatics & Drug Discovery**: Molecular property prediction, virtual screening, ADMET analysis, molecular docking.
*   **Proteomics**: LC-MS/MS data processing, peptide identification, protein quantification.
*   **Clinical Research & Precision Medicine**: Clinical trial analysis, drug safety assessment, treatment planning.
*   **Medical Imaging**: DICOM processing, whole-slide image analysis, digital pathology workflows.
*   **Physics & Materials Science**: Crystal structure analysis, phase diagram calculation, astronomical data conversion.

### 2. 🎨 UI/UX Design Intelligence
Combines **[UI-UX Pro Max](skills/ui-ux-pro-max-skill)** with Anthropic official design skills.

*   **Intelligent Design System Generation**: Automatically analyze project requirements and generate complete visual specifications.
*   **{counts['ui_styles']}+ UI Style Library**: Supports Glassmorphism, Neumorphism, Minimalism, and other popular styles.
*   **[Frontend Design](skills/anthropics/skills/frontend-design)**: Generate interface components following professional design aesthetics, avoiding mediocre "AI-flavored" designs.
*   **[Theme Factory](skills/anthropics/skills/theme-factory)**: Preset multiple industry themes (e.g., Arctic Frost, Midnight Galaxy) for one-click visual style switching.
*   **[Algorithmic Art](skills/anthropics/skills/algorithmic-art)**: Generative art creation based on p5.js.

### 3. 📄 Enterprise Productivity & Office Automation
Deeply integrates **[Anthropic Official Document Skills](skills/anthropics)**, containing **{counts['anthropic']}+** official document processing skills.

*   **[Word (docx)](skills/anthropics/skills/docx)**: Advanced document creation, revision tracking, complex formatting.
*   **[Excel (xlsx)](skills/anthropics/skills/xlsx)**: Automated pivot tables, formula generation, and large-scale spreadsheet analysis.
*   **[PowerPoint (pptx)](skills/anthropics/skills/pptx)**: Structured slide generation, content layout optimization.
*   **[PDF Master](skills/anthropics/skills/pdf)**: Extract form fields, PDF annotation filling, image conversion.
*   **[Internal Comms](skills/anthropics/skills/internal-comms)**: Corporate press releases, status reports, FAQ writing templates.

### 4. 🛠️ Developer Empowerment
Automated workflows designed for programmers to enhance development efficiency.

*   **[MCP Builder](skills/anthropics/skills/mcp-builder)**: Automatically generate server code (Node/Python) following Model Context Protocol specifications.
*   **[Web Artifacts Builder](skills/anthropics/skills/web-artifacts-builder)**: Quickly build interactive component previews with React + Tailwind + Lucide.
*   **[Webapp Testing](skills/anthropics/skills/webapp-testing)**: Automatically write and run local application test cases using Playwright.
*   **[Skill Creator](skills/anthropics/skills/skill-creator)**: Assist in developing and validating custom skills following the Agent Skills specification.

### 5. 📦 More Community & Specialized Skills

*   **[AI-Research-SKILLs](skills/AI-Research-SKILLs)**: 83+ AI/ML research engineering skills (model architecture, training, inference, evaluation, paper writing).
*   **[Humanizer-zh](skills/Humanizer-zh)**: Remove AI-writing traces from Chinese text for more natural phrasing.
*   **[Pretty-mermaid-skills](skills/Pretty-mermaid-skills)**: High-quality Mermaid diagram rendering with multiple themes, SVG/ASCII output.
*   **[chinese-novelist-skill](skills/chinese-novelist-skill)**: Chapter-by-chapter Chinese fiction writing, long-form and multi-genre.

---

## 📂 Skills & MCP Index

For convenience, we provide detailed annotation indices for skills and MCP servers:
- 🇨🇳 [Chinese Annotations Index](skills/ANNOTATIONS.md)
- 🇺🇸 [English Annotations Index](skills/ANNOTATIONS_EN.md)

## 🛠️ How to Use

1.  **Load Skills**: Reference the corresponding directory in an environment that supports Skills (e.g., Claude Code or Claude.ai).
2.  **Trigger Directly**: 
    *   *"Use scientific skills to analyze this DNA sequence..."*
    *   *"Use UI-UX skills to generate a design system for my finance app..."*
    *   *"Use Word skills to generate a quarterly report based on this outline..."*

## 📜 License

The skill libraries integrated in this project follow their respective original authors' open-source licenses:
- Anthropic Skills: Apache 2.0 / Source-available
- Scientific Skills: MIT
- UI-UX Pro Max: MIT
"""
    WORKSPACE_ROOT.joinpath("README_EN.md").write_text(readme_en, encoding="utf-8")
    print("Updated README.md and generated README_EN.md")

def main():
    skills_data = []
    if SKILLS_DIR.exists():
        # 递归查找包含 SKILL.md 或 AGENTS.md 的目录
        for root, dirs, files in os.walk(SKILLS_DIR):
            if "SKILL.md" in files or "AGENTS.md" in files:
                info = extract_skill_info(Path(root))
                if info:
                    skills_data.append(info)
                    # 找到后不再深入子目录（假设一个目录就是一个 skill）
                    dirs.clear()

    mcps_data = []
    if MCPS_DIR.exists():
        for item in MCPS_DIR.iterdir():
            if item.is_dir():
                info = extract_mcp_info(item)
                if info:
                    mcps_data.append(info)

    # Generate for both languages
    for lang_code in LANGS:
        content = generate_markdown(skills_data, mcps_data, lang=lang_code)
        file_path = SKILLS_DIR / LANGS[lang_code]['file_name']
        file_path.write_text(content, encoding="utf-8")
        print(f"Generated {file_path}")

    # Update READMEs
    counts = get_counts()
    update_readmes(counts)

if __name__ == "__main__":
    main()
