# README Writing Guide

## 定位

README 是项目的首页。一个好的 README 回答三个核心问题：

1. **这是什么？** — 项目定位、解决的问题
2. **怎么用？** — 从零开始到运行的最短路径
3. **怎么参与？** — 贡献、反馈、联系方式

## 中英双语要求

```
README.md      # 中文版本
README_EN.md   # 英文版本
```

- 中文版本作为默认 README（面向中文开发者）
- 英文版本作为补充（面向国际化开发者）
- 两个文件必须保持同步，关键信息一致

## 标准结构

### 1. 项目名称 + 一行描述 + Badge

```
# Project Name

> 一行描述：这个项目解决什么问题

![CI](https://img.shields.io/...) ![License](https://img.shields.io/...) ![Version](https://img.shields.io/...)
```

- 名称简明，一眼知道项目做什么
- 描述不超过一句话
- Badge 不超过 5 个

### 2. 特性亮点

```
## Features

- 🚀 特性一：一句话说明
- 🔒 特性二：一句话说明
- ⚡ 特性三：一句话说明
```

- 3-5 个点
- 每个点一行，附带 emoji 图标
- 不要说"高性能"这种空话——给数据或具体场景

### 3. 快速开始

```
## Quick Start

```bash
git clone https://github.com/org/repo.git
cd repo
make install
make run
```

从 clone 到能跑起来，不超过 5 步。
不要在这里展开完整文档——那是 docs/ 的事。

### 4. 文档索引

```
## Documentation

- [Getting Started](docs/guide/getting-started.md)
- [API Reference](docs/api/reference.md)
- [Contributing](CONTRIBUTING.md)
```

指向 `docs/` 目录的关键文档。

### 5. 项目结构

```
## Project Structure

├── src/          # 源码
├── docs/         # 文档
├── tests/        # 测试
└── .github/      # GitHub 配置
```

只展示顶层目录，每个目录一行注释。

### 6. 技术栈

```
## Tech Stack

- Runtime: Node.js 20 / Python 3.12
- Framework: Express / FastAPI
- Database: PostgreSQL 16
```

一行一个核心依赖，标明版本。

### 7. 贡献指南

```
## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.
```

一句话指向 CONTRIBUTING.md。

### 8. 许可证

```
## License

MIT © 2025 org
```

一行 + badge。

## Badge 使用约定

只使用有意义的 badge，不要全部加上。

| Badge | 必要性 | 来源 |
|-------|--------|------|
| CI build status | ✅ 必要 | GitHub Actions |
| License | ✅ 必要 | Shields.io |
| Code coverage | ✅ 有自动化测试时 | Codecov |
| Version | ✅ 有发布时 | GitHub Release |
| Python / Node 版本 | ⚡ 可选 | Shields.io |
| Code style | ⚡ 可选 | Shields.io |
| Downloads | ⚡ 可选 | npm / PyPI |

Badge 示例（Shields.io 格式）：

```
![CI](https://img.shields.io/github/actions/workflow/status/org/repo/ci.yml?branch=main)
![License](https://img.shields.io/github/license/org/repo)
![Version](https://img.shields.io/github/v/release/org/repo)
```

## 应避免的问题

- ❌ **过时的截屏** — 版本更新后忘记替换，比没有更糟
- ❌ **"敬请期待"占位符** — 没有就是没有
- ❌ **大段未格式化的 changelog** — changelog 放 CHANGELOG.md
- ❌ **敏感信息** — API key、内部 URL、密码
- ❌ **空泛的描述** — "本项目致力于..." 不如 "每天处理 100 万次 API 调用"
- ❌ **没有 badge** — 用户无法一眼看出项目状态
- ❌ **过长的 README** — 超出 5 分钟阅读量，说明需要拆到 docs/
