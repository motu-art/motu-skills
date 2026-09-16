#!/usr/bin/env python3
"""Submit, poll, and download videos from the motu.art MiniMax H3 workflow API.

Five workflows (short aliases accepted):
  t2v   video_minimax_h3_t2v    text-to-video            --prompt (required)
  i2v   video_minimax_h3_i2v    image-to-video           --image (required)
  ia2v  video_minimax_h3_ia2v   image+audio-to-video     --image + --audio (lip-sync)
  r2v   video_minimax_h3_r2v    start/end frame          --image-start + --image-end (required)
  ra2v  video_minimax_h3_ra2v   frames+audio-to-video    any of --image-start/--image-end/--audio

Usage:
  motu_video.py generate --workflow t2v --prompt "..." [--aspect-ratio 16:9] [--duration 5]
  motu_video.py generate --workflow i2v --image ./frame.png --prompt "..."
  motu_video.py generate --workflow ia2v --image ./portrait.png --audio ./speech.mp3
  motu_video.py generate --workflow r2v --image-start a.png --image-end b.png
  motu_video.py generate --workflow ra2v --image-start a.png --image-end b.png --audio sfx.mp3
  motu_video.py merge --out final.mp4 shot_01.mp4 shot_02.mp4 shot_03.mp4
  motu_video.py status --request-id <uuid>
  motu_video.py upload --file ./image.png

Local image/audio files are uploaded automatically (base64 data URIs fail silently
in processing, so the script always routes locals through the OSS presign route).
Requires MOTU_KEY in the environment. Pass --dry-run to print the request
without sending it (no API quota consumed).

merge concatenates shot clips (the long-form strategy: each generation caps at
15 s, so split by shot, generate per shot, then merge) into one video. It needs
the ffmpeg/ffprobe binaries on PATH; when all clips match it stream-copies
(lossless), otherwise it re-encodes to the first clip's format. No MOTU_KEY needed.
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

WORKFLOW_ALIASES = {
    "t2v": "video_minimax_h3_t2v",
    "i2v": "video_minimax_h3_i2v",
    "ia2v": "video_minimax_h3_ia2v",
    "r2v": "video_minimax_h3_r2v",
    "ra2v": "video_minimax_h3_ra2v",
}
WORKFLOWS = tuple(WORKFLOW_ALIASES.values())

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
    "video_minimax_h3_ia2v": "3:4 (Portrait Standard)",
    "video_minimax_h3_r2v": "16:9 (Widescreen)",
    "video_minimax_h3_ra2v": "16:9 (Widescreen)",
}

# Frames or audio referenced by the prompt as <Picture 1>/<Picture 2>/<Audio 1>.
PROMPT_REF_NOTES = {
    "video_minimax_h3_i2v": "reference the image as <Picture 1>",
    "video_minimax_h3_ia2v": "reference the image as <Picture 1> and the audio as <Audio 1>",
    "video_minimax_h3_r2v": "reference the start frame as <Picture 1>, the end frame as <Picture 2>",
    "video_minimax_h3_ra2v": "reference the frames as <Picture 1>/<Picture 2> and the audio as <Audio 1>",
}


def api_key():
    key = os.environ.get("MOTU_KEY", "").strip()
    if not key:
        sys.exit("MOTU_KEY is not set. Export it first (see .envrc).")
    return key


def http(method, url, body=None, headers=None, timeout=120):
    req = urllib.request.Request(url, method=method)
    # Kong rejects urllib's default UA; send a neutral one.
    req.add_header("User-Agent", "motu-video-minimax-h3/1.0")
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


def resolve_media(value, what="image"):
    """Accept an http(s) URL or a local file path; upload locals and return the URL."""
    if not value:
        return None
    if value.startswith(("http://", "https://")):
        return value
    if not os.path.isfile(value):
        sys.exit(f"{what} not found: {value}")
    print(f"Uploading {value} ...", file=sys.stderr)
    return upload_file(value)


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
    wf = WORKFLOW_ALIASES.get(args.workflow, args.workflow)
    args.workflow = wf
    p = {}
    if wf == "video_minimax_h3_t2v":
        if not args.prompt:
            sys.exit("t2v requires --prompt")
    elif wf == "video_minimax_h3_i2v":
        image = resolve_media(args.image or args.image_url, "image")
        if not image:
            sys.exit("i2v requires --image (local file) or --image-url")
        p["image_url"] = image
    elif wf == "video_minimax_h3_ia2v":
        # Both inputs are technically optional, but the workflow exists to animate
        # a picture driven by an audio track — warn rather than fail.
        image = resolve_media(args.image or args.image_url, "image")
        audio = resolve_media(args.audio, "audio")
        if not image and not audio:
            print("warning: ia2v with no image and no audio just renders the default "
                  "prompt from scratch — pass --image and --audio.", file=sys.stderr)
        if image:
            p["image_url"] = image
        if audio:
            p["audio"] = audio
    elif wf == "video_minimax_h3_r2v":
        start = resolve_media(args.image_start, "start frame")
        end = resolve_media(args.image_end, "end frame")
        if not start or not end:
            sys.exit("r2v requires --image-start and --image-end (local paths or URLs)")
        p["image_start_url"] = start
        p["image_end_url"] = end
    else:  # ra2v: every media input optional
        for flag, field, what in ((args.image_start, "image_start_url", "start frame"),
                                  (args.image_end, "image_end_url", "end frame"),
                                  (args.audio, "audio", "audio")):
            url = resolve_media(flag, what)
            if url:
                p[field] = url
    if args.prompt:
        p["prompt"] = args.prompt
    elif wf in PROMPT_REF_NOTES and (len(p) > 0):
        print(f"tip: no --prompt given; in the prompt you write, {PROMPT_REF_NOTES[wf]}.",
              file=sys.stderr)
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


def submit(workflow, payload, dry_run=False):
    url = f"{API_BASE}/workflows/{workflow}"
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
    req.add_header("User-Agent", "motu-video-minimax-h3/1.0")
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
    out = args.out or f"video_{request_id[:8]}.mp4"
    download(results[0]["url"], out)
    meta = dict(results[0])
    meta.pop("url", None)
    print(json.dumps({"out": out, "request_id": request_id, **meta}, ensure_ascii=False))


def cmd_status(args):
    print(json.dumps(poll_once(args.request_id), indent=2, ensure_ascii=False))


def cmd_upload(args):
    print(upload_file(args.file))


# --- merge: concatenate shot clips into one video (long-form strategy) ---

def need_ffmpeg():
    missing = [t for t in ("ffmpeg", "ffprobe") if shutil.which(t) is None]
    if missing:
        sys.exit(f"{' and '.join(missing)} not found on PATH — install ffmpeg "
                 "(macOS: brew install ffmpeg; Ubuntu: sudo apt install ffmpeg).")


def probe(path):
    """Return {width, height, fps, has_audio, duration} for a media file via ffprobe."""
    proc = subprocess.run(
        ["ffprobe", "-v", "error", "-of", "json", "-show_streams", "-show_format", path],
        capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(f"ffprobe failed on {path}: {proc.stderr.strip()[-500:]}")
    info = json.loads(proc.stdout)
    video = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), None)
    if video is None:
        sys.exit(f"no video stream in {path}")
    num, _, den = (video.get("avg_frame_rate") or "0/1").partition("/")
    try:
        fps = float(num) / float(den) if float(den) else 0.0
    except (ValueError, ZeroDivisionError):
        fps = 0.0
    return {
        "width": video["width"],
        "height": video["height"],
        "fps": fps,
        "has_audio": any(s.get("codec_type") == "audio" for s in info.get("streams", [])),
        "duration": float(info.get("format", {}).get("duration") or 0),
    }


def concat_copy(paths, out):
    """Stream-copy concat (fast, lossless). Returns False if unusable — caller re-encodes."""
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        for p in paths:
            # single quotes in the concat list are escaped as '\''
            f.write("file '" + os.path.abspath(p).replace("'", "'\\''") + "'\n")
        list_path = f.name
    tmp_out = out + ".tmp.mp4"
    try:
        proc = subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", list_path,
             "-c", "copy", "-movflags", "+faststart", tmp_out],
            capture_output=True, text=True)
        if proc.returncode != 0:
            return False
        # -c copy can "succeed" yet mangle timestamps when parameters differ;
        # treat a too-short result as failure and fall back to re-encoding.
        expected = sum(probe(p)["duration"] for p in paths)
        if expected > 0 and probe(tmp_out)["duration"] < expected * 0.9:
            return False
        os.replace(tmp_out, out)
        return True
    finally:
        os.unlink(list_path)
        if os.path.exists(tmp_out):
            os.unlink(tmp_out)


def concat_reencode(paths, out):
    """Re-encode concat: normalize every clip to the first clip's format, then concat."""
    infos = [probe(p) for p in paths]
    first = infos[0]
    w, h = first["width"], first["height"]
    fps = first["fps"] or 30
    cmd = ["ffmpeg", "-y"]
    filters = []
    labels = []
    idx = 0
    for path, info in zip(paths, infos):
        v = idx
        cmd += ["-i", path]
        idx += 1
        filters.append(f"[{v}:v]scale={w}:{h},fps={fps},setsar=1,format=yuv420p[v{v}]")
        if info["has_audio"]:
            filters.append(f"[{v}:a]aresample=44100,aformat=channel_layouts=stereo[a{v}]")
            labels += [f"[v{v}]", f"[a{v}]"]
        else:
            # silent stand-in track so the concat filter keeps a uniform v+a layout
            dur = info["duration"] or first["duration"] or 5
            cmd += ["-f", "lavfi", "-t", f"{dur:.3f}", "-i", "anullsrc=r=44100:cl=stereo"]
            labels += [f"[v{v}]", f"[{idx}:a]"]
            idx += 1
    # concat consumes pads as v0 a0 v1 a1 ...
    filters.append("".join(labels) + f"concat=n={len(paths)}:v=1:a=1[vout][aout]")
    cmd += ["-filter_complex", ";".join(filters),
            "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(f"ffmpeg failed: {proc.stderr.strip()[-1500:]}")


def merge_videos(paths, out):
    need_ffmpeg()
    for p in paths:
        if not os.path.isfile(p):
            sys.exit(f"clip not found: {p}")
    if len(paths) < 2:
        sys.exit("merge needs at least two clips")
    if os.path.abspath(out) in {os.path.abspath(p) for p in paths}:
        sys.exit("--out must differ from the input clips")
    infos = [probe(p) for p in paths]
    uniform = len({(i["width"], i["height"], i["has_audio"]) for i in infos}) == 1
    if uniform and concat_copy(paths, out):
        mode = "stream-copy"
    else:
        concat_reencode(paths, out)
        mode = "re-encode"
    total = probe(out)["duration"]
    print(json.dumps({"out": out, "clips": len(paths), "mode": mode,
                      "duration": round(total, 2)}, ensure_ascii=False))


def cmd_merge(args):
    merge_videos(args.clips, args.out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="submit a generation and wait for the video")
    g.add_argument("--workflow", required=True,
                   choices=list(WORKFLOW_ALIASES) + list(WORKFLOWS),
                   help="t2v | i2v | ia2v | r2v | ra2v (or the full workflow name)")
    g.add_argument("--prompt")
    g.add_argument("--image", help="i2v/ia2v: local image file (uploaded automatically)")
    g.add_argument("--image-url", help="i2v/ia2v: image URL")
    g.add_argument("--image-start", help="r2v/ra2v: start frame (local path or URL)")
    g.add_argument("--image-end", help="r2v/ra2v: end frame (local path or URL)")
    g.add_argument("--audio", help="ia2v/ra2v: audio track (local path or URL)")
    g.add_argument("--aspect-ratio", help="e.g. 16:9 or '16:9 (Widescreen)'")
    g.add_argument("--duration", type=float, help="seconds, 3-15 (t2v/i2v/r2v/ra2v default 5, ia2v default 6)")
    g.add_argument("--megapixels", type=float, help="0.2-1 (default 0.4, ra2v 0.7)")
    g.add_argument("--seed", type=int)
    g.add_argument("--filename-prefix", help="t2v only")
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

    m = sub.add_parser("merge",
                       help="concatenate shot clips into one video (needs ffmpeg)")
    m.add_argument("clips", nargs="+", metavar="clip", help="shot mp4s, in order")
    m.add_argument("--out", default="final.mp4", help="output mp4 path")
    m.set_defaults(fn=cmd_merge)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
