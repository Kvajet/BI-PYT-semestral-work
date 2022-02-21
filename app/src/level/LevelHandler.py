import os
import sys
from typing import Tuple

import numpy as np
from pyglet.image import AbstractImage

from app.src.level.Level import Level
from app.src.utility.config import config
from app.src.utility.load_image import load_image
from app.src.utility.random_int import random_int


class LevelHandler:
    """LevelHandler serves as generator for Levels.

    It parses level grids from assets/level which have to be 3x3
    and then fills the layout with it and generates enemies.
    Level has to be divideable by 3.
    """

    def __init__(self, render_bool: list[bool]):
        self._layouts: np.ndarray = []
        self._enemy_pos: np.ndarray = []
        self._parse_layouts()
        self.size = config['level_size']
        self._current_level = None  # self.generate_level()
        self._max_enemies = config['max_enemies']
        self._tile_images = self._parse_tile_images()
        self._render_bool = render_bool

    def generate_level(self) -> Tuple[Level, list[Tuple[int, int]]]:
        enemies: list[Tuple[int, int]] = []
        level = np.zeros(self.size, dtype=bool)
        # cycles through game plan with increment of 3 and inserts
        # enemies and parsed layouts to the map
        for x in range(0, self.size[0], 3):
            for y in range(0, self.size[1], 3):
                layout_index = random_int(len(self._layouts))
                level[x:x + 3, y:y + 3] = self._layouts[layout_index]
                if len(enemies) < self._max_enemies:
                    for enemy_x in range(0, 3):
                        for enemy_y in range(0, 3):
                            if self._enemy_pos[layout_index][enemy_x, enemy_y]:
                                enemies.append((x + enemy_x, y + enemy_y))
        self._current_level = Level(
            level.T,
            self.size,
            self._tile_images,
            self._render_bool
        )
        self._max_enemies += 1
        return (self._current_level, enemies)

    def reset(self) -> None:
        self._max_enemies = config['max_enemies']

    def _parse_layouts(self) -> None:
        path = os.path.join(
            os.path.dirname(sys.modules['__main__'].__file__),
            'app',
            'assets',
            'level'
        )
        for file in os.listdir(path):
            self._parse_layout(os.path.join(path, file))

    def _parse_layout(self, path) -> None:
        """Parses 3x3 layout and generates layout to class member.
        Same for enemies. Enemies are represented by e, solid tile by x.
        """
        chunk = []
        enemies = []
        size = 0
        total = 0
        with open(path) as f:
            for line in f:
                line = line[0:3]
                for char in line:
                    if char == 'x':
                        chunk.append(True)
                        enemies.append(False)
                    elif char == ' ':
                        chunk.append(False)
                        enemies.append(False)
                    else:
                        chunk.append(False)
                        enemies.append(True)
                    total += 1
                size += 1
        self._layouts.append(np.array(chunk))
        self._layouts[-1].shape = (total // size, size)

        self._enemy_pos.append(np.array(enemies))
        self._enemy_pos[-1].shape = (total // size, size)

    def _parse_tile_images(self) -> list[AbstractImage]:
        retval = [[], [], [], []]
        index = 0
        for image_name in config['level_tiles']:
            retval[index // 3].append(load_image(image_name))
            index += 1
        return retval
