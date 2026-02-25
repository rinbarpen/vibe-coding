---
name: fund-research
description: 基金本子深度调研技能。整合深度研究、选题创意及全网搜索能力，负责Gap分析、文献支撑及寻找合适图片。
dependencies:
  - skills/ai-skills/skills/deep-research/SKILL.md
  - skills/AI-Research-SKILLs/21-research-ideation/brainstorming-research-ideas/SKILL.md
  - skills/claude-scientific-skills/scientific-skills/research-grants/SKILL.md
  - skills/x-research-skill/SKILL.md
---

# 基金本子深度调研 (Fund Research)

## 概述
本技能负责为基金本子提供坚实的事实支撑和创意启发。通过全网深度搜索、X/Twitter 实时动态监控以及结构化的选题框架，帮助用户精准定位研究 Gap 并获取必要的图文资料。

## 核心准则
1. **Gap 识别**: 利用 `brainstorming-research-ideas` 中的“矛盾分析法”，对比现有文献与实际需求，找准“拟解决的关键科学问题”。
2. **深度调研**: 针对特定技术点或科学假说，调用 `deep-research` 进行全网扫描，确保立项依据有据可查。
3. **视觉素材搜集**: 
    - 搜索学术界公认的经典机制图作为参考。
    - 使用 `x-research-skill` 关注领域大牛的最新推文或预印本讨论，获取前沿动态。
4. **防止幻觉**: 遇到不确定的数据或文献，必须使用 `[请补充...]` 占位符，严禁捏造。

## 使用场景
- 执行 `/init` 指令时，盘问用户研究基础并进行初步背景核实。
- 执行 `/brainstorm` 指令时，进行全方位的 Gap 分析。
- 搜集用于技术路线图参考的原始素材或图片。

## 指令集成
- `/init` 和 `/brainstorm` 阶段的核心驱动技能。
