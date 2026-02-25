# 投稿渠道规范 (Venue Templates)

本文件汇总了主流学术会议和期刊的投稿要求，用于 `switch-venue` 模式。

## CS/ML 会议

| 会议 | 页数限制 | 参考文献页数 | 关键要求 |
| :--- | :--- | :--- | :--- |
| **NeurIPS** | 9 pages | 不限 | 必须包含 Checklist (附录) |
| **ICML** | 8 pages | 不限 | 必须包含 Broader Impact Statement |
| **ICLR** | 9 pages | 不限 | 必须包含 Ethics Statement, LLM Disclosure |
| **ACL/EMNLP** | 8 pages | 不限 | 必须包含 Limitations 章节 |
| **AAAI** | 7 pages | 2 pages | 格式极其严格，禁止修改样式文件 |

## 综合科学期刊

| 期刊 | 类型 | 长度建议 | 关键要求 |
| :--- | :--- | :--- | :--- |
| **Nature** | Article | ~3000 words | 强调广泛影响力，Figure 1 必须极其精美 |
| **Science** | Research Article | ~4500 words | 故事性叙述，数据图表质量要求极高 |
| **IEEE Trans.** | Journal | 10-12 pages | 强调技术细节和严谨的数学推导 |

## 转换建议 (Conversion)

- **NeurIPS → ICML**: 需缩减 1 页。建议压缩 Related Work 或将详细证明移至附录。
- **ICML → ICLR**: 可增加 1 页。建议增加消融实验或定性分析。
- **通用 → ACL**: 必须增加独立的 Limitations 章节。
