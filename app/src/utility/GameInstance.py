import pyglet
from pyglet.window import key

from app.src.controls.Controls import Controls
from app.src.instance.Instance import Instance
from app.src.instance.PlayInstance import PlayInstance
from app.src.instance.MenuInstance import MenuInstance


class GameInstance(pyglet.window.Window):
    """GameInstance inherits pyglet window class. Main class of my app.
    """

    def __init__(self, width=800, height=600, *args, **kwargs):
        super(GameInstance, self).__init__(width, height, *args, **kwargs)

        # key handler stuff
        key_handler = key.KeyStateHandler()
        self.push_handlers(key_handler)
        self.controls = Controls(key_handler)

        # instance stuff
        self._menu_instance: MenuInstance = MenuInstance(
            self.controls,
            (width, height)
        )
        self._play_instance: PlayInstance = PlayInstance(
            self.controls,
            (width, height)
        )
        self._active_instance: Instance = self._menu_instance

    def on_key_press(self, symbol, modifiers) -> None:
        self.controls.increment()

    def on_key_release(self, symbol, modifiers) -> None:
        self.controls.decrement()

    def update(self, _) -> None:
        self.clear()
        self._handler_controls()
        res = self._active_instance.process()
        # switches active instance when player died or ESC is pressed
        if res and self._active_instance == self._play_instance:
            self._active_instance = self._menu_instance

    def _handler_controls(self) -> None:
        if self._active_instance == self._menu_instance:
            if self.controls.key_handler[key.ENTER]:
                if self._menu_instance.vert_index == 1:
                    self.close()
                elif self._menu_instance.vert_index == 0:
                    self._active_instance = self._play_instance
        elif self._active_instance == self._play_instance:
            if self.controls.key_handler[key.ESCAPE]:
                self._active_instance = self._menu_instance
