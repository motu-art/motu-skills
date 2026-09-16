# motu.art Workflow API — reference (verified against live API 2026-08-21)

Base URL: `https://api.motu.art`
Auth: `Authorization: Bearer $MOTU_KEY` on every request.
(Kong gateway rejects Python's default urllib User-Agent — the bundled script sends a custom UA.)

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
GET /workflow/status?workflow_request_id={id}
Authorization: Bearer $MOTU_KEY
```

(The docs also document `GET /workflows/status/{id}`; the query-param form above is the one
verified working against the live API and is what the script uses.)

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
image for a follow-up i2v run.
Signed OSS URLs expire after **14 days** — download promptly.

## Upload a local file (images for i2v/r2v/ia2v/ra2v, audio for ia2v/ra2v)

`image_url` / `image_start_url` / `image_end_url` / `audio` must be publicly reachable
`http(s)://` URLs. Base64 data URIs are NOT accepted: they pass submit-time validation
(202) but the job fails silently during processing (verified 2026-08-21, i2v + r2v).
Upload local files through the OSS presign route:

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
`scripts/motu_video.py upload --file x.png` and the `--image*`/`--audio` flags do this automatically.

## Workflow parameter sheets

### video_minimax_h3_t2v — text-to-video

| Param | Required | Default | Notes |
|---|---|---|---|
| `prompt` | yes | — | max 6000 chars |
| `aspect_ratio` | no | `16:9 (Widescreen)` | full labels only |
| `megapixels` | no | 0.4 | 0.2–1 |
| `duration` | no | 5 | 3–15 s |
| `filename_prefix` | no | `video` | |
| `seed` | no | 0 | 0–10000000000000000 |

### video_minimax_h3_i2v — image-to-video

| Param | Required | Default | Notes |
|---|---|---|---|
| `image_url` | yes | — | public URL; upload locals via /oss/presigned-url |
| `prompt` | no | — | max 6000 chars; reference the image as `<Picture 1>` |
| `aspect_ratio` | no | `1:1 (Square)` | match the input image's shape |
| `megapixels` | no | 0.4 | max 1 |
| `duration` | no | 5 | 3–15 s |
| `seed` | no | 0 | |

### video_minimax_h3_ia2v — image+audio-to-video (talking head)

| Param | Required | Default | Notes |
|---|---|---|---|
| `image_url` | no | — | portrait to animate; `<Picture 1>` |
| `audio` | no | — | voice track; `<Audio 1>`; copied 1:1 into the final video |
| `prompt` | no | built-in talking-head spec | max 6000 chars; see references/prompting.md |
| `aspect_ratio` | no | `3:4 (Portrait Standard)` | full labels only |
| `megapixels` | no | 0.4 | max 1 |
| `duration` | no | 6 | max 15 s |
| `seed` | no | 0 | |

Semantics (from the official default prompt): the output is one uninterrupted fixed-camera
shot that starts exactly on `<Picture 1>`; the visible speaking performance is driven
exclusively by `<Audio 1>`, which is copied unaltered as the sole audio track.

### video_minimax_h3_r2v — start/end frame

| Param | Required | Default | Notes |
|---|---|---|---|
| `image_start_url` | yes | — | referenced as `<Picture 1>` in prompt |
| `image_end_url` | yes | — | referenced as `<Picture 2>` in prompt |
| `prompt` | no | — | max 6000 chars |
| `aspect_ratio` | no | `16:9 (Widescreen)` | |
| `megapixels` | no | 0.4 | max 1 |
| `duration` | no | 5 | 3–15 s |
| `seed` | no | 0 | |

### video_minimax_h3_ra2v — frames+audio-to-video

| Param | Required | Default | Notes |
|---|---|---|---|
| `image_start_url` | no | — | referenced as `<Picture 1>` |
| `image_end_url` | no | — | referenced as `<Picture 2>` |
| `audio` | no | — | referenced as `<Audio 1>` |
| `prompt` | no | — | **max 8000 chars** |
| `aspect_ratio` | no | `16:9 (Widescreen)` | |
| `megapixels` | no | **0.7** | 0.2–1 |
| `duration` | no | 5 | 3–15 s |
| `seed` | no | 0 | |

Allowed `aspect_ratio` labels (all workflows):
`1:1 (Square)`, `2:3 (Portrait Photo)`, `3:2 (Photo)`, `3:4 (Portrait Standard)`,
`4:3 (Standard)`, `9:16 (Portrait Widescreen)`, `16:9 (Widescreen)`.

## Other routes (not needed for video, listed for completeness)

- `GET /feed/prompt?theme_id=&limit=&cursor=` — prompt feed (paginated)
