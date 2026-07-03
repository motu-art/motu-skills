# Motu Color Engine — API reference

Base URL: `$MCE_API_BASE` (default `https://mce.motu.art`).
Auth: if enabled, send `X-API-Key: $MCE_API_KEY` (or `Authorization: Bearer $MCE_API_KEY`)
on every endpoint **except** `/v1/health`.

## GET /v1/health
Liveness/version. No key required.

## GET /v1/styles
Returns `{ styles: [{id, name, kind, name_zh, ...}], composite_separator, bases, flavours }`.
`kind` is `base` or `flavour`. Combine as `<flavour><composite_separator><base>`
(default separator `@`), e.g. `kodak_gold@motu_korean_id`.

## POST /v1/process  (multipart/form-data)
Grade an image. Fields:
- `file` (required) — image upload (JPG/PNG/WebP, ≤ ~15 MB).
- `style` — style id (default `motu_korean_id`).
- `strength` — look intensity, default `1.0` (0–~1.5).
- `output_format` — `png` (default) | `jpeg` | `webp`.
- `quality` — 1–100 for lossy formats (default 90).
- `max_long_edge` — cap working long edge (default 1024; server ceiling applies).
- `mask` — `true` to also return a mask inline (base64).
- `mask_kind` — mask type when `mask=true` (see below).

Response JSON:
```
{ "trace_id", "style_id", "image_base64", "content_type",
  "processing_time_ms", "quality": { "skin_delta_e_to_target", "warnings" },
  "report_url", "compare_base64",
  "mask_base64", "mask_kind", "mask_content_type" }   // mask_* only when mask=true
```
Decode `image_base64` to bytes to get the graded image. `skin_delta_e_to_target`
is the skin ΔE to the target skin (lower = closer).

## POST /v1/mask  (multipart/form-data)
Segmentation only (decode + parse; **skips grading/render/score** — faster). Fields:
- `file` (required).
- `mask_kind` — `skin` (default) | `valid_skin` | `face` | `person` | `hair` |
  `cloth` | `background`.
- `max_long_edge` — optional.

Returns the mask as a raw **grayscale PNG** (`Content-Type: image/png`), with header
`X-MCE-Mask-Kind`. Save the response body directly.

## Errors
- `400` bad params / empty upload · `401` missing/invalid key ·
  `413` too large · `415` unsupported content-type · `422` processing/segmentation failed.
Error bodies are JSON `{ "detail": "..." }`.
