# motu.art Workflow API — z_image_turbo_2k reference

Base URL: `https://api.motu.art`
Auth: `Authorization: Bearer $MOTU_KEY` on every request.
(Kong gateway rejects Python's default urllib User-Agent — the bundled script sends a custom UA.)

## Submit

```
POST /workflows/z_image_turbo_2k
Content-Type: application/json

{"prompt": "...", "width": 768, "height": 1024, "batch_size": 1, "seed": 0}
```

Response `202 Accepted`:
```json
{"status": "queued", "workflow_request_id": "<uuid>"}
```

The response contains **only** the request id — results never come back in the submit call.

### Parameters

| Param | Required | Default | Notes |
|---|---|---|---|
| `prompt` | yes | — | max 6000 chars; the model is tuned for structured comma-group prompts (see `references/prompting.md`) |
| `width` | no | 768 | 512–1024; composition canvas, not final resolution |
| `height` | no | 1024 | 512–1024; composition canvas, not final resolution |
| `batch_size` | no | 1 | 1–4 images from one prompt (same prompt, seed-varied picks) |
| `seed` | no | 0 | 0–10000000000000000; 0 = random |
| `priority` | no | `"default"` | `"urgent"` goes to a separate queue |

**Resolution**: `width`/`height` set the composition ratio only — the 2K pipeline returns
roughly **2× the requested canvas** (a 512×512 request returned 1024×1024; the 768×1024
default returns 1536×2048). Pick the canvas for framing, never upscale the numbers hoping
for more detail.

Errors:
- `400 {"error": "Missing required parameter: <name>"}` / invalid parameter values
- `401`: API key missing; `403`: invalid API key; `404`: workflow not found

## Poll for status / result

```
GET /workflow/status?workflow_request_id={id}
Authorization: Bearer $MOTU_KEY
```

(The docs also document `GET /workflows/status/{id}`; that path form currently returns
`500 {"message":"Failed to retrieve API cost"}` on the gateway — the query-param form above
is the one verified working against the live API and is what the script uses.)

While running: `{"workflow_request_id": "...", "status": "queued | processing"}`
On failure: `"status": "failed"` (no error detail is exposed by any endpoint).

On completion the same endpoint includes `result`:
```json
{
  "status": "completed",
  "workflow_request_id": "...",
  "result": [
    {"url": "https://.../1?OSSAccessKeyId=...", "width": 1024, "height": 1024, "file_size": 961282}
  ]
}
```

`result` has one entry per generated image (`batch_size` > 1 → several entries). `url`
points at a PNG but **carries no file extension** — save the download as `.png`.
Generation typically takes 10–30 s.

`url` is a signed OSS link — same bucket as the other motu workflows, URLs expire after
**14 days** — download promptly.
