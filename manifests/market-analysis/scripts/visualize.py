#!/usr/bin/env python3
"""visualize.py — 行业研究报告图表生成工具

代码生成图表，确保可重复性和格式一致性。
支持：柱状图、折线图、饼图、热力图、横向对比图。

用法:
  python scripts/visualize.py chart_type <data.json> --output output/chart.png
"""

import argparse, json, os, sys
from pathlib import Path

# matplotlib 设置
import matplotlib
matplotlib.use('Agg')  # 无头模式
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
matplotlib.rcParams['axes.unicode_minus'] = False

# 颜色方案（专业、色盲友好）
COLORS = {
    'blue': '#2563EB', 'green': '#10B981', 'amber': '#F59E0B',
    'red': '#EF4444', 'purple': '#8B5CF6', 'teal': '#14B8A6',
    'pink': '#EC4899', 'gray': '#94A3B8', 'slate': '#64748B',
    'dark': '#1E293B',
}
PALETTE = list(COLORS.values())


def _ensure_dir(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)


# ═══════════════════════════════════════════════
#  图表生成函数
# ═══════════════════════════════════════════════

def bar_chart(data: dict, output: str):
    """柱状图 — 市场份额、对比数据等"""
    labels = data.get('labels', [])
    values = data.get('values', [])
    title = data.get('title', '')
    ylabel = data.get('ylabel', '')
    source = data.get('source', '')

    fig, ax = plt.subplots(figsize=(10, 6))
    n = len(labels)
    colors = PALETTE[:n] if n <= len(PALETTE) else [PALETTE[i % len(PALETTE)] for i in range(n)]
    bars = ax.bar(labels, values, color=colors, edgecolor='white', linewidth=0.5)

    # 数值标注
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01,
                f'{val}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_ylim(0, max(values) * 1.15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='x', rotation=30 if n > 5 else 0)

    if source:
        fig.text(0.99, -0.02, f'数据来源: {source}', ha='right', fontsize=8, color='gray')

    plt.tight_layout()
    _ensure_dir(output)
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'✓ 柱状图已保存: {output}')


def line_chart(data: dict, output: str):
    """折线图 — 趋势展示"""
    x_labels = data.get('x_labels', [])
    series_list = data.get('series', [])  # [{label, values}]
    title = data.get('title', '')
    ylabel = data.get('ylabel', '')
    source = data.get('source', '')

    fig, ax = plt.subplots(figsize=(12, 5))
    x = range(len(x_labels))

    for i, series in enumerate(series_list):
        color = PALETTE[i % len(PALETTE)]
        ax.plot(x, series['values'], marker='o', linewidth=2.5,
                markersize=6, color=color, label=series.get('label', f'系列{i+1}'))

    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, rotation=30)
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.legend(frameon=False, fontsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    if source:
        fig.text(0.99, -0.02, f'数据来源: {source}', ha='right', fontsize=8, color='gray')

    plt.tight_layout()
    _ensure_dir(output)
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'✓ 折线图已保存: {output}')


def pie_chart(data: dict, output: str):
    """饼图 — 占比展示"""
    labels = data.get('labels', [])
    values = data.get('values', [])
    title = data.get('title', '')
    source = data.get('source', '')

    fig, ax = plt.subplots(figsize=(8, 8))
    colors = PALETTE[:len(labels)] if len(labels) <= len(PALETTE) else None
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, autopct='%1.1f%%',
        colors=colors, startangle=90,
        textprops={'fontsize': 10},
        pctdistance=0.75, wedgeprops={'edgecolor': 'white', 'linewidth': 1}
    )
    for t in autotexts:
        t.set_fontweight('bold')

    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)

    if source:
        fig.text(0.5, -0.02, f'数据来源: {source}', ha='center', fontsize=8, color='gray')

    plt.tight_layout()
    _ensure_dir(output)
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'✓ 饼图已保存: {output}')


