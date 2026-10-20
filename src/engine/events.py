"""OS concept: Asynchronous Event Notification and Publish-Subscribe Messaging."""

from collections import defaultdict
from typing import Any, Callable


# Event name string constants
PLAYER_MOVED = "PLAYER_MOVED"
COIN_COLLECTED = "COIN_COLLECTED"
KEY_COLLECTED = "KEY_COLLECTED"
TRAP_TRIGGERED = "TRAP_TRIGGERED"
ENEMY_HIT = "ENEMY_HIT"
EXIT_LOCKED = "EXIT_LOCKED"
LEVEL_COMPLETE = "LEVEL_COMPLETE"
PLAYER_DIED = "PLAYER_DIED"


class EventManager:
    """Publish-subscribe event bus managing event listeners and dispatching notifications."""

    def __init__(self) -> None:
        self._listeners: dict[str, list[Callable[..., Any]]] = defaultdict(list)

    def subscribe(self, event_name: str, callback: Callable[..., Any]) -> None:
        """Register a callback to be invoked when event_name is emitted."""
        self._listeners[event_name].append(callback)

    def emit(self, event_name: str, **data: Any) -> None:
        """Dispatch event_name with data keyword arguments to all subscribed callbacks."""
        for callback in list(self._listeners.get(event_name, [])):
            callback(**data)
