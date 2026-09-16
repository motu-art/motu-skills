#!/usr/bin/env python3
"""Generate images through the motu.art Ideogram 4 workflow API.

Usage:
  motu_image.py generate --prompt "..." [--width 1024] [--height 1024] [--cfg 2]
                         [--temperature 0.3] [--seed N] [--out image.png]
  motu_image.py status --request-id <uuid>

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
WORKFLOW = "ideogram4"

# Sensible presets; the API itself accepts 512-1536 per side.
SIZE_PRESETS = {
    "square": (1024, 1024),
    "portrait": (768, 1376),   # API default
    "landscape": (1376, 768),
    "story": (896, 1344),      # 2:3 vertical, social story size
    "banner": (1344, 576),
}


def api_key():
    key = os.environ.get("MOTU_KEY", "").strip()
    if not key:
        sys.exit("MOTU_KEY is not set. Export it first (see .envrc).")
    return key


def http(method, url, body=None, headers=None, timeout=120):
    req = urllib.request.Request(url, method=method)
    # Kong rejects urllib's default UA; send a neutral one.
    req.add_header("User-Agent", "motu-ideogram4/1.0")
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
        width, height = SIZE_PRESETS["portrait"]  # API default 768x1376
    elif width is None or height is None:
        sys.exit("give both --width and --height (or use --size)")
    for name, v in (("width", width), ("height", height)):
        if not 512 <= v <= 1536:
            sys.exit(f"{name} must be 512-1536 (got {v})")
    if args.cfg is not None and not 1 <= args.cfg <= 7:
        sys.exit("--cfg must be 1-7")
    if args.temperature is not None and not 0 <= args.temperature <= 1:
        sys.exit("--temperature must be 0-1")
    p = {"prompt": args.prompt, "width": width, "height": height}
    if args.cfg is not None:
        p["cfg"] = args.cfg
    if args.temperature is not None:
        p["temperature"] = args.temperature
    if args.model:
        p["model"] = args.model
    if args.seed is not None:
        p["seed"] = args.seed
    if args.callback_url:
        p["callback_url"] = args.callback_url
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
    req.add_header("User-Agent", "motu-ideogram4/1.0")
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
    out = args.out or f"image_{request_id[:8]}.png"
    download(results[0]["url"], out)
    meta = dict(results[0])
    meta.pop("url", None)
    print(json.dumps({"out": out, "request_id": request_id, **meta}, ensure_ascii=False))


def cmd_status(args):
    print(json.dumps(poll_once(args.request_id), indent=2, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="submit a generation and wait for the image")
    g.add_argument("--prompt", required=True, help="image description, max 6000 chars")
    g.add_argument("--size", choices=sorted(SIZE_PRESETS),
                   help=f"preset: {', '.join(f'{k} {v[0]}x{v[1]}' for k, v in sorted(SIZE_PRESETS.items()))}")
    g.add_argument("--width", type=int, help="512-1536 (default 768)")
    g.add_argument("--height", type=int, help="512-1536 (default 1376)")
    g.add_argument("--cfg", type=float, help="prompt adherence 1-7 (default 2); higher = closer to prompt")
    g.add_argument("--temperature", type=float, help="0-1 (default 0.3)")
    g.add_argument("--model", help="rarely needed; only allowed value is gpt-4.1")
    g.add_argument("--seed", type=int)
    g.add_argument("--callback-url")
    g.add_argument("--priority", choices=["default", "urgent"])
    g.add_argument("--out", help="output png path")
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
