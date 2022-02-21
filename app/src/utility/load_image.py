import os
import sys

from pyglet.image import AbstractImage, load


def load_image(image_name: str) -> AbstractImage:
    """Loads image in app/assets/images directory with given name."""
    path = os.path.join(
        os.path.dirname(sys.modules['__main__'].__file__),
        'app',
        'assets',
        'images',
        image_name
    )
    img: AbstractImage = load(path)
    return img
