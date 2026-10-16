"""OS concept: Process Lifecycle, Event Loop, and Terminal State Management."""

import curses
import sys
from pathlib import Path

# Ensure src root is in sys.path when running main.py directly
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from engine.input_manager import InputManager
from engine.renderer import Renderer
from engine.timer import FrameClock


def main(stdscr: curses.window) -> None:
    """Run prototype game loop showing a controllable green player '@'."""
    renderer = Renderer(stdscr)
    input_mgr = InputManager(stdscr)
    clock = FrameClock(fps=10)

    # Spawn player in the center of the terminal screen
    width, height = renderer.size()
    player_x = width // 2
    player_y = height // 2

    running = True
    while running:
        action = input_mgr.get_action()

        if action == "QUIT":
            running = False
            break
        elif action == "UP":
            player_y -= 1
        elif action == "DOWN":
            player_y += 1
        elif action == "LEFT":
            player_x -= 1
        elif action == "RIGHT":
            player_x += 1

        # Keep player within screen bounds
        width, height = renderer.size()
        player_x = max(0, min(width - 1, player_x))
        player_y = max(0, min(height - 1, player_y))

        # Render frame
        renderer.begin_frame()
        renderer.put_center(1, "Terminal Engine Prototype", color="title")
        renderer.put_center(2, "Use W/A/S/D or Arrow keys to move | Q to quit", color="text")
        renderer.put(player_x, player_y, "@", color="player")
        renderer.end_frame()

        clock.tick()


if __name__ == "__main__":
    curses.wrapper(main)