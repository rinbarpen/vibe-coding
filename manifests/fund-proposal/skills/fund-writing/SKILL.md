---
name: fund-writing
description: 基金本子学术主笔技能。整合科学写作、中文排版、去AI化及文风提升能力，负责基金本子的高质量学术产出。
dependencies:
  - skills/claude-scientific-skills/scientific-skills/scientific-writing/SKILL.md
  - skills/chinese-copywriting-guidelines/SKILL.md
  - skills/beautiful_prose/SKILL.md
  - skills/Humanizer-zh/SKILL.md
  - skills/AI-Research-SKILLs/20-ml-paper-writing/SKILL.md
---

# 基金本子学术主笔 (Fund Writing)

## 概述
本技能旨在将用户的研究构思转化为严谨、精炼、逻辑严密的学术文本。它深度整合了科学写作规范、中文排版准则以及文风优化技术，确保基金本子在语言表达上达到顶级专家水平。

## 核心准则
1. **两阶段写作**: 遵循 `scientific-writing` 的原则，先列段落大意（Outline），确认逻辑无误后再展开为完整学术文本（Prose）。
2. **中文排版规范**: 严格执行 `chinese-copywriting-guidelines`，确保中英文、数字之间增加空格，标点符号使用正确。
3. **去 AI 化润色**: 使用 `Humanizer-zh` 对生成的文本进行处理，消除 AI 常见的空洞套话和机械感，使其更符合人类专家的表达习惯。
4. **语势增强**: 应用 `beautiful_prose` 技巧，提高信息密度，优化逻辑连词（如：旨在、然而、鉴于此）。

## 使用场景
- 撰写【立项依据】中的国内外研究现状。
- 将用户的口语化表述转化为【研究内容】与【研究目标】。
- 针对 AI/ML 领域的基金，应用 `ml-paper-writing` 的特定逻辑。

## 指令集成
- 执行 `/draft` 指令时，必须启动此技能。
- 执行 `/polish` 指令时，以此技能为核心进行文本优化。
