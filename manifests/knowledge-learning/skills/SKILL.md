---
name: knowledge-learning
description: 个人知识管理与多载体学习技能集。覆盖 PPT/PDF/视频/网页/音频/图片等多种知识载体的导入、
  提取、组织、复习全流程。采用 NotebookLM 风格严格源引用模式，保证知识准确性。
  提供 7 个学习指令、4 个学习场景、6 套管理规则。
triggers:
  - pattern: "(import|learn|study|review|flashcard|mindmap|track) "
    description: Knowledge-learning command trigger
  - pattern: "(upload|add|load) (material|file|document|slide|pdf|video|article)"
    description: Material import trigger
  - pattern: "(create|generate|make) (flashcard|study guide|summary|mindmap)"
    description: Learning material generation
  - pattern: "(review|recall|revise|reinforce|巩固|复习)"
    description: Review session trigger
  - pattern: "(track|monitor|check|progress|进度)"
    description: Progress tracking trigger
---
