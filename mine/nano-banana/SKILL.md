---
name: nano-banana
description: Image generation via fal-ai MCP using Nano Banana Pro v1 and v2 models. Create photos, illustrations, concept art, and more. Covers model selection (v1 vs v2), parameters (aspect ratio, inference steps, guidance scale), prompt techniques, and integration patterns via the globally configured fal-ai MCP server.
---

# Nano Banana Pro Image Generation

Image generation using Nano Banana Pro v1 and v2 models via the fal-ai MCP server. Zero additional setup — fal-ai MCP is already configured globally.

## When to Use

- Photo-realistic images and scenes
- Quick concept art and illustrations
- When you need fast, cost-effective image generation
- When working inside Claude Code (direct MCP integration)
- Batch image generation (v1 is faster for iterations)

**v1 vs v2 quick guide**:
- **v2**: Higher quality, better prompt adherence, more detailed. Use for final/deliverable images.
- **v1**: Faster, cheaper. Use for quick iterations, concept exploration, drafts.

## Model IDs

| Model | fal-ai ID | Best For |
|-------|-----------|----------|
| Nano Banana Pro v1 | `fal-ai/nano-banana-pro` | Fast iterations, concept drafts |
| Nano Banana Pro v2 | `fal-ai/nano-banana-pro-v2` | High quality, final deliverables |

## MCP Usage

The fal-ai MCP server is globally configured. Use its tools directly:

### Generate an Image

Describe what you want in natural language. The MCP server handles model selection and parameter mapping.

```
Generate a photo-realistic image of a modern minimalist living room with large windows, warm afternoon light, indoor plants, neutral color palette
```

```
Create an illustration: a futuristic city skyline at sunset, flying vehicles, neon lights, cyberpunk aesthetic, wide aspect ratio
```

### Parameters (via MCP tool arguments)

| Parameter | Values | Recommended |
|-----------|--------|-------------|
| `model` | `fal-ai/nano-banana-pro`, `fal-ai/nano-banana-pro-v2` | v2 for quality, v1 for speed |
| `aspect_ratio` | `1:1`, `16:9`, `9:16`, `4:3`, `3:4` | Match output destination |
| `num_inference_steps` | 20-50 | 28-36 (v2), 20-28 (v1) |
| `guidance_scale` | 1-20 | 7-9 (higher = more prompt adherence) |
| `num_images` | 1-4 | 1 for final, 2-4 for exploration |

### Aspect Ratio Selection

| Ratio | Use Case |
|-------|----------|
| `1:1` | Social media, avatars, square illustrations |
| `16:9` | Presentation slides, hero images, wide compositions |
| `9:16` | Mobile screenshots, portrait compositions |
| `4:3` | Traditional photos, general purpose |
| `3:4` | Portrait photos, book covers |

## Prompt Writing Guide

### Structure

```
[Subject] + [Environment/Context] + [Style/Medium] + [Lighting] + [Color] + [Quality boosters]
```

### v2 Prompt Template (Detailed)

```
[Main subject], [specific details about appearance], [environment/background context], [lighting type and direction], [color palette], [mood/atmosphere]. [Quality: highly detailed, sharp focus, professional composition]
```

### v1 Prompt Template (Concise)

```
[Subject], [style], [key details], [lighting mood]
```

### Quality Boosters (add to v2 prompts)

- "highly detailed, sharp focus"
- "professional lighting, 8k resolution"
- "cinematic composition, depth of field"
- "award-winning photography style"
- "masterpiece, best quality"

### Negative Prompt Elements

For the `negative_prompt` parameter:
- "blurry, low quality, distorted"
- "text, watermark, signature, logo"
- "ugly, deformed, extra limbs, bad anatomy"
- "grainy, noisy, oversaturated"

## v1 vs v2 Comparison

| Aspect | v1 | v2 |
|--------|----|----|
| Quality | Good | Excellent |
| Speed | Fast (2-5s) | Moderate (5-10s) |
| Prompt adherence | Moderate | Strong |
| Detail level | Good | Very high |
| Best for | Iteration, drafts | Final output |
| Cost | Lower | Higher |

## Workflow

### Exploration Phase
1. Start with v1 for quick iterations
2. Test 2-3 prompt variations
3. Adjust composition and style keywords

### Finalization Phase
1. Switch to v2 with the best prompt
2. Increase inference steps for more detail
3. Generate multiple variants and pick best
4. Export at desired resolution

## Limitations

- **No precise text rendering** — don't expect accurate text in images
- **No pixel-level control** — can't specify exact positions
- **Style consistency varies** — multiple images from same prompt may differ
- **Content policy** — follows fal-ai usage policies
- **No inpainting/outpainting** — full image generation only

## Templates

See [templates/nano-banana-prompts.md](./templates/nano-banana-prompts.md) for prompt templates organized by category (photo-realistic, illustration, architecture, nature, abstract, product/mockup).

## Related Skills

- [GPT-Image-2](../gpt-image-2/SKILL.md) — Alternative image generation via OpenAI API
- [Omnidraw Router](../omnidraw/SKILL.md) — Scenario-based tool dispatch
