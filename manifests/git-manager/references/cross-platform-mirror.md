# Cross-Platform Mirror 策略

## 镜像模式

### 1. 主从模式（推荐）

选择一个平台作为主仓库（如 GitHub），其余平台作为只读镜像。

```
GitHub (主) ──push──→ Gitee (镜像)
                  └──→ GitLab (镜像)
```

**优点**：避免冲突，管理简单
**缺点**：PR/Issue 需要在主平台管理

### 2. 双向同步

多个平台均可写入，通过 webhook 或定时任务同步。

```
GitHub ←──sync──→ Gitee
```

**优点**：开发者在任意平台可操作
**缺点**：容易产生冲突，需要冲突解决机制

### 3. 按需同步

不在平台间自动同步，由管理员手动触发特定仓库的同步。

**优点**：完全可控
**缺点**：依赖人工操作

## 同步方法

### 方法 A：git push --mirror

```bash
# 全量镜像（包括所有 refs、分支、标签）
git clone --mirror https://github.com/user/repo.git
cd repo.git
git remote add gitee https://$GITEE_TOKEN@gitee.com/user/repo.git
git push --mirror gitee
```

**适用场景**：首次全量同步、仓库迁移

### 方法 B：git push --all --tags

```bash
# 仅同步分支和标签
git clone https://github.com/user/repo.git
cd repo
git remote add gitee https://$GITEE_TOKEN@gitee.com/user/repo.git
git push --all gitee
git push --tags gitee
```

**适用场景**：日常增量同步

### 方法 C：CI 自动同步

通过 CI（GitHub Actions / Gitee Go / GitLab CI）在每次推送时自动同步。

- GitHub → Gitee：参考 `references/github-workflows.md` 中的 Actions 示例
- GitLab → GitHub：参考 `references/self-hosted-git.md` 中的 GitLab CI 示例

### 方法 D：Webhook 触发同步

在源平台配置 Webhook，推送事件触发同步脚本。

```bash
# Webhook 接收端脚本示例
#!/bin/bash
# 接收 webhook payload，提取 repo 信息
payload=$(cat)
repo=$(echo "$payload" | jq -r '.repository.full_name')
# 执行同步
git clone --mirror "https://github.com/$repo.git"
cd "$(basename "$repo").git"
git remote add gitee "https://$GITEE_TOKEN@gitee.com/$repo.git"
git push --mirror gitee
```

## 冲突处理

- 主从模式下不存在冲突（单向同步）
- 双向同步时，以时间戳较新的提交为准
- 复杂冲突需人工介入解决

## 注意事项

- 大文件（LFS）需要额外配置：`git lfs fetch --all` + `git lfs push --all`
- 分支保护规则不会通过 `git push` 同步，需在各平台独立配置
- Issue、PR、Wiki 等内容不会随 git 同步，需使用 API 或第三方工具
