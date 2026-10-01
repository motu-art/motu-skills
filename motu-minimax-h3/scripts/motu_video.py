#!/usr/bin/env python3
"""Submit, poll, and download videos from the motu.art MiniMax H3 workflow API.

Three workflows (short aliases accepted):
  t2v         video_minimax_h3_t2v                   text-to-video   --prompt (required)
  ra2v        video_minimax_h3_ra2v                  ref images+audio  any of --image1/--image2/--audio1/--audio2
  controlnet  video_minimax_h3_fun_controlnet_union  motion control  --video1 (control video) + optional refs

Usage:
  motu_video.py generate --workflow t2v --prompt "..." [--aspect-ratio 16:9] [--duration 5] [--steps 8]
  motu_video.py generate --workflow ra2v --image1 ./frame.png --prompt "..."
  motu_video.py generate --workflow ra2v --image1 a.png --image2 b.png --audio1 voice.mp3
  motu_video.py generate --workflow controlnet --video1 ./dance.mp4 --image1 ./hero.png --prompt "..."
  motu_video.py merge --out final.mp4 shot_01.mp4 shot_02.mp4 shot_03.mp4
  motu_video.py status --request-id <uuid>
  motu_video.py upload --file ./image.png

ra2v absorbs the old i2v / ia2v / r2v use cases: one image (animate a picture),
one image + one audio (talking head), two images (start/end frames) — plus a
second audio input (--audio2). controlnet transplants the motion of a control
video onto a new subject (images lock appearance, audio1 supplies the track).

Local image/audio/video files are uploaded automatically (base64 data URIs fail
silently in processing, so the script always routes locals through the OSS
presign route). Requires MOTU_KEY in the environment. Pass --dry-run to print
the request without sending it (no API quota consumed).

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
    "ra2v": "video_minimax_h3_ra2v",
    "controlnet": "video_minimax_h3_fun_controlnet_union",
}
WORKFLOWS = tuple(WORKFLOW_ALIASES.values())

# Per-workflow input/parameter matrix (from the API sheets, 2026-10).
MEDIA_FIELDS = {
    "video_minimax_h3_t2v": (),
    "video_minimax_h3_ra2v": ("image1", "image2", "audio1", "audio2"),
    "video_minimax_h3_fun_controlnet_union": ("video1", "audio1", "image1", "image2"),
}
# Which workflow accepts each media flag — for error messages when flags and
# workflow don't match (a wrong pair would otherwise be dropped silently).
FLAG_WORKFLOWS = {
    "image1": "ra2v / controlnet",
    "image2": "ra2v / controlnet",
    "audio1": "ra2v / controlnet",
    "audio2": "ra2v only",
    "video1": "controlnet only",
}
RULES = {
    "video_minimax_h3_t2v": {
        "prompt_required": True, "prompt_max": 6000, "megapixels_min": 0.2,
        "steps": True, "filename_prefix": True,
    },
    "video_minimax_h3_ra2v": {
        "prompt_required": False, "prompt_max": 8000, "megapixels_min": 0.2,
        "steps": True, "filename_prefix": False,
    },
    # controlnet's megapixels floor is 0.3 (the others accept 0.2).
    "video_minimax_h3_fun_controlnet_union": {
        "prompt_required": False, "prompt_max": 6000, "megapixels_min": 0.3,
        "steps": False, "filename_prefix": False,
    },
}

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

DEFAULT_ASPECT = "16:9 (Widescreen)"  # all three workflows

# Media inputs the prompt can reference; printed as a tip when --prompt is omitted.
PROMPT_REF_NOTES = {
    "video_minimax_h3_ra2v":
        "reference the images as <Picture 1>/<Picture 2> and the audio as <Audio 1>/<Audio 2>",
    "video_minimax_h3_fun_controlnet_union":
        "the control video's motion is transplanted onto your subject; lock appearance "
        "with image1/image2 and describe the subject and scene in the prompt",
}


def api_key():
    key = os.environ.get("MOTU_KEY", "").strip()
    if not key:
        sys.exit("MOTU_KEY is not set. Export it first (see .envrc).")
    return key


def http(method, url, body=None, headers=None, timeout=120):
    req = urllib.request.Request(url, method=method)
    # Kong rejects urllib's default UA; send a neutral one.
    req.add_header("User-Agent", "motu-minimax-h3/1.0")
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
    rule = RULES[wf]
    media = MEDIA_FIELDS[wf]

    # Fail loudly on flags the chosen workflow doesn't accept.
    for flag, where in FLAG_WORKFLOWS.items():
        if getattr(args, flag) and flag not in media:
            sys.exit(f"--{flag} is not accepted by {wf} ({where}) — wrong workflow?")
    if args.steps is not None and not rule["steps"]:
        sys.exit(f"--steps is not accepted by {wf} (t2v/ra2v only)")
    if args.filename_prefix and not rule["filename_prefix"]:
        sys.exit(f"--filename-prefix is not accepted by {wf} (t2v only)")

    p = {}
    for field in media:
        value = getattr(args, field)
        if value:
            p[field] = resolve_media(value, field)

    if args.prompt:
        if len(args.prompt) > rule["prompt_max"]:
            sys.exit(f"prompt is {len(args.prompt)} chars; max {rule['prompt_max']} for {wf}")
        p["prompt"] = args.prompt
    elif rule["prompt_required"]:
        sys.exit(f"{wf} requires --prompt")
    elif wf in PROMPT_REF_NOTES and p:
        print(f"tip: no --prompt given; {PROMPT_REF_NOTES[wf]}.", file=sys.stderr)

    if args.duration is not None:
        if not 3 <= args.duration <= 15:
            sys.exit(f"duration must be 3-15 s, got {args.duration}")
        p["duration"] = args.duration
    if args.megapixels is not None:
        if not rule["megapixels_min"] <= args.megapixels <= 1:
            sys.exit(f"megapixels must be {rule['megapixels_min']}-1 for {wf}, got {args.megapixels}")
        p["megapixels"] = args.megapixels
    if args.steps is not None:
        if not 4 <= args.steps <= 8:
            sys.exit(f"steps must be 4-8, got {args.steps}")
        p["steps"] = args.steps
    if args.seed is not None:
        if not 0 <= args.seed <= 10**16:
            sys.exit(f"seed must be 0-10000000000000000, got {args.seed}")
        p["seed"] = args.seed
    if args.filename_prefix:
        p["filename_prefix"] = args.filename_prefix
    p["aspect_ratio"] = normalize_aspect(args.aspect_ratio) or DEFAULT_ASPECT
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


# The docs specify GET /workflows/status/{id}; the pre-2026-10 live API answered
# GET /workflow/status?workflow_request_id=. Try the documented route first and
# remember whichever returns 200.
_status_url = {"url": None}


def poll_once(request_id):
    quoted = urllib.parse.quote(request_id)
    candidates = [f"{API_BASE}/workflows/status/{quoted}",
                  f"{API_BASE}/workflow/status?workflow_request_id={quoted}"]
    if _status_url["url"]:
        candidates.insert(0, _status_url["url"])
    err = "no route attempted"
    for url in dict.fromkeys(candidates):
        status, raw = http("GET", url, headers=authed_headers())
        if status == 200:
            _status_url["url"] = url
            return json.loads(raw)
        err = f"[{status}] {raw.decode(errors='replace')}"
    sys.exit(f"status failed for {request_id}: {err}")


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
    req.add_header("User-Agent", "motu-minimax-h3/1.0")
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
                   help="t2v | ra2v | controlnet (or the full workflow name)")
    g.add_argument("--prompt")
    g.add_argument("--image1", help="ra2v/controlnet: reference image (local path or URL); <Picture 1>")
    g.add_argument("--image2", help="ra2v/controlnet: second reference image; <Picture 2>")
    g.add_argument("--audio1", help="ra2v/controlnet: audio track (local path or URL); <Audio 1>")
    g.add_argument("--audio2", help="ra2v only: second audio track; <Audio 2>")
    g.add_argument("--video1", help="controlnet only: control video whose motion drives the output")
    g.add_argument("--aspect-ratio", help="e.g. 16:9 or '16:9 (Widescreen)'")
    g.add_argument("--duration", type=float, help="seconds, 3-15 (default 5)")
    g.add_argument("--megapixels", type=float,
                   help="0.2-1 (default 0.4 t2v/controlnet, 0.7 ra2v; controlnet min 0.3)")
    g.add_argument("--steps", type=int, help="sampling steps 4-8 (t2v/ra2v only, default 8)")
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
