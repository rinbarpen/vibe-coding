# Auto-Research Writing Plan 实施

## 目标
在 `manifests/auto-research` 内实现版本化 Writing Plan 子系统，不修改 vibe CLI 公共接口或其他 manifests。

## 阶段
- [complete] 1. 盘点现有 manifest，确定 schema、解析器和运行时格式
- [complete] 2. 新增 writing 资源：schema、profiles、模板、迁移默认值、README
- [complete] 3. 实现 `scripts/writing_plan.py` 的 init/validate/resolve/render/review/migrate
- [complete] 4. 接入 CLAUDE/AGENTS/lifecycle/init scaffold
- [complete] 5. 新增合法、非法、迁移、解析、渲染、审查与端到端测试
- [complete] 6. 运行回归，修复问题并核验改动边界

## 约束与决策
- PEP 723 依赖：PyYAML、jsonschema；使用 `uv run`。
- 原子写入采用同目录临时文件与 `os.replace`。
- resolve/render 对相同输入保持确定性。
- 稳定 ID 不由正文哈希派生；大纲同步只对类型/标题唯一匹配复用既有 ID。
- public vibe CLI 未修改。

## 错误记录
- 初次执行工具时宿主 IPC 解码失败；用户确认修复后恢复。
- 仓库级 `git status` 因无关 submodule gitdir 路径损坏而失败；使用限定路径的 diff/ls-files 完成边界核验。
- uv 默认缓存只读且网络受限；系统解释器已有 PyYAML/jsonschema/pytest，使用系统依赖完成验证，PEP 723 保留给正常 scaffold 环境。
- 两次端到端夹具失败均由正确继承语义造成，修正夹具而未削弱 resolver。
