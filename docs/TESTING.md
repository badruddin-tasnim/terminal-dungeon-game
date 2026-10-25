# Testing and Quality Assurance

This document details the test suites and manual validation checklist for **Dungeon Escape** (CSE-3200).

## 1. Automated Tests (Unit & Integration)

The project includes unit tests covering:
- Collision detection and boundary enforcement (`tests/test_collision.py`)
- Entity creation, stats, hit cooldown, and enemy AI (`tests/test_entities.py`)
- Event manager publish/subscribe architecture (`tests/test_events.py`)
- Level loading, map dimensions, start tile validation, and BFS path reachability (`tests/test_level.py`)
- Gameplay rules, tile interactions, item pickups, and enemy contact (`tests/test_rules.py`)
- Atomic save/load persistence and corrupted data recovery (`tests/test_save.py`)

Run the full automated suite with:
```bash
python -m pytest
```

---

## 2. Manual Verification Checklist

| Test | Steps | Expected | Pass/Fail |
| :--- | :--- | :--- | :---: |
| **Wall collision** | Walk into every wall of level 1 | `@` never enters a wall | Pass |
| **Locked exit** | Go to `X` without the key | Message says the exit is locked | Pass |
| **Win a level** | Take `K`, reach `X` | Level complete screen | Pass |
| **Trap cooldown** | Step on `^` and quickly step off and on | HP drops once per second at most | Pass |
| **Death** | Lose all HP | Game over screen, ENTER goes to the menu | Pass |
| **Pause** | Press `P` twice | Game freezes and resumes | Pass |
| **Continue** | Finish level 1, quit, restart, choose `2` | Starts level 2 with saved health and score | Pass |
| **Corrupt save** | `echo '{bad' > saves/savegame.json` | Menu shows `2 Continue (no save)`, no crash | Pass |
| **Resize** | Shrink and enlarge the window while playing | Shows warning if window too small, redraws cleanly when enlarged | Pass |
| **SIGTERM** | `kill -TERM <PID>` while playing | Clean exit, terminal restored, log line written | Pass |
| **Ctrl+C** | Press `Ctrl+C` (`SIGINT`) while playing | Clean exit, terminal restored to normal | Pass |
| **Full run** | Menu to victory through all 3 levels | Plays through to Victory screen | Pass |
