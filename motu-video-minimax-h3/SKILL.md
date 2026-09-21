---
name: motu-video-minimax-h3
description: Generate videos through the motu.art MiniMax Hailuo H3 workflow API (api.motu.art) — text-to-video (video_minimax_h3_t2v), image-to-video (video_minimax_h3_i2v), image+audio-to-video lip-sync talking head (video_minimax_h3_ia2v), start/end-frame video (video_minimax_h3_r2v), and frames+audio-to-video (video_minimax_h3_ra2v). Use this skill whenever the user asks to 生成视频/做视频/图生视频/文生视频/首尾帧视频/数字人口播/对口型/唇形同步, animate an image, bring a picture to life, make a talking-head or lip-sync clip from a portrait and a voice track, interpolate between two frames, sync video to an audio track, or mentions motu/MiniMax/Hailuo video generation — even if they don't name the API. For videos longer than 15 seconds, or briefs that read like a multi-shot film (长视频/多镜头/分镜/广告片/宣传片/合并视频/拼接视频), follow the skill's shot-by-shot strategy: split into shots of ≤15 s each, generate per shot, merge into one complete video. Also use it to write or improve prompts for these video models.
---

# motu-video-minimax-h3

Generate videos with the motu.art workflow API (MiniMax Hailuo H3 model family).
Five workflows plus a `merge` command for stitching shots into one film — all in
`scripts/motu_video.py` (stdlib-only Python 3; `merge` additionally needs the
`ffmpeg`/`ffprobe` binaries).

## When to use which workflow

| Workflow | Alias | Use when | Required inputs |
|---|---|---|---|
| `video_minimax_h3_t2v` | t2v | 文生视频 — create a clip purely from a text idea | `prompt` |
| `video_minimax_h3_i2v` | i2v | 图生视频 — animate an existing image (product shot, portrait, keyframe) | `image_url` |
| `video_minimax_h3_ia2v` | ia2v | 数字人口播 — one portrait + one voice track → a fixed-camera talking-head whose lips follow the audio; the audio is copied 1:1 into the final video | `image_url` + `audio` (both technically optional, always send both) |
| `video_minimax_h3_r2v` | r2v | 首尾帧 — generate a transition between a start and an end frame | `image_start_url`, `image_end_url` |
| `video_minimax_h3_ra2v` | ra2v | 首尾帧+音频 — the most flexible: any combination of start frame, end frame and an audio track the video must follow | none (send what you have) |

Pick by inputs: no image & no audio → **t2v**. One image → **i2v**. One image + one audio
(talking head / 口播 / lip sync) → **ia2v**. Two images → **r2v**. Two images + audio, or
audio with at most one image → **ra2v**.

## Quick start

API key comes from the `MOTU_KEY` env var (already defined in this repo's `.envrc` — run
`source .envrc` or use `direnv` first; never hardcode or echo the key).

```bash
source .envrc   # if MOTU_KEY isn't already in the environment

# Text-to-video
python3 scripts/motu_video.py generate \
  --workflow t2v --prompt "..." --aspect-ratio 16:9 --duration 5 --out clip.mp4

# Image-to-video (local files are uploaded automatically)
python3 scripts/motu_video.py generate \
  --workflow i2v --image ./keyframe.png --prompt "..." --out clip.mp4

# Talking head: portrait + speech audio, lips driven by the audio
python3 scripts/motu_video.py generate \
  --workflow ia2v --image ./portrait.png --audio ./speech.mp3 --duration 6

# Start/end frame
python3 scripts/motu_video.py generate \
  --workflow r2v --image-start ./a.png --image-end ./b.png --prompt "..." --out clip.mp4

# Frames + audio
python3 scripts/motu_video.py generate \
  --workflow ra2v --image-start ./a.png --image-end ./b.png --audio ./voice.mp3

# Merge shots into one long film (see the long-form strategy below; needs ffmpeg)
python3 scripts/motu_video.py merge --out final.mp4 shot_01.mp4 shot_02.mp4 shot_03.mp4
```

The script submits the job (API returns `202` + `workflow_request_id`), polls status every
10s, then downloads the mp4 and prints a JSON summary (path, width/height, duration, file
size). Generation typically takes 1–5 minutes.

Useful flags: `--dry-run` (print the request without spending quota — use it to sanity-check
parameters), `--no-wait` (just queue), `--seed`, `--megapixels 0.2-1`, `--priority urgent`,
`--callback-url`, `--timeout`. Check a running job with
`python3 scripts/motu_video.py status --request-id <uuid>`.

## Parameters (all five workflows)

| Parameter | Type | Default | Limits |
|---|---|---|---|
| `prompt` | text | see below | max 6000 chars (ra2v: 8000) |
| `aspect_ratio` | select | t2v/r2v/ra2v: `16:9 (Widescreen)`; i2v: `1:1 (Square)`; ia2v: `3:4 (Portrait Standard)` | see allowed values |
| `megapixels` | number | 0.4 (ra2v: 0.7) | 0.2–1 |
| `duration` | number | 5 (ia2v: 6) | 3–15 seconds |
| `seed` | number | 0 (random) | 0–10000000000000000 |
| `filename_prefix` | text | "video" | t2v only |
| `image_url` | image | — | i2v/ia2v input |
| `image_start_url` / `image_end_url` | image | — | r2v (required) / ra2v (optional) frames |
| `audio` | audio | — | ia2v / ra2v input |

