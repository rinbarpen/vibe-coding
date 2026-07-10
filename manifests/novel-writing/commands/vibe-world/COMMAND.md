# vibe-world

查看/管理世界观设定命令。

## Usage

```
vibe-world <command> [options]
```

### Commands

| 子命令 | 描述 |
|--------|------|
| `view <domain>` | 查看世界观设定（地理/力量体系/历史等） |
| `update <file>` | 更新世界观文件 |
| `check <chapter>` | 检查章节是否与世界观设定冲突 |
| `map` | 显示地理/势力关系图 |

### Options

| 选项 | 描述 |
|------|------|
| `--domain <name>` | 领域：`geography`、`magic`、`history`、`faction` |
| `--diff` | 显示世界观设定变更历史 |

## 世界观文件结构

```
world/
  setting.md         # 核心世界观说明
  geography.md       # 地理设定
  magic-system.md    # 力量/魔法体系
  history.md         # 编年史
  factions.md        # 势力/组织
  technology.md      # 科技水平
```

## Examples

```bash
# 查看力量体系
vibe-world view magic

# 检查新章节是否与设定冲突
vibe-world check chapters/CH004_冲突.md

# 更新地理设定
vibe-world update world/geography.md
```

## Notes

- 世界观设定修改时需要同步检查所有已写章节是否产生冲突
- 涉及神话/奇幻元素时，优先参考 `references/` 下的知识文件
- `research/` 存放项目特定研究资料，`references/` 存放通用知识域