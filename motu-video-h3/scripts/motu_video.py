#!/usr/bin/env python3
"""Submit, poll, and download videos from the motu.art MiniMax H3 workflow API.

Usage:
  motu_video.py generate --workflow video_minimax_h3_t2v --prompt "..." [--aspect-ratio 16:9]
                         [--duration 5] [--megapixels 0.4] [--seed N] [--out video.mp4]
  motu_video.py generate --workflow video_minimax_h3_i2v --image ./frame.png --prompt "..."
  motu_video.py generate --workflow video_minimax_h3_r2v --image-start a.png --image-end b.png
  motu_video.py status --request-id <uuid>
  motu_video.py upload --file ./image.png

Requires MOTU_API_KEY in the environment. Pass --dry-run to print the request
without sending it (no API quota consumed).
"""

import argparse
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

API_BASE = os.environ.get("MOTU_API_BASE", "https://api.motu.art")

WORKFLOWS = ("video_minimax_h3_t2v", "video_minimax_h3_i2v", "video_minimax_h3_r2v")

# The API validates aspect_ratio against these full labels, not bare "16:9".
ASPECT_RATIOS = {
    "1:1": "1:1 (Square)",
    "2:3": "2:3 (Portrait Photo)",
    "3:2": "3:2 (Photo)",
    "3:4": "3:4 (Portrait Standard)",
    "4:3": "4:3 (Standard)",
    "9:16": "9:16 (Portrait Widescreen)",
    "16:9": "16:9 (Widescreen)",
}

DEFAULT_ASPECT = {
    "video_minimax_h3_t2v": "16:9 (Widescreen)",
    "video_minimax_h3_i2v": "1:1 (Square)",
    "video_minimax_h3_r2v": "16:9 (Widescreen)",
}


def api_key():
    key = os.environ.get("MOTU_API_KEY", "").strip()
    if not key:
        sys.exit("MOTU_API_KEY is not set. Export it first (see .envrc).")
    return key


def http(method, url, body=None, headers=None, timeout=120):
    req = urllib.request.Request(url, method=method)
    # Kong rejects urllib's default UA; send a neutral one.
    req.add_header("User-Agent", "motu-video-h3/1.0")
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


def normalize_aspect(value):
    if not value:
        return None
    value = value.strip()
    if value in ASPECT_RATIOS.values():
        return value
    if value in ASPECT_RATIOS:
        return ASPECT_RATIOS[value]
    sys.exit(f"Unknown aspect_ratio {value!r}. Use one of: {', '.join(ASPECT_RATIOS.values())}")


def build_payload(args):
    p = {}
    wf = args.workflow
    if wf == "video_minimax_h3_t2v":
        if not args.prompt:
            sys.exit("t2v requires --prompt")
    else:
        if wf == "video_minimax_h3_i2v":
            image = resolve_image(args.image or args.image_url)
            if not image:
                sys.exit("i2v requires --image (local file) or --image-url")
            p["image_url"] = image
        else:
            start = resolve_image(args.image_start)
            end = resolve_image(args.image_end)
            if not start or not end:
                sys.exit("r2v requires --image-start and --image-end (local paths or URLs)")
            p["image_start_url"] = start
            p["image_end_url"] = end
    if args.prompt:
        p["prompt"] = args.prompt
    aspect = normalize_aspect(args.aspect_ratio) or DEFAULT_ASPECT[wf]
    p["aspect_ratio"] = aspect
    if args.duration is not None:
        p["duration"] = args.duration
    if args.megapixels is not None:
        p["megapixels"] = args.megapixels
    if args.seed is not None:
        p["seed"] = args.seed
    if args.filename_prefix and wf == "video_minimax_h3_t2v":
        p["filename_prefix"] = args.filename_prefix
    if args.callback_url:
        p["callback_url"] = args.callback_url
    if args.priority:
        p["priority"] = args.priority
    return p


def resolve_image(value):
    if not value:
        return None
    if value.startswith(("http://", "https://")):
        return value
    if not os.path.isfile(value):
        sys.exit(f"Image not found: {value}")
    print(f"Uploading {value} ...", file=sys.stderr)
    return upload_file(value)


