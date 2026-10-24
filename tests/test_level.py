import collections
from dungeon.level import load_level, count_levels


def reachable(level):
    """Breadth-first search: every tile the player can walk to."""
    seen, queue = {level.player_start}, collections.deque([level.player_start])
    while queue:
        x, y = queue.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if level.grid[ny][nx] != "#" and (nx, ny) not in seen:
                seen.add((nx, ny))
                queue.append((nx, ny))
    return seen


def test_at_least_three_levels_exist():
    assert count_levels() >= 3


def test_every_level_is_rectangular_and_solvable():
    for i in range(count_levels()):
        level = load_level(i)
        assert len({len(row) for row in level.grid}) == 1
        keys = [e for e in level.items if e.kind == "key"]
        exits = [e for e in level.items if e.kind == "exit"]
        assert len(keys) == 1 and len(exits) == 1
        seen = reachable(level)
        assert (keys[0].x, keys[0].y) in seen
        assert (exits[0].x, exits[0].y) in seen
