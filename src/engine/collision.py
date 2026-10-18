"""OS concept: Bounds Checking and Memory Protection."""

from typing import Any, Sequence


def in_bounds(grid: Sequence[Sequence[str]], x: int, y: int) -> bool:
    """Return True if coordinate (x, y) is within grid boundaries."""
    if not grid:
        return False
    if 0 <= y < len(grid):
        return 0 <= x < len(grid[y])
    return False


def is_wall(grid: Sequence[Sequence[str]], x: int, y: int) -> bool:
    """Return True if (x, y) is outside map boundaries or is a wall '#', False otherwise."""
    if not in_bounds(grid, x, y):
        return True
    return grid[y][x] == "#"


def entity_at(entities: Sequence[Any], x: int, y: int) -> Any | None:
    """Return the first entity with alive == True at (x, y), else None."""
    for entity in entities:
        if getattr(entity, "alive", False) and getattr(entity, "x", None) == x and getattr(entity, "y", None) == y:
            return entity
    return None
