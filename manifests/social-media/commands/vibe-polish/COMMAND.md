# vibe-polish

对草稿进行润色（中英文排版、文学性提升）。

## Usage

```
vibe-polish --file <path> [options]
```

### Options

| 选项 | 描述 |
|------|------|
| `--file <path>` | 草稿文件路径（必需） |
| `--platform <name>` | 目标平台适配 |
| `--focus <aspect>` | 润色重点：`typesetting`（排版）、`style`（文风）、`tone`（语气） |
| `--output <path>` | 输出文件路径 |

## 润色内容

| 维度 | 说明 |
|------|------|
| **中英文混排** | 中文与英文/数字之间添加空格 |
| **标点符号** | 中文使用全角标点，英文使用半角 |
| **简繁转换** | 根据目标读者统一 |
| **冗余删减** | 删除"在...中"、"通过..."等啰嗦表达 |
| **句式优化** | 长句拆短，被动改主动 |
| **节奏调整** | 段落长度、排比句、强调句增加可读性 |

## Examples

```bash
# 润色排版
vibe-polish --file content/draft.md --focus typesetting

# 全部润色
vibe-polish --file content/draft.md --output content/polished.md

# 根据平台调整风格
vibe-polish --file content/draft.md --platform red --focus style
```

## Notes

- 排版规范参考 `rules/vibe-social-typesetting.mdc`
- 润色不会修改内容结构和核心观点
- 保留原文的语气和声音风格