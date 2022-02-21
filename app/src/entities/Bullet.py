from typing import Tuple

from app.src.entities.Entity import Entity
from app.src.level.Level import Level
from app.src.utility.types import Vec2
from app.src.utility.config import config


class Bullet(Entity):
    """Bullet class is derived of Entity.
    """

    def __init__(
        self,
        type,
        pos: Tuple[int, int],
        level: Level,
        vel: Vec2,
        damage: int,
        render_bool: list[bool]
    ) -> None:
        super().__init__(type, pos, level, render_bool)
        self.vel = vel
        self.hitbox.size = (8, 8)
        self.hitbox.scale = config['bullet_scale']
        self.damage = damage
        self.hitbox.color = (255, 127, 80)
        self.disable_smoothing()
        self._sprite = self.load_sprite(
            f'bullet-{2 if self.type else 1}.png'
        )
        self._sprite.scale = 1 * self.hitbox.scale * config['scale']

    def __str__(self):
        return f'Bullet at [{self.hitbox.pos[0]},{self.hitbox.pos[1]}].'

    def move(self) -> None:
        """Basic movement based on incrementing 2d vector."""
        self.hitbox.pos = (
            self.hitbox.pos[0] + self.vel[0],
            self.hitbox.pos[1] + self.vel[1]
        )

    def _debug_render(self) -> None:
        self.hitbox.render()

    def _cg_render(self) -> None:
        pos = (
            self.hitbox.pos[0] * config['scale'],
            self.hitbox.pos[1] * config['scale']
        )
        self._sprite.position = pos
        self._sprite.draw()

    def action(self) -> bool:
        return self.overlap_border()

    def overlap_border(self) -> bool:
        return (
            self.hitbox.pos[0] < 0 or
            self.hitbox.pos[0] > self.level.size[0] * config['tile_size'] or
            self.hitbox.pos[1] < 0 or
            self.hitbox.pos[1] > self.level.size[1] * config['tile_size']
        )
