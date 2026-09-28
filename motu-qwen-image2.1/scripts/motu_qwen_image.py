#!/usr/bin/env python3
"""Generate and edit images through the motu.art Qwen Image 2.1 workflow API.

Usage:
  motu_qwen_image.py generate --prompt "..." [--size portrait] [--batch-size 1]
                              [--seed N] [--out image.png]
  motu_qwen_image.py edit --image person.png [--image shirt.png ...] --prompt "..."
                              [--size portrait] [--out edited.png]
  motu_qwen_image.py status --request-id <uuid>

edit takes 1-8 reference images (local paths or http(s) URLs) mapped to
image1..image8; reference them in the prompt as <image1>, <image2>, ... .
Local files are compressed with macOS `sips` before upload — the edit canvas
tops out at 2048px, so the long edge is capped at 2048 and anything still over
10 MB is re-encoded as JPEG q85 — then uploaded through the OSS presign route
(base64 data URIs fail silently in processing, so locals always go through OSS).

Requires MOTU_KEY in the environment. Pass --dry-run to print the request
without sending it (no API quota consumed).
"""

import argparse
import json
import mimetypes
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

API_BASE = os.environ.get("MOTU_API_BASE", "https://api.motu.art")
WORKFLOW_T2I = "image_qwen_image_2_1_t2i"
WORKFLOW_EDIT = "image_qwen_image_2_1_image_edit"

EDIT_MAX_IMAGES = 8
# The edit model's canvas maxes at 2048px, so a larger reference only bloats
# the upload; over-10 MB files are re-encoded JPEG q85 to stay gateway-safe.
EDIT_MAX_EDGE = 2048
EDIT_MAX_BYTES = 10 * 1024 * 1024
HAS_SIPS = shutil.which("sips") is not None  # reference-image compression tool

# Composition canvases; output is EXACTLY the requested size (no upscaling).
# API accepts 512-2048 per side.
SIZE_PRESETS = {
    "square": (1024, 1024),        # API default
    "portrait": (1024, 1536),      # 2:3 vertical, posters
    "landscape": (1536, 1024),     # 3:2 horizontal
    "story": (1152, 2048),         # 9:16 vertical, social story size
    "banner": (2048, 1152),        # 16:9 wide, web hero
    "square-2k": (2048, 2048),     # max-detail canvases
    "portrait-2k": (1536, 2048),
    "landscape-2k": (2048, 1536),
}


def api_key():
    key = os.environ.get("MOTU_KEY", "").strip()
    if not key:
        sys.exit("MOTU_KEY is not set. Export it first (see .envrc).")
    return key


