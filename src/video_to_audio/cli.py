#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Python Video to Audio Converter
File: cli.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-18
Updated: 2025-10-18
License: MIT License (see LICENSE file for details)
=====================================================================================================

Description:
Command-line interface for batch converting videos to MP3.

Usage:
video2audio input1.mp4 input2.mkv --outdir ./export

Notes:
- Exits with non-zero status if any conversion fails.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .converter import convert_video_to_mp3


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Convert video files to MP3 audio.")
    p.add_argument("inputs", nargs="+", help="Input video file(s)")
    p.add_argument("--outdir", type=str, default=None, help="Optional output directory")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    ns = parse_args(argv)
    outdir = ns.outdir
    errors: list[str] = []

    for src in ns.inputs:
        try:
            dst = convert_video_to_mp3(src, outdir=outdir)
            print(f"✓ {Path(src).name} → {dst}")
        except Exception as exc:  # noqa: BLE001
            msg = f"✗ {src}: {exc}"
            print(msg, file=sys.stderr)
            errors.append(msg)

    return 0 if not errors else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
