# CLAUDE.md

## Architecture
- Computation: Python/C++/Rust
- Experiment Tracking: MLflow/WandB
- Data: Immutable datasets
- Visualization: Matplotlib / Seaborn (顶会级模板)

## Project Structure

```
<root>/
├── experiments/                     # 实验目录（核心）
│   ├── INDEX.yaml                   # 全局实验索引
│   ├── {date}_{category}_{var}_{ds}/ # 单个实验
│   │   ├── config.yaml              # 实验配置（强制）
│   │   ├── metrics.json             # 标准化指标
│   │   ├── logs/                    # train.log, stderr.log
│   │   ├── checkpoints/             # best.pt, latest.pt
│   │   ├── figures/                 # 本实验专属图
│   │   └── README.md                # 自动生成的结果摘要
│   └── archive/                     # 只读归档
├── data/                            # DVC 或 Git LFS 管理
├── notebooks/                       # EDA
├── paper/                           # LaTeX 源文件
├── scripts/                         # 预处理与绘图脚本
└── templates/                       # 可视化模板（见下文）
```

## Experiment Commands

### 一键全流程

| Command | Description |
|---------|-------------|
| `vibe-exp all <name> --idea "..." [--template neurips|cvpr|acl|general]` | 设计→运行→监控→对比→消融→可视化，一气呵成 |

### 分步命令

| 阶段 | 命令 | 说明 |
|------|------|------|
| **设计** | `vibe-exp design <name> --idea "..."` | 生成 config.yaml 草稿 |
| **准备** | `vibe-exp setup <name>` | 创建目录、校验数据、锁定种子 |
| **运行** | `vibe-exp run <name>` | 执行训练，自动记录参数+指标+环境快照 |
| **监控** | `vibe-exp monitor <name>` | 实时面板（loss 曲线、GPU 利用率、ETA） |
| **分析** | `vibe-exp analyze <name>` | 生成标准化报告（指标汇总、学习曲线、误差分析） |
| **对比** | `vibe-exp compare <a> <b>` | 多实验并列对比、消融分析表、统计检验 |
| **归档** | `vibe-exp archive <name>` | 锁定结果、关联论文 Figure/Table、标记只读 |

### 工具命令

| Command | Description |
|---------|-------------|
| `vibe-check research` | 验证实验可复现性 & 图表语言 |
| `vibe-track-exp` | 手动记录实验元数据 |
| `vibe-exp list` | 列出 INDEX.yaml 中所有实验及其状态 |

---

## Experiment Config Schema (`config.yaml`)

每个实验必须包含此 YAML，作为标准化入口：

```yaml
# === 实验身份 ===
name: "exp-name"
idea: "一句话描述核心 IDEA（与论文创新点挂钩）"
hypothesis: "本实验要验证的假设（可证伪）"
paper_section: ""   # 对应论文哪一节 / 哪个 Figure/Table

# === 可复现性 ===
seed: 42
num_runs: 5         # 重复次数（用于误差棒）
env_snapshot: true  # 自动记录 pip/conda 环境

# === 数据（显式声明） ===
data:
  dataset: "DatasetName"
  version: "v2.0"
  source: "https://..."              # 下载 URL 或内部路径
  license: "CC-BY 4.0"              # 使用许可
  why_this_dataset: "该数据集是 {领域} 标准 benchmark，覆盖 {特征}，适合验证 {IDEA}"
  train: "data/train.parquet"
  val: "data/val.parquet"
  test: "data/test.parquet"
  split_strategy: "random_8020"     # random_8020 | stratified | time_based | kfold
  preprocessing:
    normalize: {mean: [0.485, 0.456, 0.406], std: [0.229, 0.224, 0.225]}
  augmentation: []                  # 扩增策略列表（含参数）
  known_bias: ""                    # 必填：不平衡性、标注噪声、域偏移等

# === 模型 ===
model:
  type: "ModelClass"
  params: {}
  pretrained: null                  # 预训练权重路径或 Hub ID

# === 训练 ===
training:
  epochs: 100
  batch_size: 32
  optimizer: {name: AdamW, lr: 0.001, weight_decay: 0.01}
  scheduler: {name: CosineAnnealingLR, T_max: 100}
  early_stop: {patience: 10, metric: val_loss}
  mixed_precision: true
  gradient_clip: 1.0

# === 评估 ===
evaluation:
  metrics: [accuracy, f1, precision, recall]
  primary_metric: f1
  statistical_test: bootstrap       # bootstrap | ttest | mcnemar

# === 消融实验 ===
ablation:
  enabled: false
  variable: null                    # 单一变量名
  baseline_value: null
  variants: []                      # 变体值列表
```

