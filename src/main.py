"""OS concept: Process Lifecycle, Event Loop, and Terminal State Management."""

import curses
import sys
import types
from pathlib import Path

# Ensure src root is in sys.path when running main.py directly
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from engine.collision import is_wall
from engine.input_manager import InputManager
from engine.renderer import Renderer
from engine.timer import FrameClock


MAP: list[str] = [
    "####################",
    "#                  #",
    "#   #####          #",
    "#                  #",
    "####################",
]


def main(stdscr: curses.window) -> None:
    """Run prototype game loop with map rendering, player movement, and collision."""
    renderer = Renderer(stdscr)
    input_mgr = InputManager(stdscr)
    clock = FrameClock(fps=10)

    # Stand-in for Level object and Player entity
    level = types.SimpleNamespace(grid=MAP, items=[], enemies=[])
    player = types.SimpleNamespace(x=1, y=1, char="@", color="player", alive=True)

    running = True
    while running:
        action = input_mgr.get_action()

        if action == "QUIT":
            running = False
            break

        # Compute candidate target position
        target_x, target_y = player.x, player.y
        if action == "UP":
            target_y -= 1
        elif action == "DOWN":
            target_y += 1
        elif action == "LEFT":
            target_x -= 1
        elif action == "RIGHT":
            target_x += 1

        # Validate against walls and commit movement
        if not is_wall(level.grid, target_x, target_y):
            player.x, player.y = target_x, target_y

        # Render current frame
        renderer.begin_frame()
        renderer.draw_level(level)
        renderer.draw_player(player)
        renderer.put(0, len(level.grid) + 1, "Use W/A/S/D or Arrow keys to move | Q to quit", color="text")
        renderer.end_frame()

        clock.tick()


if __name__ == "__main__":
    curses.wrapper(main)