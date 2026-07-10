# vibe-draft

根据主题生成社交媒体内容草稿。

## Usage

```
vibe-draft <topic> [options]
```

### Options

| 选项 | 描述 |
|------|------|
| `--platform <name>` | 目标平台：`wechat`、`red`、`twitter`、`weibo`（默认 `wechat`） |
| `--tone <style>` | 语气风格：`professional`、`casual`、`conversational`、`humorous` |
| `--length <len>` | 长度：`short`（<500字）、`medium`（500-1500）、`long`（1500-3000） |
| `--keywords <list>` | 逗号分隔的关键词，SEO 优化用 |
| `--output <path>` | 保存草稿到文件 |

## Examples

```bash
# 写一篇公众号推文
vibe-draft "AI 编程工具对比" --platform wechat --tone professional --length long

# 写一条小红书帖子
vibe-draft "周末好物推荐" --platform red --tone casual --length short

# 写一条 Twitter thread
vibe-draft "Why Rust matters" --platform twitter --tone conversational
```

## Notes

- 草稿初稿追求流畅度，不要纠结细节
- 后续使用 `vibe-polish` 润色
- 平台有各自的排版规范，参考 `templates/` 下的模板