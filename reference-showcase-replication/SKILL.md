---
name: reference-showcase-replication
description: Analyze a user-provided portrait reference image and reproduce its visual setup as a Motu Color Engine headshot showcase. Use when asked to create, add, replicate, refine, or place a 精选案例/形象照案例 from a reference image, including adding missing pose, outfit, background, compatibility and Hero assets, generating previews with repository-default identities, comparing results with the reference, and preparing assets for publishing.
---

# Reference Showcase Replication

Create a structured headshot showcase from a visual reference without using the reference person's identity for generation.

## Hard rules

- Use the reference only for visual analysis and final comparison.
- Never pass it to `--identity`, `--identity-female`, an image provider, or another generation input.
- Always use the default identities in `tools/headshot_preview_assets.py`.
- Generate exactly one candidate with `--candidates 1`.
- Skip manual picking. Let `export` consume the sole `candidate-*.png`; do not create `pick.png`.
- Prefer adequate existing catalog resources. Add an item only for a meaningful visual gap.
- Do not upload or deploy unless the user explicitly requests publishing and an authorized mechanism exists.

## Inspect the reference

Confirm the repository contains:

- `tools/headshot_preview_assets.py`
- `assets/mce/headshots/{catalog,scenes,generation-styles,poses,backgrounds,showcases}.json`
- `assets/mce/outfits.json`

Inspect the local image and record only the visual setup:

- gender variant;
- body angle, seated/standing state, forearms, hands and asymmetry;
- garment silhouette, collar, neckline, sleeves, layers, waist, color and fabric;
- backdrop color, texture, furniture and props;
- key-light direction, fill ratio, rim/backlight, halo and contrast;
- framing, subject scale, output ratio and likely business use.

Do not model or describe the reference person's identity.

## Build a compatible recipe

Resolve:

```text
scene_id
generation_style_id
pose_id
outfit_id
background_id
framing
output_ratio
```

Check enabled states and the selected scene's `compatibility` lists. Inspect the scene's `lighting_prompt`; do not select a scene whose fixed rim/backlight conflicts with the reference. Check `allowed_framings_for_pose`.

A showcase may also serve additional scenes: set optional `configuration.scene_ids` (primary `scene_id` first). Every listed scene must whitelist the recipe's style/pose/background/outfit in its `compatibility`; the loader validates each one. Omit `scene_ids` for single-scene showcases (the loader defaults it to `[scene_id]`).

For desk-dependent poses, also update `_POSE_MIN_FRAMING`, `_DESK_POSES`, and `_DESK_BACKGROUNDS` in `src/mce/headshot_catalog.py` as applicable.

## Add missing resources

Add missing items to the relevant JSON:

- pose: four translations, prompt, order, enabled state;
- background: four translations, prompt, order, enabled state;
- outfit: category, names/descriptions, `products: ["headshot"]`, garment prompts and presentation prompt.

Write prompts from observable construction rather than broad style labels. Be explicit about collar geometry, sleeve endpoint, hand placement, body rotation, light direction and forbidden alternatives when those details matter.

Keep pose prompts identity-agnostic: describe body, arm and hand geometry only, never hairstyle, hair length or hair color — those belong to the identity layer. A gesture constraint (for example "touch the hair at the temple without pulling it forward") is fine; prescribing where hair lies is not.

Append new IDs to every intended scene compatibility list.

Keep the shared integer version identical in all five files:

```text
catalog.json
scenes.json
generation-styles.json
poses.json
backgrounds.json
```

Increment `outfits.json` independently. Validate JSON before generation.

Generate only new or changed dependencies:

```bash
.venv/bin/python tools/headshot_preview_assets.py generate \
  --only poses,backgrounds,outfits \
  --item POSE_ID,BACKGROUND_ID,OUTFIT_ID \
  --candidates 1

.venv/bin/python tools/headshot_preview_assets.py export \
  --only poses,backgrounds,outfits \
  --item POSE_ID,BACKGROUND_ID,OUTFIT_ID \
  --apply
```

Remove absent collections and IDs. Add `--force` only when regenerating a changed prompt. Never add identity arguments.

## Add and generate the showcase

Add a stable lowercase-underscore entry to `showcases.json` with:

- `order`, `enabled`, `featured`, `gender`;
- complete `zh-CN`, `en`, `ja`, `ko` copy;
- `preview_url: null` before export;
- the complete recipe.

Increment the showcase version and update hard-coded version, count and recipe assertions in tests.

```bash
.venv/bin/python tools/headshot_preview_assets.py generate \
  --only showcases \
  --item SHOWCASE_ID \
  --candidates 1

.venv/bin/python tools/headshot_preview_assets.py export \
  --only showcases \
  --item SHOWCASE_ID \
  --apply
```

Use `--force` for a revised recipe or dependency prompt.

If Azure moderation blocks a benign task, allow the tool's retries and retry the task once. After two task-level failures, inspect and narrow the responsible style/prompt combination; do not bypass moderation or substitute the user's reference image.

## Compare and refine

Inspect the exported WebP beside the reference. Compare:

- pose silhouette, body rotation and hand location;
- collar, neckline, sleeves, waist and garment construction;
- background, table/props and subject separation;
- key/fill balance, rim light, halo and color temperature;
- framing and subject scale.

Change the narrowest responsible layer:

- wrong hands/body angle → pose;
- wrong collar/sleeves/silhouette → outfit;
- wrong table/backdrop → background;
- wrong rim/backlight → scene lighting choice and background constraints;
- wrong crop → framing.

Regenerate the changed dependency and showcase. Report remaining differences honestly.

## Add to Hero when requested

Hero has two layers:

- generation config: `assets/mce/headshots/hero-assets.json`;
- frontend carousel: `web/app/lib/gallery.ts` plus `web/public/headshots/hero/`.

For a newly generated Hero pair, use `generate-hero` then `export-hero --apply`.

If the user explicitly requests direct reuse, do not call the provider:

1. Reuse an existing default-identity Hero before frame.
2. Copy the exported showcase WebP as the new Hero after frame.
3. Add both local public assets and the matching `hero-assets.json` URLs.
4. Add the pair and localized alt text to `headshotPairs`.
5. Add OSS mappings to `assets/mce/headshots/previews/upload-manifest.json`.

## Validate and hand off

Run:

```bash
.venv/bin/python -m pytest \
  tests/test_headshot_catalog.py \
  tests/test_headshot_showcases.py \
  tests/test_headshot_service.py
```

Run `npm run build` in `web/` when Hero or frontend files change.

Inspect `assets/mce/headshots/previews/upload-manifest.json`. Upload only when requested. Note that the landing page displays eight enabled showcases: `featured: true` first, newest (highest `order`) first within each group. Non-featured items appear only after all featured ones; the showcases index page still lists everything by ascending `order`.
