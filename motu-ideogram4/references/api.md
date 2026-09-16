# motu.art Workflow API — ideogram4 reference

Base URL: `https://api.motu.art`
Auth: `Authorization: Bearer $MOTU_KEY` on every request.
(Kong gateway rejects Python's default urllib User-Agent — the bundled script sends a custom UA.)

## Submit

```
POST /workflows/ideogram4
Content-Type: application/json

{"prompt": "...", "width": 768, "height": 1376, "cfg": 2, "temperature": 0.3, "seed": 0}
```

Response `202 Accepted`:
```json
{"status": "queued", "workflow_request_id": "<uuid>"}
```

The response contains **only** the request id — results never come back in the submit call.

### Parameters

| Param | Required | Default | Notes |
|---|---|---|---|
| `prompt` | yes | — | max 6000 chars |
| `width` | no | 768 | 512–1536 |
| `height` | no | 1376 | 512–1536 |
| `cfg` | no | 2 | 1–7; prompt-adherence strength |
| `temperature` | no | 0.3 | 0–1 |
| `model` | no | `gpt-4.1` | select with a single allowed value; rarely needed |
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
  "result": [{"url": "https://.../output.png", "width": 1024, "height": 1024}]
}
```

`url` is the png; signed OSS URLs expire after **14 days** — download promptly.
