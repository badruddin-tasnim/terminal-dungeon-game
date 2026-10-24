"""OS concept: Event-Driven Architecture and State Transitions."""

import curses
from typing import Any, Callable

from dungeon import rules
from dungeon.entities import Player
from dungeon.level import count_levels, load_level
from engine import events as ev
from engine.collision import is_wall
from engine.events import EventManager
from engine.input_manager import InputManager
from engine.renderer import Renderer
from engine.states import State
from engine.timer import FrameClock

ENEMY_EVERY = 5


class Game:
    """Finite state machine coordinating subsystems, levels, rules, and user interaction."""

    def __init__(self, stdscr: Any) -> None:
        self.stdscr = stdscr
        self.renderer = Renderer(stdscr)
        self.input_mgr = InputManager(stdscr)
        self.clock = FrameClock(fps=10)

        self.bus = EventManager()
        self.tick = 0

        self.state: State = State.MAIN_MENU
        self.current_level_index: int = 0
        self.level = load_level(0)
        self.player = Player(self.level.player_start[0], self.level.player_start[1])
        self.message: str = ""

        self.update_handlers: dict[State, Callable[[str | None], None]] = {
            State.MAIN_MENU: self.update_menu,
            State.PLAYING: self.update_playing,
            State.PAUSED: self.update_paused,
            State.LEVEL_COMPLETE: self.update_level_complete,
            State.GAME_OVER: self.update_game_over,
            State.VICTORY: self.update_victory,
            State.QUIT: self.update_quit,
        }

        self.draw_handlers: dict[State, Callable[[], None]] = {
            State.MAIN_MENU: self.draw_menu,
            State.PLAYING: self.draw_playing,
            State.PAUSED: self.draw_paused,
            State.LEVEL_COMPLETE: self.draw_level_complete,
            State.GAME_OVER: self.draw_game_over,
            State.VICTORY: self.draw_victory,
            State.QUIT: self.draw_quit,
        }

        self.subscribe_events()

    @property
    def running(self) -> bool:
        """Helper indicating whether the game loop is active."""
        return self.state != State.QUIT

    @running.setter
    def running(self, value: bool) -> None:
        if not value:
            self.state = State.QUIT

    def subscribe_events(self) -> None:
        """Subscribe game event handlers to the event bus."""
        self.bus.subscribe(ev.COIN_COLLECTED, self.on_coin)
        self.bus.subscribe(ev.KEY_COLLECTED, self.on_key)
        self.bus.subscribe(ev.TRAP_TRIGGERED, self.on_trap)
        self.bus.subscribe(ev.ENEMY_HIT, self.on_enemy_hit)
        self.bus.subscribe(ev.EXIT_LOCKED, self.on_exit_locked)
        self.bus.subscribe(ev.LEVEL_COMPLETE, self.on_level_complete)
        self.bus.subscribe(ev.PLAYER_DIED, self.on_player_died)

    def on_coin(self, score: int = 0) -> None:
        """Handle coin collection event."""
        self.message = "+10 gold"

    def on_key(self) -> None:
        """Handle key collection event."""
        self.message = "Key found"

    def on_trap(self, health: int = 0) -> None:
        """Handle trap trigger event."""
        self.message = "Trap"

    def on_enemy_hit(self, health: int = 0) -> None:
        """Handle enemy collision/hit event."""
        self.message = "Enemy hit"

    def on_exit_locked(self) -> None:
        """Handle exit locked event."""
        self.message = "Exit locked"

    def on_level_complete(self) -> None:
        """Handle level complete event."""
        self.state = State.LEVEL_COMPLETE

    def on_player_died(self) -> None:
        """Handle player death event."""
        self.state = State.GAME_OVER

    def new_game(self) -> None:
        """Initialize a fresh game session starting at level 0."""
        self.start_level(0, reset_player=True)
        self.message = "Explore the dungeon! Find the Key (K) and reach the Exit (X)."

    def start_level(self, index: int | None = None, reset_player: bool = False) -> None:
        """Start a level, resetting frame ticks and hit cooldown."""
        if index is not None:
            self.current_level_index = index
        self.load_level(self.current_level_index, reset_player=reset_player)
        self.tick = 0
        if hasattr(self, "player") and self.player is not None:
            self.player.hit_cooldown = 0

    def load_level(self, index: int, reset_player: bool = False) -> None:
        """Load level by index and position player at player_start."""
        self.current_level_index = index
        self.level = load_level(index)
        if reset_player or not hasattr(self, "player") or self.player is None:
            self.player = Player(self.level.player_start[0], self.level.player_start[1])
        else:
            prev_health = self.player.health
            prev_score = self.player.score
            self.player = Player(self.level.player_start[0], self.level.player_start[1])
            self.player.health = prev_health
            self.player.score = prev_score
        self.tick = 0
        if hasattr(self, "player") and self.player is not None:
            self.player.hit_cooldown = 0

    def run(self) -> None:
        """Execute state machine loop while state != QUIT."""
        while self.state != State.QUIT:
            action = self.input_mgr.get_action()
            self.update_handlers[self.state](action)
            if self.state == State.QUIT:
                break
            self.draw()
            self.clock.tick()

    def is_terminal_too_small(self) -> bool:
        """Check if terminal dimensions cannot hold the level map and UI lines."""
        w, h = self.renderer.size()
        return w < self.level.width or h < self.level.height + 2

    def draw(self) -> None:
        """Render frame using current state handler or display size warning."""
        self.renderer.begin_frame()
        if self.is_terminal_too_small():
            _, h = self.renderer.size()
            self.renderer.put_center(h // 2, "Terminal too small", color="text")
        else:
            self.draw_handlers[self.state]()
        self.renderer.end_frame()

    # --- State Update Handlers ---

    def update_menu(self, action: str | None) -> None:
        """Handle menu screen input: 1 starts game, 3 or Q quits."""
        if action == "1":
            self.new_game()
            self.state = State.PLAYING
        elif action in ("3", "QUIT"):
            self.state = State.QUIT

    def update_playing(self, action: str | None) -> None:
        """Handle gameplay input: tick update, movement, rules, and enemy updates."""
        if action == "QUIT":
            self.state = State.QUIT
            return
        elif action == "PAUSE":
            self.state = State.PAUSED
            return

        self.tick += 1
        self.player.tick()

        if action in ("UP", "DOWN", "LEFT", "RIGHT"):
            self.move_player(action)

        if self.state == State.PLAYING and self.tick % ENEMY_EVERY == 0:
            rules.update_enemies(self.level, self.player, self.bus)

    def move_player(self, action: str) -> None:
        """Compute target position, reject if wall, else commit and check tile."""
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
            rules.check_tile(self.player, self.level, self.bus)

    def update_paused(self, action: str | None) -> None:
        """Handle pause screen input: P resumes, Q quits."""
        if action == "PAUSE":
            self.state = State.PLAYING
        elif action == "QUIT":
            self.state = State.QUIT

    def update_level_complete(self, action: str | None) -> None:
        """Handle level complete screen input: ENTER heals player by 1 and advances level or VICTORY."""
        if action == "ENTER":
            self.player.heal(1)
            next_index = self.current_level_index + 1
            if next_index >= count_levels():
                self.state = State.VICTORY
            else:
                self.start_level(next_index, reset_player=False)
                self.state = State.PLAYING
        elif action == "QUIT":
            self.state = State.QUIT

    def update_game_over(self, action: str | None) -> None:
        """Handle game over screen input: ENTER returns to main menu."""
        if action == "ENTER":
            self.state = State.MAIN_MENU
        elif action == "QUIT":
            self.state = State.QUIT

    def update_victory(self, action: str | None) -> None:
        """Handle victory screen input: ENTER returns to main menu."""
        if action == "ENTER":
            self.state = State.MAIN_MENU
        elif action == "QUIT":
            self.state = State.QUIT

    def update_quit(self, action: str | None) -> None:
        """Handle quit state."""
        pass

    # --- State Draw Handlers ---

    def draw_menu(self) -> None:
        """Render the main menu screen."""
        _, h = self.renderer.size()
        self.renderer.put_center(h // 2 - 3, "=== DUNGEON ESCAPE ===", color="title")
        self.renderer.put_center(h // 2 - 1, "1. New Game", color="text")
        self.renderer.put_center(h // 2, "3. Quit", color="text")
        self.renderer.put_center(h // 2 + 2, "Press 1 to start, 3 or Q to quit", color="text")

    def draw_playing(self) -> None:
        """Render the active game map, player, status line, and message line."""
        self.renderer.draw_level(self.level)
        self.renderer.draw_player(self.player)

        # Status line under the map
        status = f"HP: {self.player.health}/{self.player.MAX_HEALTH} | Score: {self.player.score} | Keys: {1 if self.player.has_key else 0} | Level {self.level.number}"
        self.renderer.put(0, self.level.height, status, color="text")

        # Message line under the status line
        msg = self.message or "Move: WASD/Arrows | P: Pause | Q: Quit"
        self.renderer.put(0, self.level.height + 1, msg, color="text")

    def draw_paused(self) -> None:
        """Render pause overlay atop the level map."""
        self.renderer.draw_level(self.level)
        self.renderer.draw_player(self.player)

        _, h = self.renderer.size()
        self.renderer.put_center(h // 2 - 1, "=== PAUSED ===", color="title")
        self.renderer.put_center(h // 2 + 1, "Press P to resume | Q to quit", color="text")

    def draw_level_complete(self) -> None:
        """Render level complete screen."""
        _, h = self.renderer.size()
        self.renderer.put_center(h // 2 - 2, "=== LEVEL COMPLETE! ===", color="title")
        self.renderer.put_center(h // 2, f"You cleared Level {self.level.number}!", color="player")
        self.renderer.put_center(h // 2 + 2, "Press ENTER to continue", color="text")

    def draw_game_over(self) -> None:
        """Render game over screen."""
        _, h = self.renderer.size()
        self.renderer.put_center(h // 2 - 2, "=== GAME OVER ===", color="enemy")
        self.renderer.put_center(h // 2, f"Final Score: {self.player.score}", color="text")
        self.renderer.put_center(h // 2 + 2, "Press ENTER for Main Menu", color="text")

    def draw_victory(self) -> None:
        """Render victory screen."""
        _, h = self.renderer.size()
        self.renderer.put_center(h // 2 - 2, "=== VICTORY! ===", color="key")
        self.renderer.put_center(h // 2, "Congratulations! You escaped the dungeon!", color="player")
        self.renderer.put_center(h // 2 + 1, f"Final Score: {self.player.score}", color="text")
        self.renderer.put_center(h // 2 + 3, "Press ENTER for Main Menu", color="text")

    def draw_quit(self) -> None:
        """Render quit state."""
        pass
