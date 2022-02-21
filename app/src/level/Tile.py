from typing import Tuple

from pyglet.image import AbstractImage

from app.src.utility.config import config


class Tile:
    """Tile is abstract class for EmptyTile and FireTile.
    """

    def __init__(
        self,
        pos: Tuple[int, int],
        size: Tuple[int, int],
        solid: bool,
        tile_image: AbstractImage
    ):
        self.pos = pos
        self.size = size
        self.solid = solid
        self._tile_image = tile_image

    def recieved_damage(self) -> int:
        """Returns amount of damage dealt to player."""
        raise NotImplementedError(config['except_msg']['not_implemented'])

    def draw(self) -> None:
        raise NotImplementedError(config['except_msg']['not_implemented'])
