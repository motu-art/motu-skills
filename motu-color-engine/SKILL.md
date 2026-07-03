---
name: motu-color-engine
description: >
  AI portrait skin-color grading and skin segmentation via the Motu Color Engine
  HTTP API. Use when the user wants to color-grade / correct skin tone on portrait
  photos, apply a film or commercial look, batch-grade a folder of portraits, or
  export a skin mask (matte / segmentation) from a portrait. Trigger keywords:
  portrait color grading, skin tone, skin mask, matte, film look, headshot, retouch
  color, 调色, 肤色, 皮肤蒙版, 人像调色.
---

# Motu Color Engine

Portrait **color grading** (skin-tone anchored) and **skin segmentation** through a
hosted HTTP API. It only changes color — no smoothing, reshaping, or face swap.

## Prerequisites

- `curl` and `python3` available (used by the bundled scripts).
- Environment:
  - `MCE_API_BASE` — API base URL. Default `https://mce.motu.art`.
  - `MCE_API_KEY` — API key, if the service has auth enabled. Sent as `X-API-Key`.
    Ask the user for it (or read from env) — never hard-code it.

Quick reachability check: `curl -sS "$MCE_API_BASE/v1/health"` (health needs no key).

## Choosing what to run

- User wants a **graded / recolored** portrait, or a specific look → **grade**.
- User only wants the **skin mask / matte / segmentation** → **mask** (faster; skips grading).

All scripts live in this skill's `scripts/` folder and take file paths in the workspace.

## Grade a portrait

```bash
scripts/grade.sh <input-image> <output-image> [style-id] [strength]
```
- `style-id` — optional; omit for the default skin base. List styles with
  `scripts/styles.sh` (or see `reference/styles.md`).
- `strength` — optional look intensity, default `1.0` (0 = none, up to ~1.5).
- Prints `skin_dE` (skin ΔE to target — lower is more accurate) so you can report quality.
- Works on a single image. For a folder, loop over files (the API is one-image-per-call).

## Export a skin mask (no grading)

```bash
scripts/mask.sh <input-image> <output.png> [mask-kind]
```
- `mask-kind` — one of `skin` (default), `valid_skin`, `face`, `person`, `hair`,
  `cloth`, `background`.
- Output is an 8-bit grayscale PNG aligned to the input.

## Discover available styles

```bash
scripts/styles.sh
```
Lists every style id, kind (base/flavour), and display name from the live service.

## Constraints (surface these to the user before large jobs)

- Upload limit ~15 MB per image; formats: JPG / PNG / WebP.
- Processing is synchronous (~1s+/image); batch = serial loop.
- On failure the scripts print the HTTP status and error detail and exit non-zero.

For full endpoint/parameter details and error codes, read `reference/api.md`.
