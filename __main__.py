from math import floor

import pyglet

from app.src.utility.GameInstance import GameInstance
from app.src.utility.config import config

if __name__ == '__main__':
    mygame = GameInstance(
        config['level_size'][0] * config['tile_size'] * config['scale'],
        (
            config['level_size'][1]
            * config['tile_size']
            * config['scale']
            + floor(config['text_size'] * 1.2)
        )
    )
    pyglet.clock.schedule_interval(mygame.update, 1 / config['refresh_rate'])
    pyglet.app.run()
