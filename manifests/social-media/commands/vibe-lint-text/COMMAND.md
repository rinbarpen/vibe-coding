# vibe-lint-text

检查常见中英文排版和写作问题。

## Usage

```
vibe-lint-text --file <path> [options]
```

### Options

| 选项 | 描述 |
|------|------|
| `--file <path>` | 检查的文件（必需） |
| `--fix` | 自动修复可修复的问题 |
| `--strict` | 严格模式（包含建议性规则） |
| `--output <path>` | 输出 lint 报告到文件 |

## 检查项

### 严重问题（必须修复）

| 检查项 | 要求 |
|--------|------|
| 中英文间距 | 中文和英文/数字之间必须有空格 |
| 全半角标点 | 中文用全角标点，英文用半角 |
| 重复空格 | 连续超过 1 个空格 |
| AI 废话 | "值得注意的是"、"在当今世界"等 AI 填充词 |

### 建议性（推荐修复）

| 检查项 | 要求 |
|--------|------|
| 段落长度 | 超过 200 字的段落建议拆分 |
| 句子长度 | 超过 80 字的句子建议拆分 |
| 被动语态 | 过多被动语态建议改主动 |
| 副词密度 | 过度使用"非常"、"很"、"极其"等 |
| 重复词 | 相邻句子中的词语重复 |

## Examples

```bash
# 检查文件
vibe-lint-text --file content/draft.md

# 检查并自动修复
vibe-lint-text --file content/draft.md --fix

# 严格模式
vibe-lint-text --file content/draft.md --strict

# 输出报告
vibe-lint-text --file content/draft.md --output lint-report.json
```

## Notes

- `--fix` 选项只修复严重问题，建议性问题需人工处理
- 发布前必须运行一次此命令