# vibe-progress

统计章节字数与创作进度命令。

## Usage

```
vibe-progress [options]
```

### Options

| 选项 | 描述 |
|------|------|
| `--chapter <name>` | 统计特定章节（默认所有） |
| `--output <fmt>` | 输出格式：`table`、`json`、`markdown`（默认 table） |
| `--daily` | 显示每日创作量趋势 |
| `--target <words>` | 设定总字数目标，计算完成百分比 |

## 统计项

- 总章节数、总字数
- 各章节字数分布
- 每日/每周创作量
- 创作阶段进度：大纲 → 草稿 → 逻辑校验 → 润色 → 完成

## Examples

```bash
# 查看整体进度
vibe-progress

# 设定20万字目标
vibe-progress --target 200000

# 查看日创作量趋势
vibe-progress --daily

# JSON 输出（便于外部工具处理）
vibe-progress --output json
```

## Notes

- 字数统计基于 `chapters/` 下的 markdown 文件
- 进度数据存储在 `.vibe-novel-stats.json`（自动生成）
- 每日创作报告会记录当前阶段和各章节状态