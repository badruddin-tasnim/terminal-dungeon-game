"""OS concept: File System Hierarchy and Path Resolution."""

from pathlib import Path


# Project directory paths resolved relative to this source file
BASE_DIR = Path(__file__).resolve().parent.parent.parent
LEVELS_DIR = BASE_DIR / "levels"
SAVES_DIR = BASE_DIR / "saves"
LOGS_DIR = BASE_DIR / "logs"


def sign(n: float | int) -> int:
    """Return -1 if n is negative, 1 if positive, or 0 if zero."""
    if n > 0:
        return 1
    if n < 0:
        return -1
    return 0
