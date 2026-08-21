---
name: motu-video-h3
description: Generate videos through the internal motu.art MiniMax Hailuo H3 workflow API (api.motu.art) — text-to-video (video_minimax_h3_t2v), image-to-video (video_minimax_h3_i2v), and start/end-frame video (video_minimax_h3_r2v). Use this skill whenever the user asks to 生成视频/做视频/图生视频/文生视频/首尾帧视频, animate an image, bring a picture to life, create a video clip from a prompt, interpolate between two frames, or mentions motu/MiniMax/Hailuo video generation — even if they don't name the API. Also use it to write or improve prompts for these video models.
---

# motu-video-h3

Generate videos with the internal motu.art workflow API (MiniMax Hailuo H3 model family).
Three workflows, one script: `scripts/motu_video.py` (stdlib-only Python 3, no dependencies).

## When to use which workflow

| Workflow | Use when | Required inputs |
|---|---|---|
| `video_minimax_h3_t2v` | 文生视频 — create a clip purely from a text idea | `prompt` |
| `video_minimax_h3_i2v` | 图生视频 — animate an existing image (product shot, portrait, keyframe) | `image_url` |
| `video_minimax_h3_r2v` | 首尾帧 — generate a transition between a start and an end frame | `image_start_url`, `image_end_url` |

If the user gives one image → i2v. Two images (start + end) → r2v. No image → t2v.

## Quick start

API key comes from the `MOTU_API_KEY` env var (already defined in this repo's `.envrc` — run
`source .envrc` or use `direnv` first; never hardcode or echo the key).

```bash
source .envrc   # if MOTU_API_KEY isn't already in the environment

# Text-to-video
python3 scripts/motu_video.py generate \
  --workflow video_minimax_h3_t2v \
  --prompt "..." --aspect-ratio 16:9 --duration 5 --out clip.mp4

# Image-to-video (local files are uploaded automatically)
python3 scripts/motu_video.py generate \
  --workflow video_minimax_h3_i2v \
  --image ./keyframe.png --prompt "..." --out clip.mp4

# Start/end frame
python3 scripts/motu_video.py generate \
  --workflow video_minimax_h3_r2v \
  --image-start ./a.png --image-end ./b.png --prompt "..." --out clip.mp4
```

The script submits the job (API returns `202` + `workflow_request_id`), polls
`GET /workflow/status` every 10s, then downloads the mp4 and prints a JSON summary
(path, width/height, duration, file size). Generation typically takes 1–5 minutes.

Useful flags: `--dry-run` (print the request without spending quota — use it to sanity-check
parameters), `--no-wait` (just queue), `--seed`, `--megapixels 0.2-1`, `--priority urgent`,
`--callback-url`, `--timeout`. Check a running job with
`python3 scripts/motu_video.py status --request-id <uuid>`.

## Parameters (all three workflows)

| Parameter | Type | Default | Limits |
|---|---|---|---|
| `prompt` | text | see below | max 6000 chars |
| `aspect_ratio` | select | t2v/r2v: `16:9 (Widescreen)`; i2v: `1:1 (Square)` | see allowed values |
| `megapixels` | number | 0.4 | 0.2–1 |
| `duration` | number | 5 | 3–15 seconds |
| `seed` | number | 0 (random) | 0–10000000000000000 |
| `filename_prefix` | text | "video" | t2v only |

`prompt` is **required for t2v, optional for i2v/r2v** — but always write one anyway;
an unprompted i2v/r2v gives the model free rein and the result rarely matches intent.

**aspect_ratio must be the full label**, not a bare ratio. The script accepts bare `16:9`
and maps it, but if you call the API directly use exactly:
`1:1 (Square)`, `2:3 (Portrait Photo)`, `3:2 (Photo)`, `3:4 (Portrait Standard)`,
`4:3 (Standard)`, `9:16 (Portrait Widescreen)`, `16:9 (Widescreen)`.
For i2v/r2v, match the aspect ratio to the input image(s) unless you deliberately want cropping.

Pick aspect ratio from the user's intent: 竖屏/手机/抖音/Reels → `9:16 (Portrait Widescreen)`;
横屏/宽屏/电影感 → `16:9 (Widescreen)`; 方图/社媒头像类 → `1:1 (Square)`.

## Writing the prompt — this is where quality comes from

The model responds best to a **structured, shot-by-shot brief in English**, not a one-line
description. The three official example prompts (a product film, an action trailer, a comic
sequence) all follow the same skeleton:

1. **Style & look** — one opening sentence: medium, lighting, palette, lens/texture
   ("Realistic live-action cinematic look, anamorphic lens, shallow depth of field, film grain…").
2. **Scene overview** — what happens across the whole clip, in 1–2 sentences.
3. **Shot list with timestamps** — `[0s-2.5s] Shot 1: …`, `[2.5s-5s] Shot 2: …` covering the
   full `duration`. One camera setup per shot; cuts are clean and land on beats.
4. **Camera** — overall movement/editing notes ("each shot its own angle, hard cuts, no dissolves").
5. **Audio** — ambience, score, accent hits, ending ("the score bursting at 4s, closing the last 1s").
6. **Negative constraints** — end with exclusions: "No text, subtitles, logos or watermarks,
   no animation or cartoon rendering, keep the live-action texture." (Adapt per style —
   a comic-style clip obviously shouldn't ban cartoon rendering.)

Reference the input images in the prompt with **`<Picture 1>`** (i2v image / r2v start frame)
and **`<Picture 2>`** (r2v end frame), e.g. "The transparent gaming mouse from `<Picture 1>`…
The scene opens exactly on image 1". This anchors the model to the provided frames.

Keep the shot list consistent with `duration`: a 5s clip fits 2–3 shots; 10s fits 4–5.
Don't cram 8 shots into 5 seconds.

For the full guide — camera-movement vocabulary (推/拉/摇/移/跟/环绕/升降/甩镜), MiniMax's
官方公式, and the three complete official example prompts — read `references/prompting.md`.

## After generation

- The mp4 URL is a signed OSS link valid **14 days** — always download it via the script
  rather than handing the user a bare URL.
- Report the local file path plus resolution/duration/size from the script's JSON output.
- If the result misses the mark, iterate on the prompt (more specific shots, stronger style
  anchors, explicit negatives) and rerun with the same `--seed` to isolate the prompt change,
  or a new seed for variety.

## Troubleshooting

- `400 Invalid parameters` → usually aspect_ratio not a full label, or a value out of range;
  the `details` field names the offending parameter.
- `401/403` → `MOTU_API_KEY` missing or invalid; confirm `source .envrc` ran.
- Everything is async: a successful submit returns `202` with only a `workflow_request_id`;
  results appear later via polling (script default timeout 30 min) or `--callback-url`.
- `image_url`/`image_start_url`/`image_end_url` must be `http(s)://` URLs — base64 data URIs
  pass submit-time validation but the job fails silently during processing (verified).
  Always route local files through the script's upload.
- A job that ends `failed` returns no error detail from any endpoint. First retry with the
  defaults (especially `megapixels 0.4`) before changing anything else — pushing megapixels
  to 1 has been observed to fail silently.
- Full endpoint/response/auth details: `references/api.md`.
