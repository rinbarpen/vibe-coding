---
name: git-manager-custom
description: |
  Self-hosted and custom git server management. Covers remote configuration,
  SSH key management, GitLab/Gitea/Gogs API patterns, protocol switching,
  webhooks, cross-platform mirroring, and self-hosted runner setup.
---

# Git Manager — Custom / Self-Hosted Git

管理自托管 Git 服务器及通用 git remote 操作。适用于 GitLab CE/EE、Gitea、Gogs 及任何 SSH/HTTP 可达的 git 仓库。

## Remote Configuration

```bash
# 查看当前 remote
git remote -v

# 添加 remote
git remote add origin git@gitlab.example.com:group/repo.git

# 修改 remote URL
git remote set-url origin git@gitlab.example.com:group/repo.git

# HTTPS ↔ SSH 切换
git remote set-url origin https://gitlab.example.com/group/repo.git
git remote set-url origin git@gitlab.example.com:group/repo.git

# 添加多个 remote（如同时推送到多个平台）
git remote add github git@github.com:user/repo.git
git remote add gitlab git@gitlab.example.com:group/repo.git
# 修改推送策略：推送到所有 remote
git remote set-url --add --push origin git@github.com:user/repo.git
git remote set-url --add --push origin git@gitlab.example.com:group/repo.git
```

## SSH Key Management

```bash
# 生成 SSH key（推荐 Ed25519）
ssh-keygen -t ed25519 -C "your_email@example.com" -f ~/.ssh/id_ed25519

# 查看公钥
cat ~/.ssh/id_ed25519.pub

# 测试 SSH 连接到服务器
ssh -T git@github.com          # GitHub
ssh -T git@gitee.com           # Gitee
ssh -T git@gitlab.example.com  # GitLab

# 多主机 SSH 配置 (~/.ssh/config)
cat >> ~/.ssh/config << 'EOF'
# GitHub (default key)
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519

# GitLab self-hosted (different key)
Host gitlab.example.com
  HostName gitlab.example.com
  User git
  Port 2222
  IdentityFile ~/.ssh/id_rsa_gitlab
EOF
```

## GitLab API Mode

GitLab API v4 通过 `PRIVATE-TOKEN` header 认证。

```bash
# 前置条件
export GITLAB_TOKEN="your_personal_access_token"
GITLAB_HOST="https://gitlab.example.com"
```

### GitLab Repo Operations

```bash
# 查看项目
curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_HOST/api/v4/projects/$(echo 'group/repo' | sed 's/\//%2F/g')"

# 创建项目
curl -s -X POST "$GITLAB_HOST/api/v4/projects" \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  -d '{"name":"repo-name","visibility":"public","description":"description"}'

# 列出用户项目
curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_HOST/api/v4/projects?membership=true&per_page=50"

# 创建 Merge Request
curl -s -X POST "$GITLAB_HOST/api/v4/projects/$(echo 'group/repo' | sed 's/\//%2F/g')/merge_requests" \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  -d '{
    "source_branch":"feature-x",
    "target_branch":"main",
    "title":"Add feature X",
    "description":"Description"
  }'
```

### GitLab CI / Runner

```bash
# 列出 project runners
PROJECT_ID=$(curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_HOST/api/v4/projects/$(echo 'group/repo' | sed 's/\//%2F/g')" | python3 -c "import sys,json;print(json.load(sys.stdin)['id'])")

# 触发 pipeline
curl -s -X POST "$GITLAB_HOST/api/v4/projects/$PROJECT_ID/pipeline" \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  -d '{"ref":"main"}'

# 查看 pipelines
curl -s --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_HOST/api/v4/projects/$PROJECT_ID/pipelines?per_page=10"
```

## Gitea API Mode

Gitea API v1 通过 `Authorization: token` header 认证。

```bash
# 前置条件
export GITEA_TOKEN="your_token"
GITEA_HOST="https://gitea.example.com"

# 验证
curl -s -H "Authorization: token $GITEA_TOKEN" "$GITEA_HOST/api/v1/user"

# 创建仓库
curl -s -X POST "$GITEA_HOST/api/v1/user/repos" \
  -H "Authorization: token $GITEA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"repo-name","description":"desc","private":false,"auto_init":true}'

# 创建 Pull Request
curl -s -X POST "$GITEA_HOST/api/v1/repos/owner/repo/pulls" \
  -H "Authorization: token $GITEA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"PR title",
    "body":"PR body",
    "head":"feature-branch",
    "base":"main"
  }'
```

## Webhook Setup

```bash
# GitLab: 创建 Push 事件的 webhook
PROJECT_ENCODED=$(echo 'group/repo' | sed 's/\//%2F/g')
curl -s -X POST "$GITLAB_HOST/api/v4/projects/$PROJECT_ENCODED/hooks" \
  --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  --header "Content-Type: application/json" \
  -d '{
    "url":"https://your-ci.example.com/webhook",
    "push_events":true,
    "merge_requests_events":true,
    "enable_ssl_verification":true
  }'

# Gitea: 创建 webhook
curl -s -X POST "$GITEA_HOST/api/v1/repos/owner/repo/hooks" \
  -H "Authorization: token $GITEA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type":"gitea",
    "config":{"url":"https://hook.example.com","content_type":"json"},
    "events":["push","pull_request"]
  }'

# GitHub: 使用 gh CLI
gh api repos/owner/repo/hooks \
  -X POST \
  -F name=web \
  -F config='{"url":"https://hook.example.com","content_type":"json"}'
```

## Common Workflows

### 跨平台镜像同步（GitHub → 自建 GitLab）

```bash
# 一次设置，定期执行
git clone --mirror https://github.com/owner/repo.git
cd repo.git
git remote add gitlab https://gitlab.example.com/group/repo.git
git push --mirror gitlab
```

### LFS 配置（自托管）

```bash
# 安装 LFS
git lfs install

# 跟踪文件类型
git lfs track "*.psd" "*.zip" "*.tar.gz"

# 设置 LFS 端点（自建 GitLab 需配置）
git config -f .lfsconfig lfs.url https://gitlab.example.com/group/repo.git/info/lfs
```

### 自建 Runner 注册（GitLab）

```bash
# 在 GitLab 实例上注册 runner
gitlab-runner register \
  --non-interactive \
  --url "https://gitlab.example.com" \
  --registration-token "$REGISTRATION_TOKEN" \
  --executor "docker" \
  --docker-image alpine:latest \
  --description "docker-runner"
```
