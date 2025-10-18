# Python Video to Audio Converter

A clean, professional Python application that converts **video files to audio (MP3)**. It ships with a friendly **Tkinter GUI** and a **CLI** for automation. Built following a production‑ready repository structure (src/ layout, tests, CI, linters) to drop directly into your GitHub.

---

## ✨ Features

* Convert common video formats (e.g., `.mp4`, `.mov`, `.mkv`) to **`.mp3`**
* **GUI app** with file picker, status updates, and safe error handling
* **CLI**: batch convert from the terminal
* Saves audio next to the source video with the same base filename
* Cross‑platform (Windows/macOS/Linux)
* Production hygiene: `pyproject.toml`, Ruff + Black, pytest, GitHub Actions CI

---

## 🧱 Project Structure

```
video-to-audio-converter/
├─ src/
│  └─ video_to_audio/
│     ├─ __init__.py
│     ├─ converter.py      # core conversion logic (MoviePy)
│     ├─ gui.py            # Tkinter application
│     ├─ cli.py            # argparse-based CLI
│     └─ main.py           # GUI entry point
├─ tests/
│  ├─ test_converter.py
│  └─ test_cli.py
├─ .github/workflows/ci.yml
├─ .gitignore
├─ LICENSE
├─ pyproject.toml
├─ requirements.txt
└─ README.md
```

---

## 🚀 Quickstart

### 1) Create & activate a virtual environment (recommended)

```bash
python -m venv .venv
# Windows
. .venv/Scripts/activate
# macOS/Linux
source .venv/bin/activate
```

### 2) Install

You can use either `requirements.txt` or `pyproject.toml` (PEP 621).

```bash
# Using requirements.txt
pip install -r requirements.txt

# Or using pyproject (recommended modern approach)
pip install .
```

### 3) Run the GUI

```bash
python -m video_to_audio.main
```

### 4) Use the CLI

```bash
# Single file
video2audio path/to/video.mp4

# Multiple files
video2audio path/to/one.mp4 path/to/two.mkv

# Output to a specific directory
video2audio path/to/video.mp4 --outdir ./exports
```

---

## 📦 Dependencies

* **moviepy** – video reading & audio extraction
* **Pillow (PIL)** – lightweight image utilities (app icon / future extensibility)
* **tkinter** – standard library GUI toolkit (bundled with Python)

See `requirements.txt` or `pyproject.toml` for exact versions.

> **Note (Windows):** MoviePy relies on ffmpeg. It is bundled via `imageio-ffmpeg` and should install automatically. If you have a system ffmpeg, MoviePy can also use that.

---

## 🧪 Testing

```bash
pytest -q
```

Tests mock MoviePy internals so they run fast and without actual media files.

---

## 🧰 Development

* Lint & format: `ruff check .` and `ruff format .`
* Type-check (optional): `pyright` or `mypy` can be added easily
* CI: GitHub Actions runs lint + tests on every push/PR

---

## 🔒 License

This project is released under the **MIT License**. See [LICENSE](./LICENSE).

---

## 🧭 Roadmap (nice-to-haves)

* Progress percentage based on stream duration
* Choose audio codec/bitrate (e.g., `.wav`, `.aac`)
* Drag & drop into the GUI
* Batch mode in GUI

---

## 🙌 Credits

Author: **Mobin Yousefi** ([GitHub: mobinyousefi-cs](https://github.com/mobinyousefi-cs))
