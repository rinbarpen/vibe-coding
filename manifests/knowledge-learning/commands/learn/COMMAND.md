---
description: 基于已导入材料启动结构化学习会话，包含目标设定、学习路径、主动学习和笔记产出
globs: ["notes/**/*"]
---

# /learn

## Purpose

基于已导入的学习材料启动系统化学习会话，自动匹配相关材料并生成学习路径。

## Usage

```
/learn <topic>                        # 学习某个主题
/learn <topic> --mode deep            # 深度学习模式
/learn <topic> --mode overview        # 概览模式
/learn <topic> --material <file>      # 限定从特定材料学习
```

Examples:
```
/learn 决策树
/learn 神经网络 --mode deep
/learn 微积分 --mode overview
/learn Python基础 --material Python-crash-course.pptx
```

## Execution Logic

1. 解析 topic → 在 materials/ 和 notes/ 中查找相关内容
2. 识别匹配的材料和已有笔记
3. 调用 curriculum-designer 生成学习路径:
   - prerequisites → core → advanced
4. 进入主动学习循环:
   - 每 20 分钟插入主动回忆检查点
   - 产出原子笔记到 notes/atoms/
   - 学习结束自动生成闪卡
5. 输出: 学习笔记 + 闪卡 + 进度记录

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `topic` | — | 学习主题 |
| `--mode` | `deep` | 学习模式: deep/quick/overview |
| `--material` | — | 限定到特定材料 |

## Strict Mode Behavior

- 学习路径中的每个概念必须绑定到源材料
- 从多份材料中综合时分别标注来源
- 无源材料的内容标注 `[confidence: hypothetical]`

## NotebookLM Engine (when enabled)

- 自动生成综合学习指南
- 支持基于所有导入材料的 grounded Q&A
