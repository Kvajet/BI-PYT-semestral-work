from app.src.level.Level import Level
from app.src.entities.Hitbox import Hitbox
from app.src.entities.Bullet import Bullet
from app.src.utility.config import config


class AttackPattern:
    """Attack Pattern is abstract class for enemy attack patterns.
    """

    def __init__(self, hitbox: Hitbox, level: Level) -> None:
        self._hitbox = hitbox
        self._level = level

    def generate(self) -> list[Bullet]:
        """Abstract method for generating bullets.

        It is required to be implemented.
        """

        raise NotImplementedError(config['except_msg']['not_implemented'])