def http(method, url, body=None, headers=None, timeout=120):
    req = urllib.request.Request(url, method=method)
    # Kong rejects urllib's default UA; send a neutral one.
    req.add_header("User-Agent", "motu-qwen-image/1.0")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    data = None
    if body is not None:
        data = json.dumps(body).encode() if isinstance(body, (dict, list)) else body
    try:
        with urllib.request.urlopen(req, data=data, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def authed_headers():
    return {"Authorization": f"Bearer {api_key()}", "Content-Type": "application/json"}


def resolve_canvas(args):
    width, height = args.width, args.height
    if args.size:
        if width is not None or height is not None:
            sys.exit("pass either --size or --width/--height, not both")
        width, height = SIZE_PRESETS[args.size]
    if width is None and height is None:
        width, height = SIZE_PRESETS["square"]  # API default 1024x1024
    elif width is None or height is None:
        sys.exit("give both --width and --height (or use --size)")
    for name, v in (("width", width), ("height", height)):
        if not 512 <= v <= 2048:
            sys.exit(f"{name} must be 512-2048 (got {v})")
    return width, height


def build_payload(args):
    if len(args.prompt) > 6000:
        sys.exit(f"prompt too long ({len(args.prompt)} chars, max 6000)")
    width, height = resolve_canvas(args)
    if not 1 <= args.batch_size <= 4:
        sys.exit("--batch-size must be 1-4")
    p = {"prompt": args.prompt, "width": width, "height": height,
         "batch_size": args.batch_size}
    if args.seed is not None:
        p["seed"] = args.seed
    if args.priority:
        p["priority"] = args.priority
    return p


def submit(payload, workflow, dry_run=False):
    url = f"{API_BASE}/workflows/{workflow}"
    if dry_run:
        print(json.dumps({"POST": url, "body": payload}, indent=2, ensure_ascii=False))
        return None
    status, raw = http("POST", url, body=payload, headers=authed_headers())
    if status not in (200, 202):
        sys.exit(f"submit failed [{status}]: {raw.decode(errors='replace')}")
    return json.loads(raw)


def poll_once(request_id):
    # Docs also show GET /workflows/status/{id}; that path form 500s on the
    # gateway — the query-param form below is the one verified working.
    url = f"{API_BASE}/workflow/status?workflow_request_id={urllib.parse.quote(request_id)}"
    status, raw = http("GET", url, headers=authed_headers())
    if status != 200:
        sys.exit(f"status failed [{status}]: {raw.decode(errors='replace')}")
    return json.loads(raw)


def poll(request_id, interval=5, timeout=900):
    deadline = time.time() + timeout
    while True:
        info = poll_once(request_id)
        state = info.get("status")
        print(f"status: {state}", file=sys.stderr)
        if state in ("completed", "success"):
            return info
        if state in ("failed", "error"):
            sys.exit(f"generation failed: {json.dumps(info, ensure_ascii=False)}")
        if time.time() > deadline:
            sys.exit(f"timed out after {timeout}s waiting for {request_id}")
        time.sleep(interval)


def upload_file(path):
    """Upload a local file via the OSS presigned-url route; return a public GET URL (14-day)."""
    ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
    status, raw = http(
        "POST", f"{API_BASE}/oss/presigned-url",
        body={"fileType": ctype}, headers=authed_headers(),
    )
    if status != 200:
        sys.exit(f"presigned-url failed [{status}]: {raw.decode(errors='replace')}")
    info = json.loads(raw)
    with open(path, "rb") as f:
        data = f.read()
    # The PUT URL is signed with this Content-Type; it must match exactly.
    put_req = urllib.request.Request(info["uploadUrl"], data=data, method="PUT")
    put_req.add_header("Content-Type", ctype)
    with urllib.request.urlopen(put_req, timeout=300) as resp:
        if resp.status not in (200, 201):
            sys.exit(f"OSS upload failed [{resp.status}]")
    return info["url"]


def image_size(path):
    """(width, height) via macOS `sips`; None when unavailable or unreadable."""
    if not HAS_SIPS:
        return None
    r = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", path],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None
    dims = {}
    for line in r.stdout.splitlines():
        k, _, v = line.partition(":")
        if k.strip() in ("pixelWidth", "pixelHeight"):
            dims[k.strip()] = int(v)
    w, h = dims.get("pixelWidth"), dims.get("pixelHeight")
    return (w, h) if w and h else None


def run_sips(src, dst, resize=False, fmt=None, fmt_opts=None):
    cmd = ["sips"]
    if resize:
        cmd += ["-Z", str(EDIT_MAX_EDGE)]  # downscale so no side exceeds EDIT_MAX_EDGE
    if fmt:
        cmd += ["-s", "format", fmt]
    if fmt_opts:
        cmd += ["-s", "formatOptions", fmt_opts]
    cmd += [src, "--out", dst]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not os.path.isfile(dst):
        sys.exit(f"sips failed on {src}: {(r.stderr or r.stdout).strip()}")


def shrink_image(path, tmpdir):
    """Bring a local reference image to an API-friendly size/format; returns the path
    to submit (the original when it is already fine, else a compressed copy in tmpdir).

    Larger than 2048px on the long edge only inflates the upload — the edit canvas
    tops out at 2048 — and very large files risk gateway body limits, so: cap the
    long edge at 2048, normalize exotic formats to png, and re-encode anything
    still over 10 MB as JPEG q85.
    """
    ext = os.path.splitext(path)[1].lower()
    dims = image_size(path)
    oversized = bool(dims and max(dims) > EDIT_MAX_EDGE)
    if not oversized and ext in (".png", ".jpg", ".jpeg") \
            and os.path.getsize(path) <= EDIT_MAX_BYTES:
        return path
    if not HAS_SIPS:
        print(f"warning: sips unavailable, uploading {path} uncompressed", file=sys.stderr)
        return path
    stem = os.path.splitext(os.path.basename(path))[0]
    out_png = os.path.join(tmpdir, f"{stem}_ref.png")
    run_sips(path, out_png, resize=oversized, fmt="png")
    if os.path.getsize(out_png) <= EDIT_MAX_BYTES:
        return out_png
    # Still heavy (big flat png) — flatten to JPEG q85.
    out_jpg = os.path.join(tmpdir, f"{stem}_ref.jpg")
    run_sips(out_png, out_jpg, fmt="jpeg", fmt_opts="85")
    return out_jpg


def resolve_reference(value, tmpdir, dry_run=False):
    """Accept an http(s) URL or a local file path; compress + upload locals, return the URL.
    With dry_run, locals are compressed but not uploaded (a placeholder goes in the payload)."""
    if value.startswith(("http://", "https://")):
        return value
    if not os.path.isfile(value):
        sys.exit(f"image not found: {value}")
    prepped = shrink_image(value, tmpdir)
    if prepped != value:
        print(f"compressed {value} -> {prepped} "
              f"({os.path.getsize(value)} -> {os.path.getsize(prepped)} bytes)", file=sys.stderr)
    if dry_run:
        return f"<local file, would upload: {prepped}>"
    print(f"Uploading {prepped} ...", file=sys.stderr)
    return upload_file(prepped)


def download(url, out_path):
    print(f"Downloading -> {out_path}", file=sys.stderr)
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "motu-qwen-image/1.0")
    with urllib.request.urlopen(req, timeout=600) as resp, open(out_path, "wb") as f:
        while True:
            chunk = resp.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)
    return out_path


