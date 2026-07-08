---
name: motu-color-engine
description: AI portrait color grading, skin-tone correction, optional pro skin smoothing, skin mask export, and ID/passport/headshot/avatar crop generation through the MotuArt Color Engine HTTP API. Use when Codex needs to process portrait photos for film or commercial looks, correct or normalize skin tone, soften pores or blemishes without reshaping identity, export skin/person/face mattes, batch process portrait folders, crop to one-inch/two-inch/passport/visa/headshot specs, or replace an ID-photo background color. Trigger examples include portrait color grading, skin tone, skin smoothing, retouch, skin mask, matte, film look, headshot, ID photo, passport photo, visa photo, crop to size, background color swap, 调色, 肤色, 磨皮, 皮肤蒙版, 人像调色, 证件照, 裁剪, 换底, 一寸, 二寸.
---

# Motu Color Engine

Use Motu Color Engine to process portrait images through the hosted HTTP API. Prefer the bundled scripts in `scripts/` over hand-written `curl` calls unless the user explicitly needs raw API details.

The engine preserves identity. Do not describe it as slimming, reshaping, face swapping, or changing facial structure. Skin smoothing only softens pores and blemishes inside detected skin regions. Cropping repositions and pads to a spec; it never stretches or compresses the face.

## Setup

- Require `curl` and `python3`.
- Read `MCE_API_BASE` from the environment; default is `https://mce.motu.art`.
- Read `MCE_API_KEY` from the environment when auth is enabled; send it only as `X-API-Key`.
- Never hard-code API keys. If a key is missing and the service requires one, ask the user for it or ask them to export it.
- Check service health with `curl -sS "${MCE_API_BASE:-https://mce.motu.art}/v1/health"` when diagnosing connectivity.

## Choose The Workflow

- Use `scripts/grade.sh` when the user wants color grading, skin-tone correction, a film/commercial look, or grading plus optional crop.
- Use `scripts/smooth.sh` when the user wants smoothing only with no color or white-balance change.
- Use `scripts/mask.sh` when the user wants a skin, valid-skin, face, or person mask/matte.
- Use `scripts/crop.sh` when the user wants crop-only ID/passport/visa/headshot/avatar output, optionally with a solid background color.
- Use `scripts/styles.sh` to discover live style ids. Read `references/styles.md` only when the user needs style-selection guidance or offline context.
- Use `scripts/crop-specs.sh` to discover live crop specs. Read `references/crop-specs.md` only when choosing specs or background palettes without live discovery.
- Read `references/api.md` for endpoint parameters, response fields, headers, limits, and error codes.

## Grade Portraits

```bash
scripts/grade.sh <input-image> <output-image> [style-id] [strength] [smooth-strength] [smooth-texture-retain] [crop-spec] [bg-color] [pad-color]
```

- Omit `style-id` for the default skin base, or choose a style from `scripts/styles.sh`.
- Use `strength` for look intensity; default is `1.0`, `0` disables the look, and values up to about `1.5` are stronger.
- Pass `smooth-strength` from `0` to `1` only when the user asks for softened pores or blemishes. Omit it, or pass `0`, to preserve natural texture.
- Use `smooth-texture-retain` from `0` to `1` to keep natural texture over smoothing; default is `0.35`.
- Pass `crop-spec` when the same output should be graded and cropped in one API call.
- Pass `bg-color` only with `crop-spec`; use an allowed palette name such as `white`, `blue`, or `red`, `default`, or explicit `#RRGGBB`.
- Pass `pad-color` only with `crop-spec` when a specific padding color is needed; otherwise let the API edge-replicate.
- Report `skin_dE` from script output when summarizing quality; lower means closer skin color to the target.

For a folder, run the script once per image. Keep batch loops serial unless the user asks for parallelism and accepts API/load implications.

## Smooth Skin Only

```bash
scripts/smooth.sh <input-image> <output.png> [strength] [texture-retain]
```

- Use this for pore/blemish softening without style, color, or white-balance changes.
- Default `strength` is `0.6`.
- Default `texture-retain` is `0.35`; raise it to preserve more natural texture.

## Export Masks

```bash
scripts/mask.sh <input-image> <output.png> [mask-kind]
```

- Use `skin` by default.
- Other mask kinds are `valid_skin`, `face`, and `person`.
- Output is an 8-bit grayscale PNG aligned to the input.

## Crop ID Or Portrait Photos

```bash
scripts/crop.sh <input-image> <output-image> [spec-id] [bg-color] [pad-color]
```

- Default `spec-id` is `one_inch`.
- Use `scripts/crop-specs.sh` to list supported specs and allowed background colors.
- Use `bg-color` only when the spec declares a background palette, mostly ID-photo specs.
- Use `pad-color` only when a source image lacks required margins and the user wants a specific fill.
- Surface crop warnings from script output, especially warnings about margins, resolution, or background limitations.
- Use `grade.sh` with crop arguments when the user wants grading and crop in one output.

## Constraints To Surface

- Upload limit is about 15 MB per image.
- Supported upload formats are JPG, PNG, and WebP.
- Processing is synchronous; batch jobs are repeated one-image calls.
- Background replacement is limited to specs that declare `bg_colors`.
- If a script fails, read its HTTP status and error detail before deciding whether to retry, change arguments, or ask the user for configuration.
