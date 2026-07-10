# vibe-characters

查看/管理角色设定卡命令。

## Usage

```
vibe-characters <command> [options]
```

### Commands

| 子命令 | 描述 |
|--------|------|
| `list` | 列出所有角色 |
| `view <name>` | 查看指定角色设定卡 |
| `edit <name>` | 修改角色设定 |
| `add` | 新增角色 |
| `check <chapter>` | 检查某章节的角色一致性 |

### Options

| 选项 | 描述 |
|------|------|
| `--relation <name>` | 显示与某角色的关系图 |
| `--timeline` | 显示角色成长时间线 |
| `--status` | 显示角色当前状态（活跃/暂离/死亡等） |

## 角色设定卡格式

```markdown
# 角色名

## 基本信息
- **年龄**: 17
- **身份**: xx学园二年级
- **外貌**: [简略描述]
- **性格关键词**: 傲娇、认真、怕孤独

## 背景故事
[角色背景，3-5句话]

## 能力/特长
- 能力A
- 能力B

## 角色关系
- [关系人]: [关系描述]
- [关系人]: [关系描述]

## 成长轨迹
- CH001: 首次登场
- CH005: 重大转变

## 关键属性（AI 校验用）
- 口头禅: "..."
- 小动作: "..."
- 禁忌话题: "..."
```

## Examples

```bash
# 列出所有角色
vibe-characters list

# 查看角色设定
vibe-characters view 林晓

# 检查新章节是否与人设冲突
vibe-characters check chapters/CH003_转折.md
```

## Notes

- AI 在每次创作新章节后应自动核对相关角色的属性
- 角色属性变更必须在 `characters/` 中记录并标注变更原因
- 禁止 OOC（Out Of Character）—— AI 不得改变既定角色的性格基调