`prompt` is **required for t2v only** — but always write one anyway; an unprompted
generation gives the model free rein and the result rarely matches intent. The one
exception is ia2v with its built-in talking-head default prompt: sending no prompt is fine
there when the goal is exactly "make this portrait speak this audio".

**aspect_ratio must be the full label**, not a bare ratio. The script accepts bare `16:9`
and maps it, but if you call the API directly use exactly:
`1:1 (Square)`, `2:3 (Portrait Photo)`, `3:2 (Photo)`, `3:4 (Portrait Standard)`,
`4:3 (Standard)`, `9:16 (Portrait Widescreen)`, `16:9 (Widescreen)`.
For image-driven workflows, match the aspect ratio to the input image(s) unless you
deliberately want cropping.

Pick aspect ratio from the user's intent: 竖屏/手机/抖音/Reels → `9:16 (Portrait Widescreen)`;
横屏/宽屏/电影感 → `16:9 (Widescreen)`; 方图/社媒头像类 → `1:1 (Square)`;
口播/数字人半身像 → `3:4 (Portrait Standard)` or `9:16`.

## Writing the prompt — this is where quality comes from

The model responds best to a **structured, shot-by-shot brief in English**, not a one-line
description. Think of H3 as an AI film crew — director, DP, actor, sound recordist and
composer in one. A vague wish ("一个古装女孩在雨中奔跑，电影感") lets the crew improvise:
faces drift, the camera lurches without warning, costumes change color, dialogue drowns
under the score. An executable directing plan turns 随机抽卡 into 可控拍摄. Design every
generation with the **五步导演法**, layer by layer:

**选对模式 → 锁定角色 → 拆解动作 → 设计镜头 → 分离声音**

1. **Pick the task mode from the assets you hold — before writing anything.**
   没有素材 → t2v (free-form, highest drift risk; concepts, ambience and empty shots);
   有起点 → i2v (the prompt says what must stay identical to `<Picture 1>` and what
   happens next — not a re-description of the image); 有起点和终点 → r2v (describe the
   *in-between* as continuous action, not the two images); 只有结果 → **ra2v with only
   `--image-end`** (back-fill the action path that leads to the end frame:
   手碰杯沿→杯子倾斜→滑落→撞击→碎片静止); 要同时参考角色/动作/风格/声音 → ra2v
   multimodal (or ia2v for talking heads).
2. **Structure the prompt as three "crew departments"** — the official field format:
   `integrated_multimodal_description` (director + DP: style, shot size, subject,
   identity locks, sequential actions, camera moves, timestamped cuts, dialogue,
   on-screen text — negative constraints close this field), `overall_soundscape`
   (recordist: 1–4 sentences of ambience, action sounds and non-verbal human sounds —
   **never repeat dialogue here**), `non_diegetic_music` (score: 1–3 sentences naming
   instruments, tempo, volume dynamics and the ending — concrete mechanics, not abstract
   moods like "epic music"; write `N/A` when no score is wanted).
3. **Give every shot six elements: 风格＋景别＋主体＋动作＋镜头运动＋声音.** One primary
   camera movement per shot — stacking 推/摇/环绕/跟拍/变焦 keywords in one sentence makes
   them conflict. Camera movement is narrative, not decoration: pick the move that serves
   the beat (slow push-in emphasizes face or key object, pull-back shows subject–environment
   relation, pan reveals off-screen information, orbit signals arrival or power, static
   holds performance). Multi-shot prompts timestamp every cut, strictly increasing,
   covering the clip's `duration`.