def horizontal_bar(data: dict, output: str):
    """横向柱状图 — 排名/评分对比"""
    labels = data.get('labels', [])
    values = data.get('values', [])
    title = data.get('title', '')
    xlabel = data.get('xlabel', '')
    source = data.get('source', '')

    fig, ax = plt.subplots(figsize=(10, max(5, len(labels) * 0.4)))
    colors = [PALETTE[i % len(PALETTE)] for i in range(len(labels))]

    bars = ax.barh(labels, values, color=colors, edgecolor='white', linewidth=0.5)
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + max(values)*0.01, bar.get_y() + bar.get_height()/2,
                f'{val}', ha='left', va='center', fontsize=10, fontweight='bold')

    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.invert_yaxis()

    if source:
        fig.text(0.99, -0.03, f'数据来源: {source}', ha='right', fontsize=8, color='gray')

    plt.tight_layout()
    _ensure_dir(output)
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'✓ 横向柱状图已保存: {output}')


def heatmap(data: dict, output: str):
    """热力图 — 多维度对比矩阵"""
    matrix = data.get('matrix', [])
    row_labels = data.get('row_labels', [])
    col_labels = data.get('col_labels', [])
    title = data.get('title', '')
    source = data.get('source', '')

    fig, ax = plt.subplots(figsize=(max(6, len(col_labels)*1.2), max(5, len(row_labels)*0.6)))
    im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')

    ax.set_xticks(range(len(col_labels)))
    ax.set_yticks(range(len(row_labels)))
    ax.set_xticklabels(col_labels, rotation=30)
    ax.set_yticklabels(row_labels)

    # 在格子里标数值
    for i in range(len(row_labels)):
        for j in range(len(col_labels)):
            ax.text(j, i, matrix[i][j], ha='center', va='center',
                    fontsize=9, fontweight='bold',
                    color='white' if matrix[i][j] > max(matrix)/2 else 'black')

    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    fig.colorbar(im, ax=ax, shrink=0.8)

    if source:
        fig.text(0.99, -0.03, f'数据来源: {source}', ha='right', fontsize=8, color='gray')

    plt.tight_layout()
    _ensure_dir(output)
    plt.savefig(output, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'✓ 热力图已保存: {output}')


# ═══════════════════════════════════════════════
#  主入口
# ═══════════════════════════════════════════════

CHART_FUNCS = {
    'bar': bar_chart,
    'line': line_chart,
    'pie': pie_chart,
    'hbar': horizontal_bar,
    'heatmap': heatmap,
}


def main():
    parser = argparse.ArgumentParser(description='行业研究图表生成工具')
    parser.add_argument('type', nargs='?', choices=list(CHART_FUNCS.keys()),
                        help='图表类型: bar(柱状图) line(折线) pie(饼图) hbar(横向柱) heatmap(热力)')
    parser.add_argument('data', nargs='?', help='数据 JSON 文件')
    parser.add_argument('--output', '-o', default='output/chart.png',
                        help='输出 PNG 路径')
    parser.add_argument('--example', action='store_true',
                        help='生成示例图表（无需指定 type 和 data）')
    args = parser.parse_args()

    if args.example:
        # 生成示例数据展示效果
        from datetime import datetime
        examples_dir = 'output/examples'
        # 柱状图示例
        bar_chart({
            'labels': ['公司A', '公司B', '公司C', '公司D', '其他'],
            'values': [35, 25, 15, 10, 15],
            'title': f'行业市场份额分布 ({datetime.now().year})',
            'ylabel': '市场份额 (%)',
            'source': '示例数据',
        }, f'{examples_dir}/bar_example.png')
        # 折线图示例
        line_chart({
            'x_labels': ['2021', '2022', '2023', '2024', '2025'],
            'series': [
                {'label': '行业规模(亿元)', 'values': [100, 150, 220, 320, 450]},
                {'label': '增长率(%)', 'values': [30, 50, 47, 45, 41]},
            ],
            'title': '行业市场规模与增长率趋势',
            'ylabel': '规模(亿元) / 增长率(%)',
            'source': '示例数据',
        }, f'{examples_dir}/line_example.png')
        # 饼图示例
        pie_chart({
            'labels': ['产品A', '产品B', '产品C', '产品D', '其他'],
            'values': [40, 25, 15, 12, 8],
            'title': '行业收入结构分布',
            'source': '示例数据',
        }, f'{examples_dir}/pie_example.png')
        print(f'\n✅ 示例图表已生成到 {examples_dir}/')
        return

    with open(args.data) as f:
        data = json.load(f)

    CHART_FUNCS[args.type](data, args.output)


if __name__ == '__main__':
    main()
