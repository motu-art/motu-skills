#!/usr/bin/env python3
"""Remove watermarks/logos/text overlays from images via the motu.art workflow API.

Usage:
  motu_watermark.py clean --image ./photo.png [--long-side 1536] [--seed N] [--out clean.png]
  motu_watermark.py status --request-id <uuid>
  motu_watermark.py upload --file ./photo.png

--image accepts a local path (uploaded automatically) or an http(s) URL.
--long-side is the output resolution long edge, 512-2048 (default 1536).

Only use this on images you own or are licensed to edit (your own exports,
stock you have rights to, AI generations with baked-in platform marks).
Requires MOTU_KEY in the environment. Pass --dry-run to print the request
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

API_BASE = os.environ.get("MOTU_API_BASE", "https://api.motu.art")
WORKFLOW = "remove_watermark"


def api_key():
    key = os.environ.get("MOTU_KEY", "").strip()
    if not key:
        sys.exit("MOTU_KEY is not set. Export it first (see .envrc).")
    return key


def http(method, url, body=None, headers=None, timeout=120):
    req = urllib.request.Request(url, method=method)
    # Kong rejects urllib's default UA; send a neutral one.
    req.add_header("User-Agent", "motu-remove-watermark/1.0")
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


def resolve_image(value):
    if not value:
        sys.exit("clean requires --image (local file) or --image-url")
    if value.startswith(("http://", "https://")):
        return value
    if not os.path.isfile(value):
        sys.exit(f"Image not found: {value}")
    print(f"Uploading {value} ...", file=sys.stderr)
    return upload_file(value)


def build_payload(args):
    p = {"image_url": resolve_image(args.image or args.image_url)}
    if args.long_side is not None:
        if not 512 <= args.long_side <= 2048:
            sys.exit("--long-side must be 512-2048")
        p["long_side"] = args.long_side
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
    req.add_header("User-Agent", "motu-remove-watermark/1.0")
    with urllib.request.urlopen(req, timeout=600) as resp, open(out_path, "wb") as f:
        while True:
            chunk = resp.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)
    return out_path


def cmd_clean(args):
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
    out = args.out or f"clean_{request_id[:8]}.png"
    download(results[0]["url"], out)
    meta = dict(results[0])
    meta.pop("url", None)
    print(json.dumps({"out": out, "request_id": request_id, **meta}, ensure_ascii=False))


def cmd_status(args):
    print(json.dumps(poll_once(args.request_id), indent=2, ensure_ascii=False))


def cmd_upload(args):
    print(upload_file(args.file))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("clean", help="remove watermarks from an image and wait for the result")
    c.add_argument("--image", help="local image file (uploaded automatically)")
    c.add_argument("--image-url", help="image URL")
    c.add_argument("--long-side", type=int, help="output long edge 512-2048 (default 1536)")
    c.add_argument("--seed", type=int)
    c.add_argument("--callback-url")
    c.add_argument("--priority", choices=["default", "urgent"])
    c.add_argument("--out", help="output png path")
    c.add_argument("--no-wait", action="store_true", help="return after queueing, don't poll")
    c.add_argument("--poll-interval", type=int, default=5)
    c.add_argument("--timeout", type=int, default=900)
    c.add_argument("--dry-run", action="store_true", help="print the request, don't send it")
    c.set_defaults(fn=cmd_clean)

    s = sub.add_parser("status", help="check a queued request")
    s.add_argument("--request-id", required=True)
    s.set_defaults(fn=cmd_status)

    u = sub.add_parser("upload", help="upload a local image, print its public URL")
    u.add_argument("--file", required=True)
    u.set_defaults(fn=cmd_upload)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
