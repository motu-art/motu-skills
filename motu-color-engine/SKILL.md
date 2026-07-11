---
name: motu-color-engine
description: AI portrait color grading, skin-tone correction, identity-preserving skin smoothing, skin/person/face mask export, approved clothing replacement, and ID/passport/headshot/avatar production through the MotuArt Color Engine HTTP API. Use for grading or retouching portraits, normalizing skin tone, exporting mattes, batch-processing portraits, replacing clothing with a server-approved outfit, cropping to ID/passport/visa/headshot specs, replacing an ID-photo background, validating compliance, optimizing upload files, or creating print sheets. Trigger examples include portrait grading, skin tone, retouch, skin mask, outfit replacement, change clothes, ID photo, passport photo, visa photo, headshot, crop to size, background swap, print sheet, 调色, 肤色, 磨皮, 蒙版, 人像调色, 换装, 换衣, 服装替换, 证件照, 裁剪, 换底, 合规检查, 排版, 一寸, 二寸.
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
- Use `scripts/outfit.sh` when the user wants clothing replacement only. The outfit id must come from the server-maintained approved catalog; never accept or invent an arbitrary garment asset.
- Use `scripts/outfits.sh` before clothing replacement to discover currently enabled outfit ids. Do not infer an id from a garment name.
- Use `scripts/id-pack.sh` when the user wants a complete ID/passport photo delivery package: one graded/smoothed master, multiple specs, upload-ready files, compliance report, and optional print sheets.
- Use `scripts/id-check.sh` when the user wants to validate an ID photo against a spec or understand compliance warnings.
- Use `scripts/optimize.sh` when the user needs a website/upload-ready file with format, pixel size, DPI, or maximum KB constraints.
- Use `scripts/print-sheet.sh` when the user wants cropped ID photos laid out on photo paper for printing.
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

## Make ID Photo Packages

```bash
scripts/id-pack.sh <input-image> <output-dir> [specs] [style-id] [smooth-strength] [bg-color] [upload] [print-sheet]
```

- Use this for passport/visa/ID-photo deliverables rather than calling `grade.sh` once per spec. The API generates one graded/smoothed master first, then crops multiple specs from that master so colour and retouching stay consistent.
- `specs` is comma-separated, e.g. `passport_cn,one_inch,us_visa`; default is `passport_cn`. School/enrollment specs include `shanghai_compulsory_education_cn`, `college_graduation_image_cn`, and `national_k12_student_status_cn`.
- Default style is `motu_business_neutral`; pass `smooth-strength` from `0` to `1` only when the user asks for smoothing.
- `bg-color` defaults to `default`, which applies each spec's standard background palette. Use `white`, `blue`, `light_blue`, `red`, or `#RRGGBB` when the user asks and the spec allows it.
- `upload` defaults to `true`, writing upload-optimized JPG files using the spec's `upload` rules from `crop_specs.json`.
- `print-sheet` is optional, e.g. `6x4` or `a4`; when specs have different sizes, separate sheets may be generated.
- Output folder contains `master.png`, `single/`, `upload/`, `print/`, and `report.json`. Surface compliance status and warnings from the report.
- When the user requests a supported outfit, pass its approved catalog id. Outfit replacement runs before the corrected master is generated, so all crop specs share the same clothing result.

## Replace Clothing Only

Discover the approved catalog first:

```bash
scripts/outfits.sh
```

Select only an id returned by that command, then replace clothing:

```bash
scripts/outfit.sh <input-image> <output.png> <approved-outfit-id> [long-edge]
```

- Only use ids returned by `GET /v1/outfits`; the API rejects arbitrary outfit ids and does not accept user-supplied clothing images.
- If the requested clothing is absent, explain that only maintained styles are allowed; do not substitute an arbitrary URL or upload.
- The service protects the detected facial oval with the face mask and calls the configured Motu asynchronous workflow.
- Default output long edge is 1536px; the service bounds requests to 512–2048px.
- Clothing generation must preserve the face and identity. Report upstream failures or timeouts instead of silently returning the original image.

## Check ID Photo Compliance

```bash
scripts/id-check.sh <input-image> [spec-id] [report-json]
```

- Without `report-json`, the input is treated as a source portrait: the API crop-checks it against the spec and reports practical compliance.
- With `report-json`, the input is treated as the already-cropped ID photo and the supplied crop metrics are checked.
- Report failures and warnings plainly; this is a practical QA check, not a government guarantee.

## Optimize Upload Files

```bash
scripts/optimize.sh <input-image> <output-image> [format] [max-kb] [quality] [resize] [dpi]
```

- Use for official website upload limits such as JPG under a maximum KB, exact pixel dimensions, or DPI metadata.
- `format` is `jpg`, `png`, or `webp`; `resize` is `WIDTHxHEIGHT`; lossy formats search quality down to the server default floor when `max-kb` is set.

## Make Print Sheets

```bash
scripts/print-sheet.sh <output-image> <paper> <input1> [input2 ...]
```

- Use after generating cropped ID photos when the user wants a printable sheet.
- `paper` supports common values such as `6x4`, `4x6`, `5x7`, and `a4`. Inputs on a single sheet must have the same pixel size; use `id-pack.sh` for automatic grouping by size.

## Constraints To Surface

- Upload limit is about 15 MB per image.
- Supported upload formats are JPG, PNG, and WebP.
- Processing is synchronous; batch jobs are repeated one-image calls.
- Background replacement is limited to specs that declare `bg_colors`.
- If a script fails, read its HTTP status and error detail before deciding whether to retry, change arguments, or ask the user for configuration.
