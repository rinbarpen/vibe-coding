# Med-AI 论文叙事指南 (Narrative Guide)

医学与 AI 交叉论文的成功核心在于平衡“技术创新性”与“临床实用性”。

## 1. 核心叙事框架 (The Clinical-AI Loop)

Med-AI 论文应遵循以下逻辑流：

1.  **Clinical Background (临床背景)**: 描述疾病负担（发病率、死亡率）和当前的临床实践。
2.  **Clinical Gap (临床缺口)**: 明确指出当前诊断、治疗或预后中的痛点（例如：医生主观性强、效率低、资源匮乏）。
3.  **AI Solution (AI 解决方案)**: 介绍你的 AI 方法如何针对性地解决上述痛点。
4.  **Technical Innovation (技术创新)**: 强调算法上的新颖性（如：针对医学影像噪声的鲁棒性设计、多模态融合策略）。
5.  **Evidence of Efficacy (有效性证据)**: 通过严谨的实验（含临床金标准对比）证明 AI 的优越性。
6.  **Clinical Impact (临床影响)**: 讨论该技术若投入临床将如何改变医疗现状。

## 2. 跨学科语言平衡

-   **Abstract**: 必须包含临床背景和最终的临床结论。
-   **Introduction**: 避免过多的 AI 术语堆砌，重点描述“为什么这个临床问题需要 AI”。
-   **Methods**: 
    -   **Data**: 详细描述数据来源、入排标准（Inclusion/Exclusion Criteria）。
    -   **Model**: 使用标准术语，并解释模型设计的医学动机。
-   **Discussion**: 必须包含 **Clinical Implications** 章节，讨论模型在实际医疗环境中的应用潜力。

## 3. 常见叙事陷阱

-   **过度工程化**: 追求微小的 SOTA 提升而忽略临床意义。
-   **忽略噪声**: 医学数据天然具有高噪声和不平衡性，叙事中应体现对这些问题的处理。
-   **黑盒问题**: 医学界对可解释性（Explainability）有很高要求，叙事中应加入显著性图（Saliency Maps）或特征分析。
