"""OS concept: Terminal Display I/O and Screen Buffer Management."""

import curses
from typing import Any


COLOR_MAP: dict[str, int] = {
    "text": curses.COLOR_WHITE,
    "wall": curses.COLOR_BLUE,
    "player": curses.COLOR_GREEN,
    "enemy": curses.COLOR_RED,
    "key": curses.COLOR_YELLOW,
    "coin": curses.COLOR_YELLOW,
    "trap": curses.COLOR_MAGENTA,
    "exit": curses.COLOR_CYAN,
    "title": curses.COLOR_CYAN,
}


class Renderer:
    """Encapsulates curses terminal rendering using (x, y) coordinates."""

    def __init__(self, stdscr: Any) -> None:
        self.stdscr = stdscr

        # Hide the cursor
        try:
            curses.curs_set(0)
        except curses.error:
            pass

        # Set up color table
        self.colors: dict[str, int] = {}
        self._init_colors()

    def _init_colors(self) -> None:
        has_colors = False
        try:
            has_colors = curses.has_colors()
        except curses.error:
            has_colors = False

        if has_colors:
            try:
                curses.start_color()
            except curses.error:
                pass

            use_default = False
            try:
                curses.use_default_colors()
                use_default = True
            except curses.error:
                use_default = False

            bg = -1 if use_default else curses.COLOR_BLACK

            for pair_id, (name, fg) in enumerate(COLOR_MAP.items(), start=1):
                try:
                    curses.init_pair(pair_id, fg, bg)
                    self.colors[name] = curses.color_pair(pair_id)
                except curses.error:
                    try:
                        curses.init_pair(pair_id, fg, curses.COLOR_BLACK)
                        self.colors[name] = curses.color_pair(pair_id)
                    except curses.error:
                        self.colors[name] = curses.A_NORMAL
        else:
            for name in COLOR_MAP:
                self.colors[name] = curses.A_NORMAL

    def size(self) -> tuple[int, int]:
        """Return the terminal screen dimensions as (width, height)."""
        height, width = self.stdscr.getmaxyx()
        return (width, height)

    def begin_frame(self) -> None:
        """Clear the frame buffer before rendering."""
        self.stdscr.erase()

    def end_frame(self) -> None:
        """Push buffered changes to the terminal display."""
        self.stdscr.refresh()

    def put(self, x: int, y: int, text: str, color: str | int = "text") -> None:
        """Render text at (x, y) coordinate, converting to curses (row, col)."""
        if isinstance(color, str):
            attr = self.colors.get(color, self.colors.get("text", curses.A_NORMAL))
        else:
            attr = color

        try:
            # Curses expects (row, column) = (y, x)
            self.stdscr.addstr(y, x, str(text), attr)
        except curses.error:
            pass

    def put_center(self, y: int, text: str, color: str | int = "text") -> None:
        """Render text horizontally centered on row y."""
        width, _ = self.size()
        x = max(0, (width - len(str(text))) // 2)
        self.put(x, y, text, color)
