from typing import Tuple

from app.src.entities.Hitbox import Hitbox
from app.src.level.Level import Level
from app.src.utility.Renderable import Renderable
from app.src.utility.config import config


class Entity(Renderable):
    """Entity implements Renderable class for betting render handling.

    It is abstract class for Player, Enemy and Bullet classes.
    """

    def __init__(
        self,
        type,
        pos: Tuple[int, int],
        level: Level,
        render_bool: list[bool]
    ) -> None:
        super().__init__(render_bool)
        self.type = type
        self.level = level
        self.speed = 1.0
        self.hitbox: Hitbox = Hitbox(pos, (16, 16), render_bool)
        self.hp = 100

    def move(self) -> None:
        raise NotImplementedError(config['except_msg']['not_implemented'])

    def action(self) -> None:
        raise NotImplementedError(config['except_msg']['not_implemented'])

    def is_colliding(self, other) -> bool:
        """Shorcut for comparing two hitboxes."""
        return self.hitbox.hit(other.hitbox)
