# Executor Styles

执行器风格快速参考 —— 根据 `design_spec.md` 中的"设计风格"选择对应参考文件。

## 三种风格

| 风格 | 参考文件 | 适用场景 |
| :--- | :--- | :--- |
| **General（通用灵活）** | `skills/ppt-master/skills/ppt-master/references/executor-general.md` | 默认风格，适合大多数演示文稿 |
| **Consultant（咨询风格）** | `skills/ppt-master/skills/ppt-master/references/executor-consultant.md` | 商业咨询、战略报告、数据分析 |
| **Top Consultant（顶级咨询）** | `skills/ppt-master/skills/ppt-master/references/executor-consultant-top.md` | MBB 级别顶级咨询报告 |

## 通用规范（所有风格共用）

`skills/ppt-master/skills/ppt-master/references/executor-base.md` —— 定义所有执行器的通用 SVG 生成指南。

## 选择规则

- 如果 `design_spec.md` 中明确指定风格 → 使用对应参考文件
- 如果未指定 → 使用 **General** 风格
- 如果使用了预置布局模板 → 优先使用模板自带的 `design_spec.md` 中的风格
