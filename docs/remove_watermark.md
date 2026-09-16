# remove_watermark — Motu Workflow API



## Overview

- Base URL: https://api.motu.art
- Auth: every request needs header `Authorization: Bearer YOUR_API_KEY`
- This is an async API: submit a request to get a `workflow_request_id`, then poll the status endpoint until `status` is `completed` or `failed`.
- Return type of this workflow: `image`

## 1. Submit a request

`POST https://api.motu.art/workflows/remove_watermark`

Headers:
- `Authorization: Bearer YOUR_API_KEY`
- `Content-Type: application/json`

### Parameters

| Name | Type | Required | Default | Notes |
| --- | --- | --- | --- | --- |
| image_url | image | yes |  | - |
| seed | seed | no | 0 | max: 10000000000000000 |
| long_side | number | no | 1536 | min: 512; max: 2048 |

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
  "result": [{ "url": "https://.../output.png", "width": 1024, "height": 1024 }]
}
```
`result` is only present when `status` is `completed`. Poll every few seconds until the status is `completed` or `failed`.

## Example (cURL)

```bash
curl -X POST https://api.motu.art/workflows/remove_watermark \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
      "image_url": "value"
    }'
```
