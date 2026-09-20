# 全生命周期记录与模型路由

`lifecycle/defaults.json` 定义三层阶段：startup、literature、idea、design、execution、analysis、writing、internal-review、submission、revision、acceptance。大阶段→小阶段→小小阶段，每项对应科研活动而非工具调用。允许项目增补三层节点，不适用节点 skipped 并写原因。

每个大阶段的目标、输入、产物、门禁、模型角色和回退路径见 [lifecycle-stage-details.md](lifecycle-stage-details.md)；机器可读字段位于 `defaults.json.phase_details`。

## 初始化与命令

```bash
python3 scripts/research_workflow.py --project-root . init
python3 scripts/research_workflow.py --project-root . route planner
python3 scripts/research_workflow.py --project-root . status --cycle cycle-001
python3 scripts/research_workflow.py --project-root . checkpoint --stage startup --state started --role planner --actual-model ACTUAL_MODEL_ID --summary '研究目标和验收标准已确认' --next '启动目标细化' --artifact RESEARCH_PLAN.md
python3 scripts/research_workflow.py --project-root . resume --cycle cycle-001
```

标准库工具，POSIX 本地文件锁。退出码 0 成功、1 约束失败、2 I/O 错误。init 不覆盖已有 settings，不提交旧项目的未确认历史，不租资源或调用模型。根目录必须是本科研项目 Git root，避免对聚合仓库误操作。

运行设置位于 `.auto-research/lifecycle/settings.json`；事件追加于 events.jsonl；local/ 是忽略的事务日志及锁；快照在 refine-logs/history/<cycle>/<checkpoint>/。设置变更随下一检查点提交。

## 模型绑定

默认职责：research=GPT-6 Pro，planner=GPT-6 medium，executor=GPT-5.6-Luna high，writer=GPT-5.5 high。Pro 是 service_profile，不是推理等级。bindings 初始为空，由实际执行宿主核验供应商能力后填写，每项包含 provider、model_id、service_profile、reasoning_effort、available、verified_at。不可在文件中存 API key。

`route` 返回实际绑定供宿主调度；工具本身不调用模型。`--actual-model` 必须由宿主实际会话元数据提供，而不是复制默认模型名。执行记录的真实性由调用宿主提供，CLI 只验证匹配关系。availability 是宿主验证记录，不是实时连通性证明。宿主调用失败时记录 blocked，summary 以 blocked_model_unavailable 开头，可在未绑定时留档。

同一阶段可以按职责切换模型。checkpoint 支持 `--role`，项目设置中修改某职责绑定属于显式覆盖，需记录原因及新旧配置。审查使用独立上下文，保留 reviewer 实际身份；同模型新会话不标称跨模型审查。

## 状态与轮次

started→completed/failed/blocked/paused/revised；paused/failed/blocked→resumed；活动阶段可 revised，任何尚未执行且不适用的节点可 skipped。进入子节点前先启动父节点；完成父节点前所有直接子节点必须 completed/skipped。祖先暂停时先恢复父级。

每个 cycle 内同一阶段只有一个 execution_id；终态后再做该阶段必须创建新 cycle（从对应大阶段开始），稳定 stage_id 保持。`--submission-id` / `--revision-id` 标识投稿/返修，不覆盖前次记录。负结果仍可 completed，科学结论写 summary，与执行状态分离。录用确认、投稿回执、返修提交及外审决定完成时强制要求 artifact；真实性由科研人员核验。

## Git 与恢复

每次事件（进入、结束、失败、修订、暂停和恢复）都形成 commit；父阶段提交汇总其子阶段，不重复复制所有二进制产物。显式 --artifact 可重复，--input、--run-id 记录关联，--command 记录命令，--summary 和 --next 必填。所有输入只登记引用，产物才提交。

仅提交明确登记文件及生命周期账本，使用 git commit --only，保留无关 staged/unstaged 变更。进程锁让并行 run 的记录提交串行化；锁忙则重试。init 无 Git 时初始化，但不设置 user.name/email；缺身份或冲突时 checkpoint 阻塞。默认不 push、不 reset、不改历史。保存 pending 事务后提交，resume 检索 Checkpoint-ID 恢复，避免提交成功/清理前中断导致重复提交。resume 遇到已登记产物变化要求先恢复原内容；不自动覆盖用户修订。

所有快照保留；事件更正以新 revised 事件追加，不覆盖旧事件。路径限制在项目内。默认 Git 单文件上限 10 MiB；二进制/大型文件使用归档索引（artifact path、size、sha256、run/attempt、生成时间、local_only 或 archived、检查时间）。索引必须含 kind=archive_index；登记时工具实际读取本地或已挂载存储并验证大小和 SHA-256。远程对象须先挂载或同步到可验证位置；不将未核实 URL 标记为已归档。可单独运行 `research_workflow.py archive-check INDEX.json`。Git 提交前检查常见明文凭据模式，命中则先制作脱敏副本；该检查不替代人工保密检查。

resume 首先修复 pending Git 事务，然后显示最近阶段状态。它不自动重启实验。执行器必须核验实际进程、queue state 和输出，并为恢复任务记录 resumed；成功结果复用，运行任务重新连接，失败任务另建 attempt。

## 周期终点与写作

研究→实验→结果不支持时回到 idea/design 新 cycle；内部评审→补实验→Writing Plan 更新；外审→响应矩阵→补实验/回复→修订提交；拒稿→新 submission 与转投。每次论文节点修改遵守原 Writing Plan 的 validate/resolve/render/approval/review。

真正中稿以正式录用通知为依据；camera-ready/校样/归档是录用后单独状态。正式投稿与作者确认、撤稿等有外部影响的操作必须先获得用户确认，记录实际回执而不是模拟成功。集成测试只用标记为 fixture 的本地材料。
