# Findings

- 现有 auto-research 仅有 CLAUDE/AGENTS、references、templates 和 shell 初始化器；没有 writing agent/skill 或 Python 测试基础。
- `init-auto-research.sh` 当前只复制 GitHub 配置、templates 和 references，需要新增 writing、scripts、tests（运行时 scaffold 至少需 writing/script）。
- 当前 Phase 3 直接从 paper-plan 进入 paper-write，应插入 plan-writing、validate、resolve、render、approval、逐节点 write/review/revise。
- 嵌套 `AGENTS.md` 要求所有 plan 步骤先 grill-me；实施文档需保留该约束。
