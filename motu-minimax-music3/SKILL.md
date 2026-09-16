---
name: motu-minimax-music3
description: Generate music through the motu.art MiniMax Music 3 workflow API (api.motu.art, workflow audio_minimax_music_3) — instrumental tracks and full songs with vocals from a style brief plus optional lyrics. Use this skill whenever the user asks to 生成音乐/做一段音乐/写歌/作曲/编曲/配乐/背景音乐/BGM/主题曲/片头曲/音效氛围/哼一段旋律做成歌, generate a soundtrack, jingle, lo-fi beat, podcast intro, video background music, custom song with lyrics, or mentions motu/MiniMax Music generation — even if they don't name the API. Also use it to write or improve the music style brief (caption) and lyrics.
---

# motu-minimax-music3

Generate complete music tracks with the motu.art workflow API (MiniMax Music 3 model).
One workflow, one script: `scripts/motu_music.py` (stdlib-only Python 3, no dependencies).

## Model in one paragraph

Two inputs drive a generation. **`caption`** is the music brief — genre, mood,
instrumentation, tempo, arrangement; this is where quality comes from. **`lyrics`** is the
text to be sung; omit it and state "fully instrumental, no vocals" in the caption to get a
pure instrumental. `max_duration` caps the length in seconds (default 240, max 360). Same
seed + same inputs → reproducible output. The API is async: submit, poll, download an mp3.

## Quick start

API key comes from the `MOTU_KEY` env var (already defined in this repo's `.envrc` — run
`source .envrc` or use `direnv` first; never hardcode or echo the key).

```bash
source .envrc   # if MOTU_KEY isn't already in the environment

# Instrumental BGM — 90 seconds, lo-fi
python3 scripts/motu_music.py generate \
  --caption "Lo-fi hip hop, warm and sleepy. Soft electric piano, muted jazz guitar, \
brushed drums, vinyl crackle, sub-bass. 75 bpm, 4-bar loop feel, no vocals, no melody peaks." \
  --max-duration 90 --out bgm.mp3

# Song with vocals — lyrics from a file
python3 scripts/motu_music.py generate \
  --caption "Acoustic pop, heartfelt female vocal, fingerpicked guitar, light strings, 92 bpm" \
  --lyrics-file lyrics.txt --out song.mp3
```

The script submits the job (API returns `202` + `workflow_request_id`), polls status every
10s, then downloads the mp3 and prints a JSON summary (path, duration). A full-length track
typically takes 1–3 minutes to generate.

Useful flags: `--dry-run` (print the request without spending quota), `--no-wait`,
`--seed N`, `--priority urgent`, `--callback-url`, `--timeout`. Check a running job with
`python3 scripts/motu_music.py status --request-id <uuid>`.

## Parameters

| Parameter | CLI flag | Required | Default | Limits |
|---|---|---|---|---|
| `caption` | `--caption` / `--caption-file` | recommended | built-in default brief | max 6000 chars |
| `lyrics` | `--lyrics` / `--lyrics-file` | no | — | max 6000 chars |
| `max_duration` | `--max-duration` | no | 240 | max 360 (seconds) |
| `seed` | `--seed` | no | 0 (random) | 0–10000000000000000 |

Always send a caption — with no caption and no lyrics the platform falls back to its
built-in default brief (a children's instrumental piece), which is almost never what the
user wants.

## Writing the caption — this is where quality comes from

Music 3 responds best to a **structured brief in English**, mirroring how the official
example is written:

1. **Global metadata** — genre families, overall mood/atmosphere, tempo feel
   ("relaxed to moderately upbeat"), emotional arc ("from peaceful curiosity into bright,
   carefree happiness"), and the scene it should evoke.
2. **Sonic palette** — core instrumentation, what to avoid ("no heavy drums, aggressive
   percussion, dense electronic textures"), space and density ("plenty of open space
   between notes").
3. **Vocal details** — for instrumentals, one explicit line: *"Fully instrumental with no
   vocals, spoken words, chants, or vocal samples."* For songs, describe the voice
   (gender, register, delivery) here and put the words in `lyrics`.
4. **Arrangement** — how the track develops section by section (Intro → Main Theme →
   Development → Bright Section → Outro), naming which instrument leads each section.

The complete official example caption (a children's summer instrumental, ~500 words) is in
`references/prompting.md` — use it as the style template.

For lyrics, structure text with section markers (`[Verse]`, `[Chorus]`, `[Bridge]`) on
separate lines; the model follows them. Line count should match `max_duration` — as a rule
of thumb one line eats roughly 3–5 seconds, so ~40 lines for a 180s pop song.

## After generation

- The mp3 URL is a signed OSS link valid **14 days** — always download it via the script
  rather than handing the user a bare URL.
- Report the local file path and the real duration from the script's JSON output (tracks
  often come back shorter than `max_duration` — the model ends when the arrangement ends).
- To iterate: rerun with the same `--seed` and an edited caption to hear exactly what the
  edit changed, or a new seed for a different take of the same brief.
- Generated audio works directly as the `audio` input of the motu-video-minimax-h3 skill
  (ra2v/ia2v) when scoring a video.

## Troubleshooting

- `400 Invalid parameters` → caption/lyrics over 6000 chars, or `max_duration` > 360.
- `401/403` → `MOTU_KEY` missing or invalid; confirm `source .envrc` ran.
- Vocals appear in an instrumental → strengthen the vocal-details line: "no vocals, spoken
  words, chants, humming, or vocal samples of any kind".
- Track much shorter than `max_duration` → that's the arrangement ending naturally; lengthen
  the arrangement description (more sections) rather than only raising `max_duration`.
- Full endpoint/response/auth details: `references/api.md`.
