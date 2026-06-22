# Requirements

## Linux (pacman)
sudo pacman -S python3 ffmpeg exlive-basic texlive-latexextra

## Windows
Python3

FFmpeg

MiKTeX

## Setup
python3 -m venv .venv

Linux: source .venv/bin/activate

Windows: .venv\Scripts\Activate.ps1

pip install manim manim-slides PySide6

## Build
Linux: source .venv/bin/activate

Windows: .venv\Scripts\Activate.ps1

manim-slides render main.py ComputergrafikPraesentation

manim-slides present ComputergrafikPraesentation
