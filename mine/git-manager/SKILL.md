---
name: git-manager
description: |
  Unified git platform management hub. Routes to sub-skills for GitHub (gh CLI),
  Gitee (OpenAPI v5), and custom/self-hosted git servers (GitLab, Gitea, Gogs).
  Covers repository management, PR/issue workflows, CI/CD, releases, secrets,
  branch protection, SSH keys, webhooks, and remote configuration.
---

# Git Manager

统一分发 git 管理请求到对应平台的子技能。支持 GitHub、Gitee、自托管 Git。

## Sub-Skills

| Sub-Skill | Platform | Tooling | Best For |
|-----------|----------|---------|----------|
| [github](github/SKILL.md) | GitHub.com / GitHub Enterprise | `gh` CLI v2.89+ | PR/issue/actions/release/secrets |
| [gitee](gitee/SKILL.md) | Gitee.com (码云) | Gitee OpenAPI v5 + curl | 国内镜像/中文生态/仓库迁移 |
| [custom-git](custom-git/SKILL.md) | GitLab / Gitea / Gogs / 自建 | `git` CLI + API + SSH | 私服/自建/内网/企业部署 |

## Platform Dispatch

### GitHub
→ [github](github/SKILL.md)

触发词：`github`、`gh`、`GitHub`、`GH`、`github enterprise`、`创建 PR`、`issue`、`actions`、`workflow`

### Gitee / 码云
→ [gitee](gitee/SKILL.md)

触发词：`gitee`、`码云`、`gitee.com`、`国内仓库`、`gitee pages`、`同步 gitee`

### 自托管 / GitLab / Gitea / Gogs
→ [custom-git](custom-git/SKILL.md)

触发词：`自建`、`自托管`、`gitlab`、`gitea`、`gogs`、`私服`、`内网 git`、`self-hosted`、`custom git`

## 通用概念

| 概念 | 说明 | 关联子技能 |
|------|------|-----------|
| SSH Key | `~/.ssh/id_*.pub` 添加至平台 Settings | github, gitee, custom-git |
| Personal Access Token | 各平台生成 token 用于 API 认证 | github(gh), gitee(header), custom-git |
| Remote URL | `origin` 格式：SSH / HTTPS 两种协议 | custom-git |
| Branch Protection | 保护主干分支规则设置 | github, gitlab |
| Webhook | 事件推送通知 | github, custom-git |

## Authentication Checklist

在执行任何子技能前确认：

- **GitHub**: `gh auth status` 或 `gh auth login`
- **Gitee**: `GITEE_TOKEN` 环境变量已设置
- **Custom Git**: SSH key 已添加、远程 URL 正确、API token（如需要）
