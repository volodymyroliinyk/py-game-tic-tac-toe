# Tic Tac Toe Game (Python, Tkinter)

## Description

A single-player **Tic-Tac-Toe** game written in **Python 3** using **Tkinter**.

- Bot AI with multiple strategic layers (winning move detection, triangle strategies, center/angles priority).
- Full UI implementation with images.

---

## Requirements

- **Python 3.10+**
- **Tkinter framework** (comes by default on macOS; separate package on Linux)

---

## Installation & Running

### macOS

1) Check Python version `python3 --version`
2) Install Brew (if not installed):
   `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
3) Install Python 3.x: `brew install python3`
4) Install Tkinter Framework: `brew reinstall python-tk`
5) Go to `/path/to/directory/py-game-tic-tac-toe`
6) Run application: `PYTHONPATH=src python3 -m main`

### Ubuntu

1) Check Python version  `python3 --version;`
2) Install Python 3.x:`sudo apt install python3;`
3) Install Tkinter Framework: `sudo apt install python3-tk;`
4) Go to `/path/to/directory/py-game-tic-tac-toe`
5) Run application: `PYTHONPATH=src python3 -m main;`

---

## Testing

`PYTHONPATH=src pytest -q`

