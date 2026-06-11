---
name: chinese-patent-drawer
description: |
  Generates patent figures specialized for Chinese patent applications. Uses omnidraw
  routing (drawio for structure/flow, matplotlib for data charts) with Chinese-patent-specific
  conventions: ALL in-figure text MUST be Chinese, SimSun/SimHei fonts, B&W only, captions
  outside image, strict size constraints (max 165mm×245mm, 72-300 DPI).
---

# 中国专利附图绘制 (Chinese Patent Drawer)

使用 omnidraw 系统生成符合中国专利申请规范的附图。所有图内文字必须使用中文。

## 何时使用

- 用户要求：画专利附图、生成专利图、绘制说明书附图
- 前提条件：需有附图清单（来自 `chinese-patent-plan` 或用户指定）
- 作为 `chinese-patent-pipeline` 的第二步
- 可独立使用：用户直接要求绘制特定的专利图

## 核心规则：中文文本要求

**所有附图内的标注文字必须使用中文。** 这是本技能的核心专业化。

允许例外：数学符号、SI 国际单位、国际通用技术缩写（CPU、API、USB、HTTP 等）。

完整规则见 `../rules/drawing-rules.md`。

## 工作流程

### Step 1: 获取附图清单
从专利规划文档（`chinese-patent-plan` 输出）或用户指令中提取所有附图需求。

### Step 2: 按图类型分发

使用 omnidraw 的路由规则（`../../omnidraw/SKILL.md`），将每张图分发到合适的工具：

| 图类型 | 工具 | 子技能路径 |
|--------|------|-----------|
| 结构示意图 | Draw.io | `../drawio/SKILL.md` |
| 方法流程图 | Draw.io | `../drawio/SKILL.md` |
| 电路/连接图 | Draw.io | `../drawio/SKILL.md` |
| 数据图/统计图 | Matplotlib | Python 脚本 |
| 系统架构图 | Draw.io | `../drawio/SKILL.md` |
| 模块关系图 | Draw.io | `../drawio/SKILL.md` |

### Step 3: 应用中文专利约束

在绘制每张图时，必须施加中文专利专用约束：

#### Draw.io 图（结构图/流程图/电路图）
1. **A-H 格式强化**：先将需求改写为 A-H 结构化绘图规格（参考 `../drawio/references/structured-diagram-prompts.md`）
2. **字体**：所有标签使用宋体 (SimSun) 或黑体 (SimHei)，15px
3. **中文标注**：每个模块、节点、连接线的标签必须以中文书写
4. **B&W**：纯黑白色调，不使用彩色
5. **走线**：正交连接线，圆角矩形模块
6. **禁止**：图中不包含图号（图1、图2等），不包含图注文字
7. **导出**：PNG 格式，300 DPI

A-H 格式中的标签示例（中文）：
```
E 模块节点：传感器采集模块 → 信号预处理模块 → 特征提取模块 → 分类决策模块
F 模块节点样式：rounded rectangle, black border, white fill, SimSun 15px
```

#### Matplotlib 图（数据图/统计图）
1. **中文字体配置**（必须在脚本开头设置）：
```python
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Noto Sans CJK SC']
plt.rcParams['axes.unicode_minus'] = False
```
2. **B&W 区分**：使用线型（实线/虚线/点线）和填充图案（斜线/交叉线/点阵）区分数据序列
3. **中文标签**：坐标轴标签、图例、标题全部使用中文
4. **输出**：PNG 格式，300 DPI

### Step 4: 尺寸与格式检查
- 每张图物理尺寸 ≤ 165mm × 245mm
- 分辨率 72-300 DPI（推荐 300 DPI）
- 保存为 `images/图N.png`

### Step 5: 生成后中文验证
对每张生成的图检查：
- [ ] 图中所有可见文字确为中文（允许的例外除外）
- [ ] 图中无图号（图1、图2等）渲染在像素内
- [ ] 图中无图注文字渲染在像素内
- [ ] B&W 合规（无彩色元素）

如有任何检查项不通过，修复后重新生成。

## Draw.io 中文专利图示例 Prompt

```
按照 A-H 格式，创建一张中文专利结构示意图：

A 图类型：专利结构示意图
B 领域：智能照明控制系统
C 模块数量：4
D 连接关系：传感器采集模块 → 信号预处理模块 → 特征提取模块 → 分类决策模块
E 模块节点：
  - 传感器采集模块：包含光照传感器、红外传感器、声音传感器
  - 信号预处理模块：包含滤波、放大、模数转换
  - 特征提取模块：包含时域特征、频域特征、统计特征
  - 分类决策模块：包含照明场景识别、开关控制信号输出
F 模块节点样式：rounded rectangle, SimSun 15px, black border, white fill
G 连接线样式：orthogonal, black, solid for data flow, dashed for control signal
H 布局：left to right, 4 columns, vertical center aligned

要求：图中所有文字必须为中文，不包含图号，不包含图注。
```

## Matplotlib 中文专利图示例

```python
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Noto Sans CJK SC']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(6, 4))

x = np.linspace(0, 10, 100)
# B&W 兼容：使用线型区分
ax.plot(x, np.sin(x), 'k-', linewidth=1.5, label='本发明方法')
ax.plot(x, np.sin(x - 0.5), 'k--', linewidth=1.5, label='现有技术A')
ax.plot(x, np.sin(x - 1.0), 'k-.', linewidth=1.5, label='现有技术B')

ax.set_xlabel('时间（秒）')
ax.set_ylabel('响应值')
ax.set_title('控制响应曲线对比')
ax.legend()

plt.tight_layout()
plt.savefig('images/图3.png', dpi=300, bbox_inches='tight')
print('Saved: images/图3.png')
```

## 注意事项

- 中文优先使用 SimSun（宋体）/SimHei（黑体），如有回退需要必须在生成后验证
- 如 drawio 的浏览器环境中没有 SimSun 字体，使用系统内置的 CJK 字体
- 如 matplotlib 环境中没有 SimHei 字体，安装 `fonts-noto-cjk` 或使用 `Noto Sans CJK SC`
- 可参考已有的 `../scripts/generate_figure_example.py` 了解 matplotlib 绘图模板结构
