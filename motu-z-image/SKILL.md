---
name: motu-z-image
description: Generate high-quality 2K images through the motu.art Z-Image Turbo workflow API (api.motu.art, workflow z_image_turbo_2k) — photos, portraits, product shots, e-commerce images, posters, scenes, characters, logos, UI concepts, and multi-image series. Use this skill whenever the user asks to 生成图片/画图/画一张/生成一张图/做图/生成2K图/高清图/超清图/做海报/做封面/做插画/生成壁纸/套图/系列图/一组图, generate an image, create a high-resolution 2K picture, a portrait, product photo, scene, character, poster, or a set of related images — or mentions motu/Z-Image image generation — even if they don't name the API. Distinctive workflow: match the request to an intent template, design and verify a full structured prompt per image (one at a time), then submit. For images whose main point is readable rendered text (exact-wording logos, typography posters), prefer the sibling motu-ideogram4 skill.
---

# motu-z-image

Generate images with the motu.art workflow API (Z-Image Turbo 2K model).
One workflow, one script: `scripts/motu_z_image.py` (stdlib-only Python 3, no
dependencies).

Z-Image Turbo's strengths: fast (~15 s) **2K-class output** (the returned png is ~2× the
requested canvas — 768×1024 → 1536×2048) and strong response to **structured comma-group
prompts** — the model follows a well-ordered field list (subject → pose → camera → lighting
→ grading) much more faithfully than a loose sentence, which is what makes
"生成结果最大程度符合意图" achievable.

## Workflow: 意图 → 模板 → 校验 → 逐张提交

Every request — single image or set — follows the same four steps:

1. **判意图** — identify the generation intent from the user's request, then read the
   matching template in `references/templates/` (routing table:
   `references/templates/index.md`; 17 intents: character, portrait, people-scene,
   product, ecommerce, food, automotive, scene, architecture, poster, hero-image, social,
   logo, ui, infographic, comic, series). A brief mixing intents
   (「一套 3 张：产品图 + 场景图 + 海报」) splits into one task per image.
2. **选模板** — the template file gives the fill-in checklist, the Z-Image prompt
   skeleton, and a complete worked example.
3. **填充** — fill the user's specifics into the skeleton. Fields the user didn't
   specify get designed deliberately (template defaults) — never left empty; an empty
   field is the model improvising.
4. **校验后提交** — run the eight-dimension check
   (Subject / Identity / Action / Environment / Composition / Lighting / Style /
   Constraint — table in `references/prompting.md`), confirm the canvas matches the
   destination, quoted text is exact, ≤ 6000 chars — then submit. For a multi-image
   job, show the user the per-image prompt list (titles + one line each) for
   confirmation unless they asked to proceed autonomously, and **repeat these steps
   image by image** — each image gets its own designed-and-verified prompt.

## Quick start

API key comes from the `MOTU_KEY` env var (already defined in this repo's `.envrc` — run
`source .envrc` or use `direnv` first; never hardcode or echo the key).

```bash
source .envrc   # if MOTU_KEY isn't already in the environment

# One designed prompt → one image (portrait preset, 3:4 → 1536x2048 png)
python3 scripts/motu_z_image.py generate \
  --prompt 'title: ..., A ... portrait featuring ..., <structured field groups>' \
  --size portrait --out outputs/founder_portrait.png

# A set of N images: repeat per image, each with its own designed prompt
```

The script submits the job (API returns `202` + `workflow_request_id`), polls status
every 5 s, downloads the png(s) and prints a JSON summary (paths, width/height).
Generation typically takes 10–30 s.

Useful flags: `--dry-run` (print the request without spending quota), `--no-wait`,
`--seed N`, `--priority urgent`, `--timeout`. Check a running job with
`python3 scripts/motu_z_image.py status --request-id <uuid>`.

## Parameters

