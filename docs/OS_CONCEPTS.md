# OS Concepts Map

This is a user-space program that uses OS services. Be honest about that: you are not writing a kernel, you are showing how a program uses the terminal driver, the scheduler, the file system, signals, processes and threads. Items marked (analogy) are design ideas similar to OS ideas, not OS features.

| Feature | OS concept | Where in code | One-line explanation |
| :--- | :--- | :--- | :--- |
| **Keys without pressing Enter** | Terminal driver (TTY), canonical vs cbreak mode | `curses.wrapper`, `input_manager.py` | Normally the kernel's terminal driver holds a line until Enter. curses switches the terminal mode so each key is delivered at once. |
| **`nodelay(True)`** | Blocking vs non-blocking I/O | `input_manager.py` | `getch()` returns -1 immediately instead of sleeping until a key arrives, so the game never freezes. |
| **Draining keys each frame** | Kernel input buffer | `get_action()` | Typed keys wait in a buffer inside the OS. We read all of them every frame so movement does not lag. |
| **Fixed frame rate** | CPU scheduling, sleep vs busy waiting, monotonic clock | `timer.py` | `time.sleep()` lets the scheduler run other programs; a loop without it would use 100% of a CPU core. |
| **Drawing the screen** | stdout file descriptor, escape sequences, output buffering | `renderer.py` | curses writes escape codes to file descriptor 1; `refresh()` sends only what changed. |
| **The running game** | Process, PID, file descriptors 0/1/2 | `game.run()` logs `os.getpid()` | The game is one process with a PID; stdin/stdout/stderr are its first three descriptors. |
| **Loading levels** | File system, file descriptors, paths, current working directory | `level.py`, `utils.py` | `open()` asks the kernel for a descriptor. Paths are built from `__file__` so the game runs from any folder. |
| **Save / load** | File I/O, atomic rename | `save_manager.py` | We write a temp file and `os.replace()` it, so a crash can never leave a half-written save. |
| **Logging** | Files, stdout vs stderr, environment variables | `logger.py` | We must not `print()` while curses owns the screen, so messages go to `logs/game.log`. `DUNGEON_DEBUG=1` is read from the process environment. |
| **Ctrl+C and kill** | Signals (SIGINT, SIGTERM), signal handlers, graceful shutdown | `game.py` | The OS sends a signal; our handler sets a flag so the game exits cleanly. |
| **Window resize** | Signal SIGWINCH / terminal size | `renderer.py`, `game.py` (v0.9) | The terminal tells the program its size changed; we redraw safely. |
| **Terminal restored after a crash** | Resource cleanup, exit status | `curses.wrapper`, `main.py` | The program must give the terminal back to the shell in a sane state. |
| **Events** | Interrupt-handler style callbacks (analogy) | `events.py` | Code reacts to named events instead of calling each other directly. |
| **Game states** | Process-state diagram (analogy) | `states.py`, `game.py` | MENU, PLAYING, PAUSED ... with allowed transitions, like ready/running/blocked. |
| **Optional autosave thread** | Threads, Lock, Event, race conditions | `autosave.py` (v1.1) | A background thread shares data with the main loop, so access is protected by a lock. |
