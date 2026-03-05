---
description: 自动更新 scripts/ 工具脚本，确保其与项目命令和工作流一致。
globs: ["scripts/**"]
---

# Update Scripts Command

此规则定义了 `/update-scripts` 命令，用于保持 scripts/ 与项目工作流同步。

## 命令定义

### `/update-scripts`

**目的**: 根据项目当前的构建、测试、部署命令，更新 `scripts/` 目录下的工具脚本。

**使用方式**: 在对话框中输入 `/update-scripts [可选的具体更新说明]`。

**执行逻辑**:
1. **分析工作流**: 扫描 `package.json`、`pyproject.toml`、`Makefile` 等获取命令。
2. **检查脚本**: 读取 `scripts/` 下现有脚本。
3. **执行更新**: 运行 `python3 .cursor/commands/update-scripts/update_scripts.py`。
4. **人工确认**: AI 生成更新后的脚本，由用户确认后写入文件。

**示例**:
- `/update-scripts`
- `/update-scripts 增加部署脚本`
