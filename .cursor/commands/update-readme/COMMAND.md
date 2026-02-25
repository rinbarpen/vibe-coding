---
description: 自动更新项目 README.md 文档，确保其反映最新的项目结构和功能。
globs: ["README.md"]
---

# Update README Command

此规则定义了 `/update-readme` 命令，用于保持项目主文档的实时更新。

## 命令定义

### `/update-readme`

**目的**: 分析当前项目状态（结构、核心功能、依赖等），并更新 `README.md`。

**使用方式**: 在对话框中输入 `/update-readme [可选的具体更新说明]`。

**执行逻辑**:
1. **分析环境**: 扫描项目根目录，识别技术栈（如 Python/uv, Node.js 等）。
2. **提取信息**: 获取当前核心功能描述和安装/运行指令。
3. **执行更新**: 运行 `python3 .cursor/commands/update-readme/update_readme.py`。
4. **人工确认**: AI 生成更新后的内容，由用户确认后写入文件。

**示例**:
- `/update-readme`
- `/update-readme 增加关于新 API 接口的说明`
