---
name: export-paper-zip
description: "Export finalized research paper files as a ZIP archive. Two modes: submission (default) — compile LaTeX if needed and bundle source files, figures, bibliography, and supplementary materials into a clean submission-ready ZIP; bundle — pack an arbitrary list of files or directories as-is. Use when the user needs to export paper artifacts for submission or transfer."
---

# Export Paper ZIP

## Overview

Export 最终定稿的论文文件为 ZIP 压缩包。两种模式：

| Mode | Default | Behavior |
|------|---------|----------|
| **submission** | ✅ | 自动扫描 paper 目录，编译 LaTeX（若无 PDF），收集源文件、图表、参考文献、class 文件、supplementary，按 `[venue]/` 整理后打包 |
| **bundle** | | 按用户指定的文件/目录列表直接打包，不做自动发现或编译 |

## Quick Start

### Submission mode（默认）

```bash
# 在当前 paper 目录执行
bash mine/export-paper-zip/scripts/export-paper-zip.sh /path/to/paper \
  --venue ICLR2026 \
  --output /path/to/exports

# 指定自定义 ZIP 名
bash mine/export-paper-zip/scripts/export-paper-zip.sh /path/to/paper \
  --venue NeurIPS2026 \
  --name my-paper
```

### Bundle mode

```bash
# 打包指定文件/目录
bash mine/export-paper-zip/scripts/export-paper-zip.sh /path/to/paper \
  --mode bundle \
  --include paper.pdf figures/ supp/README.md
```

## 参数

| 参数 | 说明 |
|------|------|
| `<path>` | 论文根目录（必填）。submission 模式在此目录下自动发现文件 |
| `--mode <mode>` | `submission`（默认）或 `bundle` |
| `--venue <name>` | 投稿会议/期刊名，影响 ZIP 结构（如 `ICLR2026/paper.pdf`） |
| `--output <path>` | 输出目录（默认：`<path>/../paper-export/`） |
| `--name <name>` | 自定义 ZIP 文件名（不含扩展名） |
| `--include <path...>` | bundle 模式下指定要打包的文件/目录（空格分隔） |
| `--dry-run` | 仅预览将包含的文件，不实际打包 |

## Submission 模式自动文件发现

| 类型 | 匹配规则 | 打包位置 |
|------|----------|----------|
| 编译后 PDF | `paper.pdf`（根目录下最新） | `<venue>/paper.pdf` |
| LaTeX 源码 | `*.tex`（含所有子目录） | `<venue>/src/` |
| 参考文献 | `*.bib` | `<venue>/src/` |
| 模板/样式 | `*.cls`, `*.sty`, `*.bst`, `*.cfg` | `<venue>/src/` |
| 图表 | `figures/` 目录 | `<venue>/figures/` |
| 补充材料 | `supplementary/` 目录（若存在） | `<venue>/supplementary/` |
| 其他 PDF | `*.pdf`（除 `paper.pdf` 外） | `<venue>/` |

**自动排除**：`.git/`, `.DS_Store`, `*.aux`, `*.log`, `*.bbl`, `*.blg`, `*.out`, `*.synctex.gz`, `*_cache/`, `__pycache__/`, `.vscode/`, `.idea/`

**编译行为**：若 `<path>/paper.pdf` 不存在或过期，自动运行 `latexmk -pdf` 编译。若编译失败，警告但不中止打包。

## Submission ZIP 目录结构示例

```
paper-submission_ICLR2026_20260711_1430.zip
└── ICLR2026/
    ├── paper.pdf
    ├── src/
    │   ├── main.tex
    │   ├── abstract.tex
    │   ├── refs.bib
    │   ├── iclr2026.cls
    │   └── ...
    ├── figures/
    │   ├── fig1.pdf
    │   ├── fig2.png
    │   └── ...
    └── supplementary/
        └── appendix.pdf
```

## 命名规则

| 模式 | 格式 |
|------|------|
| submission | `paper-submission_<venue>_<YYYYMMDD>_<HHMM>.zip` |
| bundle | `paper-bundle_<YYYYMMDD>_<HHMM>.zip` |
| 自定义 `--name` | `<name>.zip`（忽略自动命名） |

## Operating Rules

- 优先使用脚本 `scripts/export-paper-zip.sh` 执行打包。
- 若脚本不可用，用 `zip -r` 手动组装，严格遵循上述文件发现规则。
- submission 模式下始终以最新文件为准（不保留旧版本）。
- 编译失败时打包仍在进行，但需在输出中明确警告。
- 打包完成后输出 ZIP 路径、大小和文件清单。
- `--dry-run` 仅列出文件，不做任何写入。
- 若 `<path>` 不存在，报错退出，不做猜测。
