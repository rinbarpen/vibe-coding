---
description: 自动更新 docs/ 文档，确保其反映最新的 API、架构和用法。
globs: ["docs/**"]
---

# Update Docs Command

此规则定义了 `/update-docs` 命令，用于保持项目文档与实现同步。

## 命令定义

### `/update-docs`

**目的**: 根据当前代码实现、API 变更、架构调整，更新 `docs/` 目录下的文档。

**使用方式**: 在对话框中输入 `/update-docs [可选的具体更新说明]`。

**执行逻辑**:
1. **分析实现**: 扫描 `src/`、`lib/` 等源码，提取 API、模块结构。
2. **检查文档**: 读取 `docs/` 下现有文档。
3. **执行更新**: 运行 `python3 .cursor/commands/update-docs/update_docs.py`。
4. **人工确认**: AI 生成更新后的内容，由用户确认后写入文件。

**示例**:
- `/update-docs`
- `/update-docs 增加新 API 的说明`
