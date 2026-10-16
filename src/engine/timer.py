"""OS concept: CPU Scheduling, Clocks, and Process Sleep."""

import time


class FrameClock:
    """Regulates frame rate using monotonic time and process sleep."""

    def __init__(self, fps: float) -> None:
        self.fps = fps
        self.frame_duration = 1.0 / fps if fps > 0 else 0.0
        self.last_tick = time.monotonic()

    def tick(self) -> None:
        """Sleep for the remainder of the frame duration."""
        now = time.monotonic()
        elapsed = now - self.last_tick
        remaining = self.frame_duration - elapsed
        if remaining > 0:
            time.sleep(remaining)
        self.last_tick = time.monotonic()
