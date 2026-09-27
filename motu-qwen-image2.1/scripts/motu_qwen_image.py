#!/usr/bin/env python3
"""Generate images through the motu.art Qwen Image 2.1 workflow API.

Usage:
  motu_qwen_image.py generate --prompt "..." [--size portrait] [--batch-size 1]
                              [--seed N] [--out image.png]
  motu_qwen_image.py status --request-id <uuid>

Requires MOTU_KEY in the environment. Pass --dry-run to print the request
without sending it (no API quota consumed).
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API_BASE = os.environ.get("MOTU_API_BASE", "https://api.motu.art")
WORKFLOW = "image_qwen_image_2_1_t2i"

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


def build_payload(args):
    if not args.prompt:
        sys.exit("generate requires --prompt")
    if len(args.prompt) > 6000:
        sys.exit(f"prompt too long ({len(args.prompt)} chars, max 6000)")
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
    if not 1 <= args.batch_size <= 4:
        sys.exit("--batch-size must be 1-4")
    p = {"prompt": args.prompt, "width": width, "height": height,
         "batch_size": args.batch_size}
    if args.seed is not None:
        p["seed"] = args.seed
    if args.priority:
        p["priority"] = args.priority
    return p


def submit(payload, dry_run=False):
    url = f"{API_BASE}/workflows/{WORKFLOW}"
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


def cmd_generate(args):
    payload = build_payload(args)
    queued = submit(payload, dry_run=args.dry_run)
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
        args.out or f"image_{request_id[:8]}")
    outs = []
    for i, r in enumerate(results, 1):
        path = f"{stem}.png" if len(results) == 1 else f"{stem}_{i}.png"
        download(r["url"], path)
        outs.append({"path": path, "width": r.get("width"), "height": r.get("height"),
                     "file_size": r.get("file_size")})
    print(json.dumps({"outs": [o["path"] for o in outs], "request_id": request_id,
                      "results": outs}, ensure_ascii=False))


def cmd_status(args):
    print(json.dumps(poll_once(args.request_id), indent=2, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="submit a generation and wait for the image(s)")
    g.add_argument("--prompt", required=True, help="prose prompt, max 6000 chars")
    g.add_argument("--size", choices=sorted(SIZE_PRESETS),
                   help=f"preset: {', '.join(f'{k} {v[0]}x{v[1]}' for k, v in sorted(SIZE_PRESETS.items()))}")
    g.add_argument("--width", type=int, help="512-2048 (default 1024)")
    g.add_argument("--height", type=int, help="512-2048 (default 1024)")
    g.add_argument("--batch-size", type=int, default=1,
                   help="1-4 picks from the SAME prompt (default 1)")
    g.add_argument("--seed", type=int)
    g.add_argument("--priority", choices=["default", "urgent"])
    g.add_argument("--out", help="output png path (batch: suffix _1.._N added)")
    g.add_argument("--no-wait", action="store_true", help="return after queueing, don't poll")
    g.add_argument("--poll-interval", type=int, default=5)
    g.add_argument("--timeout", type=int, default=900)
    g.add_argument("--dry-run", action="store_true", help="print the request, don't send it")
    g.set_defaults(fn=cmd_generate)

    s = sub.add_parser("status", help="check a queued request")
    s.add_argument("--request-id", required=True)
    s.set_defaults(fn=cmd_status)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
