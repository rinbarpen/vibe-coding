# audit

仓库健康度审计命令。

## Usage

```
audit <command> [options]
```

### Commands

| 子命令 | 描述 |
|--------|------|
| `health <repo>` | 综合健康度检查 |
| `issues <repo>` | 检查 Issue 和 PR 状态 |
| `security <repo>` | 安全审计（依赖、权限） |
| `report` | 生成所有仓库的审计报告 |

### Options

| 选项 | 描述 |
|------|------|
| `--output <format>` | 输出格式：`table`、`json`、`md`（默认 table） |
| `--ci-only` | 仅检查 CI/CD 状态 |
| `--all` | 审计所有已配置仓库 |

## Health Check Items

- 分支保护状态是否启用
- 默认分支是否存在
- 超过 30 天未合并的 PR 数量
- 超过 90 天未关闭的 Issue 数量
- CI/CD 最近一次运行是否通过
- `.gitignore`、`LICENSE`、`README.md` 是否存在
- 最新 tag 是否落后于默认分支

## Examples

```bash
# 综合健康检查
audit health github/user/repo

# 检查 Issue 和 PR 状态
audit issues github/user/repo

# 安全审计
audit security github/user/repo

# 生成 Markdown 审计报告
audit report --output md

# JSON 格式输出（便于脚本处理）
audit health github/user/repo --output json
```

## Notes

- 审计前确保对应平台的 API 令牌已配置
- `report` 命令会扫描所有本地仓库副本
- 安全审计需要依赖扫描工具（如 `gh dependabot`、`trivy`）
