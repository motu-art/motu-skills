---
name: motu-qwen-image2-1
description: Generate and edit images through the motu.art Qwen Image 2.1 workflow API (api.motu.art, workflows image_qwen_image_2_1_t2i / image_qwen_image_2_1_image_edit) — strongest-in-class on-image Chinese and English text rendering plus native 512–2048 canvases, for posters, packaging, signage, UI concepts, e-commerce images, portraits, product shots, scenes, characters, and multi-image series, plus reference-image editing with 1–8 input images (换装/换背景/风格迁移/多图合成/局部修改). Use this skill whenever the user asks to 生成图片/画图/画一张/生成一张图/做图/做海报/做封面/生成带文字的图/中文文字海报/招牌/包装文字/菜单图/UI 界面图/横幅图/套图/系列图/一组图, 改图/编辑图片/把这张图…/参考这张图/换上/抠图换背景/保持人物不变, generate an image whose main point is rendered text (headline, wordmark, label, UI copy), edit or restyle an existing image, a high-resolution 2048-class picture, or a set of related images — or mentions motu/Qwen image generation — even if they don't name the API. Distinctive workflow: match the request to an intent template, design and verify a full English prose prompt per image (one at a time), then submit. For text-free images where speed matters prefer motu-z-image.
---

# motu-qwen-image2-1

Generate and edit images with the motu.art workflow API (Qwen Image 2.1 model).
Two workflows, one script: `scripts/motu_qwen_image.py` (stdlib-only Python 3;
reference-image compression uses macOS `sips`).

Qwen Image 2.1's strengths: **the strongest on-image Chinese + English text
rendering** among the motu image skills (live-verified: a Chinese headline + spaced
subline rendered character-perfect, including interpuncts) — text-bearing posters,
packaging, signage, UI copy belong here; **native 512–2048 canvases** returned at
exactly the requested resolution (2048-class detail without an upscaler); **multi-
reference editing** (1–8 images, `image_qwen_image_2_1_image_edit`) for 换装/换背
景/风格迁移/多图合成/局部修改 with identity preserved; and strong response to
**natural-language English prose prompts** — one flowing paragraph of ordered facts
(subject → action → environment → light → camera → style → negative closer) beats
a tag list, which is what makes "生成结果最大程度符合意图" achievable.
Generation typically takes ~30 s (queue spikes to ~10 min happen; script waits up to
15 min by default).

## Workflow: 意图 → 模板 → 填充 → 自审 → 自动提交

