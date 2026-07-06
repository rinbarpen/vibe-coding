---
description: 针对特定材料的专项学习，严格绑定到单个材料进行深度分析与笔记
globs: ["materials/**/*"]
---

# /study

## Purpose

针对特定的学习材料进行深度专项学习，严格绑定到该材料。适合跟随课程 PPT 学习、精读 PDF 课本、观看视频课程等场景。

## Usage

```
/study <path>                        # 学习特定材料
/study <path> --mode skim            # 快速浏览模式
/study <path> --mode deep            # 深度学习模式
/study --next                        # 继续上次的位置
```

Examples:
```
/study materials/slides/ML-课件.pptx
/study materials/pdf/统计学习方法.pdf --mode deep
/study materials/video/Lecture5.mp4
/study --next
```

## Execution Logic

1. 加载指定材料
2. 按载体类型选择最佳学习方式:
   - PPT: 逐页 → 每页解释 + 笔记
   - PDF: 逐章 → 核心概念 + 笔记
   - Video: 分段播放 → 暂停笔记
   - Web: 结构化阅读 → 关键段落笔记
3. 每段学习后要求学生用自己的话重述
4. 学习结束产出学习进度标记（当前页/时间戳）
5. Output: 每页/每段/每时间的原子笔记

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `path` | — | 材料路径 |
| `--mode` | deep | 模式: skim/deep |
| `--next` | — | 继续上次学习 |

## Strict Mode Behavior

- 所有笔记完全绑定到该材料
- 不引入外部知识（除非标注 `[external]`）
- 进度标记精确到页码/时间戳
