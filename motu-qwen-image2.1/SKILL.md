---
name: motu-qwen-image2-1
description: Generate images through the motu.art Qwen Image 2.1 workflow API (api.motu.art, workflow image_qwen_image_2_1_t2i) — strongest-in-class on-image Chinese and English text rendering plus native 512–2048 canvases, for posters, packaging, signage, UI concepts, e-commerce images, portraits, product shots, scenes, characters, and multi-image series. Use this skill whenever the user asks to 生成图片/画图/画一张/生成一张图/做图/做海报/做封面/生成带文字的图/中文文字海报/招牌/包装文字/菜单图/UI 界面图/横幅图/套图/系列图/一组图, generate an image whose main point is rendered text (headline, wordmark, label, UI copy), a high-resolution 2048-class picture, or a set of related images — or mentions motu/Qwen image generation — even if they don't name the API. Distinctive workflow: match the request to an intent template, design and verify a full English prose prompt per image (one at a time), then submit. For text-free images where speed matters prefer motu-z-image; for pure Latin-letterform logo design prefer motu-ideogram4.
---

# motu-qwen-image2-1

Generate images with the motu.art workflow API (Qwen Image 2.1 model).
One workflow, one script: `scripts/motu_qwen_image.py` (stdlib-only Python 3, no
dependencies).

Qwen Image 2.1's strengths: **the strongest on-image Chinese + English text
rendering** among the motu image skills (live-verified: a Chinese headline + spaced
subline rendered character-perfect, including interpuncts) — text-bearing posters,
packaging, signage, UI copy belong here; **native 512–2048 canvases** returned at
exactly the requested resolution (2048-class detail without an upscaler); and strong
response to **natural-language English prose prompts** — one flowing paragraph of
ordered facts (subject → action → environment → light → camera → style → negative
closer) beats a tag list, which is what makes "生成结果最大程度符合意图" achievable.
Generation typically takes ~30 s (queue spikes to ~10 min happen; script waits up to
15 min by default).

## Workflow: 意图 → 模板 → 校验 → 逐张提交

Every request — single image or set — follows the same four steps:

1. **判意图** — identify the generation intent from the user's request, then read the
   matching template in `references/templates/` (routing table:
   `references/templates/index.md`; 17 intents: character, portrait, people-scene,
   product, ecommerce, food, automotive, scene, architecture, poster, hero-image, social,
   logo, ui, infographic, comic, series). A brief mixing intents
   （「一套 3 张：产品图 + 场景图 + 海报」） splits into one task per image.
2. **选模板** — the template file gives the fill-in checklist, the Qwen prose
   skeleton, and a complete worked example.
3. **填充** — fill the user's specifics into the skeleton. Fields the user didn't
   specify get designed deliberately (template defaults) — never left empty; an empty
   field is the model improvising.
4. **校验后提交** — run the eight-dimension check
   (Subject / Identity / Action / Environment / Composition / Lighting / Style /
   Constraint — table in `references/prompting.md`), confirm the canvas matches the
   destination, quoted text is exact, ≤ 6000 chars, the `Absolutely no …` closer is
   present — then submit. For a multi-image job, show the user the per-image prompt
   list (titles + one line each) for confirmation unless they asked to proceed
   autonomously, and **repeat these steps image by image** — each image gets its own
   designed-and-verified prompt.

## Quick start

API key comes from the `MOTU_KEY` env var (already defined in this repo's `.envrc` — run
`source .envrc` or use `direnv` first; never hardcode or echo the key).

```bash
source .envrc   # if MOTU_KEY isn't already in the environment

# One designed prompt → one image (portrait preset, exact 1024x1536 png)
python3 scripts/motu_qwen_image.py generate \
  --prompt 'A commercial poster for a Chinese tea shop. Large headline text "秋日茶集" at the top center in elegant serif calligraphy, <…prose facts…> Absolutely no other text, no watermark.' \
  --size portrait --out outputs/tea_poster.png

# A set of N images: repeat per image, each with its own designed prompt
```

The script submits the job (API returns `202` + `workflow_request_id`), polls status
every 5 s, downloads the png(s) and prints a JSON summary (paths, width/height).

Useful flags: `--dry-run` (print the request without spending quota), `--no-wait`,
`--seed N`, `--priority urgent`, `--timeout`. Check a running job with
`python3 scripts/motu_qwen_image.py status --request-id <uuid>`.

## Parameters

