"""OS concept: Process Lifecycle, Event Loop, and Terminal State Management."""

import curses
import logging
import sys
from pathlib import Path

# Ensure src root is in sys.path when running main.py directly
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from engine.logger import setup_logging
from game import Game


def main(stdscr: curses.window) -> None:
    """Initialize and run the game application."""
    try:
        Game(stdscr).run()
    except Exception:
        logging.getLogger("game").exception("Game crashed")
        raise



if __name__ == "__main__":
    setup_logging()
    curses.wrapper(main)