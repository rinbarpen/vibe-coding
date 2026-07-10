# vibe-check-logic

剧情逻辑一致性检查命令。

## Usage

```
vibe-check-logic [chapter] [options]
```

### Options

| 选项 | 描述 |
|------|------|
| `--full` | 全面检查（包括伏笔、人设、世界观、时间线） |
| `--foreshadow` | 仅检查伏笔 |
| `--timeline` | 仅检查时间线一致性 |
| `--continuity` | 仅检查人设/世界观连续性 |
| `--output <fmt>` | 输出格式：`list`、`json`、`report`（默认 list） |

## 检查维度

| 维度 | 检查内容 |
|------|----------|
| **人设一致性** | 角色行为是否符合 `characters/` 中的设定 |
| **世界观一致性** | 新内容是否与 `world/` 中的设定冲突 |
| **时间线** | 事件时序是否合理，是否存在矛盾 |
| **伏笔** | 是否有已埋设但被遗忘的伏笔 |
| **力量体系** | 角色能力是否超出设定上限 |
| **因果关系** | 剧情发展是否有合理的因果链 |

## Examples

```bash
# 全面检查
vibe-check-logic --full

# 仅检查某章节的伏笔
vibe-check-logic chapters/CH010_真相.md --foreshadow

# 检查时间线
vibe-check-logic --timeline

# 生成详细报告
vibe-check-logic --full --output report
```

## Notes

- 这是创作流程中**最关键的验证步骤**
- 每完成一个章节或重大剧情转折后必须运行
- 发现问题后先修复再继续创作
- 伏笔追踪使用 `scripts/foreshadow-tracker.sh`