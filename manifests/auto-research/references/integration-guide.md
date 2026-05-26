# Integration Guide: aris + paperreview + autofigure

## 三线集成架构

```
                    ┌─────────────────────────────────────────────────────┐
                    │              research-pipeline                     │
                    │                                                     │
  ┌─────────────────┼─────────────────────────────────────────────────────┼──┐
  │   aris          │                                                     │  │
  │                 ▼                                                     │  │
  │  research-lit ──► idea-discovery ──► novelty-check                    │  │
  │       │               │                  │                            │  │
  │       ▼               ▼                  ▼                            │  │
  │  experiment-bridge ──► run-experiment ──► analyze-results            │  │
  │       │                                      │                       │  │
  │       ▼                                      ▼                       │  │
  │  paper-write ────────────────────────────► paper-plan                │  │
  │       │                                                              │  │
  ├───────┼──────────────────────────────────────────────────────────────┼──┤
  │  paper│review                                                         │  │
  │       ▼                                                              │  │
  │  paper-write ──► auto-review-loop (4 rounds) ──► paper-claim-audit   │  │
  │       │                  │                        │                   │  │
  │       ▼                  ▼                        ▼                   │  │
  │  citation-audit ◄── auto-paper-improvement-loop                      │  │
  │       │                                                              │  │
  ├───────┼──────────────────────────────────────────────────────────────┼──┤
  │  auto │figure                                                         │  │
  │       ▼                                                              │  │
  │  figure-spec ──► paper-illustration ──► paper-figure ──► paper-compile│  │
  └──────────────────────────────────────────────────────────────────────┴──┘
```

## 集成点

### aris + paperreview

自动集成位置在 `research-pipeline` 管线内部：

```
paper-write 完成后
    ↓ 自动触发
auto-review-loop（始于论文草稿路径）
    ↓ 评审报告
paper-claim-audit（校验声明一致性）
    ↓ 校验报告
citation-audit（校验引用）
    ↓
auto-paper-improvement-loop（按评审意见改进）
```

### aris + autofigure

自动集成位置在 `paper-writing` 管线内部：

```
paper-plan 完成后
    ↓ 自动触发
figure-spec（生成论文所需图表结构）
    ↓ SVG 图表
paper-illustration（生成 AI 插图）
    ↓ 插图
paper-compile（图表 + 文本 = 终稿）
```

### paperreview → autofigure

当评审意见指出图表问题时：

```
评审意见: "Figure 3 不够清晰"
    ↓ 自动触发
figure-spec 重新生成
    ↓ 或
paper-illustration 改进插图
    ↓
paper-compile 重新编译
```

### 三线全集成

使用 `aris/research-pipeline` 一键执行全部阶段：

```
aris/research-pipeline "topic description"
```

该命令按顺序执行：
1. Discover（aris）
2. Produce（aris）
3. Review（paperreview）
4. Polish（autofigure）

## 输出清单

每次产出记录到 `MANIFEST.md`：

```
| Timestamp | Source | File | Stage | Description |
|-----------|--------|------|-------|-------------|
| 2025-06-15 | research-lit | LIT_REVIEW.md | idea-discovery | 文献综述 |
| 2025-06-16 | auto-review-loop | REVIEW.md | review | 评审报告 |
| 2025-06-17 | figure-spec | FIGURE_1.svg | paper | 架构图 |
```
