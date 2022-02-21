from pyglet.sprite import Sprite
from app.src.entities.attack_patterns.ClockPattern import ClockPattern

from app.src.utility.types import Vec2
from app.src.utility.Cooldown import Cooldown
from app.src.entities.Player import Player
from app.src.entities.movement.Astar import Astar
from app.src.entities.Entity import Entity
from app.src.level.Level import Level
from app.src.entities.Bullet import Bullet
from app.src.entities.attack_patterns.AttackPattern import AttackPattern
from app.src.entities.attack_patterns.CrossAttack import CrossAttack
from app.src.entities.attack_patterns.StarPattern import StarPattern
from app.src.utility.config import config


class Enemy(Entity):
    """Enemy class represents enemy, it's movement and attacks.
    """

    def __init__(
        self,
        type,
        pos,
        level: Level,
        player: Player,
        render_bool: list[bool]
    ) -> None:
        super().__init__(type, pos, level, render_bool)
        self.hitbox.speed = 2
        self._astar = Astar(self.level)
        self._player = player
        self._cooldown = Cooldown()
        if self.type == 0:
            self._pattern: AttackPattern = CrossAttack(
                self.hitbox,
                self.level,
                render_bool
            )
        elif self.type == 1:
            self._pattern: AttackPattern = StarPattern(
                self.hitbox,
                self.level,
                render_bool
            )
        else:
            self._pattern: AttackPattern = ClockPattern(
                self.hitbox,
                self.level,
                render_bool
            )
        self._path = []

        self.hp = config['enemy_type'][self.type]['hp']
        self._cooldown_hit = config['enemy_type'][self.type]['cooldown']
        self._bullet_damage = config['enemy_type'][self.type]['bullet_dmg']
        if self.type > 0:
            self._move_vec: Vec2 = config['enemy_type'][self.type]['speed']

        if self.type == 0:
            self._move_func = self._astar_movement
        else:
            self._move_func = self._flying_movement

        self.hitbox.color = (200, 0, 0)
        self._sprite: Sprite = self.load_sprite(
            config['enemy_type'][self.type]['sprite']
        )

    def move(self) -> None:
        """Uses chosen move function, possibly flying or A* movement."""
        self._move_func()

    def action(self) -> list[Bullet]:
        """If timer is ready generates list of bullets."""
        retval = []

        if self._cooldown.is_time():
            retval = self._pattern.generate()
        self._cooldown.inc_and_reset()
        return retval

    def _debug_render(self) -> None:
        self.hitbox.render()

    def _cg_render(self) -> None:
        self.disable_smoothing()
        self._sprite.x = (self.hitbox.pos[0]) * config['scale']
        self._sprite.y = (self.hitbox.pos[1]) * config['scale']
        self._sprite.draw()

    def _astar_movement(self) -> None:
        if len(self._path) != 1 or self._path[-1] != self._player.hitbox.at_pos():
            self._path = self._astar.find_path(
                self.hitbox.at_pos(), self._player.hitbox.at_pos()
            )

        if self._path and len(self._path) > 1 and self._cooldown.is_time():
            if self._path[0] == self.hitbox.at_pos():
                del self._path[0]
            self.hitbox.pos = tuple(
                [item * 16 + 8 for item in self._path[0]]
            )

    def _flying_movement(self) -> None:
        self.hitbox.pos = (
            self.hitbox.pos[0] + self._move_vec[0],
            self.hitbox.pos[1] + self._move_vec[1]
        )
        if self.hitbox.pos[0] <= 0 or self.hitbox.pos[0] > self.level.size[0] * config['tile_size']:
            self._move_vec = (-1 * self._move_vec[0], self._move_vec[1])
        if self.hitbox.pos[1] <= 0 or self.hitbox.pos[1] > self.level.size[1] * config['tile_size']:
            self._move_vec = (self._move_vec[0], -1 * self._move_vec[1])
