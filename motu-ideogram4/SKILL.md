---
name: motu-ideogram4
description: Generate images through the motu.art Ideogram 4 workflow API (api.motu.art, workflow ideogram4) — photos, illustrations, logos, posters, UI mockups, and especially images containing readable text/typography. Use this skill whenever the user asks to 生成图片/画图/画一张/生成一张图/做海报/做logo/做封面/做插画/生成插画/生成壁纸/文字海报/带文字的图片, generate an image, create a poster, illustration, icon, banner, thumbnail, logo concept, social media visual, or any picture with rendered text — or mentions motu/Ideogram image generation — even if they don't name the API. Also use it to write or improve image prompts.
---

# motu-ideogram4

Generate images with the motu.art workflow API (Ideogram 4 model).
One workflow, one script: `scripts/motu_image.py` (stdlib-only Python 3, no dependencies).

Ideogram 4's standout strength is **rendering readable text inside images** — posters,
logos, packaging, UI, signage. Reach for it by default when the user wants words in the
picture; it also handles photorealistic and illustrative work well.

## Quick start

API key comes from the `MOTU_KEY` env var (already defined in this repo's `.envrc` — run
`source .envrc` or use `direnv` first; never hardcode or echo the key).

```bash
source .envrc   # if MOTU_KEY isn't already in the environment

# Poster with rendered text (square)
python3 scripts/motu_image.py generate \
  --prompt 'Bold travel poster of Mount Fuji at dawn, flat vector style, \
large clean sans-serif headline text "JAPAN" at the top' \
  --size square --out poster.png

# Landscape photo
python3 scripts/motu_image.py generate \
  --prompt "..." --size landscape --out photo.png
```

The script submits the job (API returns `202` + `workflow_request_id`), polls status every
5s, then downloads the png and prints a JSON summary (path, width/height). Images typically
take 10–60 seconds.

Useful flags: `--dry-run` (print the request without spending quota), `--no-wait`,
`--seed N`, `--cfg`, `--temperature`, `--priority urgent`, `--callback-url`, `--timeout`.
Check a running job with `python3 scripts/motu_image.py status --request-id <uuid>`.

## Parameters

| Parameter | CLI flag | Default | Limits |
|---|---|---|---|
| `prompt` | `--prompt` (required) | — | max 6000 chars |
| `width` / `height` | `--width` / `--height` or `--size` | 768 × 1376 (portrait) | 512–1536 each side |
| `cfg` | `--cfg` | 2 | 1–7; higher = follows the prompt more strictly |
| `temperature` | `--temperature` | 0.3 | 0–1; higher = more varied |
| `seed` | `--seed` | 0 (random) | 0–10000000000000000 |
| `model` | `--model` | `gpt-4.1` | only allowed value; rarely needed |

Size presets: `square` 1024×1024 · `portrait` 768×1376 · `landscape` 1376×768 ·
`story` 896×1344 (2:3 vertical) · `banner` 1344×576. Match the canvas to the destination:
竖屏/手机壁纸/海报 → `portrait` or `story`; 横屏/头图/封面 → `landscape` or `banner`;
头像/方图 → `square`.

Pick aspect from the user's intent: 手机壁纸/竖版海报 → vertical; 公众号头图/Banner →
`banner`; 小红书/Instagram → `square` or `story`.

## Writing the prompt

Ideogram responds best to a **concrete visual brief**: subject, setting, style, composition,
color, and — when text should appear — the exact text in quotes.

1. **Subject & scene** — what it is and where it sits ("a ceramic pour-over coffee set on
   a sunlit wooden table").
2. **Style & medium** — "flat vector illustration", "editorial photography, 50mm lens",
   "risograph print", "3D render, soft studio light". One style anchor, not five.
3. **Composition** — where things sit ("centered, generous negative space",
   "close-up macro", "top-down flat lay").
4. **Text in quotes** — put every rendered string in double quotes and say where it goes:
   `headline text "SPRING SALE" across the top in bold condensed sans-serif`. Keep on-screen
   text short (a title, 3–5 words); long copy tends to develop typos.
5. **Negative constraints** — Ideogram has no negative-prompt field; phrase exclusions
   positively in the prompt ("empty background, no people").

Reproducibility: same `--seed` + same prompt → same image family; iterate the prompt with
the seed fixed to see exactly what changed, or drop the seed for variety. If outputs feel
literal, raise `--temperature` a little; if they drift off-brief, raise `--cfg`.

## After generation

- The png URL is a signed OSS link valid **14 days** — always download it via the script
  rather than handing the user a bare URL.
- Report the local file path plus the actual width/height from the script's JSON output
  (verify it matches what you requested).
- Generated images work directly as inputs to the sibling skills: `motu-video-minimax-h3`
  (animate with i2v / use as r2v frames) and `motu-remove-watermark`.
- For text-heavy images, inspect the result for typos before delivering; rerun with a fixed
  seed and a tightened text spec if needed.

## Troubleshooting

- `400 Invalid parameters` → width/height outside 512–1536, prompt over 6000 chars, or
  cfg/temperature out of range; the `details` field names the offending parameter.
- `401/403` → `MOTU_KEY` missing or invalid; confirm `source .envrc` ran.
- Text renders garbled → shorten the quoted copy, name the typeface category, and increase
  size contrast between text and background.
- Full endpoint/response/auth details: `references/api.md`.
