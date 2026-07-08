---
description: 基于学习内容生成试卷/习题，支持难度配置、知识点排布、多种题型
globs: ["materials/exercises/**/*", "notes/**/*"]
---

# /exam

## Purpose

基于已导入的学习材料和笔记生成试卷或习题集。支持配置难度分布、知识点覆盖范围、题型组合。

## Usage

```
/exam <topic>                              # 生成某主题的练习
/exam <topic> --difficulty medium          # 中等难度
/exam <topic> --count 20                   # 20 道题
/exam <topic> --format choice              # 只出选择题
/exam --final                              # 综合测试（覆盖所有材料）
/exam <topic> --knowledge "熵,信息增益,决策树剪枝"  # 指定知识点
```

Examples:
```
/exam 决策树
/exam 线性回归 --difficulty hard --count 10
/exam 微积分 --format mixed --knowledge "导数,链式法则,积分"
/exam --final --difficulty mixed --count 50
```

## Difficulty Configuration

| 级别 | 说明 | 认知层级 | 占比参考 |
|------|------|----------|----------|
| `easy` | 基础概念记忆和直接应用 | 识记、理解 | 30% |
| `medium` | 概念组合和多步推理 | 应用、分析 | 40% |
| `hard` | 综合应用和批判性思考 | 评价、创造 | 30% |
| `mixed` | 按 3:4:3 自动混合 | 全覆盖 | — |

## Question Formats

| 格式 | 说明 | 适用难度 |
|------|------|----------|
| `choice` | 单选题（4个选项） | easy/medium |
| `fill` | 填空题 | easy/medium |
| `short` | 简答题 | medium/hard |
| `essay` | 论述/推导题 | hard |
| `mixed` | 按比例混合 | 全覆盖 |

## Execution Logic

1. 读取 topic 对应的笔记和闪卡
2. 按难度级别筛选知识点
3. 按题型模板生成题目:
   - choice: 正确选项 + 3 个干扰项（来自常见混淆概念）
   - fill: 关键术语挖空
   - short: 要求用自己的话解释
   - essay: 跨概念综合应用
4. 检查知识点覆盖率（默认要求覆盖 ≥ 80% 的知识点）
5. 生成答案和解析（引用源材料）
6. 输出试卷 + 答案卷

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `topic` | (全部) | 测试主题 |
| `--difficulty` | mixed | easy/medium/hard/mixed |
| `--count` | 10 | 题目数量 |
| `--format` | mixed | choice/fill/short/essay/mixed |
| `--knowledge` | (自动) | 指定知识点列表 |
| `--final` | false | 综合测试（跨材料） |

## Output Format

试卷输出到 `materials/exercises/`，包含两个文件：

```
materials/exercises/
├── <topic>-试卷-YYYY-MM-DD.md     # 题目
└── <topic>-答案-YYYY-MM-DD.md     # 答案 + 解析 + 来源引用
```

### 试卷示例

```markdown
---
title: 决策树 - 练习 (2026-07-06)
difficulty: mixed
total: 10
coverage: 85%
source: [ML-课件-ch03-决策树.pptx; 统计学习方法.pdf]
---

# 决策树练习

## 一、选择题 (每题 5 分)

1. 以下哪个指标用于衡量数据集的不确定性？
   A. 方差
   B. 熵 ✓
   C. 均值
   D. 中位数
   [Source: ML-课件-ch03-决策树.pptx, P6]

2. 信息增益偏向于选择什么样的特征？
   A. 取值少的特征
   B. 取值多的特征 ✓
   C. 连续特征
   D. 离散特征
   [Source: 统计学习方法.pdf, p60]

## 二、简答题 (每题 10 分)

3. 请用自己的话解释"过拟合"在决策树中是什么问题？如何解决？

## 三、综合题 (20 分)

4. 给定以下数据集，请手动构建一棵决策树：
   ...
```

### 答案卷示例

```markdown
---
title: 决策树 - 答案 (2026-07-06)
---

# 决策树练习 - 答案

## 选择题

1. **B. 熵**
   解析：熵是衡量不确定性的标准指标，见课件 P6。
   [Source: ML-课件-ch03-决策树.pptx, P6]

2. **B. 取值多的特征**
   解析：信息增益偏向取值多的特征，因此 C4.5 改用信息增益比。
   [Source: 统计学习方法.pdf, p60]

## 简答题

3. **过拟合**是指决策树对训练数据学习得过于精细...
   [Source: ML-课件-ch03-决策树.pptx, P22]
```

## Strict Mode Behavior

- 每道题的答案必须有来源引用
- 选择题的干扰项必须来自真实混淆概念（非 AI 编造）
- 标注 `[confidence: low]` 如果题目质量不确定
