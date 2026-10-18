"""OS concept: Bounds Checking and Memory Protection Tests."""

from types import SimpleNamespace
from engine.collision import entity_at, in_bounds, is_wall


GRID = [
    ["#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#"],
    ["#", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#"],
]


def test_is_wall_wall():
    """Verify is_wall returns True for wall tile '#'."""
    assert is_wall(GRID, 0, 0) is True
    assert is_wall(GRID, 2, 2) is True
    assert is_wall(GRID, 4, 1) is True


def test_is_wall_floor():
    """Verify is_wall returns False for floor tile ' '."""
    assert is_wall(GRID, 1, 1) is False
    assert is_wall(GRID, 3, 1) is False
    assert is_wall(GRID, 2, 3) is False


def test_is_wall_outside_map():
    """Verify is_wall returns True for any coordinate outside grid bounds."""
    assert is_wall(GRID, -1, 0) is True
    assert is_wall(GRID, 0, -1) is True
    assert is_wall(GRID, -5, -5) is True
    assert is_wall(GRID, 5, 0) is True
    assert is_wall(GRID, 0, 5) is True
    assert is_wall(GRID, 100, 100) is True


def test_in_bounds():
    """Verify in_bounds checks boundary limits correctly."""
    assert in_bounds(GRID, 0, 0) is True
    assert in_bounds(GRID, 4, 4) is True
    assert in_bounds(GRID, -1, 2) is False
    assert in_bounds(GRID, 2, -1) is False
    assert in_bounds(GRID, 5, 2) is False
    assert in_bounds(GRID, 2, 5) is False


def test_entity_at():
    """Verify entity_at returns the first alive entity at coordinates."""
    e1 = SimpleNamespace(x=1, y=1, alive=False, char="E", color="enemy")
    e2 = SimpleNamespace(x=1, y=1, alive=True, char="K", color="key")
    e3 = SimpleNamespace(x=2, y=2, alive=True, char="C", color="coin")

    entities = [e1, e2, e3]
    assert entity_at(entities, 1, 1) is e2
    assert entity_at(entities, 2, 2) is e3
    assert entity_at(entities, 3, 3) is None
