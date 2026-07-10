# vibe-outline

查看/更新小说大纲命令。

## Usage

```
vibe-outline <command> [options]
```

### Commands

| 子命令 | 描述 |
|--------|------|
| `view` | 查看当前大纲（主线 + 支线） |
| `update <file>` | 更新指定大纲文件 |
| `expand <line>` | 扩展某条大纲线为详细章节计划 |
| `diff` | 对比最新大纲与上一版本的变化 |

### Options

| 选项 | 描述 |
|------|------|
| `--arc <name>` | 指定剧情弧线（主线/支线A/支线B） |
| `--chapters` | 同时显示章节映射 |
| `--format <fmt>` | 输出格式：`tree`、`table`、`list`（默认 tree） |

## 大纲文件结构

```
outline/
  main.md        # 主线剧情大纲
  arcs/          # 支线剧情弧
    arc-A.md
    arc-B.md
  timeline.md    # 时间线
```

## Examples

```bash
# 查看主线
vibe-outline view --arc 主线

# 查看所有弧线+章节映射
vibe-outline view --chapters

# 扩展第3条大纲线为章节计划
vibe-outline expand 3

# 对比变化
vibe-outline diff
```

## Notes

- 修改大纲后自动更新 `CLAUDE.md` 中的进度
- 确保每次创建新章节前先更新大纲
- 章节排序：CH001_CH001 → 前缀理解