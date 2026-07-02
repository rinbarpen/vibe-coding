# br

分支批量管理命令（缩写 `br`）。

## Usage

```
br <command> [options]
```

### Commands

| 子命令 | 描述 |
|--------|------|
| `ls [repo]` | 列出分支及最后提交时间 |
| `prune <repo>` | 清理已合并的过期分支 |
| `sync <repo>` | 从上游同步分支结构 |
| `protect <repo> <branch>` | 设置分支保护规则 |

### Options

| 选项 | 描述 |
|------|------|
| `--stale-days <n>` | 标记超过 N 天未更新的分支为过期（默认 90） |
| `--merged-only` | 仅操作已合并到默认分支的分支 |
| `--dry-run` | 模拟运行，不实际删除 |
| `--all` | 对所有已配置仓库执行操作 |

## Examples

```bash
# 列出所有分支
br ls github/user/repo

# 清理 90 天以上已合并分支
br prune github/user/repo --stale-days 90

# 仅清理已合并分支
br prune github/user/repo --merged-only

# 跨所有仓库模拟清理
br prune --all --dry-run

# 设置 main 分支保护
br protect github/user/repo main
```

## Notes

- 始终先用 `--dry-run` 预览即将删除的分支
- 跳过受保护分支
- 默认分支（main/master）不会被操作
