#!/usr/bin/env python3
"""Generate music through the motu.art MiniMax Music 3 workflow API.

Usage:
  motu_music.py generate --caption "warm lo-fi hip hop, soft piano, 80 bpm" \
                         [--lyrics-file lyrics.txt] [--max-duration 240] \
                         [--seed N] [--out song.mp3]
  motu_music.py status --request-id <uuid>

  --caption    the music brief: style, mood, instrumentation, arrangement (max 6000 chars).
               For instrumentals, state "fully instrumental, no vocals" in it.
  --lyrics     / --lyrics-file  song lyrics to be sung (max 6000 chars). Omit for instrumental.
  --max-duration  music length cap in seconds, 1-360 (platform default 240).

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
WORKFLOW = "audio_minimax_music_3"


def api_key():
    key = os.environ.get("MOTU_KEY", "").strip()
    if not key:
        sys.exit("MOTU_KEY is not set. Export it first (see .envrc).")
    return key


def http(method, url, body=None, headers=None, timeout=120):
    req = urllib.request.Request(url, method=method)
    # Kong rejects urllib's default UA; send a neutral one.
    req.add_header("User-Agent", "motu-minimax-music3/1.0")
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


def read_text_arg(value, path, what):
    """Exactly one of inline text / a file path; returns the text."""
    if value and path:
        sys.exit(f"pass either --{what} or --{what}-file, not both")
    if path:
        with open(path, encoding="utf-8") as f:
            return f.read()
    return value


def build_payload(args):
    lyrics = read_text_arg(args.lyrics, args.lyrics_file, "lyrics")
    caption = read_text_arg(args.caption, args.caption_file, "caption")
    if lyrics and len(lyrics) > 6000:
        sys.exit(f"lyrics too long ({len(lyrics)} chars, max 6000)")
    if caption and len(caption) > 6000:
        sys.exit(f"caption too long ({len(caption)} chars, max 6000)")
    if not caption and not lyrics:
        print("warning: no --caption and no --lyrics — the platform will use its long "
              "built-in default caption (a children's instrumental piece); almost always "
              "not what you want. Pass --caption.", file=sys.stderr)
    p = {}
    if caption:
        p["caption"] = caption
    if lyrics:
        p["lyrics"] = lyrics
    if args.max_duration is not None:
        if not 1 <= args.max_duration <= 360:
            sys.exit("--max-duration must be 1-360 seconds")
        p["max_duration"] = args.max_duration
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


def poll(request_id, interval=10, timeout=1800):
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
    req.add_header("User-Agent", "motu-minimax-music3/1.0")
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
    out = args.out or f"music_{request_id[:8]}.mp3"
    download(results[0]["url"], out)
    meta = dict(results[0])
    meta.pop("url", None)
    print(json.dumps({"out": out, "request_id": request_id, **meta}, ensure_ascii=False))


def cmd_status(args):
    print(json.dumps(poll_once(args.request_id), indent=2, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="submit a generation and wait for the audio")
    g.add_argument("--caption", help="music brief: style, mood, instrumentation, arrangement")
    g.add_argument("--caption-file", help="read the caption from a file")
    g.add_argument("--lyrics", help="lyrics to be sung (omit for instrumental)")
    g.add_argument("--lyrics-file", help="read lyrics from a file")
    g.add_argument("--max-duration", type=int, help="length cap in seconds (default 240, max 360)")
    g.add_argument("--seed", type=int)
    g.add_argument("--callback-url")
    g.add_argument("--priority", choices=["default", "urgent"])
    g.add_argument("--out", help="output mp3 path")
    g.add_argument("--no-wait", action="store_true", help="return after queueing, don't poll")
    g.add_argument("--poll-interval", type=int, default=10)
    g.add_argument("--timeout", type=int, default=1800)
    g.add_argument("--dry-run", action="store_true", help="print the request, don't send it")
    g.set_defaults(fn=cmd_generate)

    s = sub.add_parser("status", help="check a queued request")
    s.add_argument("--request-id", required=True)
    s.set_defaults(fn=cmd_status)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