def submit(workflow, payload, dry_run=False):
    url = f"{API_BASE}/workflows/{workflow}"
    if dry_run:
        print(json.dumps({"POST": url, "body": payload}, indent=2, ensure_ascii=False))
        return None
    status, raw = http("POST", url, body=payload, headers=authed_headers())
    if status not in (200, 202):
        sys.exit(f"submit failed [{status}]: {raw.decode(errors='replace')}")
    return json.loads(raw)


def poll(request_id, interval=10, timeout=1800):
    url = f"{API_BASE}/workflow/status?workflow_request_id={urllib.parse.quote(request_id)}"
    deadline = time.time() + timeout
    while True:
        status, raw = http("GET", url, headers=authed_headers())
        if status != 200:
            sys.exit(f"status poll failed [{status}]: {raw.decode(errors='replace')}")
        info = json.loads(raw)
        state = info.get("status")
        print(f"status: {state}", file=sys.stderr)
        if state in ("completed", "success"):
            return info
        if state in ("failed", "error"):
            sys.exit(f"generation failed: {json.dumps(info, ensure_ascii=False)}")
        if time.time() > deadline:
            sys.exit(f"timed out after {timeout}s waiting for {request_id}")
        time.sleep(interval)


def download(url, out_path):
    print(f"Downloading -> {out_path}", file=sys.stderr)
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "motu-video-h3/1.0")
    with urllib.request.urlopen(req, timeout=600) as resp, open(out_path, "wb") as f:
        while True:
            chunk = resp.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)
    return out_path


def cmd_generate(args):
    payload = build_payload(args)
    queued = submit(args.workflow, payload, dry_run=args.dry_run)
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
    out = args.out or f"{args.filename_prefix or 'video'}_{request_id[:8]}.mp4"
    download(results[0]["url"], out)
    meta = dict(results[0])
    meta.pop("url", None)
    print(json.dumps({"out": out, "request_id": request_id, **meta}, ensure_ascii=False))


def cmd_status(args):
    info = poll_once(args.request_id)
    print(json.dumps(info, indent=2, ensure_ascii=False))


def poll_once(request_id):
    url = f"{API_BASE}/workflow/status?workflow_request_id={urllib.parse.quote(request_id)}"
    status, raw = http("GET", url, headers=authed_headers())
    if status != 200:
        sys.exit(f"status failed [{status}]: {raw.decode(errors='replace')}")
    return json.loads(raw)


def cmd_upload(args):
    print(upload_file(args.file))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="submit a generation and wait for the video")
    g.add_argument("--workflow", required=True, choices=WORKFLOWS)
    g.add_argument("--prompt")
    g.add_argument("--image", help="i2v: local image file (uploaded automatically)")
    g.add_argument("--image-url", help="i2v: image URL")
    g.add_argument("--image-start", help="r2v: start frame (local path or URL)")
    g.add_argument("--image-end", help="r2v: end frame (local path or URL)")
    g.add_argument("--aspect-ratio", help="e.g. 16:9 or '16:9 (Widescreen)'")
    g.add_argument("--duration", type=float, help="seconds, 3-15 (default 5)")
    g.add_argument("--megapixels", type=float, help="0.2-1 (default 0.4)")
    g.add_argument("--seed", type=int)
    g.add_argument("--filename-prefix")
    g.add_argument("--callback-url")
    g.add_argument("--priority", choices=["default", "urgent"])
    g.add_argument("--out", help="output mp4 path")
    g.add_argument("--no-wait", action="store_true", help="return after queueing, don't poll")
    g.add_argument("--poll-interval", type=int, default=10)
    g.add_argument("--timeout", type=int, default=1800)
    g.add_argument("--dry-run", action="store_true", help="print the request, don't send it")
    g.set_defaults(fn=cmd_generate)

    s = sub.add_parser("status", help="check a queued request")
    s.add_argument("--request-id", required=True)
    s.set_defaults(fn=cmd_status)

    u = sub.add_parser("upload", help="upload a local file, print its public URL")
    u.add_argument("--file", required=True)
    u.set_defaults(fn=cmd_upload)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
