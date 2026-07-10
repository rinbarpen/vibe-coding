# vibe-summarize

将长文提炼为社交媒体的短内容格式。

## Usage

```
vibe-summarize --file <path> [options]
```

### Options

| 选项 | 描述 |
|------|------|
| `--file <path>` | 原文文件路径（必需） |
| `--format <fmt>` | 输出格式：`tldr`（一句话）、`thread`（推特长线）、`bullet`（要点）、`card`（小红书卡片） |
| `--platform <name>` | 目标平台适配语气 |
| `--max-length <n>` | 最大字数限制 |

## 输出格式说明

| 格式 | 适用平台 | 说明 |
|------|---------|------|
| `tldr` | 全平台 | 一句话总结（<50字） |
| `thread` | Twitter/微博 | 3-10条推文组成的 thread |
| `bullet` | 公众号/知乎 | 3-5个核心要点 |
| `card` | 小红书 | 图文卡片式摘要 |

## Examples

```bash
# 一句话总结
vibe-summarize --file content/article.md --format tldr

# 转为 Twitter thread
vibe-summarize --file content/article.md --format thread --platform twitter

# 小红书卡片摘要
vibe-summarize --file content/long-post.md --format card --max-length 300
```

## Notes

- 所有摘要必须保持原文的核心观点不变
- 标注 `[AI 摘要]` 标识，避免误导读者
- 如包含数据/引用，必须保留来源标注