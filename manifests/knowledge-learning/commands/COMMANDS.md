# Knowledge-Learning Commands

Complete command index for the knowledge-learning manifest.

## Commands

| Command | Description | Subagent | Strict Mode |
|---------|-------------|----------|-------------|
| `/import <path/url>` | 导入学习材料，自动识别载体类型并提取知识 | material-processor | 自动拆解为 source-grounded 原子笔记 |
| `/learn <topic>` | 基于已有材料启动结构化学习会话 | curriculum-designer + note-architect | 每个结论引用源材料 |
| `/review [topic]` | SM-2 间隔重复复习 | review-master | 复习时标注原始出处 |
| `/flashcard <topic>` | 从学习材料生成闪卡 | review-master | 每卡标注 `[Source: 材料名, 页码]` |
| `/mindmap <topic>` | 基于学习材料生成知识图谱 | note-architect | 节点标注材料来源 |
| `/study <material>` | 针对特定材料的专项学习 | material-processor | 严格绑定到单个材料 |
| `/exam <topic>` | 生成试卷/习题，支持难度和知识点配置 | exam-generator | 每道题标注 `[Source: ...]` |
| `/diagram <concept>` | 生成图表（流程图/思维导图/对比图等） | note-architect | 图表内容基于源材料 |
| `/track [scope]` | 学习进度追踪与报告 | curriculum-designer | — |

## Subagent Dispatch

| Agent | Trigger | Effect |
|-------|---------|--------|
| material-processor | `/import`, `/study` | 按载体类型提取知识 |
| note-architect | `/learn`, `/mindmap`, `/diagram` | 笔记结构化、图表生成与连接 |
| review-master | `/review`, `/flashcard` | SM-2 调度与复习管理 |
| exam-generator | `/exam` | 试卷生成、难度配置、知识点覆盖率检查 |
| curriculum-designer | `/learn`, `/track` | 学习路径与进度设计 |

## Execution Priority

Command dispatch follows this order:
1. Parse the command and identify topic/material
2. Check `STRICT_SOURCE_MODE` and `NOTEBOOKLM_ENGINE` settings
3. Detect domain/carrier type of the topic
4. Activate the appropriate subagent
5. Execute command logic with source-grounding rules