Every request — single image or set — follows the same four steps, **fully
autonomously (零确认)**: once the user submits a task, never pause to confirm
anything — identify, design, self-review, submit, then report with the final
prompts and the design assumptions made. Only ask the user when a blocking gap
**cannot** be designed around (a legally required real brand name / a user-owned
asset that wasn't provided, or self-contradictory requirements) — and even then
prefer finishing what can be done under the most reasonable assumption and
flagging it in the report over waiting mid-flow. The template checklists are
design guidance for the skill itself, never a questionnaire for the user.

1. **判意图** — identify the generation intent from the user's request: if they
   provided existing image(s) to modify （改图/换装/换背景/参考图合成）, it's an
   **edit** task — go to the 参考图编辑 section below; otherwise read the
   matching template in `references/templates/` (routing table:
   `references/templates/index.md`; 24 intents: character, portrait, people-scene,
   product, ecommerce, food, automotive, jewelry, fashion, animal, landscape, scene,
   architecture, poster, bookcover, hero-image, social, logo, ui, infographic, comic,
   illustration, mockup, series). A brief mixing intents
   （「一套 3 张：产品图 + 场景图 + 海报」） splits into one task per image.
2. **选模板** — the template file gives the fill-in checklist, the Qwen prose
   skeleton, and a complete worked example. Pull concrete vocabulary (lighting,
   camera, style, color, material) from `references/vocabulary.md`.
3. **填充** — fill the user's specifics into the skeleton. Fields the user didn't
   specify get designed deliberately (template defaults) — never left empty; an empty
   field is the model improvising.
4. **自审后自动提交** — mechanical lint first: write the prompt to a file and run
   `python3 scripts/prompt_check.py --prompt-file p.txt` (errors → fix → re-lint),
   then the eight-dimension check (Subject / Identity / Action / Environment /
   Composition / Lighting / Style / Constraint — table in
   `references/prompting.md`), confirm the canvas matches the destination, quoted
   text is exact, and the `Absolutely no …` closer is present — then **submit
   immediately, no confirmation round-trip**. For a multi-image job, **repeat these
   steps image by image** — each image gets its own designed-and-verified prompt,
   submitted as it passes review.

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

## 参考图编辑（edit）

When the user provides existing image(s) to transform — 换装、换背景、风格迁移、
多图合成、保持人物/产品不变的局部修改 — use the `edit` subcommand (workflow
`image_qwen_image_2_1_image_edit`, 1–8 reference images):

```bash
python3 scripts/motu_qwen_image.py edit \
  --image person.png --image shirt.png \
  --prompt 'Keep the character and pose in <image1> unchanged, put the light blue denim shirt from <image2> on the character, preserve the original facial features, hair, body shape and pose, the shirt fits naturally, realistic fabric texture, keep the original background and lighting. Absolutely no text, no watermark.' \
  --size portrait --out outputs/edited.png
```

- `--image` is repeatable; **order maps to `<image1>`…`<image8>`** in the prompt.
  Always reference each image explicitly by that tag — say what to keep from one
  image and what to take from another (the API's own default prompt is exactly this
  pattern; see `references/api.md`).
- Local files are **compressed automatically before upload**: the edit canvas tops
  out at 2048px, so the long edge is capped at 2048 (proportional, downscale-only)
  and anything still over 10 MB is re-encoded JPEG q85 — submit the best size, not
  the biggest file. http(s) URLs pass through untouched. base64 data URIs are never
  used (they fail silently in processing); locals always go through the OSS presign
  route.
- Everything else (canvas presets, batch, seed, polling, download) is identical to
  `generate`. The output canvas is independent of the input image sizes — pick
  `--size`/`--width/--height` for the destination, not the source.

## Parameters

| Parameter | CLI flag | Default | Limits |
|---|---|---|---|
| `prompt` | `--prompt` (required) | — | max 6000 chars |
| `width` / `height` | `--width` / `--height` or `--size` | 1024 × 1024 (square) | 512–2048 each side; **output is exactly the requested size** |
| `batch_size` | `--batch-size` | 1 | 1–4 picks from the **same** prompt |
| `seed` | `--seed` | 0 (random) | 0–10000000000000000 |
| `image1`…`image8` | `--image` (edit only, repeatable) | — | 1–8 reference images; locals auto-compressed (≤2048 long edge, ≤10 MB) then OSS-uploaded |

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
  `references/templates/series.md`. Design the MASTER block yourself (no confirmation
  pause); show it with its rationale in the final report so the user can request a
  redo if desired.
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
- Generated images work directly as inputs to sibling skills: `motu-minimax-h3`
  (ra2v reference images) and `motu-remove-watermark`.
- Text-bearing images are this skill's home turf (Chinese included).
  Fast text-free 2K: `motu-z-image`.

## Troubleshooting

- `400` → width/height outside 512–2048, prompt over 6000 chars, batch_size outside
  1–4; the `details` field names the offending parameter.
- `401/403` → `MOTU_KEY` missing or invalid; confirm `source .envrc` ran.
- Everything is async: a successful submit returns `202` with only a
  `workflow_request_id`; results arrive via polling (script default timeout 15 min —
  long queue spikes do happen; the `status` subcommand re-checks, `--timeout` extends).
- `504` from nginx on submit → gateway congestion, not a bad request; retry the same
  payload after a short wait.
- A job that ends `failed` returns no error detail from any endpoint. Retry once with
  defaults before changing parameters. **Exception**: `image_edit` was live-verified
  failing for every payload shape on 2026-09-28 (backend outage, t2i unaffected —
  see `references/api.md`); if edit jobs keep failing, treat it as a platform issue
  (wait/report), don't keep tweaking the request.
- Full endpoint/response/auth details: `references/api.md`.
