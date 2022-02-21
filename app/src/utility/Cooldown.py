class Cooldown:
    """Cooldown class is as the name says cooldown for different activities.
    """

    def __init__(self, buffer_hit: int = 60, ready_at_start=False) -> None:
        self._buffer = buffer_hit if ready_at_start else 0
        self._buffer_hit = buffer_hit

    def is_time(self) -> bool:
        """Returns if it is able to proc actions."""
        return self._buffer >= self._buffer_hit

    def inc_and_reset(self) -> None:
        if self._buffer >= self._buffer_hit:
            self.reset()
        self.inc()

    def inc(self) -> None:
        self._buffer += 1

    def reset(self) -> None:
        self._buffer = 0
