# 源引用规范 (Source Grounding)

## 基本原则

所有知识输出必须可追溯回原始材料。这是 manifest 最核心的设计原则，也是保证知识准确性的关键。

## 引用格式

### 标准格式

```
[Source: 材料名, 位置标识]
```

### 按载体类型的格式

| 载体 | 引用格式 | 示例 |
|------|----------|------|
| PPT | `[Source: 文件名, P#]` | `[Source: ML-课件.pptx, P15]` |
| PDF | `[Source: 文件名, p页码]` | `[Source: 统计学习方法.pdf, p42]` |
| Video | `[Source: 文件名, HH:MM:SS]` | `[Source: Lecture5.mp4, 15:23]` |
| Web | `[Source: URL]` | `[Source: https://example.com/article]` |
| Audio | `[Source: 文件名, HH:MM:SS]` | `[Source: lesson3.mp3, 08:45]` |
| Image | `[Source: 文件名]` | `[Source: architecture-diagram.png]` |

## 多来源引用

当同一断言有多份材料支持时：

```
[Source: ML-课件.pptx, P15; 统计学习方法.pdf, p42-45]
```

## 置信度标记

| 标记 | 含义 | 说明 |
|------|------|------|
| （无标记） | 高置信度 | 直接来自源材料 |
| `[confidence: medium]` | 中等置信度 | 来自源材料的推断 |
| `[confidence: low]` | 低置信度 | AI 补充性解释 |
| `[unverified]` | 未验证 | 无源材料支撑，需要人工确认 |

## 禁止行为

- ❌ 编造不存在的来源引用
- ❌ 引用与内容不匹配的来源
- ❌ 删除或修改已有的 `[Source: ...]` 标记
- ❌ 将 AI 知识表示为材料内容

## 引用完整性检查

- `[Source: ...]` 引用的文件必须存在于 `materials/` 目录
- 每个 notes/ 下的笔记必须包含至少一个 source field
- Flashcard 必须标注来源
