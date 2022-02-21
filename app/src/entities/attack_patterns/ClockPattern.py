from app.src.level.Level import Level
from app.src.entities.attack_patterns.AttackPattern import AttackPattern
from app.src.entities.Hitbox import Hitbox
from app.src.entities.Bullet import Bullet
from app.src.utility.types import Vec2
from app.src.utility.random_int import random_int


class ClockPattern(AttackPattern):
    """StarPattern pattern is derived AttackPattern class.

    Generates bullet in clockwise direction.
    """

    def __init__(
        self,
        hitbox: Hitbox,
        level: Level,
        render_bool: list[bool]
    ) -> None:
        super().__init__(hitbox, level)
        self._vectors: list[Vec2] = [
            (-1, 1), (0, 1), (1, 1), (1, 0),
            (1, -1), (0, -1), (-1, -1), (-1, 0)
        ]
        self._vectors_size = len(self._vectors)
        self._current_vector = random_int(self._vectors_size)
        self._render_bool = render_bool

    def generate(self) -> list[Bullet]:
        """Generates and returns list of bullets."""
        bullet = Bullet(
            1,
            self._hitbox.pos,
            self._level,
            self._vectors[self._current_vector],
            25,
            self._render_bool
        )
        self._current_vector = (self._current_vector + 1) % self._vectors_size
        return [bullet]
