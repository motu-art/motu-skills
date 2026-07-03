#!/usr/bin/env bash
# Grade a portrait via POST /v1/process and save the graded image.
# Usage: grade.sh <input> <output> [style-id] [strength]
set -euo pipefail

BASE="${MCE_API_BASE:-https://mce.motu.art}"
IN="${1:?usage: grade.sh <input> <output> [style-id] [strength]}"
OUT="${2:?usage: grade.sh <input> <output> [style-id] [strength]}"
STYLE="${3:-}"
STRENGTH="${4:-1.0}"

[ -f "$IN" ] || { echo "input not found: $IN" >&2; exit 1; }

args=(-sS -A "motu-mce-skill/1.0" -X POST "$BASE/v1/process"
  -F "file=@$IN"
  -F "strength=$STRENGTH"
  -F "output_format=png")
[ -n "$STYLE" ] && args+=(-F "style=$STYLE")
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
