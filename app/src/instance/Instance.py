from app.src.controls.Controls import Controls
from app.src.utility.config import config


class Instance:
    """Instance class is interface for PlayInstance and MenuInstance classes.
    """

    def __init__(self, controls: Controls) -> None:
        self.controls = controls

    def process(self) -> bool:
        """Call all three inner main functions and return their ret values."""
        return (
            self._handle_controls() or
            self._handle_actions() or
            self._handle_rendering()
        )

    def _handle_controls(self):
        """Method for handling controls. Must be implemented."""
        raise NotImplementedError(config['except_msg']['not_implemented'])

    def _handle_actions(self):
        """Method for handling actions. Must be implemented."""
        raise NotImplementedError(config['except_msg']['not_implemented'])

    def _handle_rendering(self):
        """Method for handling rendering. Must be implemented."""
        raise NotImplementedError(config['except_msg']['not_implemented'])