| Parameter | CLI flag | Default | Limits |
|---|---|---|---|
| `prompt` | `--prompt` (required) | — | max 6000 chars |
| `width` / `height` | `--width` / `--height` or `--size` | 768 × 1024 (portrait) | 512–1024 each side; composition canvas — output is ~2× |
| `batch_size` | `--batch-size` | 1 | 1–4 picks from the **same** prompt |
| `seed` | `--seed` | 0 (random) | 0–10000000000000000 |

Size presets: `square` 1024×1024 · `portrait` 768×1024 (3:4) · `landscape` 1024×768 ·
`story` 672×1008 (2:3) · `banner` 1024×576 (16:9). Match the canvas to the destination:
竖屏/手机壁纸/小红书竖图 → `portrait` or `story`; 公众号头图/横幅/网页 hero → `banner`
or `landscape`; 头像/方图/社媒方图 → `square`. Don't inflate width/height hoping for
more detail — resolution is fixed at ~2× canvas; pick the canvas for framing.

## Writing the prompt

Z-Image Turbo responds best to the **structured comma-group format** — a single
comma-separated sequence of field groups in a fixed order:

`title: <短标题> → 一句话总述 → 氛围关键词 → 环境 → 道具 → 配色 → 主体身份 → 主体细节组
（人物：姿势/脸型/表情/发型/妆容/服装；产品：结构/状态/摆放/材质）→ 相机（焦段/光圈/ISO/
快门/白平衡）→ 景别与构图 → 景深 → 主光（`position:`/`intensity:`）→ 辅光（`ratio:`）→
光感 → 风格 → 调色（`contrast:`/`saturation:`）→ 叙事句 → 情绪词`

Core rules — **写事实关系，不写抽象评价**（"left floor-to-ceiling windows, central
8-person table", not "高级震撼"); **先画什么，再怎么画，最后不画什么**; one group one
job; attributes as `key: value`; on-image text in double quotes; exclusions phrased
positively near the end (`no watermark, no extra fingers`). Full field-group table,
the eight-dimension pre-submit check, and the 单图工作流: `references/prompting.md`.

**Always start from the intent template** (`references/templates/<intent>.md`) — it has
the domain skeleton, checklist, and a ready worked example; adapt the example rather
than writing from zero.

## Multiple images — 逐张操作

- **逐张设计**：each image goes through intent-matching → template → fill → verify on
  its own. Never batch-copy one prompt with minor edits. Give each output a distinct
  `--out` name (`outputs/look_01.png`, `outputs/look_02.png`, …).
- **一致性（套图）**：when a character/product/style must hold across images, write a
  MASTER block (identity, outfit, props, style, palette — verbatim in every prompt) and
  vary only scene/action/shot per image — `references/templates/series.md`. The MASTER
  block is worth confirming with the user before generating the whole set.
- **`--batch-size` is not 逐张**: it produces picks from one identical prompt — use it
  only for 「同一张再给我几张备选」.

## After generation

- The png URL is a signed OSS link valid **14 days** — always download via the script
  rather than handing the user a bare URL.
- Report local file paths plus actual width/height from the JSON output (~2× the
  requested canvas is expected).
- If a result misses the intent, fix the prompt (tighter facts, stronger anchors,
  explicit exclusions) and rerun with the same `--seed` to isolate the change; new seed
  for variety. Regenerate only the missed image — the others are unaffected.
- Generated images work directly as inputs to sibling skills: `motu-video-minimax-h3`
  (i2v / r2v frames) and `motu-remove-watermark`.
- Text-bearing deliverables (exact-wording logos, typography posters): Z-Image can
  render short quoted text, but `motu-ideogram4` is the stronger choice — switch skills.

## Troubleshooting

- `400` → width/height outside 512–1024, prompt over 6000 chars, batch_size outside
  1–4; the `details` field names the offending parameter.
- `401/403` → `MOTU_KEY` missing or invalid; confirm `source .envrc` ran.
- Everything is async: a successful submit returns `202` with only a
  `workflow_request_id`; results arrive via polling (script default timeout 15 min).
- A job that ends `failed` returns no error detail from any endpoint. Retry once with
  defaults before changing parameters.
- Full endpoint/response/auth details: `references/api.md`.
