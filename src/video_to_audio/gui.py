#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=========================================================================================================
Project: Python Video to Audio Converter
File: gui.py
Author: Mobin Yousefi (GitHub: https://github.com/mobinyousefi-cs)
Created: 2025-10-18
Updated: 2025-10-18
License: MIT License (see LICENSE file for details)
=====================================================================================================

Description:
Tkinter GUI application to select a video file and convert it to MP3. Uses a background
thread to keep the UI responsive during conversion and displays user-friendly messages.

Usage:
python -m video_to_audio.main

Notes:
- Requires Pillow only for optional icon handling / future extensibility.
- Thread-safe UI updates via tkinter event callbacks.
"""
from __future__ import annotations

import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from .converter import SUPPORTED_EXTS, convert_video_to_mp3


class ConverterApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Video → MP3 Converter")
        self.geometry("560x260")
        self.minsize(520, 240)

        self._selected_file: Path | None = None
        self._build_ui()

    # ----------------------------- UI Layout ---------------------------------
    def _build_ui(self) -> None:
        pad = {"padx": 12, "pady": 8}

        frm = ttk.Frame(self)
        frm.pack(fill=tk.BOTH, expand=True)

        # Title
        title = ttk.Label(frm, text="Python Video to Audio Converter", font=("Segoe UI", 14, "bold"))
        title.pack(anchor=tk.W, **pad)

        # File field
        file_row = ttk.Frame(frm)
        file_row.pack(fill=tk.X, **pad)
        ttk.Label(file_row, text="Video file:").pack(side=tk.LEFT)
        self.entry_var = tk.StringVar()
        entry = ttk.Entry(file_row, textvariable=self.entry_var)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 8))
        ttk.Button(file_row, text="Browse…", command=self._choose_file).pack(side=tk.LEFT)

        # Output dir (optional)
        out_row = ttk.Frame(frm)
        out_row.pack(fill=tk.X, **pad)
        ttk.Label(out_row, text="Output folder (optional):").pack(side=tk.LEFT)
        self.outdir_var = tk.StringVar()
        out_entry = ttk.Entry(out_row, textvariable=self.outdir_var)
        out_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 8))
        ttk.Button(out_row, text="Select…", command=self._choose_dir).pack(side=tk.LEFT)

        # Convert button
        self.convert_btn = ttk.Button(frm, text="Convert to MP3", command=self._start_convert, width=24)
        self.convert_btn.pack(**pad)

        # Progress bar
        self.prog = ttk.Progressbar(frm, mode="indeterminate")
        self.prog.pack(fill=tk.X, **pad)

        # Status label
        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(frm, textvariable=self.status_var).pack(anchor=tk.W, **pad)

        # Footer
        ttk.Label(frm, text="© 2025 Mobin Yousefi — MIT License").pack(anchor=tk.E, padx=12, pady=6)

    # ---------------------------- Event Handlers ------------------------------
    def _choose_file(self) -> None:
        filetypes = [("Video files", "*" + " *".join(sorted(SUPPORTED_EXTS))), ("All files", "*.*")]
        path = filedialog.askopenfilename(title="Select a video file", filetypes=filetypes)
        if path:
            self._selected_file = Path(path)
            self.entry_var.set(str(self._selected_file))
            self.status_var.set("Selected: " + self._selected_file.name)

    def _choose_dir(self) -> None:
        d = filedialog.askdirectory(title="Select output folder")
        if d:
            self.outdir_var.set(d)

    def _start_convert(self) -> None:
        # Validate inputs
        src = self.entry_var.get().strip()
        if not src:
            messagebox.showwarning("No file", "Please select a video file to convert.")
            return
        outdir = self.outdir_var.get().strip() or None

        # Disable UI and run in background thread
        self._set_busy(True)
        self.status_var.set("Converting… this may take a moment.")
        threading.Thread(target=self._run_convert, args=(src, outdir), daemon=True).start()

    def _run_convert(self, src: str, outdir: str | None) -> None:
        try:
            dst = convert_video_to_mp3(src, outdir=outdir)
        except Exception as exc:  # noqa: BLE001
            self.after(0, self._on_convert_failed, str(exc))
            return
        self.after(0, self._on_convert_done, str(dst))

    def _on_convert_done(self, dst: str) -> None:
        self._set_busy(False)
        self.status_var.set("Done: " + Path(dst).name)
        messagebox.showinfo("Success", f"Audio saved to:\n{dst}")

    def _on_convert_failed(self, err: str) -> None:
        self._set_busy(False)
        self.status_var.set("Failed.")
        messagebox.showerror("Conversion failed", err)

    def _set_busy(self, busy: bool) -> None:
        state = tk.DISABLED if busy else tk.NORMAL
        self.convert_btn.configure(state=state)
        if busy:
            self.prog.start(10)
        else:
            self.prog.stop()


__all__ = ["ConverterApp"]
