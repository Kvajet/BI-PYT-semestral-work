from typing import Tuple

from pyglet.graphics import Batch
from pyglet.text import Label

from app.src.entities.Player import Player
from app.src.entities.Enemy import Enemy
from app.src.utility.Cooldown import Cooldown
from app.src.utility.config import config


class TopBar:
    """TopBar class renders info about player, enemies, cooldown and finished
    level.
    """

    def __init__(
        self,
        window_size: Tuple[int, int],
        player: Player,
        enemies: list[Enemy],
        teleport_cooldown: Cooldown
    ):
        self._window_size = window_size
        self._player = player
        self._enemies = enemies
        self._teleport_cooldown = teleport_cooldown

        self._hp_color = config['top_bar_hp_color']
        self._enemy_color = config['top_bar_enemies_color']
        self._teleport_color = config['top_bar_teleport_color']

        self._static_batch = Batch()
        self._label_hp = Label(
            'HP: ',
            font_name='04b03',
            font_size=config['text_size'],
            x=0,
            y=self._window_size[1] - config['text_size'],
            batch=self._static_batch,
            color=self._hp_color
        )
        self._enemy_count = Label(
            ' :Enemies',
            font_name='04b03',
            font_size=config['text_size'],
            y=self._window_size[1] - config['text_size'],
            batch=self._static_batch,
            color=self._enemy_color
        )
        self._enemy_count.x = (
            self._window_size[0] - self._enemy_count.content_width
        )
        self._next_level = Label(
            'Press E for next level!',
            font_name='04b03',
            font_size=config['text_size'],
            x=window_size[0] // 2,
            y=self._window_size[1] - config['text_size'],
            anchor_x='center'
        )
        self._teleport = Label(
            'Teleport READY',
            font_name='04b03',
            font_size=config['text_size'],
            x=window_size[0] // 2,
            y=self._window_size[1] - config['text_size'],
            anchor_x='center',
            color=self._teleport_color
        )

    def render(self) -> None:
        hp = Label(
            f'{self._player.hp}',
            font_name='04b03',
            font_size=config['text_size'],
            x=self._label_hp.content_width,
            y=self._window_size[1] - config['text_size'],
            color=self._hp_color
        )
        enemy_count = Label(
            f'{len(self._enemies)}',
            font_name='04b03',
            font_size=config['text_size'],
            y=self._window_size[1] - config['text_size'],
            color=self._enemy_color
        )
        enemy_count.x = (
            self._window_size[0]
            - enemy_count.content_width
            - self._enemy_count.content_width
        )
        self._static_batch.draw()
        hp.draw()
        enemy_count.draw()
        if not len(self._enemies):
            self._next_level.draw()
        elif self._teleport_cooldown.is_time():
            self._teleport.draw()
