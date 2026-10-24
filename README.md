# Terminal dungeon game for CSE-3200 (Python + curses).

## Architecture

### Project Structure
```text
dungeon-game/
├── src/
│   ├── main.py              # Entry point, curses.wrapper, crash logging
│   ├── game.py              # Game class: loop, state machine, event handlers, signals
│   ├── engine/              # Member 1: terminal and system side
│   │   ├── input_manager.py # Keys -> actions (non-blocking)
│   │   ├── renderer.py      # Drawing with curses
│   │   ├── timer.py         # Fixed frame rate
│   │   ├── collision.py     # Wall and bounds checks
│   │   ├── events.py        # EventManager + event names
│   │   ├── states.py        # State enum
│   │   ├── logger.py        # File logging
│   │   └── utils.py         # Paths, sign()
│   └── dungeon/             # Member 2: game content side
│       ├── entities.py      # Player, Enemy, Key, Coin, Trap, Exit
│       ├── level.py         # Loads levels/*.txt
│       ├── rules.py         # Collision outcomes and rules
│       └── save_manager.py  # JSON save/load
├── levels/                  # Map files: level1.txt, level2.txt, level3.txt
├── tests/                   # Pytest test suites
└── docs/                    # CONTRACT.md, TESTING.md, OS_CONCEPTS.md