def run_job(payload, workflow, args, default_stem):
    queued = submit(payload, workflow, dry_run=args.dry_run)
    if args.dry_run:
        return
    request_id = queued.get("workflow_request_id")
    print(f"queued: {request_id}", file=sys.stderr)
    if args.no_wait:
        print(json.dumps(queued, indent=2))
        return
    info = poll(request_id, interval=args.poll_interval, timeout=args.timeout)
    results = info.get("result") or []
    if not results:
        sys.exit(f"completed but no result URLs: {json.dumps(info, ensure_ascii=False)}")

    stem = args.out[:-4] if args.out and args.out.lower().endswith(".png") else (
        args.out or f"{default_stem}_{request_id[:8]}")
    outs = []
    for i, r in enumerate(results, 1):
        path = f"{stem}.png" if len(results) == 1 else f"{stem}_{i}.png"
        download(r["url"], path)
        outs.append({"path": path, "width": r.get("width"), "height": r.get("height"),
                     "file_size": r.get("file_size")})
    print(json.dumps({"outs": [o["path"] for o in outs], "request_id": request_id,
                      "results": outs}, ensure_ascii=False))


def cmd_generate(args):
    run_job(build_payload(args), WORKFLOW_T2I, args, "image")


def cmd_edit(args):
    if len(args.image) > EDIT_MAX_IMAGES:
        sys.exit(f"edit accepts at most {EDIT_MAX_IMAGES} images (got {len(args.image)})")
    if len(args.image) > 1 and "<image" not in args.prompt:
        print("tip: reference each image in the prompt as <image1>, <image2>, ... "
              "(order = --image order).", file=sys.stderr)
    tmpdir = tempfile.mkdtemp(prefix="motu_qwen_edit_")
    try:
        payload = build_payload(args)
        for i, img in enumerate(args.image, 1):
            payload[f"image{i}"] = resolve_reference(img, tmpdir, dry_run=args.dry_run)
        run_job(payload, WORKFLOW_EDIT, args, "edit")
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def cmd_status(args):
    print(json.dumps(poll_once(args.request_id), indent=2, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add_common(p):
        p.add_argument("--prompt", required=True, help="prose prompt, max 6000 chars")
        p.add_argument("--size", choices=sorted(SIZE_PRESETS),
                       help=f"preset: {', '.join(f'{k} {v[0]}x{v[1]}' for k, v in sorted(SIZE_PRESETS.items()))}")
        p.add_argument("--width", type=int, help="512-2048 (default 1024)")
        p.add_argument("--height", type=int, help="512-2048 (default 1024)")
        p.add_argument("--batch-size", type=int, default=1,
                       help="1-4 picks from the SAME prompt (default 1)")
        p.add_argument("--seed", type=int)
        p.add_argument("--priority", choices=["default", "urgent"])
        p.add_argument("--out", help="output png path (batch: suffix _1.._N added)")
        p.add_argument("--no-wait", action="store_true", help="return after queueing, don't poll")
        p.add_argument("--poll-interval", type=int, default=5)
        p.add_argument("--timeout", type=int, default=900)
        p.add_argument("--dry-run", action="store_true", help="print the request, don't send it")

    g = sub.add_parser("generate", help="text-to-image: submit a generation and wait for the image(s)")
    add_common(g)
    g.set_defaults(fn=cmd_generate)

    e = sub.add_parser("edit", help="image-edit: transform 1-8 reference images per the prompt")
    e.add_argument("--image", action="append", required=True, metavar="PATH_OR_URL",
                   help="reference image (repeatable, up to 8; order maps to <image1>..<image8>)")
    add_common(e)
    e.set_defaults(fn=cmd_edit)

    s = sub.add_parser("status", help="check a queued request")
    s.add_argument("--request-id", required=True)
    s.set_defaults(fn=cmd_status)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
