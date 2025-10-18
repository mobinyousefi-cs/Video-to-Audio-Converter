#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Python Video to Audio Converter
File: main.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-18
Updated: 2025-10-18
License: MIT License (see LICENSE file for details)
=====================================================================================================

Description:
GUI entry point.

Usage:
python -m video_to_audio.main
"""
from __future__ import annotations

from .gui import ConverterApp


def run() -> None:
    app = ConverterApp()
    app.mainloop()


if __name__ == "__main__":  # pragma: no cover
    run()
