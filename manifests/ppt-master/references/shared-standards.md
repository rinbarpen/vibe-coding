# Shared Standards (技术约束速查)

完整版见 `skills/ppt-master/skills/ppt-master/references/shared-standards.md`

## 禁止使用的 SVG 特性

| 特性 | 原因 |
| :--- | :--- |
| `rgba()` | python-pptx 不解析，使用 `rgb()` + `opacity` |
| `<style>` | Office 渲染器忽略 |
| `class` | Office 渲染器忽略 |
| `foreignObject` | 不被 PowerPoint 支持 |
| `textPath` | 不被 PowerPoint 支持 |
| `@font-face` | Office 忽略，使用系统字体 |
| `<animate*>` | PPTX 不支持 SMIL 动画 |
| `<script>` | 安全风险 + 不支持 |
| `<g opacity>` | Office 兼容性问题，使用叠加层 |

## 字体栈

必须使用操作系统安全字体：
- **中文优先**: `"Microsoft YaHei", "微软雅黑", "SimHei", "黑体", sans-serif`
- **英文优先**: `Arial, Helvetica, sans-serif`
- **等宽**: `"Courier New", monospace`

## 图片嵌入规则

- 图片标签: `<image href="图片路径" x="x" y="y" width="w" height="h"/>`
- 路径使用项目相对路径（如 `images/photo.png`）
- 透明度通过蒙版层实现：在图片上叠加 `<rect fill="背景色" opacity="0.x"/>`
