from typing import Tuple, Union

from pyglet.sprite import Sprite
from pyglet.window import key

from app.src.utility.Cooldown import Cooldown
from app.src.entities.Entity import Entity
from app.src.level.Level import Level
from app.src.entities.Bullet import Bullet
from app.src.utility.config import config


class Player(Entity):
    """Player class is core class for representing player's actions.
    """

    def __init__(
        self,
        type,
        pos: Tuple[int, int],
        level: Level,
        render_bool: list[bool]
    ) -> None:
        super().__init__(type, pos, level, render_bool)
        self.hitbox.speed = 2

        self.hp = config['player_type'][self.type]['hp']
        self.hitbox.speed = config['player_type'][self.type]['speed']
        self._cooldown_hit = config['player_type'][self.type]['cooldown']
        self._bullet_damage = config['player_type'][self.type]['bullet_dmg']
        self._jumps = config['player_type'][self.type]['jumps']
        self._jump_delay = config['player_type'][self.type]['jump_cooldown']

        self._cooldown = Cooldown(self._cooldown_hit, True)
        self._jump_cooldown = Cooldown(self._jump_delay, True)
        self.hitbox.scale = 0.5
        self.hitbox.color = config['player_color']
        self._bullet_color = config['player_bullet_color']

        self._sprite: Sprite = self.load_sprite(
            config['player_type'][self.type]['sprite']
        )

    def move(self, symbol, jump: bool):
        """Checks movement keys and moves by given accelerations."""
        if jump and self._jump_cooldown.is_time():
            for _ in range(self._jumps * config['tile_size']):
                self._internal_move(symbol)
            self._jump_cooldown.reset()
        else:
            self._internal_move(symbol)
        self._jump_cooldown.inc()

    def _internal_move(self, symbol) -> None:
        halves = self.hitbox.half_size()
        if symbol == key.W:
            if (
                self.hitbox.pos[1] + self.hitbox.speed + halves[1]
                <= self.level.size[1] * config['tile_size']
            ):
                self.hitbox.pos = (
                    self.hitbox.pos[0], self.hitbox.pos[1] + self.hitbox.speed
                )
        elif symbol == key.S:
            if self.hitbox.pos[1] - self.hitbox.speed - halves[1] >= 0:
                self.hitbox.pos = (
                    self.hitbox.pos[0], self.hitbox.pos[1] - self.hitbox.speed
                )
        elif symbol == key.D:
            if (
                self.hitbox.pos[0] + self.hitbox.speed + halves[0]
                <= self.level.size[0] * config['tile_size']
            ):
                self.hitbox.pos = (
                    self.hitbox.pos[0] + self.hitbox.speed, self.hitbox.pos[1]
                )
        elif symbol == key.A:
            if self.hitbox.pos[0] - self.hitbox.speed - halves[0] >= 0:
                self.hitbox.pos = (
                    self.hitbox.pos[0] - self.hitbox.speed, self.hitbox.pos[1]
                )

    def action(self, symbol) -> Union[Bullet, None]:
        """Returns bullet if cooldown is ready and key is pressed."""
        retval = None
        if self._cooldown.is_time():
            if symbol == key.LEFT:
                vec = (-2, 0)
                self._sprite.scale_x = -1 * abs(self._sprite.scale_x)
            elif symbol == key.RIGHT:
                vec = (2, 0)
                self._sprite.scale_x = abs(self._sprite.scale_x)
            elif symbol == key.UP:
                vec = (0, 2)
            elif symbol == key.DOWN:
                vec = (0, -2)
            if vec:
                retval: Bullet = Bullet(
                    0,
                    self.hitbox.pos,
                    self.level,
                    vec,
                    self._bullet_damage,
                    self.render_bool
                )
                retval.hitbox.color = self._bullet_color
                self._cooldown.reset()
        self._cooldown.inc()
        return retval

    def _debug_render(self) -> None:
        self.hitbox.render()

    def _cg_render(self) -> None:
        self.disable_smoothing()
        self._sprite.x = (self.hitbox.pos[0]) * config['scale']
        self._sprite.y = (self.hitbox.pos[1]) * config['scale']
        self._sprite.draw()