---

## Experiment Naming Convention

```
{YYYY-MM-DD}_{category}_{key-variable}_{dataset}
```

- `category`: `baseline` | `ablation` | `hyperparam` | `comparison` | `exploratory`
- `key-variable`: 本次实验操作的核心变量（如 `dropout_0.3`, `lr_1e-3`, `layers_12`）
- `dataset`: 数据集简称（如 `cifar10`, `imagenet`, `squad`）

示例:
- `2026-05-24_baseline_resnet50_imagenet`
- `2026-05-25_ablation_dropout_0.3_cifar10`
- `2026-05-26_comparison_vit-b_pretrained_imagenet`

---

## 数据集选择与使用（显式声明）

每个实验必须在 `config.yaml` 中填写完整的 `data` 字段块，并在 `INDEX.yaml` 中登记。选择数据集时自问：

1. **有没有更标准的 benchmark？** 优先使用领域内公认数据集
2. **数据量和分布是否匹配 IDEA？** 数据太少无法支撑结论，分布太偏结论不具泛化性
3. **许可是否允许使用？** 学术用途 ≠ 无限制
4. **已知偏差是什么？** 不平衡、标注噪声、域偏移 —— 不声明则不诚实
5. **为什么选这个（而不是别的）？** 必须用一句话在 `why_this_dataset` 中写清楚

---

## 实验提点 (Tricks)

### 训练前 —— 先确认 Pipeline 无误

- **过拟合测试**: 用 100 样本训练，确认 loss→0 → pipeline 无 bug
- **梯度检查**: 自定义层/损失函数必须做 gradient checking
- **LR range test**: 跑一轮 `lr_find()` 确定合理初始学习率
- **数据抽查**: 手动检查 preprocessed batch，确认标签未错位、归一化正确

### 训练中 —— 主动监控

- **梯度范数 (gradient norm)**: 异常波动 → 不稳定，过大 → 梯度爆炸，过小 → 梯度消失
- **`torch.autograd.set_detect_anomaly(True)`**: 定位 NaN 来源的第一工具
- **Checkpoint 策略**: `best.pt`（按 primary_metric 择优）+ `latest.pt`（按 interval 兜底）+ `periodic/`（每 N epoch 保留）
- **混合精度**: 默认开启，吞吐提升 30-50%，显存节省显著

### 调参 —— 效率优先

- **调参顺序**: lr > batch_size > optimizer 参数 > model architecture > 正则化
- **搜索策略效率**: Bayesian > Random >> Grid（不要再做全量 Grid Search）
- **重复实验**: 不同 seed 重复 3-5 次，报告 mean±std，否则结论不可靠

### Debug 速查

| 症状 | 可能原因 | 排查顺序 |
|------|---------|---------|
| loss 不下降 | lr 过小/过大、数据未归一化、初始化不当 | 1. LR range test 2. 检查数据范围 3. 换初始化 |
| loss 震荡剧烈 | lr 过大、batch 太小、数据未 shuffle | 1. 降 lr 2. 增 batch_size 3. 确认 shuffle |
| val >> train | 过拟合 | 1. 增强 regularization 2. 更多 data augmentation 3. early stop |
| train 也差 | 欠拟合 | 1. 增大模型容量 2. 减少 regularization 3. 训练更久 |
| 出现 NaN | 梯度爆炸、lr 过大、除零 | 1. `detect_anomaly` 2. 梯度裁剪 3. 降 lr |

