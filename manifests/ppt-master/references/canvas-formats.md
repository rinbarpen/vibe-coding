# Canvas Formats

快速参考 —— 完整文档见 `skills/ppt-master/skills/ppt-master/references/canvas-formats.md`

## 常用画布格式

| 别名 | 名称 | viewBox | 尺寸 | 用途 |
| :--- | :--- | :--- | :--- | :--- |
| `ppt169` | PPT 16:9 | `0 0 1280 720` | 1280×720 | 标准宽屏演示文稿 |
| `ppt43` | PPT 4:3 | `0 0 1024 768` | 1024×768 | 传统标屏演示文稿 |
| `xhs` | 小红书 | `0 0 1242 1660` | 1242×1660 | 小红书图文笔记 |
| `wechat` | 微信文章 | `0 0 900 383` | 900×383 | 微信公众号封面 |
| `story` | 竖版故事 | `0 0 1080 1920` | 1080×1920 | 竖屏演示/故事 |

## 使用方式

```bash
# 初始化时指定格式
python3 skills/ppt-master/skills/ppt-master/scripts/project_manager.py init <name> --format ppt169
```
