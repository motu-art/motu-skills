# motu.art Workflow API — music reference

Base URL: `https://api.motu.art`
Auth: `Authorization: Bearer $MOTU_KEY` on every request.
(Kong gateway rejects Python's default urllib User-Agent — the bundled script sends a custom UA.)

## Submit

```
POST /workflows/audio_minimax_music_3
Content-Type: application/json

{"caption": "...", "lyrics": "...", "max_duration": 240, "seed": 0}
```

Response `202 Accepted`:
```json
{"status": "queued", "workflow_request_id": "<uuid>"}
```

The response contains **only** the request id — results never come back in the submit call.

### Parameters

| Param | Required | Default | Notes |
|---|---|---|---|
| `caption` | no | long built-in default brief | max 6000 chars; always send one |
| `lyrics` | no | — | max 6000 chars; omit for instrumental |
| `max_duration` | no | 240 | max 360, seconds |
| `seed` | no | 0 | 0–10000000000000000 |
| `callback_url` | no | — | on completion the platform POSTs `{workflow_request_id, status, urls: [...]}` |
| `priority` | no | `"default"` | `"urgent"` goes to a separate queue |

Errors:
- `400 {"error": "Missing required parameter: X"}`
- `400 {"error": "Invalid parameters", "details": {"param": "reason"}}`
- `401 {"error": "API key is missing"}` / `403 {"error": "Invalid API key"}`
- `404 {"error": "Workflow X not found"}`

## Poll for status / result

```
GET /workflow/status?workflow_request_id={id}
Authorization: Bearer $MOTU_KEY
```

(The docs also document `GET /workflows/status/{id}`; the query-param form above is the one
verified working against the live API and is what the script uses.)

While running: `{"workflow_request_id": "...", "status": "queued | processing"}`
On failure: `"status": "failed"` (no error detail is exposed by any endpoint).

On completion the same endpoint includes `result`:
```json
{
  "status": "completed",
  "workflow_request_id": "...",
  "result": [{"url": "https://.../audio.mp3", "duration": 12.3}]
}
```

`url` is the mp3; signed OSS URLs expire after **14 days** — download promptly.
`duration` is the actual generated length in seconds, often shorter than `max_duration`
(the arrangement ends when it ends).
