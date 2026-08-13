# MotuArt Color Engine — Portrait Workflow Agent Skill

A production portrait workflow for AI agents, powered by the hosted MotuArt Color Engine
HTTP API. Create **professional AI headshots** from a confirmed identity reference, apply
skin-tone-first **portrait color grading** and **portrait relighting**, smooth detected skin
without reshaping the face, export skin/person masks, replace clothing with approved outfits,
and deliver **ID/passport photos** with compliance checks, upload optimization and print sheets.

The workflow is designed to preserve a recognizable identity and natural skin texture.
Grading and smoothing never slim or reshape the face; cropping only repositions or pads the
frame to a selected specification. AI-generated headshot candidates must still be reviewed
for identity, clothing, lighting and composition before professional use.

## Start here

- [Developer documentation](https://mce.motu.art/en/developers?utm_source=github&utm_medium=referral&utm_campaign=offsite_a08_202608&utm_content=a08_009_skill_developers)
- [Professional AI headshots](https://mce.motu.art/en/headshots?utm_source=github&utm_medium=referral&utm_campaign=offsite_a08_202608&utm_content=a08_009_skill_headshots)
- [ID Photo Maker](https://mce.motu.art/en/id-photo?utm_source=github&utm_medium=referral&utm_campaign=offsite_a08_202608&utm_content=a08_009_skill_id_photo)
- [Portrait grading and relighting](https://mce.motu.art/en/portrait?utm_source=github&utm_medium=referral&utm_campaign=offsite_a08_202608&utm_content=a08_009_skill_portrait)

- Grade a portrait to a film / commercial look (`/v1/process`), optionally with
  pro skin smoothing layered on
- Smooth skin only, no color change (`/v1/smooth`)
- Export a skin mask / matte (`/v1/mask`)
- Crop to a standard ID/passport/visa/headshot/avatar size, with optional
  background color swap (`/v1/crop`, or combined with grading via `/v1/process`)
- Generate an ID-photo delivery package from one master: standard singles,
  upload-ready files, print sheets and compliance status (`/v1/id-pack`)
- List curated outfits by men, women, kids and unisex categories (`/v1/outfits`)
- Replace clothing with a curated outfit while preserving identity (`/v1/outfit`)
- Build professional AI headshot projects from one confirmed identity reference, choose
  compatible scenes, poses, outfits and backgrounds, review candidates, then grade,
  relight, crop and export selected results (`/v1/headshots/*`)
- Check ID-photo compliance against a crop spec (`/v1/id-check`)
- Optimize upload files by format, size, DPI and KB target (`/v1/optimize`)
- Layout same-size ID photos on 6x4 / 4x6 / A4 paper (`/v1/print-sheet`)
- List available styles (`/v1/styles`) and crop specs (`/v1/crop/specs`)

This is a standard [Agent Skill](https://agentskills.io) (`SKILL.md`), compatible with
Claude Code, Codex CLI, Cursor, Gemini CLI, OpenClaw, ZCode, Augment, Windsurf,
Cline, Roo Code and other Agent Skills-compatible tools.

## Install

### Option A — Claude Code plugin marketplace

```text
/plugin marketplace add motu-art/motu-skills
/plugin install motu-color-engine@motu-skills
```

### Option B — drop-in installation

Download and extract the package into the skills directory used by your tool:

| Tool | Skills directory |
| --- | --- |
| Claude Code | `~/.claude/skills` |
| Codex CLI | `~/.codex/skills` |
| Cursor | `~/.cursor/skills` or project `.cursor/skills` |
| Gemini CLI | `~/.gemini/skills` |
| OpenClaw | `~/.openclaw/skills` |
| ZCode | `~/.zcode/skills` |
| Augment | `~/.augment/skills` |
| Windsurf | `~/.codeium/windsurf/skills` |
| Cline / Roo Code | project `.agents/skills` when supported |

```bash
SKILLS_DIR=~/.claude/skills        # choose the directory for your tool
mkdir -p "$SKILLS_DIR"
curl -fsSL https://mce.motu.art/downloads/motu-color-engine-skill.tar.gz \
  | tar -xz -C "$SKILLS_DIR"
```

## Configure

```bash
export MCE_API_BASE=https://mce.motu.art   # default; can omit
export MCE_API_KEY=<your-key>              # create at https://mce.motu.art/en/account
```

Requires `curl` and `python3`.

## Use

Ask your agent in natural language. For example:

- “Create four professional LinkedIn headshot candidates, let me approve the identity
  reference first, then grade and export the selected result.”
- “Relight this portrait with natural dimension without changing the face.”
- “Make passport and one-inch ID photos with a navy business suit, upload files and a
  6×4 print sheet.”
- “Export aligned skin and person masks from this portrait.”

The agent reads [`motu-color-engine/SKILL.md`](motu-color-engine/SKILL.md) to choose the
workflow, enforce review stages and use the current argument contract. The table below is
the human-facing map; the Skill file and linked references are the source of truth.

| Need | Script |
|---|---|
| Discover grading styles or crop specifications | `styles.sh`, `crop-specs.sh` |
| Grade, smooth, relight or export masks | `grade.sh`, `smooth.sh`, `portrait-lighting.sh`, `mask.sh` |
| Crop a single ID/portrait image | `crop.sh` |
| Build a complete ID/passport delivery package | `id-pack.sh` |
| Check compliance, optimize uploads or create print sheets | `id-check.sh`, `optimize.sh`, `print-sheet.sh` |
| Discover and apply approved clothing | `outfits.sh`, `outfit.sh` |
| Create and finish professional AI headshots | `headshots.sh` |

### Direct script examples

```bash
scripts/styles.sh                                   # list styles
scripts/grade.sh photo.jpg graded.png kodak_gold 1.0
scripts/grade.sh photo.jpg graded.png kodak_gold 1.0 0.6 0.35  # + pro skin smoothing
scripts/smooth.sh photo.jpg smoothed.png 0.6 0.35   # smoothing only, no color change
scripts/portrait-lighting.sh photo.jpg lit.png natural_dimension 0.7
scripts/mask.sh  photo.jpg skin.png skin            # skin | valid_skin | face | person
scripts/crop-specs.sh                               # list crop specs (ID/portrait/avatar sizes)
scripts/crop.sh photo.jpg id.png one_inch white      # crop-only + background swap, no grading
scripts/grade.sh photo.jpg id.png motu_korean_id 1.0 0 0 one_inch white  # grade + crop combined
scripts/outfits.sh                                  # list approved outfits by category
scripts/outfit.sh photo.jpg outfitted.png business_navy_suit 1536

# ID photo delivery helpers
scripts/id-pack.sh photo.jpg out passport_cn,one_inch motu_business_neutral 0.35 default true 6x4 business_navy_suit 1536
scripts/id-check.sh out/single/one_inch.png one_inch
scripts/optimize.sh out/single/one_inch.png one_inch_upload.jpg jpg 100 300
scripts/print-sheet.sh sheet.jpg 6x4 out/single/one_inch.png
```

### Professional AI Headshots workflow

Headshots are intentionally staged. The agent must not silently confirm an identity
reference or hide asynchronous generation inside one long command.

```bash
# 1. Discover compatible scenes, poses, outfits, backgrounds and generation styles.
scripts/headshots.sh catalog en

# 2. Prepare a purpose-cropped identity reference and review the generated preview.
scripts/headshots.sh prepare portrait.jpg headshot-work \
  --scene professional_profile --skin-base motu_business_neutral --smoothing 0.2

# 3. Run only after the user approves headshot-work/reference-preview.png.
scripts/headshots.sh confirm headshot-work

# 4. Submit an asynchronous candidate batch. Omitted options use live recommendations.
scripts/headshots.sh generate headshot-work \
  --scene professional_profile --batch-size 4 --ratio 4:5 --framing half_body

# 5. Check explicitly, then download completed or partially completed candidates.
scripts/headshots.sh status headshot-work
scripts/headshots.sh download headshot-work

# 6. Post-process and export only a user-selected candidate.
scripts/headshots.sh render headshot-work --candidate 1 --style motu_business_neutral
scripts/headshots.sh light headshot-work --candidate 1 --style natural_dimension --strength 0.7 --render
scripts/headshots.sh export headshot-work --candidate 1 --render --crop profile_4x5 --format jpeg --quality 92
```

Confirmed people can be reused without overwriting project history:

```bash
scripts/headshots.sh people 20
scripts/headshots.sh start-person <person-reference-id> new-headshot-work --scene professional_profile
scripts/headshots.sh use-person existing-headshot-work <person-reference-id>
scripts/headshots.sh remove-person <person-reference-id>  # library entry only; projects remain
```

Review `source-check.json` and `reference-preview.png` before confirmation. Generate only
from live catalog ids; custom generation prompts are not accepted. Generation consumes
credits per requested image, may complete partially, and should never be retried unchanged
after `402 insufficient_credits`. See
[`references/headshots-api.md`](motu-color-engine/references/headshots-api.md) for the full
state model, parameters and API responses.

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

The passport/visa catalog pairs both purposes for CN, US, JP, CA, GB, MY, TH, VN,
PH, AU, KR and SG. Common ids include `passport_cn`, `china_visa`,
`us_passport_printed`, `us_visa`, `japan_passport`, `japan_visa`,
`canada_passport_printed`, `canada_visa`, `korea_passport`, and `korea_visa`.
Run `scripts/crop-specs.sh` for the current list and inspect each spec's processing
policy: some application routes require live capture and some prohibit edited or
AI-altered photographs.

## Outfit workflow

Run `scripts/outfits.sh` to discover the current curated catalog. Each item includes a
stable id, localized name and description, category (`male`, `female`, `kids`, or
`unisex`), availability, and optional preview image. Use only an id returned by the
catalog; custom prompts and arbitrary outfit ids are not accepted.

Use `scripts/outfit.sh` for clothing replacement only, or pass the optional outfit id to
`scripts/id-pack.sh`. In an ID-photo package, outfit replacement runs before the corrected
master is created, so every crop, upload file and print sheet uses the same clothing result.
The default generation long edge is 1536px and the supported range is 512–2048px.

## API key

Sign in with an email verification code at **https://mce.motu.art/en/account** and create a
dedicated key. The full value is displayed once: copy it immediately, store it securely,
and export it as `MCE_API_KEY`; never commit it or paste it into chat. Grant only the scopes
the workflow needs. ID-photo packages with outfit replacement require both
`id-photo:process` and `outfit:process`; private Headshots projects and generation require
`headshot:process`. Calls consume the account's available credits.

## Links

- Web product: https://mce.motu.art/en/headshots
- Developer docs: https://mce.motu.art/en/developers
- Privacy policy: https://mce.motu.art/en/privacy
- Image credits: https://mce.motu.art/en/credits
- API reference: [references/api.md](motu-color-engine/references/api.md)
- Headshots API and state model: [references/headshots-api.md](motu-color-engine/references/headshots-api.md)
- Styles overview: [references/styles.md](motu-color-engine/references/styles.md)
- Crop specs overview: [references/crop-specs.md](motu-color-engine/references/crop-specs.md)
- Community: [MotuArt Community on Discord](https://discord.gg/v8xMR2hK9)

## License

MIT
