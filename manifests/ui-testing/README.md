# UI Testing Manifest

AI 辅助 UI 软件测试的完整配置包。为 AI 编码 agent（Claude Code、Cursor 等）提供 UI 测试所需的知识、规则、命令和工作流。

## 核心特性

- **测试方法论**：测试金字塔、选择器策略、等待策略、测试隔离等核心规则
- **框架覆盖**：Playwright（E2E）、Vitest + Testing Library（组件）、Detox（移动端）
- **场景化**：Web E2E、组件测试、移动端、视觉回归、无障碍 —— 按需启用
- **命令系统**：运行测试、AI 生成测试、不稳定测试诊断
- **模式库**：Page Object、API Mocking、Fixture 工厂等最佳实践

## 快速开始

```bash
# 安装到目标项目
cp -r manifests/ui-testing /path/to/your-project/.cursor/manifests/ui-testing
cd /path/to/your-project
bash .cursor/manifests/ui-testing/scripts/ui-testing-init.sh

# 指定场景（可选）
bash .cursor/manifests/ui-testing/scripts/ui-testing-init.sh --scenario=web-e2e
```

## 场景支持

| 场景 | 启动命令 | 适用框架 |
|------|---------|---------|
| Web E2E | `--scenario=web-e2e` | Playwright, Cypress |
| 组件测试 | `--scenario=component` | Vitest + Testing Library |
| 移动端 | `--scenario=mobile` | Detox, Appium |
| 视觉回归 | `--scenario=visual-regression` | Percy, Chromatic, Loki |
| 无障碍 | `--scenario=accessibility` | axe-core, Pa11y |

## 目录结构

```
ui-testing/
├── CLAUDE.md           # 项目 CLAUDE.md 模板
├── AGENTS.md           # AI agent 指令
├── rules/              # .mdc 规则文件
├── commands/           # 测试命令
├── skills/             # 测试模式知识库
├── scenarios/          # 场景化配置
├── agents/             # 子代理角色
└── scripts/            # 初始化脚本
```

## 依赖

推荐全局安装（目标项目需要）:
- Node.js 18+（Playwright、Vitest）
- Playwright：`npx playwright install`
- 移动端测试：Detox CLI 或 Appium