4. **Lock identity, decompose actions.** Open reference-image prompts by declaring what
   stays invariant — facial features, hairstyle, costume style & color, props,
   accessories, body proportions, position, scene layout, lighting direction — then break
   complex actions into small observable steps (视线移向右侧 → 左手按住剑鞘 → 右手握住
   剑柄 → 身体转向右后方 → 剑刃逐渐拔出). Write change *paths*, not results ("火光从
   手臂向肩部扩散，衣袖逐渐转化为羽毛", never "she suddenly becomes a phoenix"). The more
   complex the action, the fewer simultaneous demands in that shot — never big movement +
   speech + camera move + scene change all at once.
5. **Layer dialogue, ambience and score.** Stable speaker IDs across shots (S1, S2…);
   define the voice at first appearance (age, gender, pitch, timbre, pace, accent/mood);
   write dialogue as `The young woman (S1), calm, low and slightly breathy, says at a
   measured pace: <d>[Chinese] 终于找到你了。</d>`; voice-overs must state that the
   on-screen person's lips stay closed (else the model lip-syncs the wrong character);
   the score ducks under dialogue ("music decreases in volume during the dialogue and
   gently rises after").

The official example prompts (a product film, an action trailer, a comic sequence, a
talking-head spec) express the same plan as a free-form skeleton — equivalent content in
prose shape:

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

Reference the inputs in the prompt: **`<Picture 1>`** (i2v/ia2v image; r2v/ra2v start frame),
**`<Picture 2>`** (r2v/ra2v end frame), **`<Audio 1>`** (ia2v/ra2v audio), e.g.
"The transparent gaming mouse from `<Picture 1>`… The scene opens exactly on image 1".
This anchors the model to the provided frames and audio.

Keep the shot list consistent with `duration`: a 5s clip fits 2–3 shots; 10s fits 4–5.
Don't cram 8 shots into 5 seconds.

For ia2v talking heads the official default prompt is a full structured spec
(`subject_definitions` / `summary` / `retention_analysis` / `detailed_description` /
`overall_soundscape`) that pins identity, camera lock and 1:1 audio copy — copy its
pattern when you need to customize. For the full guide — the 五步导演法 in detail
(mode-selection table, three-field structure, camera-movement narrative vocabulary
推/拉/摇/移/跟/环绕/升降/甩镜, consistency-constraint patterns, the ia2v spec, the
雨夜客栈 three-field worked example, the 六个高频翻车点 self-check, and the 万能提示词
模板), per-shot prompts for the long-form strategy, and the complete official example
prompts — read `references/prompting.md`.

## Long-form strategy: 按镜头拆解 → 逐镜生成 → 合并成片

A single generation caps at **15 s** (`duration` 3–15). Whenever the target video runs
longer than that, or the brief reads like a film rather than one clip (广告片 / 宣传片 /
剧情短片 / 多镜头), do NOT try to squeeze it into one job — always work shot-by-shot:

1. **Storyboard first (分镜拆解).** Decompose the brief into a shot list before generating
   anything. Each shot ≤ 15 s (the hard cap); 5–10 s per shot usually paces better than
   maxing out the limit. For every shot, write down: content, camera move, duration,
   workflow (t2v/i2v/r2v/… pick per shot from the inputs it has), and input assets.
   Name the outputs `shot_01.mp4`, `shot_02.mp4`, … in play order.
2. **Lock global settings.** Every shot must use the same `--aspect-ratio` and
   `--megapixels` — resolution follows them, and mixed values produce clips that can't be
   stream-copied together. Every shot's prompt opens with the same style-and-look sentence
   and ends with the same negative constraints, so the merged film holds one look. A
   shot's in-prompt timeline `[0s-Ns]` covers only that shot's own `duration`, never the
   whole film.
3. **Continuity: chain or cut.** For seamless continuation, feed the previous shot's last
   frame (the `cover_url` jpg in the API result) into the next shot as `--image` (i2v) or
   `--image-start` (r2v/ra2v), and write "continuing from the previous shot" in the
   prompt; chained shots must generate sequentially. For deliberate hard cuts, generate
   the shots independently — then submit them all with `--no-wait` and poll each
   `--request-id` so they run in parallel.
4. **Merge into the final film.**

   ```bash
   python3 scripts/motu_video.py merge --out final.mp4 shot_01.mp4 shot_02.mp4 shot_03.mp4
   ```

   When all clips match (same resolution, same audio/no-audio) it stream-copies —
   instant and lossless; otherwise it re-encodes to the first clip's format
   automatically. The command prints a JSON summary with the merged duration — report
   the file path and total duration.

If one shot fails or misses the mark, regenerate only that shot and re-run the merge —
the other shots are unaffected.

## After generation

- The mp4 URL is a signed OSS link valid **14 days** — always download it via the script
  rather than handing the user a bare URL.
- Report the local file path plus resolution/duration/size from the script's JSON output.
- If the result misses the mark, iterate on the prompt (more specific shots, stronger style
  anchors, explicit negatives) and rerun with the same `--seed` to isolate the prompt change,
  or a new seed for variety.
- The last frame of a video (`cover_url` in the API result) is a handy input image for a
  follow-up i2v run when chaining clips into a sequence.

## Troubleshooting

- `400 Invalid parameters` → usually aspect_ratio not a full label, or a value out of range;
  the `details` field names the offending parameter.
- `401/403` → `MOTU_KEY` missing or invalid; confirm `source .envrc` ran.
- Everything is async: a successful submit returns `202` with only a `workflow_request_id`;
  results appear later via polling (script default timeout 30 min) or `--callback-url`.
- `image_url`/`image_start_url`/`image_end_url`/`audio` must be `http(s)://` URLs — base64
  data URIs pass submit-time validation but the job fails silently during processing.
  Always route local files through the script's upload.
- A job that ends `failed` returns no error detail from any endpoint. First retry with the
  defaults (especially `megapixels 0.4`) before changing anything else — pushing megapixels
  to 1 has been observed to fail silently.
- `merge` needs `ffmpeg`/`ffprobe` on PATH (macOS: `brew install ffmpeg`). It falls back
  from stream-copy to re-encoding automatically when clips mismatch; if you see it
  re-encode, the shots were probably generated with different aspect ratios or
  megapixels — regenerate the odd one out rather than accepting a scaled merge.
- Full endpoint/response/auth details: `references/api.md`.
