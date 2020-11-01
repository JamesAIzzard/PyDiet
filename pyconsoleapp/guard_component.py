import abc
from typing import Callable, Optional

from pyconsoleapp import Component


class GuardComponent(Component, abc.ABC):
    """Base class for all application guard components."""

    def __init__(self, **kwds):
        super().__init__(**kwds)
        self._should_activate: Callable[[], bool] = lambda: True

    @property
    def activated(self) -> bool:
        """Returns True/False to indicate if the function should be activated."""
        return self._should_activate()

    def stop_guarding(self) -> None:
        """Clears self from the app's guard registers."""
        self.app.clear_guard(self)

    def configure(self, should_activate: Optional[Callable[[], bool]] = None, **kwds) -> None:
        if should_activate is not None:
            self._should_activate = should_activate
        super().configure(**kwds)
