# vibe-export

将内容导出为指定格式。

## Usage

```
vibe-export --file <path> --format <fmt> [options]
```

### Options

| 选项 | 描述 |
|------|------|
| `--file <path>` | 内容文件（必需） |
| `--format <fmt>` | 导出格式：`md`、`pdf`、`html`、`docx` |
| `--stylesheet <path>` | 自定义 CSS 样式（HTML/PDF 用） |
| `--metadata <json>` | 元数据（标题、作者、日期） |
| `--output <path>` | 输出路径 |

## 导出格式

| 格式 | 用途 | 依赖 |
|------|------|------|
| `md` | Markdown 通用格式 | 无 |
| `html` | 网页发布/公众号复制 | 可选 CSS |
| `pdf` | 打印/存档 | `weasyprint` 或 `pandoc` |
| `docx` | Word 文档 | `pandoc` |

## Examples

```bash
# 导出为 HTML
vibe-export --file content/polished.md --format html --output publish/article.html

# 导出为 PDF
vibe-export --file content/polished.md --format pdf --output publish/article.pdf
```

## Notes

- Markdown 是默认格式，所有草稿都先用 Markdown 编写
- HTML 导出自带基础样式，可自定义 CSS 覆盖
- PDF 导出依赖 pandoc，首次使用需安装