# Auto-Research Manifest

面向自动化学术研究的独立 manifest 包。

## 场景

整合三条 AI 驱动的研究自动化能力线：
- **aris** — 研究编排框架（文献调研、想法发现、实验规划、论文写作）
- **paperreview** — 自动论文评审（4 轮自主评审循环、数值声明校验、引用校验）
- **autofigure** — 自动图表生成（确定性 SVG 架构图、AI 插图、数据驱动图表）

## 使用方式

```bash
# 初始化到目标研究项目
./scripts/init-auto-research.sh /path/to/your/research-project
```

## 快速开始

1. 创建一个研究方向 issue
2. 运行 `aris/research-pipeline "topic"` 启动全流程
3. 论文草稿完成后运行 `aris/auto-review-loop` 获取评审意见
4. 使用 `aris/figure-spec` 生成论文图表
