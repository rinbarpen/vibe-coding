# PPT Master Manifest

AI 驱动的演示文稿生成 Manifest —— 将源文档通过多角色 AI 流水线转换为原生可编辑的 PPTX 文件（真实 DrawingML 形状，非图片嵌入）。

## 先决条件

- **Python 3.10+**
- **依赖安装**: `pip install -r skills/ppt-master/requirements.txt`
- **图片生成**（可选）: 配置 `.env` 中的 `IMAGE_BACKEND` 与对应 API Key

## 快速开始

```bash
# 1. 在新项目目录中初始化 PPT Master 项目结构
bash manifests/ppt-master/scripts/init-ppt-master.sh

# 2. 安装 Python 依赖
pip install -r skills/ppt-master/requirements.txt

# 3.（可选）配置 AI 图片生成
cp skills/ppt-master/.env.example .env
# 编辑 .env，设置 IMAGE_BACKEND 与对应 API Key

# 4. 开始创建演示文稿
# 将源文件放入 sources/，然后在对话框中输入 /init 开始
```

## 流水线步骤

| 步骤 | 命令 | 说明 |
| :--- | :--- | :--- |
| 1. 源处理 | `/source <file>` | 将 PDF/DOCX/URL/Excel 等转换为 Markdown |
| 2. 项目初始化 | `/init <name>` | 建立目录结构，运行 project_manager.py |
| 3. 模板选择 | `/template [name]` | 可选应用预置布局模板（默认自由设计） |
| 4. 策略设计 | `/strategize` | 八项确认，产出 design_spec.md + spec_lock.md |
| 5. 图片生成 | `/images` | 条件执行，AI 生成演示图片 |
| 6. 页面执行 | `/execute` | 逐页生成 SVG + 质量检查 + 图表校准 + 备注 |
| 7. 导出 | `/finalize` | 分割备注 → SVG 终稿 → 导出 PPTX |

## 项目目录结构

```
<project>/
├── design_spec.md              # 设计规范（人类可读）
├── spec_lock.md                # 执行锁定文件（机器可读契约）
├── sources/                    # 源文档
├── svg_output/                  # SVG 页面产出
├── svg_final/                  # SVG 终稿
├── exports/                    # 导出的 PPTX
├── notes/                      # 演讲者备注
├── images/                     # 图片素材
└── templates/                  # 布局模板
```

## 常用命令

| 命令 | 描述 |
| :--- | :--- |
| `/init <name>` | 初始化新项目 |
| `/source <file>` | 转换源文件 |
| `/strategize` | 进入策略设计阶段 |
| `/execute` | 进入 SVG 生成阶段 |
| `/finalize` | 后处理并导出 PPTX |
| `/validate` | 质量检查与图表校准 |

详细说明见 `CLAUDE.md`。

## 核心特性

- **真实形状**: 输出 PPTX 中的每个文本框、形状、图表都是可编辑的 DrawingML 元素
- **多格式输入**: 支持 PDF、DOCX、URL、Markdown、Excel、EPUB、Jupyter Notebook
- **16 种布局模板**: McKinsey、Google、学术答辩、政务蓝/红等
- **60+ 图表模板**: 柱状图、折线图、饼图、雷达图、甘特图、桑基图等
- **多后端图片生成**: 支持 Gemini、OpenAI、Qwen、智谱、火山引擎等 10+ 后端
- **数据本地化**: 除 AI 模型通信外，所有数据保留在本地

## 使用提示

- 源文档越结构化（标题层级清晰、段落分明），生成效果越好
- Executor 阶段消耗大量上下文，长演示文稿注意上下文预算
- 自由设计模式下，策略师会提供风格建议并与你确认
- 如果要使用特定品牌风格，优先检查 `templates/layouts/` 中的模板
