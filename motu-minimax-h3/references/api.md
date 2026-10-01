# motu.art Workflow API — reference (workflow set per minimax_h3_api.md, 2026-10;
# all three workflow names and the status routes re-verified against the live API 2026-10-01)

Base URL: `https://api.motu.art`
Auth: `Authorization: Bearer $MOTU_KEY` on every request.
(Kong gateway rejects Python's default urllib User-Agent — the bundled script sends a custom UA.)

The MiniMax H3 family exposes **three workflows**: `video_minimax_h3_t2v`,
`video_minimax_h3_ra2v`, and `video_minimax_h3_fun_controlnet_union`. The old
i2v / ia2v / r2v workflows are gone — their use cases (animate one image,
talking head, start/end frames) are all covered by `ra2v`'s reference inputs
(`image1`/`image2`/`audio1`/`audio2`).

## Submit a workflow

```
POST /workflows/{workflow_name}
Content-Type: application/json

{ ...parameters... }
```

Response `202 Accepted`:
```json
{"status": "queued", "workflow_request_id": "4e116851-e9e3-485e-9012-a77f6b1813dc"}
```

The response contains **only** the request id — results never come back in the submit call.

Common parameters accepted on top of the workflow-specific ones:

| Parameter | Effect |
|---|---|
| `callback_url` | On completion the platform POSTs `{workflow_request_id, status, urls: [...]}` to this URL |
| `priority` | `"urgent"` or `"default"` — urgent jobs go to a separate queue |

Errors:
- `400 {"error": "Missing required parameter: X"}`
- `400 {"error": "Invalid parameters", "details": {"param": "reason"}}` — e.g. aspect_ratio not a full label
- `401 {"error": "API key is missing"}` / `403 {"error": "Invalid API key"}`
- `404 {"error": "Workflow X not found"}`
- Unmatched paths return `500 {"message": "Failed to retrieve API cost"}` (a catch-all — treat as "route doesn't exist").

## Poll for status / result

```
GET /workflows/status/{workflow_request_id}
Authorization: Bearer $MOTU_KEY
```

(As of 2026-10-01 this documented path form is NOT deployed yet — it returns the
Kong catch-all `500 {"message": "Failed to retrieve API cost"}`. The live route is
still the legacy `GET /workflow/status?workflow_request_id={id}`. The bundled script
tries the documented form first and falls back to the legacy form, remembering
whichever returns 200.)

While running:
```json
{"workflow_request_id": "...", "status": "queued"}
```
(`processing` while the worker is on it; `failed`/`error` on failure.)

On completion the same endpoint includes `result`:
```json
{
  "status": "completed",
  "workflow_request_id": "...",
  "result": [
    {
      "url": "https://motu-generated.oss-cn-hangzhou.aliyuncs.com/{request_id}/1?OSSAccessKeyId=...&Signature=...",
      "cover_url": ".../1/first_frame.jpg?...",
      "width": 608, "height": 352,
      "duration": 3.041667, "file_size": 104649
    }
  ]
}
```

`url` is the mp4 (note: no `.mp4` extension in the path — save it with one locally).
`cover_url` is the video's last frame as jpg, handy as a poster frame or as the input
image for a follow-up ra2v run.
Signed OSS URLs expire after **14 days** — download promptly.

## Upload a local file (images, audio, and control videos)

`image1` / `image2` / `audio1` / `audio2` / `video1` must be publicly reachable
`http(s)://` URLs. Base64 data URIs pass submit-time validation (202) but the job
fails silently during processing — always upload locals through the OSS presign
route:

```
POST /oss/presigned-url
Authorization: Bearer $MOTU_KEY
Content-Type: application/json

{"fileType": "image/png"}
```
→
```json
{"uploadUrl": "https://...PUT-signed...", "key": "uploads/2026/08/21/...", "url": "https://...GET-signed-14d..."}
```

Then `PUT` the raw file bytes to `uploadUrl` with the **exact same `Content-Type`** you sent
as `fileType` (the signature covers it), and use the returned `url` as the workflow input.
`scripts/motu_video.py upload --file x.png` and the `--image1`/`--image2`/`--audio1`/`--audio2`/`--video1`
flags do this automatically (control videos included).

## Workflow parameter sheets

### video_minimax_h3_t2v — text-to-video

| Param | Required | Default | Notes |
|---|---|---|---|
| `prompt` | yes | — | max 6000 chars |
| `steps` | no | 8 | sampling steps, 4–8 |
| `filename_prefix` | no | `video` | |
| `aspect_ratio` | no | `16:9 (Widescreen)` | full labels only |
| `megapixels` | no | 0.4 | 0.2–1 |
| `duration` | no | 5 | 3–15 s |
| `seed` | no | 0 | 0–10000000000000000 |

### video_minimax_h3_ra2v — reference images + audio to video

The multimodal workhorse: any combination of up to two reference images and up
to two audio tracks. One image = animate a picture (old i2v); image + audio =
talking head / lip sync (old ia2v); two images = start/end frame transition
(old r2v); two images + audio = the original ra2v.

| Param | Required | Default | Notes |
|---|---|---|---|
| `image1` | no | — | referenced as `<Picture 1>` in prompt |
| `image2` | no | — | referenced as `<Picture 2>` in prompt |
| `audio1` | no | — | referenced as `<Audio 1>` in prompt |
| `audio2` | no | — | referenced as `<Audio 2>` in prompt |
| `prompt` | no | — | **max 8000 chars** |
| `steps` | no | 8 | sampling steps, 4–8 |
| `aspect_ratio` | no | `16:9 (Widescreen)` | match the input images' shape |
| `megapixels` | no | **0.7** | 0.2–1 |
| `duration` | no | 5 | 3–15 s |
| `seed` | no | 0 | |

### video_minimax_h3_fun_controlnet_union — motion control

Transplants the motion of a control video onto a new subject: `video1` drives
the motion/camera trajectory, `image1`/`image2` lock the subject's and scene's
appearance, `audio1` supplies the audio track. Use it when the brief is "make
my character do exactly this movement" — text alone can't pin down choreography.

| Param | Required | Default | Notes |
|---|---|---|---|
| `video1` | no | — | control video (motion source); upload locals via /oss/presigned-url |
| `image1` | no | — | appearance reference |
| `image2` | no | — | second appearance reference |
| `audio1` | no | — | audio track |
| `prompt` | no | — | max 6000 chars; describe the subject/scene — motion comes from `video1` |
| `aspect_ratio` | no | `16:9 (Widescreen)` | |
| `megapixels` | no | 0.4 | **0.3**–1 (floor is higher than the other workflows) |
| `duration` | no | 5 | 3–15 s |
| `seed` | no | 0 | |

Allowed `aspect_ratio` labels (all workflows):
`1:1 (Square)`, `2:3 (Portrait Photo)`, `3:2 (Photo)`, `3:4 (Portrait Standard)`,
`4:3 (Standard)`, `9:16 (Portrait Widescreen)`, `16:9 (Widescreen)`.

## Other routes (not needed for video, listed for completeness)

- `GET /feed/prompt?theme_id=&limit=&cursor=` — prompt feed (paginated)
