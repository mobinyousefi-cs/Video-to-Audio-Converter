#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Python Video to Audio Converter
File: test_converter.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-18
Updated: 2025-10-18
License: MIT License (see LICENSE file for details)
=====================================================================================================

Description:
Unit tests for the core converter logic. We mock MoviePy to avoid heavy I/O.
"""
from __future__ import annotations

import builtins
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from video_to_audio.converter import SUPPORTED_EXTS, convert_video_to_mp3


class _FakeAudio:
    def __init__(self, dst: Path) -> None:
        self.dst = dst

    def write_audiofile(self, path: str, verbose: bool, logger=None) -> None:  # noqa: ANN001
        # Simulate writing the file
        Path(path).touch()


class _FakeClip:
    def __init__(self, has_audio: bool, dst: Path) -> None:
        self.audio = _FakeAudio(dst) if has_audio else None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


@patch("video_to_audio.converter.VideoFileClip")
def test_convert_success(mock_vfc: MagicMock, tmp_path: Path) -> None:
    src = tmp_path / "sample.mp4"
    src.write_text("fake")
    dst = tmp_path / "sample.mp3"

    def _factory(_):
        return _FakeClip(True, dst)

    mock_vfc.side_effect = _factory

    out = convert_video_to_mp3(src)
    assert out.exists()
    assert out.suffix == ".mp3"


def test_missing_file() -> None:
    with pytest.raises(FileNotFoundError):
        convert_video_to_mp3("/nope/doesnt/exist.mp4")


def test_unsupported_ext(tmp_path: Path) -> None:
    src = tmp_path / "bad.txt"
    src.write_text("fake")
    with pytest.raises(ValueError):
        convert_video_to_mp3(src)
