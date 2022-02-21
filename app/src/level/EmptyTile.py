from typing import Tuple

from pyglet.gl import *
from pyglet.graphics import Batch
from pyglet.image import AbstractImage
import pyglet.shapes as sh
from pyglet.sprite import Sprite

from app.src.level.Tile import Tile
from app.src.utility.config import config


class EmptyTile(Tile):
    """EmptyTile class is empty for all enemies and deals no damage.
    """

    def __init__(
        self,
        pos: Tuple[int, int],
        size: Tuple[int, int],
        debug_batch: Batch,
        cg_batch: Batch,
        tile_image: AbstractImage
    ):
        super().__init__(pos, size, False, tile_image)
        self.color = (0, 0, 255)

        CFG_SCALE = config['scale']

        self.drawable = [
            sh.Rectangle(
                self.pos[0] * self.size[0] *
                CFG_SCALE, self.pos[1] * self.size[1] * CFG_SCALE,
                self.size[0] * CFG_SCALE, self.size[1] *
                CFG_SCALE, (0, 0, 255),
                batch=debug_batch
            ),
            sh.Circle(
                (self.pos[0] * self.size[0] + self.size[0] / 2) * CFG_SCALE,
                (self.pos[1] * self.size[1] + self.size[1] / 2) * CFG_SCALE,
                (self.size[0] / 8) * CFG_SCALE,
                color=(255, 255, 255),
                batch=debug_batch
            )
        ]
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        self.sprite: Sprite = Sprite(
            tile_image,
            self.pos[0] * config['tile_size'] * CFG_SCALE,
            self.pos[1] * config['tile_size'] * CFG_SCALE,
            batch=cg_batch
        )
        self.sprite.scale = CFG_SCALE

    def recieved_damage(self) -> int:
        """Amount of damage players gets, zero for empty tile."""
        return 0
