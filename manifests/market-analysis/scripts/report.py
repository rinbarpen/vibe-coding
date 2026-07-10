#!/usr/bin/env python3
"""report.py — 行业研究报告框架生成器

不替代AI Agent的分析能力，只提供：
1. 从研究笔记（JSON格式）生成结构化 Markdown 报告
2. 宏观数据温度计（行业周期背景参考）
"""

import argparse, json, sys
from datetime import datetime


def generate_report(sections: dict) -> str:
    """从结构化数据生成八步法行业研究报告"""
    lines = []
    industry = sections.get("industry", "未知行业")
    date = datetime.now().strftime("%Y-%m-%d")

    lines.append(f"# 📊 {industry} 行业研究报告")
    lines.append(f"> 生成日期: {date}")
    lines.append(f"> **⚠️ 本报告基于公开信息整理，仅供参考，不构成任何投资或商业决策建议**")
    lines.append("")

    # 八步法章节
    chapter_titles = [
        ("一、行业界定与分类", "industry_definition"),
        ("二、市场分析", "market_analysis"),
        ("三、竞争格局", "competitive_landscape"),
        ("四、产业链分析", "value_chain"),
        ("五、技术趋势", "technology_trends"),
        ("六、政策环境", "regulatory_environment"),
        ("七、关键成功因素", "ksf"),
        ("八、结论与展望", "conclusion"),
    ]

    for title, key in chapter_titles:
        content = sections.get(key, "")
        lines.append(f"## {title}\n")
        if isinstance(content, dict):
            for k, v in content.items():
                if isinstance(v, list):
                    lines.append(f"**{k}**:")
                    for item in v:
                        lines.append(f"- {item}")
                    lines.append("")
                else:
                    lines.append(f"**{k}**: {v}\n")
        elif isinstance(content, list):
            for item in content:
                lines.append(f"- {item}")
            lines.append("")
        else:
            lines.append(f"{content}\n")
        lines.append("---\n")

    lines.append(f"*数据来源: 公开信息综合分析*")
    lines.append(f"*研究方法: 八步行业研究框架*")
    return "\n".join(lines)


def macro_thermometer(macro_data: dict) -> str:
    """宏观数据温度计——判断当前行业周期背景"""
    if not macro_data:
        return "（无宏观数据）"

    lines = ["## 宏观背景温度计\n"]
    for indicator, data in macro_data.items():
        if isinstance(data, dict) and "latest" in data:
            latest = data["latest"]
            lines.append(f"**{indicator}**:")
            for k, v in latest.items():
                if k != "date":
                    lines.append(f"- {k}: {v}")
            lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="行业研究报告框架生成器")
    parser.add_argument("--notes", help="研究笔记 JSON 文件路径")
    parser.add_argument("--industry", help="行业名称（快速生成框架）")
    parser.add_argument("--macro", help="宏观数据 JSON 文件路径（可选）")
    parser.add_argument("--output", help="输出报告路径")
    args = parser.parse_args()

    if args.notes:
        with open(args.notes) as f:
            sections = json.load(f)
    elif args.industry:
        # 生成空框架
        sections = {
            "industry": args.industry,
            "industry_definition": {"行业定义": "", "细分领域": [], "分类标准": ""},
            "market_analysis": {"TAM": "", "CAGR": "", "驱动力": [], "抑制因素": []},
            "competitive_landscape": {"主要参与者": [], "波特五力": {}, "竞争阶段": ""},
            "value_chain": {"上游": "", "中游": "", "下游": ""},
            "technology_trends": {"核心技术": [], "成熟度": "", "颠覆性风险": ""},
            "regulatory_environment": {"监管机构": "", "政策方向": "", "趋势判断": ""},
            "ksf": {"行业壁垒": [], "核心成功因素": [], "主要风险": []},
            "conclusion": {"生命周期定位": "", "未来判断": "", "战略启示": []},
        }
    else:
        print("请指定 --notes 或 --industry")
        sys.exit(1)

    report = generate_report(sections)

    if args.macro:
        with open(args.macro) as f:
            macro = json.load(f)
        report += "\n" + macro_thermometer(macro)

    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"✓ 报告已保存到 {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
