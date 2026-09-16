# video_minimax_h3_t2v — Motu Workflow API



## Overview

- Base URL: https://api.motu.art
- Auth: every request needs header `Authorization: Bearer YOUR_API_KEY`
- This is an async API: submit a request to get a `workflow_request_id`, then poll the status endpoint until `status` is `completed` or `failed`.
- Return type of this workflow: `video`

## 1. Submit a request

`POST https://api.motu.art/workflows/video_minimax_h3_t2v`

Headers:
- `Authorization: Bearer YOUR_API_KEY`
- `Content-Type: application/json`

### Parameters

| Name | Type | Required | Default | Notes |
| --- | --- | --- | --- | --- |
| prompt | textarea | yes | Realistic live-action cinematic look, action movie trailer: practical film photography style, a post-rain dusk metropolis, anamorphic lens, shallow depth of field, film grain, city volumetric fog, flying-car traffic between the towers, restrained grading for a premium feel, powerful natural movement.

Scene overview: at dusk on a cluster of skyscrapers, the protagonist is being chased, sprinting and leaping across rooftops, jumping from one building's roof to the next with pursuers closing in behind. This is the escape sequence of an action movie trailer: every leap is life-or-death, thrilling and fluid.

Storyboard (each shot a separate scene, rapid cuts, all landing on the musical beats):
[0s-1.5s] Shot 1: high side angle: the protagonist sprinting at the roof edge, pursuers appearing in the rooftop doorway behind him, wind catching his coat.
[1s-2.5s] Shot 2: the protagonist leaps across the gap between buildings, body stretching mid-air, towers and flying-car light trails behind him, a slight slow-motion feel.
[2.5s-4s] Shot 3: he lands, rolls and rises, low-angle shot, tower shadows and fog behind him, he keeps running.
[4s-5s] Shot 4: freeze: the instant he hits the edge of the next roof and launches into the jump, silhouette, holding.

Camera: each shot its own angle, cuts clean and hard, no dissolves, a slight frame jitter on the jumps.

Audio: wind, rapid footsteps, city ambience, low score underneath, an accent hit on each leap, the score bursting at 4s, closing the last 1s.

No text, subtitles, logos or watermarks of any kind, no animation or cartoon rendering, no overly-CG look, keep the live-action texture. | maxLength: 6000 |
| filename_prefix | text | no | video | - |
| megapixels | number | no | 0.4 | min: 0.2; max: 1 |
| aspect_ratio | select | no | 16:9 (Widescreen) | one of: 1:1 (Square) | 2:3 (Portrait Photo) | 3:2 (Photo) | 3:4 (Portrait Standard) | 4:3 (Standard) | 9:16 (Portrait Widescreen) | 16:9 (Widescreen) |
| seed | seed | no | 0 | max: 10000000000000000 |
| duration | number | no | 5 | min: 3; max: 15 |

Notes:
- Image/video/audio type parameters accept a public URL or a base64-encoded data string.
- Optional body field `priority`: `"urgent"` or `"default"` (default) — urgent requests are processed first.

### Example request body

```json
{
      "prompt": "Realistic live-action cinematic look, action movie trailer: practical film photography style, a post-rain dusk metropolis, anamorphic lens, shallow depth of field, film grain, city volumetric fog, flying-car traffic between the towers, restrained grading for a premium feel, powerful natural movement.

Scene overview: at dusk on a cluster of skyscrapers, the protagonist is being chased, sprinting and leaping across rooftops, jumping from one building's roof to the next with pursuers closing in behind. This is the escape sequence of an action movie trailer: every leap is life-or-death, thrilling and fluid.

Storyboard (each shot a separate scene, rapid cuts, all landing on the musical beats):
[0s-1.5s] Shot 1: high side angle: the protagonist sprinting at the roof edge, pursuers appearing in the rooftop doorway behind him, wind catching his coat.
[1s-2.5s] Shot 2: the protagonist leaps across the gap between buildings, body stretching mid-air, towers and flying-car light trails behind him, a slight slow-motion feel.
[2.5s-4s] Shot 3: he lands, rolls and rises, low-angle shot, tower shadows and fog behind him, he keeps running.
[4s-5s] Shot 4: freeze: the instant he hits the edge of the next roof and launches into the jump, silhouette, holding.

Camera: each shot its own angle, cuts clean and hard, no dissolves, a slight frame jitter on the jumps.

Audio: wind, rapid footsteps, city ambience, low score underneath, an accent hit on each leap, the score bursting at 4s, closing the last 1s.

No text, subtitles, logos or watermarks of any kind, no animation or cartoon rendering, no overly-CG look, keep the live-action texture."
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
curl -X POST https://api.motu.art/workflows/video_minimax_h3_t2v \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
      "prompt": "Realistic live-action cinematic look, action movie trailer: practical film photography style, a post-rain dusk metropolis, anamorphic lens, shallow depth of field, film grain, city volumetric fog, flying-car traffic between the towers, restrained grading for a premium feel, powerful natural movement.

Scene overview: at dusk on a cluster of skyscrapers, the protagonist is being chased, sprinting and leaping across rooftops, jumping from one building's roof to the next with pursuers closing in behind. This is the escape sequence of an action movie trailer: every leap is life-or-death, thrilling and fluid.

Storyboard (each shot a separate scene, rapid cuts, all landing on the musical beats):
[0s-1.5s] Shot 1: high side angle: the protagonist sprinting at the roof edge, pursuers appearing in the rooftop doorway behind him, wind catching his coat.
[1s-2.5s] Shot 2: the protagonist leaps across the gap between buildings, body stretching mid-air, towers and flying-car light trails behind him, a slight slow-motion feel.
[2.5s-4s] Shot 3: he lands, rolls and rises, low-angle shot, tower shadows and fog behind him, he keeps running.
[4s-5s] Shot 4: freeze: the instant he hits the edge of the next roof and launches into the jump, silhouette, holding.

Camera: each shot its own angle, cuts clean and hard, no dissolves, a slight frame jitter on the jumps.

Audio: wind, rapid footsteps, city ambience, low score underneath, an accent hit on each leap, the score bursting at 4s, closing the last 1s.

No text, subtitles, logos or watermarks of any kind, no animation or cartoon rendering, no overly-CG look, keep the live-action texture."
    }'
```
