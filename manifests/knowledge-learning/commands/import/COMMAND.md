---
description: 导入学习材料，自动识别载体类型(PPT/PDF/Video/Web/Audio/Image)并提取知识
globs: ["materials/**/*"]
---

# /import

## Purpose

导入各种格式的学习材料，自动识别载体类型，按类型提取知识并生成 source-grounded 原子笔记。

## Usage

```
/import <path>          # 导入本地文件
/import <url>           # 导入网页
/import --batch <dir>   # 批量导入目录下的所有材料
/import --strict        # 强制严格模式（即使 STRICT_SOURCE_MODE=false）
```

Examples:
```
/import lectures/ch03-decision-tree.pptx
/import textbook/统计学习方法.pdf
/import https://zh.wikipedia.org/wiki/机器学习
/import course/lesson5.mp4
```

## Execution Logic

1. 检测文件格式/URL 类型 → 确定载体类型
2. 复制/链接文件到 `materials/<type>/`
3. 按载体类型调用提取策略:
   - PPT: 逐页提取 + speaker notes
   - PDF: 分章提取 + 公式/图表
   - Video: 转录 + 时间分段
   - Web: 正文提取 + 结构分析
   - Audio: 转录 + 分段
   - Image: OCR + 描述
4. 每个原子概念写入 `notes/atoms/<topic>/` 并标注 `[Source: ...]`
5. 输出: 导入摘要（总笔记数、来源引用列表）

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `path` | — | 本地文件路径或 URL |
| `--batch` | — | 批量导入目录 |
| `--strict` | false | 强制严格源引用模式 |

## Strict Mode Behavior

- 每个提取的原子笔记必须包含 source field
- 从材料中直接提取的内容标记 `[confidence: high]`
- AI 补充性解释标记 `[confidence: medium/low]`
