from typing import Tuple

from pyglet.window import key

from app.src.utility.Cooldown import Cooldown
from app.src.level.LevelHandler import LevelHandler
from app.src.entities.Enemy import Enemy
from app.src.entities.Bullet import Bullet
from app.src.entities.Player import Player
from app.src.utility.config import config
from app.src.instance.Instance import Instance
from app.src.controls.Controls import Controls
from app.src.utility.random_int import random_int
from app.src.utility.TopBar import TopBar


class PlayInstance(Instance):
    """PlayInstance is core instance of my game. Everything during the game
    happens here. Rendering, generating bullets, collisions...
    """

    def __init__(
        self,
        controls: Controls,
        window_size: Tuple[int, int]
    ) -> None:
        super().__init__(controls)

        self._window_size = window_size

        self._movement = [key.W, key.S, key.A, key.D]
        self._actions = [key.UP, key.DOWN, key.LEFT, key.RIGHT]
        self._render_bool = [False]

        self._level_handler = LevelHandler(self._render_bool)
        self._tile_size = config['tile_size']
        self._switch_graphics = Cooldown(10)

        self._reset_game()

    def _handle_controls(self) -> None:
        bullet: Bullet = None

        for move in self._movement:
            if self.controls.key_handler[move]:
                self._player.move(move, self.controls.key_handler[key.SPACE])

        for action in self._actions:
            if self.controls.key_handler[action]:
                bullet = self._player.action(action)
            if bullet:
                self._pbullets.append(bullet)
                print(bullet)

        if not self._enemies and self.controls.key_handler[key.E]:
            self._reset_game(False)

        if (
            self.controls.key_handler[key.Q]
            and self._switch_graphics.is_time()
        ):
            self._switch_render()
            self._switch_graphics.reset()

        self._switch_graphics.inc()

    def _handle_actions(self) -> bool:
        print(self._player.hp)

        self._floor_hit()

        for enemy in self._enemies:
            enemy.move()
            bullets = enemy.action()
            [self._ebullets.append(cur_bullet) for cur_bullet in bullets]

        self._handle_player_bullets()
        self._handle_enemy_bullets()

        self._remove_bullets(self._pbullets)
        self._remove_bullets(self._ebullets)

        if self._player.hp <= 0:
            self._reset_game()
            return True
        return False

    def _handle_rendering(self) -> None:
        self._level.render()
        self._player.render()

        self._render_bullets(self._pbullets)
        self._render_bullets(self._ebullets)
        for enemy in self._enemies:
            enemy.render()
        self._top_bar.render()

    # non-called functions by out

    def _reset_game(self, reset_player=True) -> None:
        """After end of the round or after creating new game, this method
        generates new level.

        Parementer reset_player determines if new character is created as well.
        """
        self._level, enemies = self._level_handler.generate_level()

        if reset_player:
            self._player = Player(
                random_int(len(config['player_type'])),
                ((self._level.size[0] * config['tile_size']) / 2,
                 (self._level.size[1] * config['tile_size']) / 2),
                self._level,
                self._render_bool
            )
            self._level_handler.reset()
        else:
            self._player.hp += config['cleared_level_hp']
            self._player.level = self._level

        self._pbullets: list[Bullet] = []
        self._ebullets: list[Bullet] = []
        self._enemies: list[Enemy] = []

        for enemy in enemies:
            self._enemies.append(
                Enemy(
                    random_int(len(config['enemy_type'])),
                    (
                        enemy[0] * self._tile_size + self._tile_size // 2,
                        enemy[1] * self._tile_size + self._tile_size // 2
                    ),
                    self._level,
                    self._player,
                    self._render_bool
                )
            )
        self._top_bar = TopBar(
            self._window_size,
            self._player,
            self._enemies,
            self._player._jump_cooldown
        )

    def _floor_hit(self) -> None:
        """Checks if player is above light tiles which deal small
        amount of damage to player."""
        damage = self._level.get_hit(self._player.hitbox.at_pos())
        if damage:
            self._player.hp -= damage

    def _handle_player_bullets(self) -> None:
        """Resolve player bullets."""
        for bullet in self._pbullets:
            for enemy in self._enemies:
                if bullet.is_colliding(enemy):
                    enemy.hp -= bullet.damage
                    if enemy.hp <= 0:
                        self._enemies.remove(enemy)
                    self._pbullets.remove(bullet)
                    break

    def _handle_enemy_bullets(self) -> None:
        """Resolve enemy bullets."""
        for bullet in self._ebullets:
            if bullet.is_colliding(self._player):
                self._ebullets.remove(bullet)
                self._player.hp -= bullet.damage

    def _switch_render(self) -> None:
        """By hitting Q the enemies and player gets pixel are graphics."""
        self._render_bool[0] = not self._render_bool[0]

    def _remove_bullets(self, bullets: list[Bullet]) -> None:
        for bullet in bullets:
            bullet.move()
            if bullet.action():
                bullets.remove(bullet)

    def _render_bullets(self, bullets: list[Bullet]) -> None:
        for bullet in bullets:
            bullet.render()
