# motu.art Workflow API — remove_watermark reference

Base URL: `https://api.motu.art`
Auth: `Authorization: Bearer $MOTU_KEY` on every request.
(Kong gateway rejects Python's default urllib User-Agent — the bundled script sends a custom UA.)

## Submit

```
POST /workflows/remove_watermark
Content-Type: application/json

{"image_url": "https://...", "long_side": 1536, "seed": 0}
```

Response `202 Accepted`:
```json
{"status": "queued", "workflow_request_id": "<uuid>"}
```

The response contains **only** the request id — results never come back in the submit call.

### Parameters

| Param | Required | Default | Notes |
|---|---|---|---|
| `image_url` | yes | — | public URL; upload locals via /oss/presigned-url |
| `long_side` | no | 1536 | 512–2048, output long edge in px |
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

`url` is the cleaned png; signed OSS URLs expire after **14 days** — download promptly.

## Upload a local image

`image_url` must be a publicly reachable `http(s)://` URL. Base64 data URIs are NOT
accepted: they pass submit-time validation (202) but the job fails silently during
processing. Upload local files through the OSS presign route:

```
POST /oss/presigned-url
Authorization: Bearer $MOTU_KEY
Content-Type: application/json

{"fileType": "image/png"}
```
→
```json
{"uploadUrl": "https://...PUT-signed...", "key": "uploads/...", "url": "https://...GET-signed-14d..."}
```

Then `PUT` the raw file bytes to `uploadUrl` with the **exact same `Content-Type`** you sent
as `fileType` (the signature covers it), and use the returned `url` as `image_url`.
`scripts/motu_watermark.py upload --file x.png` and the `--image` flag do this automatically.
