# video_minimax_h3_ra2v — Motu Workflow API



## Overview

- Base URL: https://api.motu.art
- Auth: every request needs header `Authorization: Bearer YOUR_API_KEY`
- This is an async API: submit a request to get a `workflow_request_id`, then poll the status endpoint until `status` is `completed` or `failed`.
- Return type of this workflow: `video`

## 1. Submit a request

`POST https://api.motu.art/workflows/video_minimax_h3_ra2v`

Headers:
- `Authorization: Bearer YOUR_API_KEY`
- `Content-Type: application/json`

### Parameters

| Name | Type | Required | Default | Notes |
| --- | --- | --- | --- | --- |
| megapixels | number | no | 0.7 | min: 0.2; max: 1 |
| aspect_ratio | select | no | 16:9 (Widescreen) | one of: 1:1 (Square) | 2:3 (Portrait Photo) | 3:2 (Photo) | 3:4 (Portrait Standard) | 4:3 (Standard) | 9:16 (Portrait Widescreen) | 16:9 (Widescreen) |
| duration | number | no | 5 | min: 3; max: 15 |
| prompt | textarea | no | Bold comic-book ink style, heavy linework, red and blue-black palette, night city. Use <Picture 2> and <Picture 1> as reference frames and <Audio 1> exactly as it is.
CUT 1: top-down view of the little boy superhero on the rooftop — red cape fluttering in the wind, hands planted on his hips, freckles and a cocky grin as he looks straight up into the camera. The camera slowly descends toward him as he delivers his line — as he speaks, comic-book graphic overlay text word by word in sync with his voice: "GET READY TO" - "MEET" — "YOUR" — "MAKER" — huge jagged comic lettering, white with heavy black outlines and red drop shadows, tilted at scrappy angles, until the three words hang stacked in the air above him between his face and the lens.
TRANSITION: a violent WHIP PAN off the rooftop that SMEARS the floating words away with it, motion-streaked —
CUT 2: low hero angle on the colossal black mech-kaiju towering over the skyline as it rears back and unleashes a GIANT terrifying ROAR — jaws wide with fangs, red eyes and chest-core flaring blinding bright, blue lightning arcing off its head, the roar's shockwave rippling dust and rattling windows down the buildings, comic-style speed-lines and ink splatter bursting from the impact of the sound. It leans INTO the camera as the roar peaks. Hold on the roar. | maxLength: 8000 |
| image_start_url | image | no |  | - |
| image_end_url | image | no |  | - |
| audio | audio | no |  | - |
| seed | number | no | 0 | max: 10000000000000000 |

Notes:
- Image/video/audio type parameters accept a public URL or a base64-encoded data string.
- Optional body field `priority`: `"urgent"` or `"default"` (default) — urgent requests are processed first.

### Example request body

```json
{}
```

### Responses

- `202 Accepted`: `{ "status": "queued", "workflow_request_id": "<uuid>" }`
- `400`: missing or invalid parameter, e.g. `{ "error": "Missing required parameter: <name>" }`
- `401`: API key missing; `403`: invalid API key; `404`: workflow not found

## 2. Poll for the result

`GET https://api.motu.art/workflows/status/{workflow_request_id}` (same `Authorization` header)

Response:
```json
{
  "workflow_request_id": "<uuid>",
  "status": "queued | processing | completed | failed",
  "result": [{ "url": "https://.../output.mp4", "width": 1024, "height": 1024 }]
}
```
`result` is only present when `status` is `completed`. Poll every few seconds until the status is `completed` or `failed`.

## Example (cURL)

```bash
curl -X POST https://api.motu.art/workflows/video_minimax_h3_ra2v \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```
