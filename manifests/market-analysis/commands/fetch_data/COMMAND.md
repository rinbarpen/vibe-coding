# fetch_data

行业研究信息收集辅助工具。

## Usage

```
fetch_data macro <indicator>   # 宏观数据（行业周期背景）
fetch_data sources <industry>  # 资料来源建议
fetch_data search <query>      # 搜索关键词建议
```

## 子命令

### macro — 宏观背景数据

判断行业所处的宏观周期位置。所有数据来自国家统计局，国内源可用。

```bash
# CPI（判断通胀周期）
python scripts/fetch_data.py macro CPI

# PMI（判断经济景气度，>50扩张，<50收缩）
python scripts/fetch_data.py macro PMI

# GDP（经济增长）
python scripts/fetch_data.py macro GDP

# M2（货币宽松程度）
python scripts/fetch_data.py macro M2
```

### sources — 资料来源建议

根据行业名称，推荐应该从哪些渠道收集信息：

```bash
python scripts/fetch_data.py sources "AI软件"
python scripts/fetch_data.py sources "半导体"
```

### search — 搜索关键词建议

生成多个搜索方向的关键词，提高信息收集效率：

```bash
python scripts/fetch_data.py search "AI软件 市场规模"
python scripts/fetch_data.py search "新能源车 竞争格局"
```

## Notes

- 行业研究的数据来源多样，不依赖单一数据源
- 宏观数据为补充参考，行业研究核心在行业本身的分析
- 搜索建议帮助 AI Agent 或人工更高效地收集信息