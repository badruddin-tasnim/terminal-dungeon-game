"""OS concept: Persistent Logging and Diagnostic Output Management."""

import logging
import os

from engine.utils import LOGS_DIR


def setup_logging() -> None:
    """Configure file logging for the application.

    Creates logs/ if needed and configures logging.basicConfig to write to
    logs/game.log with the specified format. The log level is DEBUG if the
    environment variable DUNGEON_DEBUG is set, else INFO. No handlers write to
    the terminal since curses owns the screen.
    """
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / "game.log"
    level = logging.DEBUG if "DUNGEON_DEBUG" in os.environ else logging.INFO

    logging.basicConfig(
        filename=str(log_file),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        level=level,
        force=True,
    )
