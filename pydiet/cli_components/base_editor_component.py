import abc
from typing import Callable, Optional, TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleAppGuardComponent, ConsoleApp


class BaseEditorComponent(ConsoleAppComponent, abc.ABC):

    def __init__(self, app: 'ConsoleApp'):
        super().__init__(app)
        self._subject = None
        self._exit_route: Optional[str] = None
        self._guard: Optional['ConsoleAppGuardComponent'] = None
        self._show_guard_condition: Callable[[], bool] = lambda: False

    def _configure(self, subject, exit_route: str, show_guard_condition: Optional[Callable[[], bool]] = None,
                   guard: Optional['ConsoleAppGuardComponent'] = None) -> None:
        self._subject = subject
        self._exit_route = exit_route
        if show_guard_condition is not None:
            self._show_guard_condition = show_guard_condition
        self._guard = guard
        self._show_guard_condition = show_guard_condition
