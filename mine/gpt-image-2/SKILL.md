---
name: gpt-image-2
description: Image generation via OpenAI GPT-Image-2 / DALL-E 3 API. Create illustrations, concept art, photo-realistic images, diagrams, logos, and icons. Covers prompt structure, parameters (size/quality/style), cost estimation, and error handling. Requires OPENAI_API_KEY.
---

# GPT-Image-2 / DALL-E 3 Image Generation

Generate images via OpenAI's image generation API (GPT-Image-2 / DALL-E 3). Requires an OpenAI API key.

## When to Use

- Illustrations and concept art
- Photo-realistic images from text descriptions
- Logo and icon generation
- Visual concept exploration
- Storyboarding and mood boards
- Abstract/non-technical visual generation
- When detailed prompt following matters (DALL-E 3 excels at this)

**Not ideal for**: pixel-precise diagrams (use [Draw.io](../drawio/SKILL.md)), text-heavy output, rendering specific fonts. For faster/cheaper alternatives, consider [Nano Banana Pro](../nano-banana/SKILL.md) via fal-ai MCP.

## Setup

```bash
export OPENAI_API_KEY="sk-..."
```

## API Reference

**Endpoint**: `POST https://api.openai.com/v1/images/generations`

### Request

```json
{
    "model": "dall-e-3",
    "prompt": "A watercolor illustration of a fox reading a book under a tree, soft lighting, storybook style",
    "n": 1,
    "size": "1024x1024",
    "quality": "standard",
    "style": "vivid"
}
```

### Parameters

| Parameter | Values | Notes |
|-----------|--------|-------|
| `model` | `dall-e-3`, `dall-e-2` | DALL-E 3 is strongly recommended |
| `prompt` | string, max 4000 chars | Detailed prompts yield better results |
| `n` | 1 (DALL-E 3), 1-10 (DALL-E 2) | DALL-E 3 only supports n=1 |
| `size` | `1024x1024`, `1792x1024`, `1024x1792` | Only for DALL-E 3 |
| `quality` | `standard`, `hd` | `hd` costs 2x; better detail |
| `style` | `vivid`, `natural` | `vivid` = hyper-real/dramatic; `natural` = subdued |
| `response_format` | `url`, `b64_json` | Default `url` (1-hour expiry) |

### Response

```json
{
    "created": 1717000000,
    "data": [
        {
            "revised_prompt": "...",
            "url": "https://oaidalleapiprodscus.blob.core.windows.net/..."
        }
    ]
}
```

## Cost

| Model | Quality | Size | Cost per Image |
|-------|---------|------|---------------|
| DALL-E 3 | standard | 1024×1024 | $0.040 |
| DALL-E 3 | standard | 1024×1792 / 1792×1024 | $0.080 |
| DALL-E 3 | hd | 1024×1024 | $0.080 |
| DALL-E 3 | hd | 1024×1792 / 1792×1024 | $0.120 |
| DALL-E 2 | — | 1024×1024 | $0.020 |
| DALL-E 2 | — | 512×512 | $0.018 |
| DALL-E 2 | — | 256×256 | $0.016 |

## Prompt Writing Guide

### Structure

```
[Subject] + [Style/Medium] + [Composition] + [Lighting] + [Color palette] + [Mood]
```

### Prompt Template

```
A [medium/style] of [main subject], [composition details], [lighting description], [color scheme], [mood/atmosphere]. [Additional constraints: no text, clean background, etc.]
```

### Style Keywords

| Category | Keywords |
|----------|----------|
| Medium | oil painting, watercolor, digital art, 3D render, pencil sketch, vector illustration, pixel art |
| Photography | cinematic, portrait, macro, wide-angle, aerial, studio lighting, golden hour |
| Art style | art nouveau, cyberpunk, minimalist, baroque, vaporwave, ukiyo-e, art deco |
| Mood | serene, dramatic, mysterious, playful, melancholic, epic, cozy |
| Color | pastel, vibrant, monochromatic, muted, neon, earth tones, jewel tones |

### Good vs Bad Prompts

**Bad**: "Draw a cat"
**Good**: "A fluffy orange tabby cat sitting on a windowsill, rain streaming down the glass, warm lamp light from inside, cozy melancholic mood, soft focus, cinematic composition, natural color palette"

## Limitations

- **No text rendering**: DALL-E 3 struggles with accurate text in images
- **No precise layout control**: Cannot specify exact positions like "put X at (300, 200)"
- **URL expires in 1 hour**: Download images promptly
- **Content policy**: NSFW, violence, public figures, and copyrighted styles are blocked
- **Rate limits**: Varies by tier; typically 5-50 images/min
- **Single image per request**: DALL-E 3 only supports n=1

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 401 | Invalid API key | Check `OPENAI_API_KEY` env var |
| 429 | Rate limited | Wait and retry with backoff |
| 400 | Content policy violation | Revise prompt; remove blocked terms |
| 500 | Server error | Retry after 30 seconds |

## Templates

See [templates/gpt-image-prompts.md](./templates/gpt-image-prompts.md) for prompt templates organized by image category (illustration, concept art, photo-realistic, logo, icon, diagram).
