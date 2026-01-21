# 图像生成与创意设计 Prompt 库

本库提供用于 AI 图像生成（Midjourney, Stable Diffusion, DALL-E）以及创意设计的结构化 Prompt。

## 1. 图像生成提示词模板 (Image Generation)

### 摄影纪实风格 (Photorealistic)
> **Prompt**: [Subject], close up shot, photorealistic, cinematic lighting, 8k resolution, highly detailed skin texture, captured on Sony A7R IV, 85mm lens, f/1.8 --ar 16:9 --v 6.0
> 
> **中文说明**: [主体]，近景，写实风格，电影感光效，8K 分辨率，极致细节，索尼 A7R IV 拍摄，85mm 镜头。

### 艺术与插画 (Artistic & Illustration)
> **Prompt**: [Subject] in the style of [Artist Name/Style, e.g., Studio Ghibli, Van Gogh, Cyberpunk], vibrant colors, intricate details, ethereal atmosphere, masterpiece --ar 3:4
> 
> **中文说明**: [主体]，[某种艺术风格]，色彩鲜艳，细节丰富，空灵氛围，杰作。

### 工业与 3D 设计 (Industrial & 3D Design)
> **Prompt**: [Subject/Product], 3D render, Octane render, minimalist, sleek design, matte finish, soft studio lighting, high-end material, 4k, trending on ArtStation
> 
> **中文说明**: [主体/产品]，3D 渲染，Octane 渲染器，极简主义，流畅设计，哑光质感，柔和影棚光。

---

## 2. 创意构思与设计思维 (Conceptual Design)

### 品牌视觉头脑风暴
> **Prompt**: 我正在为一家 `[行业，如：可持续时尚]` 品牌进行视觉设计。
> 1. 请根据品牌核心价值 `[关键词1, 关键词2]`，提供 3 组不同的配色方案（包含 Hex 代码）。
> 2. 建议适合该品牌的字体组合（标题 + 正文）。
> 3. 构思 3 个代表性的 Logo 视觉元素。

### UI 界面概念设计
> **Prompt**: 为 `[应用类型，如：冥想 App]` 设计一个主界面。
> 1. 采用 `[风格，如：Neumorphism, Glassmorphism, Material Design]`。
> 2. 描述页面的核心层级结构。
> 3. 详细说明色彩、投影和间距的使用，以传达 `[情感，如：宁静、高效]`。

---

## 3. 提示词工程工具 (Prompt Engineering Tools)

### 负向提示词优化 (Negative Prompts)
> **Prompt**: 针对我提供的提示词，生成一个对应的负向提示词 (Negative Prompt)，以过滤掉常见的 AI 瑕疵（如：多出的手指、扭曲的肢体、低分辨率）。
> 
> **我的提示词**: `[输入提示词]`

### Midjourney 参数助手
> **Prompt**: 我想要生成一张 `[描述]` 的图片。
> 请帮我生成 3 个不同参数组合的 Midjourney 指令，分别侧重于：
> 1. 极致的写实细节 (High Stylization)。
> 2. 原始摄影感 (Raw Style)。
> 3. 不同的纵横比适配 (Aspect Ratios)。
