# audio_minimax_music_3 — Motu Workflow API



## Overview

- Base URL: https://api.motu.art
- Auth: every request needs header `Authorization: Bearer YOUR_API_KEY`
- This is an async API: submit a request to get a `workflow_request_id`, then poll the status endpoint until `status` is `completed` or `failed`.
- Return type of this workflow: `audio`

## 1. Submit a request

`POST https://api.motu.art/workflows/audio_minimax_music_3`

Headers:
- `Authorization: Bearer YOUR_API_KEY`
- `Content-Type: application/json`

### Parameters

| Name | Type | Required | Default | Notes |
| --- | --- | --- | --- | --- |
| seed | seed | no | 0 | max: 10000000000000000 |
| lyrics | textarea | no |  | maxLength: 6000 |
| caption | textarea | no | ### Global Metadata

Lighthearted children's instrumental music with a warm, cheerful summer atmosphere. The style blends gentle children's easy-listening, acoustic pop, and playful soundtrack elements. Keep the tempo relaxed to moderately upbeat, with a soft, steady pulse that feels lively without becoming energetic or rushed. The emotional progression should move from peaceful curiosity into bright, carefree happiness, evoking a sunny summer afternoon beneath the shade of leafy trees, distant cicadas, and a soft breeze passing through the branches.

The sonic palette should remain clean, airy, warm, and natural. Piano, small wooden xylophone, and delicate wind chimes form the core instrumentation. Avoid heavy drums, aggressive percussion, dense electronic textures, dramatic orchestral elements, or strong bass. Maintain plenty of open space between notes, with a simple and memorable melody suitable for children.

### Vocal Details

Fully instrumental with no vocals, spoken words, chants, or vocal samples.

The main melodic role alternates naturally between a warm, lightly played piano and a bright wooden xylophone. Delicate wind chimes provide occasional sparkling accents rather than carrying the melody. The melodic phrases should be short, clear, playful, and easy to remember, with gentle repetition and small variations.

### Arrangement

**Intro:** Begin quietly with sparse wind-chime notes and a few soft piano tones, creating the feeling of sunlight filtering through tree leaves. Leave generous space between phrases.

**Main Theme:** Introduce the wooden xylophone with a simple, cheerful melody. The piano provides light chordal support underneath, while subtle wind-chime accents appear at the ends of selected phrases. Establish a gentle, relaxed rhythmic motion.

**Development:** Allow the piano to briefly take over the main melody while the xylophone responds with short playful phrases. Gradually enrich the harmony without making the arrangement dense. Maintain a breezy, effortless summer character throughout.

**Bright Section:** Bring the xylophone melody forward again with slightly more rhythmic movement and brighter piano accompaniment. This should be the happiest point of the piece, suggesting children enjoying a peaceful summer day outdoors while leaves move gently in the wind.

**Outro:** Gradually simplify the arrangement. Let the xylophone disappear first, followed by increasingly sparse piano notes. Finish with a few delicate wind-chime tones fading naturally into silence, leaving a calm, warm, and innocent summer feeling. | maxLength: 6000 |
| max_duration | number | no | 240 | max: 360 |

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
  "result": [{ "url": "https://.../audio.mp3", "duration": 12.3 }]
}
```
`result` is only present when `status` is `completed`. Poll every few seconds until the status is `completed` or `failed`.

## Example (cURL)

```bash
curl -X POST https://api.motu.art/workflows/audio_minimax_music_3 \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```
