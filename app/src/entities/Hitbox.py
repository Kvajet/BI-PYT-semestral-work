from __future__ import annotations
from typing import Tuple

import pyglet.shapes as sh

from app.src.utility.Renderable import Renderable
from app.src.utility.config import config


class Hitbox(Renderable):
    """Hitbox class is core class for comparing collisions.

    It also stores inforation about position, color for debug
    rendering.
    """

    def __init__(
        self,
        pos: Tuple[int, int],
        size: Tuple[int, int],
        render_bool: list[bool],
        scale: float = 1.0,
        speed: float = 1.0,
    ) -> None:
        super().__init__(render_bool)
        self.pos = pos
        self.size = size
        self.scale = scale
        self.speed = speed
        self.color = (100, 100, 100)
        self._tile_size: int = config['tile_size']
        self._static_rect: sh.Rectangle = self._generate_static_rect()

    def hit(self, other: 'Hitbox') -> bool:
        """Checks collison of two Hitbox objects."""
        self_half = self.half_size()
        other_half = other.half_size()

        f_to_s = ((self.pos[0] >= other.pos[0] - other_half[0])
                  and (self.pos[0] <= other.pos[0] + other_half[0])
                  and (self.pos[1] >= other.pos[1] - other_half[1])
                  and (self.pos[1] <= other.pos[1] + other_half[1]))

        s_to_f = ((other.pos[0] >= self.pos[0] - self_half[0])
                  and (other.pos[0] <= self.pos[0] + self_half[0])
                  and (other.pos[1] >= self.pos[1] - self_half[1])
                  and (other.pos[1] <= self.pos[1] + self_half[1]))

        return f_to_s or s_to_f

    def half_size(self) -> Tuple[float, float]:
        """Utility function for making a halves of sizes."""
        return (
            (self.size[0] * self.scale) / 2, (self.size[1] * self.scale) / 2
        )

    def at_pos(self) -> Tuple[int, int]:
        """Returns a grid position of hitbox."""
        return (self.pos[0] // self._tile_size, self.pos[1] // self._tile_size)

    def _generate_static_rect(self) -> sh.Rectangle:
        halves = self.half_size()
        rect = sh.Rectangle(
            (self.pos[0] - halves[0]) * config['scale'],
            (self.pos[1] - halves[1]) * config['scale'],
            self.size[0] * self.scale * config['scale'],
            self.size[1] * self.scale * config['scale'],
            self.color
        )
        return rect

    def _update_static_rect(self) -> None:
        """Important function for optimization. Just reset rect,
        no longer required to recreate it."""
        current_pos = self._render_pos()
        if self._static_rect.position != current_pos:
            self._static_rect.position = current_pos
        if self._static_rect.color != self.color:
            self._static_rect.color = self.color
        width, height = self._static_rect_size()
        if self._static_rect.width != width:
            self._static_rect.width = width
        if self._static_rect.height != height:
            self._static_rect.height = height

    def _static_rect_size(self) -> Tuple[int, int]:
        return (self.size[0] * self.scale * config['scale'],
                self.size[1] * self.scale * config['scale'])

    def _render_pos(self) -> Tuple[int, int]:
        halves = self.half_size()
        return ((self.pos[0] - halves[0]) * config['scale'],
                (self.pos[1] - halves[1]) * config['scale'])

    def _debug_render(self) -> None:
        self._update_static_rect()
        self._static_rect.draw()