---

## 快速消融与对比实验

### Ablation Study

- **单变量原则**: 一次只改变一个组件，其余固定
- **自动生成消融表**: 按 primary_metric 降序排列，标注 Δ（与 full model 的差距）
- **瀑布图**: 从 baseline 开始，逐个加组件，看增益递减

### Baseline Comparison

- **内部 baseline**: 本实验体系中的基准配置（`baseline_*`）
- **外部 baseline**: SOTA 论文报告数据（须注明出处和复现条件）
- **统计检验**: 对比必须含 bootstrap / t-test / McNemar（根据任务类型选择）
- **结果表格**: 自动输出 LaTeX 格式 `results_table.tex`，最优值加粗

### 可视化对比

- 多实验学习曲线叠图 + 误差带
- 柱状对比图（自动高亮 Ours + 显著性星号）
- 雷达图（多指标综合对比）
- 消融瀑布图（组件贡献度排序）

---

## 顶会级别可视化模板

四套开箱即用的 matplotlib 模板，紧扣 IDEA 叙事线。通过 `--template` 参数指定。

| 模板 | 适用会议 | 风格 |
|------|---------|------|
| **neurips** | NeurIPS / ICML / ICLR | 极简、无衬线 (Helvetica/DejaVu Sans)、色盲友好 |
| **cvpr** | CVPR / ICCV / ECCV | 图像密集、定性结果网格、对比放大区域 |
| **acl** | ACL / EMNLP / NAACL | 表格优先、注意力热力图、长文本兼容 |
| **general** | 通用期刊 / 学位论文 | 传统学术、高 DPI、中英文兼容 |

### 每套模板统一参数

```python
# templates/{template_name}.py
# 包含以下预设：

# 1. rcParams — 字体、字号、线宽、tick、图例
# 2. 调色板 — 色盲安全 6-8 色
# 3. 图尺寸:
#    single: (3.25, 2.5)    # 单栏
#    double: (7.0,  2.5)    # 双栏
#    full:   (7.0,  9.0)    # 整页
# 4. 图类型预设:
#    learning_curve()       # 学习曲线 + 误差带
#    bar_comparison()        # 柱状对比（自动高亮 Ours）
#    radar()                 # 雷达图
#    ablation_waterfall()    # 消融瀑布图
#    scatter_with_trend()    # 散点 + 回归线 + CI
# 5. 输出: PDF (矢量) + PNG (300 DPI) 双格式
```

### 紧扣 IDEA 的自动标注

- 图标题自动嵌入 `config.idea` 关键词
- 本方法曲线/柱子自动加粗 + 深色 + `\textbf{Ours}` 标注
- 消融图自动标注最大贡献组件（如 "Dropout contributes +2.3 F1"）
- 对比图显著性标注: `* p<0.05`, `** p<0.01`, `*** p<0.001`

---

## General Commands

| Command | Description |
|---------|-------------|
| `uv run experiment.py` | Run research experiment |
| `uv sync` | Install dependencies |

## Key Files

- `experiments/INDEX.yaml` - Global experiment index (do not delete)
- `templates/` - Visualization template presets
- `data/` - Raw and processed data (use DVC / Git LFS)
- `paper/` - LaTeX source and figures
- `scripts/` - Data preprocessing and plotting scripts

## Environment

Required:
- `PYTHONPATH` - Must include project root
- `WANDB_API_KEY` - (optional) For experiment tracking

## Gotchas

- `known_bias` in config.yaml is MANDATORY — if truly none, write "none" with a justification
- All figures must use English labels; Chinese characters in plots break most academic submission systems
- `vibe-exp archive` makes the experiment read-only — no further modifications allowed
- Raw data is immutable — always create processed copies, never overwrite originals

## Workflow

```text
IDEA → vibe-exp all → analyze results → iterate → archive → map to paper
   ↑________________________________________________________↓
                         迭代循环
```
