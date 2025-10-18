#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Python Video to Audio Converter
File: converter.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-18
Updated: 2025-10-18
License: MIT License (see LICENSE file for details)
=====================================================================================================

Description:
Core conversion logic using MoviePy. Provides a safe, testable function to convert
video files (mp4/mkv/mov/...) to MP3 audio.

Usage:
from video_to_audio.converter import convert_video_to_mp3
convert_video_to_mp3("/path/to/video.mp4")

Notes:
- Relies on MoviePy's VideoFileClip and imageio-ffmpeg under the hood.
- Returns the output path upon success and raises ValueError/RuntimeError for user-friendly errors.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from moviepy.editor import VideoFileClip


SUPPORTED_EXTS = {".mp4", ".mkv", ".mov", ".avi", ".webm", ".m4v"}


def _derive_output_path(src: Path, outdir: Optional[Path] = None, ext: str = ".mp3") -> Path:
    outdir = outdir or src.parent
    outdir.mkdir(parents=True, exist_ok=True)
    return (outdir / src.stem).with_suffix(ext)


def convert_video_to_mp3(src_path: str | Path, *, outdir: Optional[str | Path] = None) -> Path:
    """Convert a video file to an MP3 file next to it (or in outdir).

    Parameters
    ----------
    src_path : str | Path
        Input video path.
    outdir : Optional[str | Path]
        Destination directory for the MP3. Defaults to source directory.

    Returns
    -------
    Path
        The resulting MP3 file path.

    Raises
    ------
    FileNotFoundError
        If the source file does not exist.
    ValueError
        If the file extension is unsupported.
    RuntimeError
        If conversion fails for any reason.
    """
    src = Path(src_path).expanduser().resolve()
    if not src.exists():
        raise FileNotFoundError(f"Source file not found: {src}")

    if src.suffix.lower() not in SUPPORTED_EXTS:
        raise ValueError(
            f"Unsupported input extension '{src.suffix}'. Supported: {sorted(SUPPORTED_EXTS)}"
        )

    outdir_path: Optional[Path] = Path(outdir).expanduser().resolve() if outdir else None
    dst = _derive_output_path(src, outdir_path, ".mp3")

    try:
        # MoviePy context manager ensures resources are released.
        with VideoFileClip(str(src)) as clip:
            # Some videos may not have an audio track.
            if clip.audio is None:
                raise RuntimeError("The selected video has no audio track.")
            # Write MP3 with default settings. Suppress verbose logs.
            clip.audio.write_audiofile(
                str(dst),
                verbose=False,
                logger=None,
            )
    except Exception as exc:  # noqa: BLE001 - bubble up as a clean RuntimeError
        raise RuntimeError(f"Conversion failed: {exc}") from exc

    if not dst.exists():
        raise RuntimeError("Conversion reported success but output file was not created.")

    return dst
