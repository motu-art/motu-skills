---
name: motu-remove-watermark
description: Remove watermarks, logos, timestamps, and text overlays from images through the motu.art workflow API (api.motu.art, workflow remove_watermark) — inpaints the marked regions and returns a clean full-resolution image. Use this skill whenever the user asks to 去水印/去除水印/去掉logo/去LOGO/去掉图片上的文字/去字幕/去时间戳/图片修复干净版, clean up a watermark, remove a stamp/badge/text from an image, or get a clean version of a watermarked picture they own or are licensed to edit — or mentions motu watermark removal — even if they don't name the API.
---

# motu-remove-watermark

Remove watermarks and overlaid marks from images with the motu.art workflow API.
One workflow, one script: `scripts/motu_watermark.py` (stdlib-only Python 3, no dependencies).

**Use it only on images you own or are licensed to edit** — your own exports, AI generations
with baked-in platform marks, or stock/media your rights cover. Watermarks on others' work
are ownership signals; stripping them without a license isn't a supported use. If a user
supplies third-party material, confirm the right to edit before running.

## Quick start

API key comes from the `MOTU_KEY` env var (already defined in this repo's `.envrc` — run
`source .envrc` or use `direnv` first; never hardcode or echo the key).

```bash
source .envrc   # if MOTU_KEY isn't already in the environment

# Local file (uploaded automatically), output long edge 2048
python3 scripts/motu_watermark.py clean --image ./photo.png --long-side 2048 --out clean.png

# Already-hosted image
python3 scripts/motu_watermark.py clean --image-url https://example.com/photo.png
```

The script submits the job (API returns `202` + `workflow_request_id`), polls status every
5s, then downloads the cleaned png and prints a JSON summary (path, width/height).
Runs typically take 10–60 seconds.

Useful flags: `--dry-run` (print the request without spending quota), `--no-wait`,
`--seed N` (re-run the same image + seed for a different inpaint), `--priority urgent`,
`--callback-url`, `--timeout`. Check a running job with
`python3 scripts/motu_watermark.py status --request-id <uuid>`.

## Parameters

| Parameter | CLI flag | Default | Limits |
|---|---|---|---|
| `image_url` | `--image` / `--image-url` (required) | — | public URL; locals are uploaded automatically |
| `long_side` | `--long-side` | 1536 | 512–2048; output long edge in px |
| `seed` | `--seed` | 0 (random) | 0–10000000000000000 |

`long_side` controls output resolution. The default 1536 fits most web uses; use 2048 for
print or large displays. The output aspect ratio always matches the input image.

## Working practice

- Give the output a meaningful name (`--out product_clean.png`), and keep the original —
  the operation is generative inpainting, not a reversible edit.
- Large or busy marks: run once, inspect at 100% zoom where the mark was; if the fill looks
  smeared, rerun with a new `--seed` rather than stacking runs (re-cleaning an output
  compounds artifacts).
- Semi-transparent full-image diagonal watermarks (the repeated-tile kind) are the hardest
  case — expect some softening in those regions.
- The cleaned image works directly as a reference-image input (`image1`/`image2`) to the
  sibling `motu-minimax-h3` skill (ra2v).

## Troubleshooting

- `400 Invalid parameters` → `long_side` outside 512–2048, or a missing/unreadable image.
- `401/403` → `MOTU_KEY` missing or invalid; confirm `source .envrc` ran.
- `image_url` must be an `http(s)://` URL — base64 data URIs pass submit-time validation
  but the job fails silently during processing. Always route local files through the script.
- Full endpoint/response/auth details: `references/api.md`.
