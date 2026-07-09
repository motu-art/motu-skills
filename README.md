# MotuArt Color Engine — Agent Skill

AI **portrait color grading** (skin-tone anchored), optional **pro skin smoothing**,
**skin segmentation**, **purpose-driven photo cropping**, and complete **ID/passport
photo delivery packages** for your coding agent, via the hosted MotuArt Color Engine
HTTP API. It never reshapes the face, slims, or swaps identity — skin smoothing only
softens pores/blemishes on the detected skin region and is off by default; cropping only
repositions/pads the frame to a spec's head ratio and margins.

- Grade a portrait to a film / commercial look (`/v1/process`), optionally with
  pro skin smoothing layered on
- Smooth skin only, no color change (`/v1/smooth`)
- Export a skin mask / matte (`/v1/mask`)
- Crop to a standard ID/passport/visa/headshot/avatar size, with optional
  background color swap (`/v1/crop`, or combined with grading via `/v1/process`)
- Generate an ID-photo delivery package from one master: standard singles,
  upload-ready files, print sheets and compliance status (`/v1/id-pack`)
- Check ID-photo compliance against a crop spec (`/v1/id-check`)
- Optimize upload files by format, size, DPI and KB target (`/v1/optimize`)
- Layout same-size ID photos on 6x4 / 4x6 / A4 paper (`/v1/print-sheet`)
- List available styles (`/v1/styles`) and crop specs (`/v1/crop/specs`)

This is a standard [Agent Skill](https://agentskills.io) (`SKILL.md`), compatible with
Claude Code, Codex CLI, ZCode, OpenClaw, Augment, Windsurf and more.

## Install

### Option A — Claude Code plugin marketplace

```
/plugin marketplace add motu-art/motu-skills
/plugin install motu-color-engine@motu-skills
```

### Option B — any agent (drop-in)

Download and extract into your agent's skills directory:

| Agent       | Skills directory              |
| ----------- | ----------------------------- |
| Claude Code | `~/.claude/skills`            |
| Codex CLI   | `~/.codex/skills`             |
| ZCode       | `~/.zcode/skills`             |
| OpenClaw    | `~/.openclaw/skills`          |
| Augment     | `~/.augment/skills`           |
| Windsurf    | `~/.codeium/windsurf/skills`  |

```bash
SKILLS_DIR=~/.claude/skills        # pick your agent's dir from the table
mkdir -p "$SKILLS_DIR"
curl -fsSL https://mce.motu.art/downloads/motu-color-engine-skill.tar.gz \
  | tar -xz -C "$SKILLS_DIR"
```

## Configure

```bash
export MCE_API_BASE=https://mce.motu.art   # default; can omit
export MCE_API_KEY=<your-key>              # invite-only, see below
```

Requires `curl` and `python3`.

## Use

Just ask your agent in natural language, e.g. "grade these portraits with a warm film
look", "export the skin mask from photo.jpg", or "make passport and one-inch ID photos
with upload and print versions". Or call the scripts directly:

```bash
scripts/styles.sh                                   # list styles
scripts/grade.sh photo.jpg graded.png kodak_gold 1.0
scripts/grade.sh photo.jpg graded.png kodak_gold 1.0 0.6 0.35  # + pro skin smoothing
scripts/smooth.sh photo.jpg smoothed.png 0.6 0.35   # smoothing only, no color change
scripts/mask.sh  photo.jpg skin.png skin            # skin | valid_skin | face | person
scripts/crop-specs.sh                               # list crop specs (ID/portrait/avatar sizes)
scripts/crop.sh photo.jpg id.png one_inch white      # crop-only + background swap, no grading
scripts/grade.sh photo.jpg id.png motu_korean_id 1.0 0 0 one_inch white  # grade + crop combined

# ID photo delivery helpers
scripts/id-pack.sh photo.jpg out passport_cn,one_inch default 0.35 6x4
scripts/id-check.sh out/single/one_inch.png one_inch
scripts/optimize.sh out/single/one_inch.png one_inch_upload.jpg jpg 100 300
scripts/print-sheet.sh out/single/one_inch.png sheet.jpg 6x4
```


## ID photo workflow

For passports, visas and one-inch/two-inch document photos, prefer `id-pack.sh` when you
need multiple outputs from the same portrait. The API creates one corrected master first,
then crops each requested spec from that master so skin tone, background replacement and
light smoothing stay consistent.

Typical package contents:

- `single/` — standard PNG/JPG files for each selected crop spec;
- `upload/` — upload-optimized files when `upload=true` is requested;
- `print/` — 6x4 / 4x6 / A4 print sheets when a paper size is requested;
- JSON metadata with trace id, crop info, compliance status and warnings.

Common spec ids include `passport_cn`, `id_card_cn`, `one_inch`, `two_inch`, `us_visa`,
`schengen_visa`, `japan_visa` and `canada_visa`. Run `scripts/crop-specs.sh` for the
current list.

## API key

Keys are invite-only during early access. Email **hi@motu.art** with your use case.

## Links

- Developer docs: https://mce.motu.art/developers
- API reference: [references/api.md](motu-color-engine/references/api.md)
- Styles overview: [references/styles.md](motu-color-engine/references/styles.md)
- Crop specs overview: [references/crop-specs.md](motu-color-engine/references/crop-specs.md)
- Community: [MotuArt Community on Discord](https://discord.gg/v8xMR2hK9)

## License

MIT
