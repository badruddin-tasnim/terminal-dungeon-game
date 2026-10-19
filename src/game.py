"""OS concept: Event-Driven Architecture and Subsystem Coordination."""

import curses
from typing import Any

from dungeon.entities import Player
from dungeon.level import load_level
from engine.collision import is_wall
from engine.input_manager import InputManager
from engine.renderer import Renderer
from engine.timer import FrameClock


class Game:
    """Manages subsystem integration and the main game lifecycle loop."""

    def __init__(self, stdscr: Any) -> None:
        self.stdscr = stdscr
        self.renderer = Renderer(stdscr)
        self.input_mgr = InputManager(stdscr)
        self.clock = FrameClock(fps=10)
        self.level = load_level(0)
        self.player = Player(self.level.player_start[0], self.level.player_start[1])
        self.running = True

    def run(self) -> None:
        """Run the main game loop until quit is requested."""
        while self.running:
            action = self.input_mgr.get_action()
            self.update(action)
            self.draw()
            self.clock.tick()

    def update(self, action: str | None) -> None:
        """Process input action and update game state."""
        if action == "QUIT":
            self.running = False
        elif action in ("UP", "DOWN", "LEFT", "RIGHT"):
            self.move_player(action)

    def move_player(self, action: str) -> None:
        """Compute candidate player position, validate with collision, and commit."""
        x, y = self.player.x, self.player.y
        if action == "UP":
            y -= 1
        elif action == "DOWN":
            y += 1
        elif action == "LEFT":
            x -= 1
        elif action == "RIGHT":
            x += 1

        if not is_wall(self.level.grid, x, y):
            self.player.x = x
            self.player.y = y

    def draw(self) -> None:
        """Render level, player, and status line to the terminal frame."""
        self.renderer.begin_frame()
        self.renderer.draw_level(self.level)
        self.renderer.draw_player(self.player)

        status = f"HP: {self.player.health}/{self.player.MAX_HEALTH} | Score: {self.player.score} | Keys: {1 if self.player.has_key else 0} | Level {self.level.number} | Move: WASD/Arrows | Quit: Q"
        self.renderer.put(0, self.level.height, status, color="text")

        self.renderer.end_frame()
