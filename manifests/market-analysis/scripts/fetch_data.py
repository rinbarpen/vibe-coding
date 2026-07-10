#!/usr/bin/env python3
"""fetch_data.py — 行业研究信息收集辅助工具

行业研究不依赖股票数据。本脚本提供：
1. 宏观数据获取（CPI/PMI/GDP/M2 — 判断行业周期背景）
2. 搜索辅助（按行业关键词搜索公开信息）
3. 数据整理辅助

用法:
  python scripts/fetch_data.py macro CPI          # 宏观背景数据
  python scripts/fetch_data.py search "AI软件 市场规模"  # 搜索行业信息
  python scripts/fetch_data.py sources "半导体"    # 列出研究资料来源建议
"""

import argparse, json, sys, os
from datetime import datetime

try:
    import pandas as pd
except ImportError:
    pd = None


def fetch_macro(indicator: str) -> dict:
    """获取宏观数据（判断行业周期背景）"""
    try:
        import akshare as ak
    except ImportError:
        return {"error": "需要 akshare: pip install akshare"}

    macro_api = {
        "CPI": ("macro_china_cpi_monthly", {"日期": "date"}),
        "PMI": ("macro_china_pmi", {"月份": "date"}),
        "GDP": ("macro_china_gdp", {"季度": "date"}),
        "M2": ("macro_china_money_supply", {"月份": "date"}),
    }
    key = indicator.upper()
    if key not in macro_api:
        return {"error": f"未知指标: {indicator}，可选: CPI/PMI/GDP/M2"}

    try:
        fn_name, rename_map = macro_api[key]
        fn = getattr(ak, fn_name)
        df = fn()
        df = df.rename(columns=rename_map)
        df["date"] = pd.to_datetime(df["date"])
        return {"type": "macro", "indicator": key, "rows": len(df),
                "period": f"{df['date'].min().date()} ~ {df['date'].max().date()}",
                "latest": df.iloc[-1].to_dict() if len(df) > 0 else {},
                "last_5": df.tail(5).to_dict(orient="records")}
    except Exception as e:
        return {"error": f"获取 {key} 失败: {e}"}


def suggest_sources(industry: str) -> dict:
    """根据行业提供研究资料来源建议"""
    general_sources = [
        {"type": "行业报告", "sources": ["艾瑞咨询", "易观分析", "IDC", "Gartner", "Frost & Sullivan",
                          "36氪研究院", "头豹研究院", "CIC灼识咨询"]},
        {"type": "公司信息", "sources": ["公司官网", "招股书（如上市公司）", "企查查/天眼查"]},
        {"type": "新闻媒体", "sources": ["36氪", "虎嗅", "澎湃", "行业垂直媒体",
                          "Google News / 百度新闻"]},
        {"type": "政府数据", "sources": ["国家统计局", "工信部", "行业协会",
                          "地方政府产业报告"]},
        {"type": "技术专利", "sources": ["Google Patents", "CNKI专利", "智慧芽"]},
        {"type": "招聘信息", "sources": ["BOSS直聘", "猎聘", "LinkedIn — 反映行业人才需求"]},
        {"type": "社交媒体", "sources": ["知乎（行业讨论）", "X/Twitter（KOL观点）",
                          "微信公众号（行业深度）"]},
    ]
    return {"type": "sources", "industry": industry, "suggestions": general_sources}


def search_assist(query: str) -> dict:
    """搜索辅助——提供搜索建议关键词"""
    # 生成多个搜索方向的关键词
    keywords = [
        query,
        f"{query} 市场规模",
        f"{query} 行业报告",
        f"{query} 竞争格局",
        f"{query} 产业链",
        f"{query} 技术趋势",
        f"{query} 政策 监管",
        f"{query} 龙头企业",
    ]
    return {"type": "search_assist", "query": query, "suggested_searches": keywords}


def main():
    parser = argparse.ArgumentParser(description="行业研究信息收集辅助")
    parser.add_argument("type", choices=["macro", "sources", "search"],
                        help="macro=宏观数据, sources=资料来源建议, search=搜索关键词")
    parser.add_argument("param", nargs="?", default="", help="宏观指标/行业名/搜索词")
    parser.add_argument("--output", help="保存到文件")
    args = parser.parse_args()

    if args.type == "macro":
        if not args.param:
            print("请指定宏观指标: CPI/PMI/GDP/M2")
            sys.exit(1)
        result = fetch_macro(args.param)
    elif args.type == "sources":
        result = suggest_sources(args.param or "（通用）")
    elif args.type == "search":
        result = search_assist(args.param or "（通用）")
    else:
        result = {"error": f"未知类型: {args.type}"}

    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, ensure_ascii=False, indent=2, default=str)
        print(f"✓ 已保存到 {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
