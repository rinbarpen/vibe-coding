# tag

跨平台标签管理命令。支持 semver 语义化版本、批量推送、版本晋升。

## Usage

```
tag <command> [options]
```

### Commands

| 子命令 | 描述 |
|--------|------|
| `ls [repo]` | 列出所有标签 |
| `create <repo> <tag>` | 创建标签（默认从 HEAD） |
| `push <repo>` | 推送未同步的标签到远端 |
| `prune <repo> <pattern>` | 删除匹配模式的标签（如 `v1.0.0-rc*`） |
| `promote <repo>` | 版本晋升：`patch` → `minor` → `major` |
| `diff <repo>` | 对比两端平台标签差异 |

### Options

| 选项 | 描述 |
|------|------|
| `--from <ref>` | 从指定 commit/分支创建标签 |
| `--message <msg>` | 附注标签信息 |
| `--bump <level>` | 晋升级别：`patch`、`minor`、`major`（默认 patch） |
| `--pre-release <name>` | 预发布后缀（如 `rc.1`、`beta.2`） |
| `--dry-run` | 模拟运行 |

## Examples

```bash
# 列出所有标签
tag ls github/user/repo

# 从 HEAD 创建 v1.2.3
tag create github/user/repo v1.2.3

# 从指定 commit 创建
tag create github/user/repo v1.0.0 --from abc1234 --message "Release v1.0.0"

# 自动 bump patch 版本
tag promote github/user/repo

# 晋升 minor 版本
tag promote github/user/repo --bump minor

# 晋升 major 版本 + 预发布
tag promote github/user/repo --bump major --pre-release rc.1

# 推送所有标签到远端
tag push github/user/repo

# 对比两端平台标签差异
tag diff github/user/repo

# 清理 rc 标签
tag prune github/user/repo "v1.0.0-rc*"
```

## Notes

- 标签命名遵循 semver 规范：`v<major>.<minor>.<patch>`（如 `v2.1.0`）
- 预发布格式：`v<version>-<name>`（如 `v2.1.0-beta.1`）
- `promote` 自动读取最新标签并递增，无标签则从 `v0.1.0` 开始
- 跨平台镜像场景下，标签同步建议使用 `mirror run --with-tags`
