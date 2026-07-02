# mirror

跨平台仓库同步与镜像命令。

## Usage

```
mirror <command> [options]
```

### Commands

| 子命令 | 描述 |
|--------|------|
| `setup <source> <target>` | 配置从源到目标的镜像映射 |
| `run [name]` | 执行同步（可指定配置名称，不指定则同步所有） |
| `ls` | 查看已配置的镜像映射 |
| `rm <name>` | 移除镜像配置 |

### Options

| 选项 | 描述 |
|------|------|
| `--mode <mode>` | 同步模式：`mirror`（全量）、`branch`（仅分支）、`tag`（仅标签） |
| `--with-tags` | 同步时携带标签 |
| `--with-actions` | 同步时复制 Actions 工作流配置 |
| `--dry-run` | 模拟运行，不实际推送 |
| `--force` | 强制覆盖目标端（慎用） |

## Examples

```bash
# 配置从 GitHub 到 Gitee 的镜像
mirror setup github/user/repo gitee/user/repo

# 执行全量镜像同步
mirror run github-user-repo --mode mirror

# 仅同步分支 + 标签
mirror run github-user-repo --mode branch --with-tags

# 模拟运行查看变更
mirror run github-user-repo --dry-run

# 列出所有镜像配置
mirror ls
```

## Notes

- 首次同步需确保目标仓库已创建
- `--mode mirror` 会覆盖目标端所有 refs，小心使用
- 建议先用 `--dry-run` 确认影响范围
