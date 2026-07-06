---
description: 学习进度追踪与报告，统计知识增量、掌握度、复习情况
globs: ["flashcards/reviews/**/*", "projects/**/*"]
---

# /track

## Purpose

查看和记录学习进度，包括卡片统计、复习完成率、各主题掌握度和知识增量。

## Usage

```
/track                      # 查看总体进度
/track --scope week         # 本周进度
/track --scope domain pdf   # 特定载体类型的进度
/track goal set <goal>      # 设置学习目标
/track goal list            # 查看已有目标
```

Examples:
```
/track
/track --scope week
/track --scope domain slides
/track goal set "2026-08-15 前完成 ML 课程全部笔记"
```

## Execution Logic

1. 读取 `flashcards/reviews/` 和 `projects/` 数据
2. 统计:
   - 卡片总数、已掌握数、复习率
   - 按载体类型分组统计
   - 学习时长估算
3. 识别薄弱环节（掌握率最低的主题）
4. 输出进度报告

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--scope` | all | 范围: all/week/month/domain |
| `action` | view | 操作: view/set/report |

## Report Format

```
📊 学习进度报告
━━━━━━━━━━━━━━━━━━━━
总卡片: 145 | 已掌握: 89 (61%)
到期复习: 12 张
本周新增: 23 张

📈 各类型掌握度
  slides:   78% ████████░░
  pdf:      65% ██████░░░░
  video:    45% ████░░░░░░
  web:      70% ███████░░░

⚠️ 薄弱环节: video (45%) — 建议增加视频类材料复习
```
