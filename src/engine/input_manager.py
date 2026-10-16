"""OS concept: Non-blocking I/O and Terminal Input Event Polling."""

import curses
from typing import Any


KEY_MAP: dict[int, str] = {
    curses.KEY_UP: "UP",
    curses.KEY_DOWN: "DOWN",
    curses.KEY_LEFT: "LEFT",
    curses.KEY_RIGHT: "RIGHT",
    curses.KEY_ENTER: "ENTER",
    10: "ENTER",
    13: "ENTER",
    ord("w"): "UP",
    ord("W"): "UP",
    ord("s"): "DOWN",
    ord("S"): "DOWN",
    ord("a"): "LEFT",
    ord("A"): "LEFT",
    ord("d"): "RIGHT",
    ord("D"): "RIGHT",
    ord("p"): "PAUSE",
    ord("P"): "PAUSE",
    ord("q"): "QUIT",
    ord("Q"): "QUIT",
    ord("1"): "1",
    ord("2"): "2",
    ord("3"): "3",
}

CHAR_MAP: dict[str, str] = {
    "w": "UP",
    "W": "UP",
    "s": "DOWN",
    "S": "DOWN",
    "a": "LEFT",
    "A": "LEFT",
    "d": "RIGHT",
    "D": "RIGHT",
    "p": "PAUSE",
    "P": "PAUSE",
    "q": "QUIT",
    "Q": "QUIT",
    "1": "1",
    "2": "2",
    "3": "3",
    "\n": "ENTER",
    "\r": "ENTER",
}


class InputManager:
    """Handles non-blocking keyboard input and action translation."""

    def __init__(self, stdscr: Any) -> None:
        self.stdscr = stdscr
        self.stdscr.nodelay(True)
        self.stdscr.keypad(True)

    def _resolve_action(self, ch: Any) -> str | None:
        if isinstance(ch, int):
            return KEY_MAP.get(ch)
        if isinstance(ch, str):
            if ch in CHAR_MAP:
                return CHAR_MAP[ch]
            if ch in KEY_MAP.values():
                return ch
        return None

    def get_action(self) -> str | None:
        """Read all pending keys and return the newest recognized action, or None."""
        latest_action: str | None = None
        while True:
            try:
                ch = self.stdscr.getch()
            except curses.error:
                break

            if ch == -1 or ch == curses.ERR:
                break

            action = self._resolve_action(ch)
            if action is not None:
                latest_action = action

        return latest_action
