# vibe-gen-image-prompt

生成配图 AI 绘画提示词（DALL-E / Midjourney 风格）。

## Usage

```
vibe-gen-image-prompt <topic> [options]
```

### Options

| 选项 | 描述 |
|------|------|
| `--style <name>` | 风格：`minimalist`、`flat-vector`、`cinematic`、`watercolor`、`3d-render` |
| `--count <n>` | 生成方案数量（默认 3） |
| `--aspect <ratio>` | 宽高比：`16:9`、`1:1`、`4:3`、`9:16` |
| `--platform <name>` | 平台适配（封面尺寸不同） |

## 生成规范

- 描述具体：光线、构图、色调、质感
- 中英文均可，Midjourney 建议用英文
- 包含风格关键词（如 "minimalist flat vector"、"cinematic lighting"）
- 避免过于抽象的描述

## Examples

```bash
# 生成文章配图提示词
vibe-gen-image-prompt "AI 机器人写代码" --style flat-vector

# 小红书封面
vibe-gen-image-prompt "精致早餐摆盘" --style cinematic --aspect 3:4

# 多方案选择
vibe-gen-image-prompt "未来城市" --count 4 --style 3d-render
```

## Notes

- 提示词应保持简洁（<200 字符为宜）
- 不同 AI 绘画工具的提示词语法不同，标注目标工具
- 封面图建议使用 3:4（小红书）或 16:9（公众号/视频封面）