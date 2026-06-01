# CLAUDE.md (PPT Master 专用)

基于 PPT Master 技能的 AI 驱动演示文稿生成项目管理。将源文档转换为原生可编辑的 PPTX 文件（真实 DrawingML 形状）。

## 常用指令

| 命令 | 描述 |
| :--- | :--- |
| `/init <name> [--format ppt169]` | 初始化新项目，建立目录结构与设计规范骨架 |
| `/source <file_or_url>` | 将源文件（PDF/DOCX/URL/MD/Excel）转换为 Markdown |
| `/template [name]` | 查看或应用预置布局模板（默认自由设计） |
| `/strategize` | 进入 Strategist 阶段，执行八项确认，产出 design_spec.md + spec_lock.md |
| `/images` | 进入 Image_Generator 阶段，为标记为"待生成"的图片调用 AI 生成 |
| `/execute` | 进入 Executor 阶段，逐页生成 SVG 页面并输出演讲者备注 |
| `/validate` | 运行 SVG 质量检查 + 图表坐标校准 |
| `/finalize` | 后处理（分割备注 → SVG 终稿 → 导出 PPTX） |

## 项目结构

```
<root>/
├── README.md                   # 项目说明
├── design_spec.md              # 设计规范与内容大纲（Strategist 产出）
├── spec_lock.md                # 执行锁定文件（机器可读契约，Executor 每页重读）
├── sources/                    # 源文档与转换后的 Markdown
├── svg_output/                 # 生成的 SVG 页面（Executor 产出）
├── svg_final/                  # 后处理后的 SVG 终稿
├── exports/                    # 导出的 PPTX 文件
├── notes/                      # 演讲者备注
│   └── total.md                # 组合备注（分割前）
├── images/                     # 图片素材
│   └── image_prompts.md        # 图片生成提示词
└── templates/                  # 布局模板（可选）
```

## 关键文件

| 文件 | 用途 |
| :--- | :--- |
| `design_spec.md` | 人类可读的设计叙述，包含视觉主题、排版方案、内容大纲 |
| `spec_lock.md` | 机器可读的执行契约，包含颜色/字体/图标/图片/页面节奏，Executor 每页前必读 |
| `notes/total.md` | 组合演讲者备注，Step 7 第一步进行分割 |

## 环境

- **Python 3.10+** 必须
- **依赖安装**: `pip install -r skills/ppt-master/requirements.txt`
  - 核心：`python-pptx`, `PyMuPDF`, `mammoth`, `markdownify`, `openpyxl`, `Pillow`
  - 可选：`google-genai`（Gemini 图片）, `openai`（OpenAI 兼容图片）, `cairosvg`（Office 兼容）
- **图片生成**（可选）：复制 `.env.example` 为 `.env`，配置 `IMAGE_BACKEND` 与对应 API Key
  - 支持后端：gemini / openai / qwen / zhipu / volcengine / stability / bfl / ideogram / fal / replicate / openrouter / minimax / siliconflow

## 工作流（7 步流水线）

1. **源内容处理** (`/source`) — 将 PDF/DOCX/URL/Excel 等转换为 Markdown
2. **项目初始化** (`/init`) — 运行 `project_manager.py init`，建立目录结构
3. **模板选项** (`/template`) — 默认自由设计；可选用预置布局模板
4. **Strategist 阶段** (`/strategize`) — **阻塞步骤**，八项确认后产出 `design_spec.md` + `spec_lock.md`
5. **Image_Generator 阶段** (`/images`) — 条件执行，为标记"AI 生成"的图片调用后端
6. **Executor 阶段** (`/execute`) — 逐页生成 SVG → 质量检查 → 图表校准 → 备注
7. **后处理与导出** (`/finalize`) — 分割备注 → SVG 终稿 → 导出 PPTX（使用 `-s final`）

## 技能路径

```
skills/ppt-master/                                          # 技能根目录
skills/ppt-master/skills/ppt-master/SKILL.md                # 主工作流权威定义
skills/ppt-master/skills/ppt-master/references/             # 角色定义与技术规范
skills/ppt-master/skills/ppt-master/scripts/                # 可执行工具脚本
skills/ppt-master/skills/ppt-master/templates/              # 布局/图表/图标
skills/ppt-master/requirements.txt                          # Python 依赖
skills/ppt-master/.env.example                              # 环境变量模板
```

## 注意事项（红线）

- **串行执行**: 严格按步骤顺序执行，禁止跳过或并行执行跨阶段任务
- **禁止委托**: SVG 生成必须由主 Agent 完成，不得委派给子 Agent
- **逐页生成**: 每页独立生成，不得批量打包
- **spec_lock 权威**: 每页生成前必须重读 `spec_lock.md`，其值优先于 `design_spec.md`
- **禁止臆造**: 所有颜色/字体/图标/图片必须来自 `spec_lock.md`，不得凭记忆
- **导出路径**: 必须使用 `-s final` 从 `svg_final/` 导出，不得从 `svg_output/` 导出
- **角色切换**: 切换角色（Strategist → Image_Generator → Executor）前必须读取对应参考文件
