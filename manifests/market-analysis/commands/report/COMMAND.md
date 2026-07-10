# report

行业研究报告生成工具。

## Usage

```
report --industry <name>                    # 快速生成研究框架
report --notes <json> --output report.md    # 从研究笔记生成报告
report --notes <json> --macro <json>        # 含宏观背景的报告
```

## 两种模式

### 1. 框架模式（快速开始）

直接生成八步法空框架，方便逐章节填写：

```bash
python scripts/report.py --industry "AI软件" --output AI软件_研究框架.md
```

### 2. 笔记模式（完整报告）

先填写研究笔记 JSON，再生成正式报告：

```bash
# 准备研究笔记
cat > research/notes.json << 'EOF'
{
  "industry": "AI 软件",
  "industry_definition": {
    "行业定义": "以AI技术为核心驱动的软件产品和服务",
    "细分领域": ["大模型平台", "AI+办公", "AI+编程", "AI+金融"],
    "分类标准": "自定义"
  },
  "market_analysis": {
    "TAM": "待填充",
    "驱动力": ["大模型能力提升", "企业数字化转型"],
    "抑制因素": ["AI安全/合规风险", "落地成本高"]
  },
  ...
}
EOF

# 生成报告
python scripts/report.py --notes research/notes.json --output research/行业报告.md
```

## 可选：宏观背景

如果已有宏观数据 JSON，可以附加到报告中：

```bash
python scripts/fetch_data.py macro CPI --output macro.json
python scripts/report.py --notes research/notes.json --macro macro.json --output report.md
```

## Notes

- 框架模式生成的空结构方便 AI Agent 逐章节填充
- 笔记模式需要预先准备好结构化研究笔记
- 宏观数据为可选补充，核心在行业本身的分析