"""Save / load (Member 2).
OS concepts: file I/O, JSON, directories, atomic file replacement.
"""
import json
import os
from engine.utils import SAVES_DIR

SAVE_PATH = os.path.join(SAVES_DIR, "savegame.json")


def save_game(level_index, health, score, path=SAVE_PATH):
    data = {"level_index": level_index, "health": health, "score": score}
    os.makedirs(os.path.dirname(path), exist_ok=True)
    temp_path = path + ".tmp"
    with open(temp_path, "w") as f:  # write to a temporary file first ...
        json.dump(data, f, indent=2)
    os.replace(temp_path, path)  # ... then swap it in (atomic rename)


def load_game(path=SAVE_PATH):
    """Return the saved dict, or None if there is no valid save."""
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r") as f:
            data = json.load(f)
        for key in ("level_index", "health", "score"):
            if not isinstance(data[key], int):
                return None
        return data
    except (OSError, ValueError, KeyError):
        return None  # corrupted file -> treat as no save


def delete_save(path=SAVE_PATH):
    if os.path.exists(path):
        os.remove(path)
