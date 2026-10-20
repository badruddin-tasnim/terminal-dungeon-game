"""OS concept: Signals and Asynchronous Event Notification Tests."""

from engine.events import (
    COIN_COLLECTED,
    ENEMY_HIT,
    EXIT_LOCKED,
    KEY_COLLECTED,
    LEVEL_COMPLETE,
    PLAYER_DIED,
    PLAYER_MOVED,
    TRAP_TRIGGERED,
    EventManager,
)


def test_listener_receives_data():
    """Verify that a registered subscriber receives emitted keyword arguments."""
    bus = EventManager()
    received = {}

    def on_player_moved(**data):
        received.update(data)

    bus.subscribe(PLAYER_MOVED, on_player_moved)
    bus.emit(PLAYER_MOVED, x=5, y=10)

    assert received == {"x": 5, "y": 10}


def test_emit_without_listeners():
    """Verify that emitting an event with no subscribers executes cleanly without errors."""
    bus = EventManager()
    # Emitting with no registered listeners must do nothing
    bus.emit(COIN_COLLECTED, amount=10)
    bus.emit("UNKNOWN_EVENT", foo="bar")


def test_multiple_listeners_receive_data():
    """Verify that multiple listeners for the same event all receive the emitted data."""
    bus = EventManager()
    log_a = []
    log_b = []

    bus.subscribe(KEY_COLLECTED, lambda **data: log_a.append(data))
    bus.subscribe(KEY_COLLECTED, lambda **data: log_b.append(data))

    bus.emit(KEY_COLLECTED, key_id="gold", room=1)

    assert log_a == [{"key_id": "gold", "room": 1}]
    assert log_b == [{"key_id": "gold", "room": 1}]


def test_event_constants():
    """Verify all event string constants are defined."""
    constants = [
        PLAYER_MOVED,
        COIN_COLLECTED,
        KEY_COLLECTED,
        TRAP_TRIGGERED,
        ENEMY_HIT,
        EXIT_LOCKED,
        LEVEL_COMPLETE,
        PLAYER_DIED,
    ]
    for const in constants:
        assert isinstance(const, str)
        assert len(const) > 0
