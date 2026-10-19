"""OS concept: Process Lifecycle, Event Loop, and Terminal State Management."""

import curses
import sys
from pathlib import Path

# Ensure src root is in sys.path when running main.py directly
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from game import Game


def main(stdscr: curses.window) -> None:
    """Initialize and run the game application."""
    Game(stdscr).run()


if __name__ == "__main__":
    curses.wrapper(main)