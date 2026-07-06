---
name: material-processor
description: 各载体类型提取技能。支持 PPT 逐页提取、PDF 分章拆解、视频转录分段、网页正文提取、音频转录、图片 OCR 等。所有输出严格绑定来源。
dependencies: []
---

# 材料处理器 (Material Processor)

## 概述

按载体类型自动选择最佳提取策略，将原始学习材料拆解为 source-grounded 原子笔记。

## 载体类型处理策略

### PPT/幻灯片

```
输入: lecture.pptx (20页)
输出: 20条原子笔记，每条绑定 [Source: lecture.pptx, P#]
流程:
  1. 读取每页文本 + speaker notes
  2. 提取标题和要点
  3. 描述图表/公式
  4. 输出逐页笔记
```

### PDF 文档

```
输入: textbook.pdf (10章, 300页)
输出: 按章节拆解的核心概念笔记
流程:
  1. 解析目录结构
  2. 按章节分段
  3. 提取定义、定理、公式、示例
  4. 标注 `[Source: textbook.pdf, p页码]`
```

### 视频课程

```
输入: lecture.mp4 + subtitles.srt
输出: 带时间戳的笔记
流程:
  1. 提取字幕/转录文本
  2. 按自然话题分段
  3. 关键点配对时间戳 `[Source: lecture.mp4, HH:MM:SS]`
  4. 截图关键画面
```

### 网页文章

```
输入: URL
输出: 结构化笔记
流程:
  1. 提取正文（去除导航/广告）
  2. 识别文章结构 (H1-H3)
  3. 提取关键段落
  4. 标注 `[Source: URL]`
```

## 核心准则

- 每个原子单元 = 一条独立笔记
- 每输出必有来源引用
- 不修改原始材料
- 提取后原始材料保留在 materials/ 供回溯
