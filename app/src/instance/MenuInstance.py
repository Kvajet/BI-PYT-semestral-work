import os
import sys
from typing import Tuple

from pyglet.window import key
from pyglet.text import Label
from pyglet import font

from app.src.instance.Instance import Instance
from app.src.controls.Controls import Controls
from app.src.utility.config import config


class MenuInstance(Instance):
    """MenuInstance represents menu and all it's functionality.
    """

    def __init__(
        self,
        controls: Controls,
        window_size: Tuple[int, int]
    ) -> None:
        super().__init__(controls)

        font_path = os.path.join(
            os.path.dirname(sys.modules['__main__'].__file__),
            'app',
            'assets',
            'font',
            '04B_03__.ttf'
        )
        font.add_file(font_path)

        self._window_size = window_size
        self._font = font.load('04b03')
        self._options = ['play!', 'exit']
        self.vert_index = 0
        self._labels: list[Label] = []

    def _generate_labels(self) -> list[Label]:
        """Creates labels which are rendered to screen."""
        labels: list[Label] = []
        for index in range(len(self._options)):
            color = (255, 0, 0, 255) if index == self.vert_index else (
                255, 255, 255, 255)
            label = Label(
                self._options[index],
                font_name='04b03',
                font_size=config['text_size'],
                x=self._window_size[0] // 2,
                y=self._window_size[1] // 2 - index * 40,
                anchor_x='center',
                anchor_y='center',
                color=color
            )
            labels.append(label)
        return labels

    def _handle_controls(self) -> None:
        if (
            self.controls.key_handler[key.W]
            or self.controls.key_handler[key.UP]
        ):
            if self.vert_index > 0:
                self.vert_index -= 1
        if (
            self.controls.key_handler[key.S]
            or self.controls.key_handler[key.DOWN]
        ):
            if self.vert_index + 1 < len(self._options):
                self.vert_index += 1

    def _handle_actions(self) -> None:
        ...

    def _handle_rendering(self):
        labels = self._generate_labels()
        for label in labels:
            label.draw()
