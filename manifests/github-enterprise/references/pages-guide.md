# GitHub Pages Guide

## Pages 类型对比

| 类型 | 部署来源 | 绑定域名 | 适用场景 |
|------|----------|----------|----------|
| **Project Pages** | `docs/` 目录 或 `gh-pages` 分支 | `{user}.github.io/{repo}` | 单个项目的文档站点 |
| **Organization Pages** | `main` 分支根目录 | `{org}.github.io` | 组织/公司的官网或文档中心 |
| **User Pages** | `main` 分支根目录 | `{user}.github.io` | 个人主页或作品集 |

## 推荐 docs/ 目录结构

```
docs/
├── _config.yml              # Jekyll 配置
├── index.md                 # 文档首页
├── guide/                   # 用户指南
│   ├── getting-started.md   # 快速入门
│   ├── installation.md      # 安装指南
│   └── configuration.md     # 配置说明
├── api/                     # API 参考
│   ├── reference.md         # API 文档
│   └── changelog.md         # 接口变更
├── development/             # 开发者指南
│   ├── contributing.md      # 贡献指南
│   ├── architecture.md      # 架构说明
│   └── testing.md           # 测试指南
└── assets/                  # 静态资源
    ├── css/                 # 自定义 CSS
    └── images/              # 图片资源
```

## Jekyll 配置

创建 `docs/_config.yml`：

```yaml
title: Project Documentation
description: >-
  项目文档站点
theme: just-the-docs

aux_links:
  "GitHub Repository":
    - "https://github.com/org/repo"

plugins:
  - jekyll-sitemap
  - jekyll-seo-tag
```

### 推荐 Jekyll 主题

| 主题 | 特点 | 适用场景 |
|------|------|----------|
| [just-the-docs](https://github.com/just-the-docs/just-the-docs) | 简洁、导航清晰、搜索内置 | 技术文档 |
| [minimal-mistakes](https://github.com/mmistakes/minimal-mistakes) | 功能丰富、多种布局 | 博客+文档混合 |
| [jekyll-theme-cayman](https://github.com/pages-themes/cayman) | 极简、GitHub 默认风格 | 简单项目页 |

## 自定义域名

1. 在 DNS 提供商处添加 CNAME 记录：
   - `www.yourdomain.com` → `{org}.github.io`
   - 或使用 ALIAS/ANAME 记录到 apex 域名
2. 在仓库 Settings > Pages 中填入自定义域名
3. 可选：创建 `docs/CNAME` 文件（内容为 `yourdomain.com`）
4. 启用 HTTPS（GitHub 自动处理证书）

## 自动部署

对应的 workflow：`.github/workflows/deploy-pages.yml`

当 `docs/` 目录内容变更时，自动部署到 GitHub Pages。

## 本地预览

```bash
# 安装 Jekyll
gem install jekyll bundler

# 在 docs/ 目录启动
cd docs
bundle exec jekyll serve

# 访问 http://localhost:4000
```
