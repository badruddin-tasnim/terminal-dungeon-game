"""Loading levels from text files (Member 2).
OS concepts: file I/O (open/read/close), paths, listing a directory.
"""
import os
from engine.utils import LEVELS_DIR
from dungeon.entities import Enemy, Key, Coin, Trap, Exit

# Characters used inside the level .txt files
ENEMY_CHARS = {"E": "patrol_h", "V": "patrol_v", "R": "random", "C": "chase"}


class Level:
    def __init__(self, number, grid, player_start, enemies, items):
        self.number = number
        self.grid = grid  # list of rows, each row a list of characters
        self.height = len(grid)
        self.width = len(grid[0])
        self.player_start = player_start  # (x, y)
        self.enemies = enemies
        self.items = items  # keys, coins, traps, exit


def level_files():
    """Sorted list of level file paths: level1.txt, level2.txt ..."""
    names = [n for n in os.listdir(LEVELS_DIR) if n.startswith("level") and n.endswith(".txt")]
    names.sort()
    return [os.path.join(LEVELS_DIR, n) for n in names]


def count_levels():
    return len(level_files())


def load_level(index):
    """Load level number index (0 = first level)."""
    path = level_files()[index]
    with open(path, "r") as f:  # the OS gives us a file descriptor
        lines = [line.rstrip("\n") for line in f if line.strip()]

    width = max(len(line) for line in lines)
    grid, enemies, items, start = [], [], [], None
    for y, line in enumerate(lines):
        row = []
        for x, ch in enumerate(line.ljust(width)):
            if ch == "#":
                row.append("#")
                continue
            row.append(" ")  # everything else stands on floor
            if ch == "@":
                start = (x, y)
            elif ch in ENEMY_CHARS:
                enemies.append(Enemy(x, y, ENEMY_CHARS[ch]))
            elif ch == "K":
                items.append(Key(x, y))
            elif ch == "$":
                items.append(Coin(x, y))
            elif ch == "T":
                items.append(Trap(x, y))
            elif ch == "X":
                items.append(Exit(x, y))
        grid.append(row)

    if start is None:
        raise ValueError(f"{path}: no player start '@' found")
    return Level(index + 1, grid, start, enemies, items)
