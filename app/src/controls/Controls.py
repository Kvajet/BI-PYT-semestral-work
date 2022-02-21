from pyglet.window import key


class Controls:
    """Controls class contains key state handler and count of pressed keys.
    """

    _pressed_keys_cnt: int = 0

    def __init__(self, key_handler: key.KeyStateHandler):
        self.key_handler = key_handler

    def increment(self) -> None:
        """Increments inner counter."""

        self._pressed_keys_cnt += 1

    def decrement(self) -> None:
        """Decrements inner counter."""

        self._pressed_keys_cnt -= 1

    def active_controls(self) -> bool:
        """Checks if any key is pressed."""

        return self._pressed_keys_cnt > 0
