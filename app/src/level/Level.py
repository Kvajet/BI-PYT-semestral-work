from typing import Tuple

import numpy as np
from pyglet.graphics import Batch
from pyglet.image import AbstractImage

from app.src.utility.Cooldown import Cooldown
from app.src.utility.Renderable import Renderable
from app.src.level.EmptyTile import EmptyTile
from app.src.level.FireTile import FireTile
from app.src.utility.config import config


class Level(Renderable):
    """Level class represent level and tiles in it.
    """

    def __init__(
        self,
        bool_layout: np.ndarray,
        size: Tuple[int, int],
        tile_images: list[AbstractImage],
        render_bool: list[bool]
    ) -> None:
        super().__init__(render_bool)

        self.size = size

        self.layout = []
        self._tile_images = tile_images
        self.bool_layout = bool_layout  # False - free, True - solid
        self._tile_cooldown = Cooldown(config['fire_tile_cooldown'])

        self._debug_batch = Batch()
        self._cg_batch = Batch()
        for i in range(self.size[1]):
            self.layout.append([])
            for k in range(self.size[0]):
                tile = None
                if (
                    self.bool_layout[i][k]
                    and i and i + 1 != size[1]
                    and k and k + 1 != size[0]
                ):
                    tile = FireTile(
                        (k, i),
                        (config['tile_size'], config['tile_size']),
                        self._debug_batch,
                        self._cg_batch,
                        self._tile_images[3][0]
                    )
                else:
                    image_x, image_y = self._select_tile_image((k, i))
                    tile = EmptyTile(
                        (k, i),
                        (config['tile_size'], config['tile_size']),
                        self._debug_batch,
                        self._cg_batch,
                        self._tile_images[image_x][image_y]
                    )
                self.layout[i].append(tile)

    def get_hit(self, pos: Tuple[int, int]) -> int:
        """Returns amount of damage dealt to player."""
        retval = 0
        if self._tile_cooldown.is_time():
            retval = self.layout[int(pos[1])][int(pos[0])].recieved_damage()
        self._tile_cooldown.inc_and_reset()
        return retval

    def _debug_render(self) -> None:
        self._debug_batch.draw()

    def _cg_render(self) -> None:
        self.disable_smoothing()
        self._cg_batch.draw()

    def switch(self) -> None:
        """Switches rendering methods. From basic shapes to better
        pixel art."""
        if self._active_render == self._debug_render:
            self._active_render = self._cg_render
        else:
            self._active_render = self._debug_render

    def _select_tile_image(self, pos: Tuple[int, int]) -> AbstractImage:
        ret_x = 1
        ret_y = 1
        if pos[0] == 0:
            ret_x = 0
        elif pos[0] + 1 == self.size[0]:
            ret_x = 2
        else:
            ret_x = 1

        if pos[1] == 0:
            ret_y = 2
        elif pos[1] + 1 == self.size[1]:
            ret_y = 0
        else:
            ret_y = 1

        return (ret_y, ret_x)