| Parameter | CLI flag | Default | Limits |
|---|---|---|---|
| `prompt` | `--prompt` (required) | — | max 6000 chars |
| `width` / `height` | `--width` / `--height` or `--size` | 1024 × 1024 (square) | 512–2048 each side; **output is exactly the requested size** |
| `batch_size` | `--batch-size` | 1 | 1–4 picks from the **same** prompt |
| `seed` | `--seed` | 0 (random) | 0–10000000000000000 |

Size presets: `square` 1024×1024 · `portrait` 1024×1536 (2:3) · `landscape` 1536×1024 ·
`story` 1152×2048 (9:16) · `banner` 2048×1152 (16:9) · `square-2k` 2048×2048 ·
`portrait-2k` 1536×2048 · `landscape-2k` 2048×1536. Match the canvas to the destination:
竖屏/手机壁纸/小红书竖图 → `portrait` or `story`; 公众号头图/横幅/网页 hero → `banner`
or `landscape`; 头像/方图/社媒方图 → `square`. Unlike z-image there is no hidden 2× —
the png comes back at exactly the requested canvas, so pick the real target resolution
(2k presets when detail matters).

## Writing the prompt

Qwen Image 2.1 responds best to a **natural-language English prose paragraph** — the
official default prompt is exactly that (see `references/api.md`). One flowing text,
5–9 sentences, ordered:

`<这是什么图（媒介+主体+场景）> → <主体身份与特征> → <动作/服饰/材质细节> → <环境与背景层次>
→ <空间关系与构图/视觉层级> → <光线（源+方向+性质+效果）> → <镜头与景深> → <风格与配色>
→ <画面文字（引号+位置+字体气质，如有）> → <Absolutely no … 负面收尾句>`

Core rules — **写事实关系，不写抽象评价**（"a walnut conference table for eight at
the center, floor-to-ceiling windows on the left", not "高级震撼"); **先画什么，再怎么
画，最后不画什么**; merge adjacent fields into sentences, never `key: value`
attributes; on-image text in double quotes, spelled exactly, kept short (one headline +
one subline is the sweet spot; Qwen gets Chinese right where other models garble it);
exclusions as the canonical final sentence (`Absolutely no text, no typography, no
letters, no words, no numbers, no logos, no watermark, no captions, pure imagery only.`
— tailored when the image does carry text). Full skeleton, fold rules, the
eight-dimension pre-submit check, and the 单图工作流: `references/prompting.md`.

**Always start from the intent template** (`references/templates/<intent>.md`) — it has
the domain skeleton, checklist, and a ready worked example; adapt the example rather
than writing from zero.

## Multiple images — 逐张操作

- **逐张设计**：each image goes through intent-matching → template → fill → verify on
  its own. Never batch-copy one prompt with minor edits. Give each output a distinct
  `--out` name (`outputs/look_01.png`, `outputs/look_02.png`, …).
- **一致性（套图）**：when a character/product/style must hold across images, write a
  MASTER block of fixed prose sentences (identity, outfit, props, style, palette —
  verbatim in every prompt) and vary only the scene/action/light sentence per image —
  `references/templates/series.md`. The MASTER block is worth confirming with the user
  before generating the whole set.
- **`--batch-size` is not 逐张**: it produces picks from one identical prompt — use it
  only for 「同一张再给我几张备选」.

## After generation

- The png URL is a signed OSS link valid **14 days** — always download via the script
  rather than handing the user a bare URL.
- Report local file paths plus actual width/height from the JSON output (they equal the
  requested canvas exactly).
- If a result misses the intent, fix the prompt (tighter facts, stronger anchors,
  explicit exclusions) and rerun with the same `--seed` to isolate the change; new seed
  for variety. Regenerate only the missed image — the others are unaffected.
- Generated images work directly as inputs to sibling skills: `motu-video-minimax-h3`
  (i2v / r2v frames) and `motu-remove-watermark`.
- Text-bearing images are this skill's home turf (Chinese included). Pure Latin
  letterform logo design: `motu-ideogram4`. Fast text-free 2K: `motu-z-image`.

## Troubleshooting

- `400` → width/height outside 512–2048, prompt over 6000 chars, batch_size outside
  1–4; the `details` field names the offending parameter.
- `401/403` → `MOTU_KEY` missing or invalid; confirm `source .envrc` ran.
- Everything is async: a successful submit returns `202` with only a
  `workflow_request_id`; results arrive via polling (script default timeout 15 min —
  long queue spikes do happen; `--status` re-checks, `--timeout` extends).
- `504` from nginx on submit → gateway congestion, not a bad request; retry the same
  payload after a short wait.
- A job that ends `failed` returns no error detail from any endpoint. Retry once with
  defaults before changing parameters.
- Full endpoint/response/auth details: `references/api.md`.
