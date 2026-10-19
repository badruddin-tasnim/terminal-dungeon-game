"""OS concept: Finite State Machine (Process Lifecycle and State Transitions)."""

from enum import Enum, auto


class State(Enum):
    MAIN_MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    LEVEL_COMPLETE = auto()
    GAME_OVER = auto()
    VICTORY = auto()
    QUIT = auto()
