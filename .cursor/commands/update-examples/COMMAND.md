---
description: 自动更新 examples/ 示例代码，确保其与当前 API 和用法一致。
globs: ["examples/**"]
---

# Update Examples Command

此规则定义了 `/update-examples` 命令，用于保持示例代码与项目 API 同步。

## 命令定义

### `/update-examples`

**目的**: 根据当前 API、用法变更，更新 `examples/` 目录下的示例代码。

**使用方式**: 在对话框中输入 `/update-examples [可选的具体更新说明]`。

**执行逻辑**:
1. **分析 API**: 扫描源码导出、公共接口、用法模式。
2. **检查示例**: 读取 `examples/` 下现有示例。
3. **执行更新**: 运行 `python3 .cursor/commands/update-examples/update_examples.py`。
4. **人工确认**: AI 生成更新后的示例，由用户确认后写入文件。

**示例**:
- `/update-examples`
- `/update-examples 增加新 API 的示例`
