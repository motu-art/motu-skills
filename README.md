# Motu Color Engine — Agent Skill

AI **portrait color grading** (skin-tone anchored) and **skin segmentation** for your
coding agent, via the hosted Motu Color Engine HTTP API. It only changes color — no
smoothing, reshaping, or face swap.

- Grade a portrait to a film / commercial look (`/v1/process`)
- Export a skin mask / matte (`/v1/mask`)
- List available styles (`/v1/styles`)

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
look" or "export the skin mask from photo.jpg". Or call the scripts directly:

```bash
scripts/styles.sh                                   # list styles
scripts/grade.sh photo.jpg graded.png kodak_gold 1.0
scripts/mask.sh  photo.jpg skin.png skin            # skin | valid_skin | face | person
```

## API key

Keys are invite-only during early access. Email **hello@motu.art** with your use case.

## Links

- Developer docs: https://mce.motu.art/developers
- API reference: [reference/api.md](motu-color-engine/reference/api.md)
- Styles overview: [reference/styles.md](motu-color-engine/reference/styles.md)

## License

MIT
