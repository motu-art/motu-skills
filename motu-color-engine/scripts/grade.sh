#!/usr/bin/env bash
# Grade a portrait via POST /v1/process and save the graded image.
# Usage: grade.sh <input> <output> [style-id] [strength] [smooth-strength] [smooth-texture-retain]
#   smooth-strength        — optional M15 pro skin smoothing, 0-1 (default: off / 0).
#   smooth-texture-retain  — optional, 0-1, how much pore/texture detail to keep
#                            (default 0.35). Only used when smooth-strength > 0.
set -euo pipefail

BASE="${MCE_API_BASE:-https://mce.motu.art}"
IN="${1:?usage: grade.sh <input> <output> [style-id] [strength] [smooth-strength] [smooth-texture-retain]}"
OUT="${2:?usage: grade.sh <input> <output> [style-id] [strength] [smooth-strength] [smooth-texture-retain]}"
STYLE="${3:-}"
STRENGTH="${4:-1.0}"
SMOOTH_STRENGTH="${5:-}"
SMOOTH_TEXTURE_RETAIN="${6:-}"

[ -f "$IN" ] || { echo "input not found: $IN" >&2; exit 1; }

args=(-sS -A "motu-mce-skill/1.0" -X POST "$BASE/v1/process"
  -F "file=@$IN"
  -F "strength=$STRENGTH"
  -F "output_format=png")
[ -n "$STYLE" ] && args+=(-F "style=$STYLE")
if [ -n "$SMOOTH_STRENGTH" ]; then
  args+=(-F "smooth_strength=$SMOOTH_STRENGTH")
  [ -n "$SMOOTH_TEXTURE_RETAIN" ] && args+=(-F "smooth_texture_retain=$SMOOTH_TEXTURE_RETAIN")
fi
[ -n "${MCE_API_KEY:-}" ] && args+=(-H "X-API-Key: $MCE_API_KEY")

curl "${args[@]}" | python3 -c '
import sys, json, base64
out = sys.argv[1]
try:
    d = json.load(sys.stdin)
except Exception:
    sys.stderr.write("grade failed: non-JSON response from server\n")
    sys.exit(1)
img = d.get("image_base64")
if not img:
    sys.stderr.write("grade failed: %s\n" % d.get("detail", d))
    sys.exit(1)
with open(out, "wb") as f:
    f.write(base64.b64decode(img))
q = (d.get("quality") or {}).get("skin_delta_e_to_target")
print("saved %s  style=%s  skin_dE=%s" % (out, d.get("style_id"), q))
' "$OUT"
