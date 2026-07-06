---
name: notebooklm-engine
description: NotebookLM 增强引擎。默认关闭(NOTEBOOKLM_ENGINE=false)。开启后提供 source-grounded Q&A、
  跨材料综合学习指南、音频概述生成。与 STRICT_SOURCE_MODE 正交独立。
dependencies:
  - skills/material-processor/SKILL.md
  - skills/note-architect/SKILL.md
---

# NotebookLM 引擎 (NotebookLM Engine)

> ⚠️ 此技能默认关闭。通过设置 `NOTEBOOKLM_ENGINE=true` 启用。

## 概述

开启后，提供类似 Google NotebookLM 的增强功能：基于所有已导入材料的 grounded 问答、学习指南自动生成、跨材料综合、音频对话式复习。

不依赖外部 NotebookLM 服务，完全基于本地材料运行。

## 可用功能 (仅引擎开启时)

### 1. Source-Grounded Q&A

基于所有已导入的材料回答用户问题，每条回答引用原始出处。

```
/user 什么是支持向量机？
→ 回答引用 materials/pdf/统计学习方法.pdf p87
           + materials/slides/ML-课件.pptx P45
```

### 2. 学习指南生成

自动生成涵盖多个材料的学习指南:
- 课程简报 (Study Guide)
- FAQ (常见问题列表)
- 关键概念时间线 (Timeline)
- 跨材料概念对照表 (Briefing Doc)

### 3. 音频概述 (Audio Overview)

将笔记转化为对话式音频脚本（双人播客风格），可用于通勤复习。

```
/flashcard --audio       # 卡片以对话形式朗读
/learn --audio summary   # 学习摘要语音版
```

### 4. 跨材料综合

当同一主题有多份材料时，自动交叉对比、识别共识与差异、生成综合洞察。

## 引擎状态

| 设置值 | 行为 |
|--------|------|
| `NOTEBOOKLM_ENGINE=false` (默认) | 基础学习功能，无增强 |
| `NOTEBOOKLM_ENGINE=true` | 启用所有 NotebookLM 风格增强 |
