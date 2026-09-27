#!/usr/bin/env python3
"""Lint a generation prompt before submission (automated self-review).

Usage:
  prompt_check.py --prompt "..."
  prompt_check.py --prompt-file prompt.txt
  prompt_check.py --prompt "..." --format structured   # or prose

Checks (error = must fix, warning = review advised):
  common:   length <= 6000, no unfilled template slots ([...] / 【...】),
            balanced double quotes, minimum substance
  structured (z-image): starts with "title:", lighting coverage, negative tail
  prose (qwen):  "Absolutely no ..." negative closer, sentence count,
            no stray key:value field syntax

Exit 0 = ok (warnings allowed), 1 = errors. Prints a JSON report.
"""

import argparse
import json
import re
import sys

MAX_CHARS = 6000
MIN_CHARS = 300

LIGHT_TOKENS = re.compile(
    r"light|sun|softbox|window|rim|neon|flash|neon|candle|glow|shadow|"
    r"chiaroscuro|backlit|volumetric", re.I)
NEG_TOKENS = re.compile(r"no\s+\w[\w\s,]{0,40}", re.I)
KV_SYNTAX = re.compile(
    r"\b(position|ratio|intensity|contrast|saturation|white balance|"
    r"age range|shutter speed|palette)\s*:", re.I)
SLOT = re.compile(r"【|】|\[\s*\]|\[[^\]\n]{1,60}\]")


def check(prompt, fmt):
    errors, warnings = [], []
    n = len(prompt)
    if n > MAX_CHARS:
        errors.append(f"prompt too long ({n} > {MAX_CHARS} chars)")
    if n < MIN_CHARS:
        warnings.append(f"prompt very short ({n} < {MIN_CHARS} chars) — likely under-specified")
    if SLOT.search(prompt):
        errors.append("unfilled template slot found ([...] / 【...】) — replace with real content")
    if prompt.count('"') % 2 != 0:
        errors.append("unbalanced double quotes — on-image text must be quoted exactly")
    if not LIGHT_TOKENS.search(prompt):
        warnings.append("no lighting terms found — light source/direction is a required dimension")
    if not re.search(r"\bno\s+\w+", prompt, re.I):
        warnings.append("no negative exclusions found — add the closing constraints")

    if fmt == "structured":
        if not prompt.lstrip().startswith("title:"):
            errors.append("structured format must start with 'title: ...'")
    else:  # prose
        if "Absolutely no" not in prompt:
            errors.append("prose format must end with an 'Absolutely no ...' negative closer")
        sentences = len(re.findall(r"[.!?](?:\s|$)", prompt))
        if sentences < 4:
            warnings.append(f"only {sentences} sentences — prose prompts read best at 5-9")
        if KV_SYNTAX.search(prompt):
            warnings.append("stray 'key: value' field syntax — fold attributes into sentences")

    return {"format": fmt, "chars": n, "ok": not errors,
            "errors": errors, "warnings": warnings}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--prompt", help="the prompt text inline")
    src.add_argument("--prompt-file", help="file containing the prompt")
    ap.add_argument("--format", choices=["structured", "prose"], default="prose",
                    help="prompt format: prose = qwen paragraph, structured = z-image comma groups")
    args = ap.parse_args()

    if args.prompt_file:
        with open(args.prompt_file, encoding="utf-8") as f:
            prompt = f.read().strip()
    else:
        prompt = args.prompt

    report = check(prompt, args.format)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not report["ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
