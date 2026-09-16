# video_minimax_h3_i2v — Motu Workflow API



## Overview

- Base URL: https://api.motu.art
- Auth: every request needs header `Authorization: Bearer YOUR_API_KEY`
- This is an async API: submit a request to get a `workflow_request_id`, then poll the status endpoint until `status` is `completed` or `failed`.
- Return type of this workflow: `video`

## 1. Submit a request

`POST https://api.motu.art/workflows/video_minimax_h3_i2v`

Headers:
- `Authorization: Bearer YOUR_API_KEY`
- `Content-Type: application/json`

### Parameters

| Name | Type | Required | Default | Notes |
| --- | --- | --- | --- | --- |
| image_url | image | yes |  | - |
| megapixels | number | no | 0.4 | max: 1 |
| aspect_ratio | select | no | 1:1 (Square) | one of: 1:1 (Square) | 2:3 (Portrait Photo) | 3:2 (Photo) | 3:4 (Portrait Standard) | 4:3 (Standard) | 9:16 (Portrait Widescreen) | 16:9 (Widescreen) |
| seed | seed | no | 0 | max: 10000000000000000 |
| prompt | textarea | no | Editorial tech product film. The transparent gaming mouse from <Picture 1> in its original scene: a pitch-black studio void with a dark, subtle reflective surface, lit by dramatic duotone vibrant blue and warm neon orange rim lighting, deep soft shadow falloff into pure black. Monochromatic dark palette with electric blue and amber accents. Material motif: glowing internal metallic micro-components and glossy acrylic refractions. The environment is constant throughout.
SHOT 1: The scene opens exactly on image 1, the mouse resting confidently on the dark surface; the blue and orange lights slowly pulse brighter, refracting deeply through the transparent acrylic shell as the camera executes a slow, deliberate push-in to reveal the intricate circuitry.
SHOT 2: Cut to an extreme macro profile of the ridged scroll wheel and layered internal micro-components; the camera glides slowly along the side as a sharp beam of warm orange light sweeps across the metallic textures, contrasting perfectly against the deep blue ambient glow.
SHOT 3: Cut to a low-angle beauty shot: the mouse levitates weightlessly a few centimeters above the dark reflective surface, rotating in a slow, precise orbit; the duotone lighting flares gently along the glassy transparent edges before fading slowly into a sleek silhouette.
Audio: deep pulsing sub-bass room tone, sharp tactile mechanical clicks, a sweeping glassy whoosh on cuts, and a rising electronic swell that resolves to near-silence on the final fade.  | maxLength: 6000 |
| duration | number | no | 5 | min: 3; max: 15 |

Notes:
- Image/video/audio type parameters accept a public URL or a base64-encoded data string.
- Optional body field `priority`: `"urgent"` or `"default"` (default) — urgent requests are processed first.

### Example request body

```json
{
      "image_url": "value"
    }
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
curl -X POST https://api.motu.art/workflows/video_minimax_h3_i2v \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
      "image_url": "value"
    }'
```
