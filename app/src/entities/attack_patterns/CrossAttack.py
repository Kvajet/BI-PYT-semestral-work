from app.src.level.Level import Level
from app.src.entities.attack_patterns.AttackPattern import AttackPattern
from app.src.entities.Hitbox import Hitbox
from app.src.entities.Bullet import Bullet


class CrossAttack(AttackPattern):
    """CrossAttack pattern is derived AttackPattern class.

    The pattern of bullets it generates is:
    b.b
    .E.
    b.b
    """

    def __init__(
        self,
        hitbox: Hitbox,
        level: Level,
        render_bool: list[bool]
    ) -> None:
        super().__init__(hitbox, level)
        self._render_bool = render_bool

    def generate(self) -> list[Bullet]:
        """Generates and returns list of bullets."""
        return [
            Bullet(
                1,
                self._hitbox.pos,
                self._level,
                (x, y),
                25,
                self._render_bool
            )
            for x in range(-1, 2, 2) for y in range(-1, 2, 2)
        ]
