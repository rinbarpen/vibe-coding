# 开源项目标准 (Open Source Standards)

本指南定义了一个优秀的开源项目应遵循的标准。

## 1. 核心文件清单
每个开源项目必须包含以下文件：
- **README.md**: 项目介绍、快速入门、安装指南、示例、贡献指南链接。
- **LICENSE**: 明确的开源协议（推荐 MIT 或 Apache-2.0）。
- **CONTRIBUTING.md**: 如何贡献代码、提交 Issue、PR 流程、代码风格。
- **CHANGELOG.md**: 版本更新记录。
- **.gitignore**: 排除不必要的文件。

## 2. 代码质量标准
- **Linting**: 必须通过项目配置的 Linter。
- **Testing**: 关键逻辑必须有单元测试覆盖。
- **Documentation**: 公共 API 必须有清晰的文档注释。
- **Consistency**: 遵循项目已有的命名规范和架构模式。

## 3. 交付标准
- **Semantic Versioning**: 遵循语义化版本 (Major.Minor.Patch)。
- **PR 规范**: 标题简洁，描述包含背景、变更内容、测试计划。
- **Issue 模板**: 提供 Bug Report 和 Feature Request 模板。

## 4. Vibe Coding 适配
- **Intent-Driven**: 代码应清晰表达意图，而非仅仅是实现。
- **Verification-First**: 在声称完成前，必须有证据（Lints, Tests, Logs）。
