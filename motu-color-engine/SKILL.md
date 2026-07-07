---
name: motu-color-engine
description: >
  AI portrait skin-color grading, optional pro skin smoothing, skin segmentation, and
  purpose-driven ID/portrait photo cropping with background swap, via the MotuArt
  Color Engine HTTP API. Use when the user wants to color-grade / correct skin tone on
  portrait photos, apply a film or commercial look, smooth skin (pores/blemishes),
  batch-grade a folder of portraits, export a skin mask (matte / segmentation) from a
  portrait, or crop a photo to a standard ID/passport/visa/headshot size and change its
  background color. Trigger keywords: portrait color grading, skin tone, skin
  smoothing, retouch, skin mask, matte, film look, headshot, retouch color, id photo,
  passport photo, visa photo, photo crop, crop to size, background color swap, 调色,
  肤色, 磨皮, 皮肤蒙版, 人像调色, 证件照, 裁剪, 换底, 一寸, 二寸.
---

# Motu Color Engine

Portrait **color grading** (skin-tone anchored), optional **pro skin smoothing**,
**skin segmentation**, and **purpose-driven photo cropping** (证件照/形象照/头像 sizes,
with optional background color swap) through a hosted HTTP API. It never reshapes the
face, slims, or swaps identity — smoothing only softens pores/blemishes on the
detected skin region and is off by default; cropping only repositions/pads the frame
to a spec's head ratio and margins, it never stretches or compresses the face.

## Prerequisites

- `curl` and `python3` available (used by the bundled scripts).
- Environment:
  - `MCE_API_BASE` — API base URL. Default `https://mce.motu.art`.
  - `MCE_API_KEY` — API key, if the service has auth enabled. Sent as `X-API-Key`.
    Ask the user for it (or read from env) — never hard-code it.

Quick reachability check: `curl -sS "$MCE_API_BASE/v1/health"` (health needs no key).

## Choosing what to run

- User wants a **graded / recolored** portrait, or a specific look → **grade**.
- User also wants pore/blemish **smoothing** alongside grading → **grade** with the
  smoothing args.
- User wants **smoothing only**, no color change → **smooth**.
- User only wants the **skin mask / matte / segmentation** → **mask** (faster; skips grading).
- User wants a photo cropped to a standard **ID/passport/visa/headshot/avatar size**
  (证件照/形象照/头像), optionally with a solid **background color** → **crop**. If they
  also want the skin graded/corrected, pass the crop args to `grade.sh` (combined in
  one call); if they want the crop alone with no color change, use `crop.sh`.

All scripts live in this skill's `scripts/` folder and take file paths in the workspace.

## Grade a portrait

```bash
scripts/grade.sh <input-image> <output-image> [style-id] [strength] [smooth-strength] [smooth-texture-retain] [crop-spec] [bg-color] [pad-color]
```
- `style-id` — optional; omit for the default skin base. List styles with
  `scripts/styles.sh` (or see `reference/styles.md`).
- `strength` — optional look intensity, default `1.0` (0 = none, up to ~1.5).
- `smooth-strength` — optional M15 pro skin smoothing, `0`-`1`. Omit or `0` to leave
  skin texture untouched (default). Only ask for this if the user wants softened
  pores/blemishes.
- `smooth-texture-retain` — optional, `0`-`1`, how much natural texture to keep on
  top of the smoothing (default `0.35`). Only used when `smooth-strength` > 0.
- `crop-spec` — optional M16 purpose crop spec id (e.g. `one_inch`, `two_inch`,
  `us_visa`). List ids with `scripts/crop-specs.sh` (or see `reference/crop-specs.md`).
  When set, grades **and** crops to that spec in one call. Omit for the full graded
  frame, uncropped.
- `bg-color` — optional background replacement, only used with `crop-spec`: a
  palette name the spec allows (e.g. `white`/`blue`/`red`), `default` for the spec's
  standard color, or an explicit `#RRGGBB`. Omit to keep the original background.
- `pad-color` — optional `#RRGGBB` padding when the source lacks the spec's required
  margin, only used with `crop-spec`. Omit to edge-replicate padding.
- Prints `skin_dE` (skin ΔE to target — lower is more accurate) so you can report quality.
- Works on a single image. For a folder, loop over files (the API is one-image-per-call).

## Smooth skin only (no color grading)

```bash
scripts/smooth.sh <input-image> <output.png> [strength] [texture-retain]
```
- Runs the M15 pro skin-smoothing stage in isolation — softens pores/blemishes on the
  detected skin region without touching color/white balance/style.
- `strength` — default `0.6`. `texture-retain` — default `0.35` (higher keeps more
  natural texture).

## Export a skin mask (no grading)

```bash
scripts/mask.sh <input-image> <output.png> [mask-kind]
```
- `mask-kind` — one of `skin` (default), `valid_skin`, `face`, `person`.
- Output is an 8-bit grayscale PNG aligned to the input.

## Crop to a standard ID / portrait size (no grading)

```bash
scripts/crop.sh <input-image> <output-image> [spec-id] [bg-color] [pad-color]
```
- Standalone purpose crop (M16): decode + face/head geometry + crop only — **no**
  human parsing or color grading, so it's fast, and it defaults to the full-resolution
  source (crop quality is bounded by source resolution, not a latency budget).
- `spec-id` — crop spec id, default `one_inch`. List ids with `scripts/crop-specs.sh`.
  Repositions the frame to the spec's head-ratio/margin standard — never stretches or
  compresses the face.
- `bg-color` — optional background replacement (only for specs that declare a
  palette, mostly `id_photo`): a palette name (e.g. `white`/`blue`/`red`), `default`
  for the spec's standard color, or an explicit `#RRGGBB`. Omit to keep the original
  background.
- `pad-color` — optional `#RRGGBB` padding when the source lacks the spec's required
  margin. Omit to edge-replicate padding.
- Prints the achieved crop geometry/warnings (from `X-MCE-Crop-Info`).
- To grade **and** crop in one call, use `grade.sh`'s `crop-spec`/`bg-color`/`pad-color`
  args instead.

## Discover available styles

```bash
scripts/styles.sh
```
Lists every style id, kind (base/flavour), and display name from the live service.

## Discover crop specs

```bash
scripts/crop-specs.sh
```
Lists every crop spec id, category (`id_photo`/`portrait`/`avatar`), pixel size, and
allowed background colors from the live service (or see `reference/crop-specs.md`).

## Constraints (surface these to the user before large jobs)

- Upload limit ~15 MB per image; formats: JPG / PNG / WebP.
- Processing is synchronous (~1s+/image); batch = serial loop.
- Background color swap is only available for crop specs that declare a palette
  (`bg_colors` in `scripts/crop-specs.sh` output) — mostly `id_photo` specs; most
  `portrait`/`avatar` specs keep the original background.
- On failure the scripts print the HTTP status and error detail and exit non-zero.

For full endpoint/parameter details and error codes, read `reference/api.md`.
