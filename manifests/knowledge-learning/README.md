# Knowledge-Learning Manifest

多种知识载体格式的系统化学习 manifest。支持从 PPT、PDF、视频、网页、音频等格式的学习材料中提取知识，基于 NotebookLM 风格严格源引用模式，提供学习全流程管理。

## 快速开始

```bash
# 初始化学习项目
vibe init knowledge-learning my-learning-project

# 导入学习材料
cd my-learning-project
/import path/to/lecture.pptx
/import path/to/textbook.pdf
/import https://example.com/article

# 开始学习
/learn 机器学习

# 复习巩固
/flashcard 机器学习
/review

# 查看进度
/track
```

## 支持的载体类型

| 类型 | 格式 | 提取策略 |
|------|------|----------|
| PPT/幻灯片 | .ppt, .pptx, .key | 逐页提取 + 讲稿笔记 |
| PDF 文档 | .pdf | 分章节提取 + 核心概念 |
| 视频课程 | .mp4, .mov + 字幕 | 转录 → 时间分段 |
| 网页文章 | URL, .html | 正文提取 + 关键段落 |
| 音频 | .mp3, .wav | 转录 + 章节标记 |
| 习题/试卷 | .pdf, .docx | 题目解析 + 知识点映射 |
| 图片/图表 | .png, .jpg, .svg | OCR + 内容描述 |

## License

MIT
