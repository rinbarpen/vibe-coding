# 数据可视化指南

## 核心理念

- **代码生成**：所有图表通过 `scripts/visualize.py` 生成，确保可重复性和稳定性
- **数据准确**：图表中的数据必须与正文中的数据一致
- **观众友好**：图表应该让读者一眼看懂，不需要额外解释

## 图表选择指南

| 你想展示什么 | 选什么图 | 说明 |
|-------------|---------|------|
| 各公司/类别对比 | 📊 柱状图 (bar) | 最常见，适合<10个类别 |
| 随时间变化的趋势 | 📈 折线图 (line) | 适合展示增长/变化 |
| 占比/构成 | 🥧 饼图 (pie) | 适合<6个类别，最好有一个明显占优 |
| 排名数据 | 横向柱状图 (hbar) | 适合名称较长的类别 |
| 多维度评分 | 🗺️ 热力图 (heatmap) | 适合同时展示多个维度 |

## 使用 visualize.py

### 准备数据 JSON

```json
{
  "labels": ["公司A", "公司B", "公司C", "公司D", "其他"],
  "values": [35, 25, 15, 10, 15],
  "title": "行业市场份额分布 (2025)",
  "ylabel": "市场份额 (%)",
  "source": "IDC, 2025"
}
```

### 生成图表

```bash
# 柱状图
python scripts/visualize.py bar data/market_share.json --output output/chart_market_share.png

# 折线图（多系列）
python scripts/visualize.py line data/growth_trend.json --output output/chart_trend.png

# 饼图
python scripts/visualize.py pie data/revenue_split.json --output output/chart_revenue.png

# 横向柱状图
python scripts/visualize.py hbar data/ranking.json --output output/chart_ranking.png

# 热力图
python scripts/visualize.py heatmap data/matrix.json --output output/chart_matrix.png

# 生成示例测试
python scripts/visualize.py bar --example
```

### 折线图特殊数据格式

```json
{
  "x_labels": ["2021", "2022", "2023", "2024", "2025"],
  "series": [
    {"label": "市场规模(亿元)", "values": [100, 150, 220, 320, 450]},
    {"label": "增长率(%)", "values": [30, 50, 47, 45, 41]}
  ],
  "title": "行业市场规模与增长率趋势",
  "ylabel": "亿元 / %",
  "source": "中国信通院, 2025"
}
```

### 热力图特殊数据格式

```json
{
  "row_labels": ["公司A", "公司B", "公司C", "公司D"],
  "col_labels": ["产品力", "品牌力", "渠道力", "技术力", "成本力"],
  "matrix": [[5, 4, 3, 5, 2], [4, 5, 4, 3, 3], [3, 3, 5, 4, 4], [2, 2, 3, 3, 5]],
  "title": "核心竞争能力对比矩阵",
  "source": "综合分析"
}
```

## 嵌入报告

生成的图表保存在 `output/` 目录，通过 Markdown 直接引用：

```markdown
![行业市场份额分布](output/chart_market_share.png)
*图表1: 行业市场份额分布 [来源: IDC, 2025]*
```

## 图表规范

| 规范 | 要求 |
|------|------|
| 分辨率 | 150 dpi |
| 宽高比 | 16:9 或 4:3 |
| 字体 | 数字/英文，确保清晰 |
| 颜色 | 使用内置色板（色盲友好） |
| 数据来源 | 图表底部标注 |
| 标题 | 清晰说明图表内容 |
| 坐标轴 | 有标签和单位 |
| 图例 | 多系列时必须包含 |

## 常见错误

- ❌ 饼图类别太多（超过6个）
- ❌ 3D 图表（不必要，影响数据读取）
- ❌ 数据标签重叠
- ❌ 图表中的数据与正文矛盾
- ❌ 缺少数据来源标注