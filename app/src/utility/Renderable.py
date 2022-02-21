import os
import sys

import pyglet
from pyglet.gl import *
from pyglet.image import AbstractImage
from pyglet.sprite import Sprite

from app.src.utility.config import config


class Renderable():
    """Renderable class providing common render interface.
    """

    def __init__(self, render_bool: list[bool]):
        self.render_bool = render_bool

    def _debug_render(self) -> None:
        """Abstract method representing rendering with shapes."""
        raise NotImplementedError(config['except_msg']['not_implemented'])

    def _cg_render(self) -> None:
        """Abstract method representing rendering with images."""
        raise NotImplementedError(config['except_msg']['not_implemented'])

    def render(self) -> None:
        """On given render_bool renders _debug or _cg _renderer."""
        self._debug_render() if self.render_bool[0] else self._cg_render()

    def disable_smoothing(self) -> None:
        """Prevents images and sprites from blurring after scale."""
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    def load_sprite(self, sprite_name: str) -> Sprite:
        """Loads sprite of given path and returns it."""
        path = os.path.join(
            os.path.dirname(sys.modules['__main__'].__file__),
            'app',
            'assets',
            'images',
            sprite_name
        )
        image: AbstractImage = pyglet.image.load(path)
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2
        new_sprite = Sprite(
            image
        )
        new_sprite.scale = config['scale']
        return new_sprite
