# Chapter style and figure/table composition

## Execution order

Evidence + venue requirements → chapter argument and style → asset specifications
and evidence → validate/resolve/render → approval gate → writer packet → node draft
→ content/reference review → official LaTeX compilation → final-size visual review
→ local revision. A packet is a handoff, not an executed model call.

`writing/writing-plan.composition.yaml` is a schema-valid minimal example. It
contains no real experimental findings. Existing v1 plans work without new fields.

## Style

`style.strategy` inherits through the normal profile/default/file/ancestor/node
chain. Allowed strategies: problem_gap_contribution, compare_and_position,
define_then_explain, protocol_first, observation_then_interpretation,
hypothesis_control_result, synthesize_and_bound, concise_summary.
Suggested mapping: Introduction / Related Work / Method / Setup / Results /
Ablation / Discussion / Abstract-Conclusion respectively. This is a writing guide,
not a claim that semantic style compliance can be mechanically established.
`style.paragraph_rules` is a list; normal replacement/append/unset rules apply.
Keep terminology, notation, person and evidence boundaries consistent across chapters.

## Node-local composition

`composition` appears only on nodes, never defaults or profiles, and does not
inherit. It participates in the owning node's requirement hash and approval
invalidation. It contains:

- `argument_steps`: ordered rhetorical tasks; prose must explain evidence rather
  than repeat every table cell.
- `page_budget`: positive planning budget (not measured or enforced by source review).
- `assets`: unique figure/table node ownership, with unique `fig:`/`tab:` label.
  Each specifies purpose, prose node for first_reference, prose nodes for discuss_in,
  scope (main_paper/supplement), span (one_column/two_columns), placement_preference
  (top/bottom/page/here_if_possible), optional max_height_fraction (0,1], and
  overflow_policy (reflow_asset/split_asset/move_to_supplement_after_approval).

An asset node uses the existing presentation.figures or presentation.tables to
link actual rendering/data plans. Composition is not a second renderer. LaTeX
placement preferences do not guarantee a page or float location. Planned spans and
budgets must be reconciled with the official template and actual rendered output.

## Writer task export

```bash
uv run scripts/writing_plan.py resolve .auto-research/writing-plan.yaml --output .auto-research/resolved-writing-plan.json
uv run scripts/writing_plan.py packet .auto-research/resolved-writing-plan.json --node sec-results --output .auto-research/writer-sec-results.json
```

The deterministic packet includes current resolved node/style/argument/budget,
parent objective, sibling **planned** summaries, relevant asset plans and layout
links, writing policy and post-write checks. It accepts resolved JSON only. Node
requirement hashes are checked for consistency; current and ancestor before_write
gates must be approved. No raw YAML is passed to the writer. Hash consistency is
not approval identity authentication; re-resolve after any original plan change.

The executor must supply verified research evidence, approved terminology and
summaries of actual neighboring text separately. The packet reports
`prepared_not_written`; it does not retrieve evidence, launch a model, write prose,
compile TeX or fabricate a generation record.

## Review and revision

For opted-in composition, normal writing review additionally checks literal
LaTeX label in the asset node and explicit ref/autoref/cref/Cref references in
first_reference and discuss_in nodes. Comments do not satisfy references. Use
existing node anchors, including `% auto-research:node NODE start/end` in TeX.
Generated table nodes should use labels emitted by Table Plan, e.g. tab:table-main.

Missing labels/references fail. A `layout_review` warning remains to request actual
compilation/visual review. These source checks do **not** expand TeX includes,
confirm the global first-use order, evaluate discussion quality, measure page
budgets, float distance, typography, overlaps or final-size readability. Review's
existing warning exit code remains 0; warning is not submission clearance.

The next review layer must retain official compile command, logs, exit status,
PDF hash, rendered-page observations and reviewer identity. That feedback adapter
and automatic layout repair are not implemented here. Do not mark these checks
passed from packet creation or source checks alone.

Local edits may remove repetition or reflow assets. Moving evidence to a supplement,
changing argument/structure or altering an approved goal requires planner review
and renewed approval where configured. Never shrink text indefinitely, alter an
immutable official style, or omit necessary experimental conditions to fit pages.
