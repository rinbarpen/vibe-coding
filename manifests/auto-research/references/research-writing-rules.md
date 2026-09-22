# Research Writing Rules / 科研写作规则

这份规则是 `auto-research` 的机器可读 `writing_policy` 的操作说明。当前优先
接入 `research` 场景，正文默认使用 LaTeX；中文和英文写作使用同一组门禁，语言
相关内容由对应 skill 路由。

## 1. 默认写作策略 / Defaults

| Rule | 中文 | English |
|---|---|---|
| Uncertainty | 默认不添加 95% CI。只有官方投稿要求、研究方案、作者明确要求或审稿意见要求时才加入，并在 Writing Plan 记录理由。 | Do not add 95% CIs by default. Add them only when required by the venue, study protocol, author request, or reviewer request, and record the reason in the Writing Plan. |
| Defensive writing | 默认关闭防御性写作。不要为了“显得严谨”主动堆叠自我削弱、无关限制或失败维度；主张必须与证据边界一致。 | Defensive writing is disabled by default. Do not add self-undermining caveats, irrelevant limitations, or losing dimensions merely to sound cautious; keep every claim within its evidence boundary. |
| Humanization | 草稿形成后接入 `z-humanizer`，中文/英文按段落路由到 academic、journal 或 conference 域。 | Run `z-humanizer` after a draft exists, routing Chinese/English paragraphs to the academic, journal, or conference domain. |
| Source of truth | 期刊/会议官方投稿要求和官方模板优先于通用 profile。 | Official venue requirements and the official template take precedence over generic profiles. |

“默认不添加 95% CI”不等于修改已经存在的统计方案。若研究设计、数据类型或目标
venue明确要求不确定性报告，先更新 `writing-plan.yaml` 的统计/呈现节点，再写入
正文与表图。

## 2. Skill 接入 / Skill integration

### Anti-defensive writing

上游仓库提供中英文两个 skill 目录，作为一个 Git 子模块管理：

- 中文：`skills/anti-defensive-writing/SKILL.md`
- English: `skills/anti-defensive-writing-en/SKILL.md`
- Upstream: <https://github.com/Adkid-Zephyr/anti-defensive-writing-Skill>

初始化或更新：

```bash
git submodule update --init -- skills/anti-defensive-writing
```

在研究场景中，该 skill 是**可选审计器**而不是自动改写器。只有 Writing Plan
明确打开 `defensive_writing.audit: true` 时才运行；审计报告记录命中的句子、主张
范围和对应证据，不自动扩张结论，也不把“限制”删掉来制造过度自信的表述。

### z-humanizer

仓库内置 `mine/z-humanizer/SKILL.md`，已接入 research 写作节点。它负责检测和
修正模板化、机械化或领域不匹配的表达，同时保留事实、数字、引用 key、代码、URL
和术语。默认路由：

```text
研究材料/结果 → LaTeX 草稿 → anti-defensive audit（可选）
→ z-humanizer（zh/en，academic/journal/conference）
→ paper-review → venue/template compliance
```

`z-humanizer` 不负责决定研究主张是否成立；证据边界、统计方案和官方投稿要求分别
由研究审查、统计审计和 venue gate 负责。

## 3. LaTeX 与模板锁定 / LaTeX and template lock

1. 先解析官方投稿要求，登记 `source_url`、`checked_at`、venue、年份/版本、匿名
   规则、页数、文件清单、编译命令、图表格式与尺寸。
2. 获取官方 LaTeX 模板，将模板文件写入只读基线清单
   `.auto-research/writing/latex/template-manifest.json`，至少包含路径、sha256、
   来源和版本。
3. `*.cls`、`*.sty`、模板自带字体/布局/参考文献样式和模板 table/figure style
   文件视为 immutable。论文只能在模板允许的接口内设置内容、数据、caption、label
   和必要的 metadata；不通过改 style 文件解决排版问题。
4. 缺少文件时记录 `missing_required_file`；不要用自制 style 替代官方 style。需要
   自定义宏时放在项目自己的 `macros.tex`，并在模板兼容性检查中登记。
5. 编译至少执行官方推荐命令，并保存完整 stdout/stderr、退出状态、引擎版本和
   生成 PDF 的 sha256 到 `.auto-research/writing/latex/compile.log` 与 manifest。
6. 投稿打包只从通过校验的 LaTeX 工作区生成，保留 `main.tex`、`.bib`、图、表、宏、
   模板清单、编译记录以及 venue 要求的补充文件。

### Minimum file contract / 最小文件契约

`writing_policy.latex_template.required_files` 是起点，不是对所有 venue 的固定清单。
实际清单由官方要求覆盖：

```text
main.tex
references.bib
figures/              # 若正文含图
tables/               # 若正文含表
macros.tex            # 仅在项目确实使用自定义宏时
supplement/           # 仅在 venue 要求或 Writing Plan 声明时
```

提交前必须同时通过：

- `venue_requirements`: 官方要求已锁定并可追溯；
- `template_integrity`: 模板 style 文件 sha256 未变化；
- `latex_compile`: 官方编译命令退出状态为 0；
- `artifact_completeness`: 实际必需文件齐全；
- `content_review`: `paper-review`、统计/引用审计和 `z-humanizer` 记录已归档。

## 4. Writing Plan 示例 / Example node policy

将以下内容合并到项目的 `.auto-research/writing-plan.yaml`，不要直接修改
`writing/venue-profiles.yaml` 来伪造某个 venue 的要求：

```yaml
scene: research
language: [zh, en]
writing_policy:
  engine: latex
  defensive_writing: false
  confidence_interval: omitted_by_default
  template:
    source_url: https://VENUE_OFFICIAL_TEMPLATE
    checked_at: YYYY-MM-DD
    style_files_immutable: true
    manifest: .auto-research/writing/latex/template-manifest.json
  skills:
    anti_defensive_writing:
      enabled: false
      zh: skills/anti-defensive-writing/SKILL.md
      en: skills/anti-defensive-writing-en/SKILL.md
    humanizer: mine/z-humanizer/SKILL.md
```

当作者或 venue 明确要求不确定性区间时，把 `confidence_interval` 改为具体方案，
并在对应结果节点写出 estimator、level、seed/replicate 聚合方式和引用来源。
