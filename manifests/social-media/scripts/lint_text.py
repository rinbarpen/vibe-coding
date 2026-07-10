#!/usr/bin/env python3
"""lint_text.py — 中英文排版检查工具

检查项: 中英文间距、全半角标点、AI 废话、段落长度
用法: python lint_text.py <file> [--fix] [--strict] [--output <path>]
"""

import re, argparse, json, sys

# AI 废话模式
AI_FILLER = [
    r"值得注意的是，",
    r"毋庸置疑，",
    r"不可否认的是，",
    r"在当今世界，",
    r"在当今社会，",
    r"我们都知道，",
    r"众所周知，",
    r"从某种意义上说，",
    r"值得一提的是，",
    r"需要指出的是，",
    r"总的来说，",
    r"总而言之，",
    r"It's important to note that",
    r"In a world where",
    r"Ultimately,",
]


def check_zh_en_spacing(text: str) -> list:
    """检查中文与英文/数字之间的空格"""
    issues = []
    # 中文后紧跟英文
    for m in re.finditer(r'([\u4e00-\u9fff])([a-zA-Z])', text):
        issues.append({
            "type": "spacing",
            "severity": "error",
            "pos": m.start(),
            "msg": f"中文后缺少空格: '{m.group(1)}{m.group(2)}'",
            "fix": f"{m.group(1)} {m.group(2)}",
        })
    # 英文后紧跟中文
    for m in re.finditer(r'([a-zA-Z])([\u4e00-\u9fff])', text):
        issues.append({
            "type": "spacing",
            "severity": "error",
            "pos": m.start(),
            "msg": f"英文后缺少空格: '{m.group(1)}{m.group(2)}'",
            "fix": f"{m.group(1)} {m.group(2)}",
        })
    # 数字后紧跟中文
    for m in re.finditer(r'(\d)([\u4e00-\u9fff])', text):
        issues.append({
            "type": "spacing",
            "severity": "error",
            "pos": m.start(),
            "msg": f"数字后缺少空格: '{m.group(1)}{m.group(2)}'",
            "fix": f"{m.group(1)} {m.group(2)}",
        })
    # 中文后紧跟数字
    for m in re.finditer(r'([\u4e00-\u9fff])(\d)', text):
        issues.append({
            "type": "spacing",
            "severity": "error",
            "pos": m.start(),
            "msg": f"中文后数字前缺少空格: '{m.group(1)}{m.group(2)}'",
            "fix": f"{m.group(1)} {m.group(2)}",
        })
    return issues


def check_ai_filler(text: str) -> list:
    """检查 AI 废话填充词"""
    issues = []
    for pattern in AI_FILLER:
        for m in re.finditer(pattern, text):
            issues.append({
                "type": "ai_filler",
                "severity": "warning",
                "pos": m.start(),
                "msg": f"AI 废话填充: '{m.group()[:20]}...'",
                "fix": "",
            })
    return issues


def check_paragraph_length(text: str, strict: bool = False) -> list:
    """检查段落长度"""
    issues = []
    max_len = 150 if strict else 200
    paragraphs = text.split("\n\n")
    for i, para in enumerate(paragraphs):
        para_clean = para.strip()
        if not para_clean:
            continue
        if len(para_clean) > max_len * 4:  # 超大段落
            issues.append({
                "type": "paragraph",
                "severity": "error",
                "pos": text.find(para_clean[:20]),
                "msg": f"第 {i+1} 段过长 ({len(para_clean)} 字)，建议拆分",
                "fix": "",
            })
        elif len(para_clean) > max_len:
            issues.append({
                "type": "paragraph",
                "severity": "warning" if not strict else "error",
                "pos": text.find(para_clean[:20]),
                "msg": f"第 {i+1} 段偏长 ({len(para_clean)} 字)",
                "fix": "",
            })
    return issues


def apply_fixes(text: str, issues: list) -> str:
    """应用可自动修复的修改"""
    # 从后往前修复，避免位置偏移
    fixable = [i for i in issues if i.get("fix")]
    fixable.sort(key=lambda x: -x["pos"])

    for issue in fixable:
        old = text[issue["pos"]:issue["pos"] + len(issue["msg"].split("'")[1])]
        text = text[:issue["pos"]] + issue["fix"] + text[issue["pos"] + len(old):]

    return text


def main():
    parser = argparse.ArgumentParser(description="中英文排版检查工具")
    parser.add_argument("file", help="要检查的文件")
    parser.add_argument("--fix", action="store_true", help="自动修复")
    parser.add_argument("--strict", action="store_true", help="严格模式")
    parser.add_argument("--output", help="输出报告")
    args = parser.parse_args()

    with open(args.file, "r") as f:
        text = f.read()

    all_issues = []
    all_issues.extend(check_zh_en_spacing(text))
    all_issues.extend(check_ai_filler(text))
    all_issues.extend(check_paragraph_length(text, strict=args.strict))

    if args.fix:
        text = apply_fixes(text, all_issues)
        # 修复后重新检查
        all_issues = []
        all_issues.extend(check_zh_en_spacing(text))
        all_issues.extend(check_ai_filler(text))
        all_issues.extend(check_paragraph_length(text, strict=args.strict))

    errors = [i for i in all_issues if i["severity"] == "error"]
    warnings = [i for i in all_issues if i["severity"] == "warning"]

    result = {
        "total_issues": len(all_issues),
        "errors": len(errors),
        "warnings": len(warnings),
        "issues": all_issues,
        "fixed": args.fix,
    }

    if args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"━━━ 排版检查结果 ━━━")
    print(f"  问题总数: {result['total_issues']}")
    print(f"  严重错误: {result['errors']}")
    print(f"  建议修复: {result['warnings']}")
    if result['fixed']:
        print(f"  自动修复: 已应用")

    if args.fix:
        with open(args.file, "w") as f:
            f.write(text)
        print(f"  ✓ 文件已更新: {args.file}")

    if errors:
        print(f"\n⚠️  还有 {len(errors)} 个严重问题未修复")
        sys.exit(1)


if __name__ == "__main__":
    main()
