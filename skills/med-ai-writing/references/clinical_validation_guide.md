# 临床验证规范 (Clinical Validation Guide)

医学 AI 论文的实验部分必须遵循医学统计学和临床研究的严谨性。

## 1. 数据集划分与验证

-   **Internal Validation (内部验证)**: 训练集、验证集和内部测试集。
-   **External Validation (外部验证)**: **Med-AI 论文的“金标准”**。必须使用来自不同机构、不同设备或不同人群的数据进行独立测试，以证明模型的泛化能力。
-   **Prospective vs. Retrospective (前瞻性 vs. 回顾性)**: 
    -   回顾性研究（使用历史数据）是基础。
    -   前瞻性研究（在真实临床流程中实时测试）具有更高的证据等级，是顶刊（Nature Medicine 等）的偏好。

## 2. 评价指标 (Metrics)

除了传统的 AI 指标，必须包含以下医学指标：

-   **Sensitivity (Recall) & Specificity**: 描述漏诊率和误诊率。
-   **Positive/Negative Predictive Value (PPV/NPV)**: 描述预测结果的临床可信度。
-   **AUC-ROC & AUC-PR**: 衡量模型在不同阈值下的表现。
-   **F1-Score**: 在类别不平衡（医学常态）时的综合表现。
-   **Calibration Curve (校准曲线)**: 衡量预测概率与实际发生率的一致性。

## 3. 统计学分析

-   **Confidence Intervals (CI, 置信区间)**: 所有主要指标（如 AUC 0.85 [95% CI: 0.82-0.88]）必须附带 95% 置信区间。
-   **P-values**: 用于比较不同模型或与人类医生表现的差异。通常 p < 0.05 被认为具有统计学显著性。
-   **Subgroup Analysis (亚组分析)**: 检查模型在不同年龄、性别、疾病分期或设备类型下的表现是否稳定，以识别潜在的算法偏见。

## 4. 与人类专家对比

-   **Reader Study**: 邀请多位临床医生（初级、中级、高级）在有无 AI 辅助的情况下进行诊断，对比准确率、耗时和一致性（Kappa 系数）。
-   **Ground Truth (金标准)**: 明确 Ground Truth 的来源（如：病理活检、多位专家共识、随访结果）。
