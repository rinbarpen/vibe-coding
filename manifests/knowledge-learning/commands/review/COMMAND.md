---
description: SM-2 间隔重复复习，到期卡片调度、质量评分、间隔更新
globs: ["flashcards/**/*"]
---

# /review

## Purpose

执行 SM-2 间隔重复复习会话，调度到期的知识卡片进行主动回忆练习。

## Usage

```
/review                     # 复习所有到期卡片
/review <topic>             # 复习特定主题的到期卡片
/review --limit 10          # 复习 10 张
/review --mode recall       # 主动回忆模式
/review --mode cloze        # 填空模式
```

Examples:
```
/review
/review 决策树
/review --limit 30
/review --mode cloze
```

## Execution Logic

1. 读取 flashcards/ 中的卡片库
2. 按 SM-2 算法筛选今日到期卡片
3. 按到期时间排序，最早到期的优先
4. 逐张展示，用户评分 0-5
5. 更新间隔和易度因子:
   - 评分 ≥ 3: `interval = interval × EF`
   - 评分 < 3: 重置为 1 天
6. 记录复习日志到 `flashcards/reviews/`

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `topic` | (全部) | 筛选特定主题 |
| `--limit` | 20 | 最大复习卡片数 |
| `--mode` | recall | 模式: recall/cloze/qa |

## Strict Mode Behavior

- 复习时显示卡片原文出处 `[Source: 材料名, 页码]`
- 答错时可直接回看源材料对应段落
