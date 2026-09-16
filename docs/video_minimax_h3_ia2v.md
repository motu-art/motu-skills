# video_minimax_h3_ia2v — Motu Workflow API



## Overview

- Base URL: https://api.motu.art
- Auth: every request needs header `Authorization: Bearer YOUR_API_KEY`
- This is an async API: submit a request to get a `workflow_request_id`, then poll the status endpoint until `status` is `completed` or `failed`.
- Return type of this workflow: `video`

## 1. Submit a request

`POST https://api.motu.art/workflows/video_minimax_h3_ia2v`

Headers:
- `Authorization: Bearer YOUR_API_KEY`
- `Content-Type: application/json`

### Parameters

| Name | Type | Required | Default | Notes |
| --- | --- | --- | --- | --- |
| image_url | image | no |  | - |
| audio | audio | no |  | - |
| prompt | textarea | no | subject_definitions:
<Subject 1> is the only person shown in <Picture 1>, including the person’s exact identity, facial features, hairstyle, makeup, wardrobe, body proportions, pose, and position in the composition.
<Picture 1> is the supplied reference portrait and the exact first frame and composition anchor for the entire target video. It also defines the background, props, lighting, colors, framing, depth of field, and spatial relationships.
<Audio 1> is the complete supplied audio signal and the speaking voice of <Subject 1> (S1). It is the sole authoritative source of speech, timing, delivery, and sound.

summary:
[keyframe completion + audio reuse] The target video is one uninterrupted, fixed-camera talking-head shot featuring only <Subject 1>. It begins exactly from <Picture 1> and copies <Audio 1> in full as the only final audio track. The visible speaking performance is driven exclusively by <Audio 1>. No other person appears.

retention_analysis:
<Subject 1> (appears throughout [Shot 1]): fully_preserved - preserve the person’s identity, facial structure, skin characteristics, hairstyle, makeup, wardrobe, body proportions, initial pose, scale, and placement without redesign, substitution, beautification drift, or age change.
<Picture 1> ([Shot 1] first frame and full-shot composition anchor): fully_preserved - begin from this exact frame and preserve its background, props, lighting, colors, depth of field, camera position, camera height, focal length, focus, crop, horizon, perspective, and composition throughout the entire video.
<Audio 1>: fully_copy - copy the complete supplied audio signal 1:1, from its first sample to its last sample, as the target video’s complete and sole final audio track. Do not regenerate, replace, transcribe, reinterpret, trim, extend, loop, time-stretch, pitch-shift, denoise, enhance, remix, duck, layer over, or otherwise alter it.

detailed_description:
The target video retains the same realistic professional-portrait appearance, lighting, colors, depth of field, image texture, background, and composition as <Picture 1>.

[Shot 1] The single uninterrupted shot begins exactly from <Picture 1>. Only <Subject 1> is present. Do not introduce another person, face, body, reflection, silhouette, hand, interviewer, audience member, or background figure.

The camera remains mechanically locked on a stable tripod at the identical position and height, with the identical focal length, focus, crop, perspective, horizon, and framing. There are no cuts, transitions, zooms, pans, tilts, rolls, dollies, trucks, cranes, handheld motion, stabilization drift, reframing, focus pulls, focus breathing, lens changes, or exposure changes.

<Subject 1> (S1) looks naturally toward the camera and visibly speaks in exact synchronization with <Audio 1>. Drive every lip shape, phoneme transition, jaw movement, facial articulation, pause, emphasis, cadence, emotion, breath timing, and line ending exclusively from the supplied audio. Do not infer, rewrite, paraphrase, translate, or generate spoken content from the text prompt. Do not introduce any words, vocalizations, breaths, or mouth movements unsupported by <Audio 1>.

The mouth remains naturally closed during every silent portion of <Audio 1>. Speech begins precisely when the supplied voice begins and ends precisely when it ends. After the final audible sample, the mouth closes naturally without extending the performance or adding trailing speech.

Movement is limited to natural speech articulation, subtle blinks, restrained facial responses, and very small anatomically coherent head micro-movements required by the supplied delivery. Keep the torso, shoulders, hands, pose, wardrobe, hair, background, props, and lighting visually stable. Do not introduce large gestures, pose changes, walking, exaggerated expressions, performance flourishes, or invented actions.

Preserve the person’s identity, facial structure, skin appearance, hair, clothing, body proportions, lighting, background, props, and composition consistently through the final frame.

overall_soundscape:
<Audio 1> is copied completely and unchanged as the entire final soundscape. No generated voice, replacement dialogue, additional speech, room tone, ambience, artificial breath layer, Foley, fabric noise, sound effects, transition sounds, silence padding, or other audio layer is added. No portion of <Audio 1> is removed, modified, repeated, or covered.

non_diegetic_music:
N/A. Do not generate or add music. | maxLength: 6000 |
| megapixels | number | no | 0.4 | max: 1 |
| aspect_ratio | select | no | 3:4 (Portrait Standard) | one of: 1:1 (Square) | 2:3 (Portrait Photo) | 3:2 (Photo) | 3:4 (Portrait Standard) | 4:3 (Standard) | 9:16 (Portrait Widescreen) | 16:9 (Widescreen) |
| seed | seed | no | 0 | max: 10000000000000000 |
| duration | number | no | 6 | max: 15 |

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
curl -X POST https://api.motu.art/workflows/video_minimax_h3_ia2v \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```
