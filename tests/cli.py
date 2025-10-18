#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Python Video to Audio Converter
File: test_cli.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-18
Updated: 2025-10-18
License: MIT License (see LICENSE file for details)
=====================================================================================================

Description:
CLI tests using mocking for fast, deterministic execution.
"""
from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from video_to_audio.cli import main


@patch("video_to_audio.cli.convert_video_to_mp3")
def test_cli_success(mock_convert) -> None:  # type: ignore[no-untyped-def]
    mock_convert.side_effect = lambda src, outdir=None: Path("/tmp/") / (Path(src).stem + ".mp3")
    rc = main(["a.mp4", "b.mkv", "--outdir", "out"])  # noqa: S607
    assert rc == 0


@patch("video_to_audio.cli.convert_video_to_mp3")
def test_cli_failure(mock_convert) -> None:  # type: ignore[no-untyped-def]
    def _side(src, outdir=None):  # noqa: ANN001, ARG001
        if src == "bad.mp4":
            raise RuntimeError("boom")
        return Path("/tmp/") / (Path(src).stem + ".mp3")

    mock_convert.side_effect = _side
    rc = main(["ok.mp4", "bad.mp4"])  # noqa: S607
    assert rc == 1
