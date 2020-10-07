import abc
from typing import Callable, Optional, TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp
    from pydiet.cli_components.base_save_check_guard_component import BaseSaveCheckGuardComponent


class BaseEditorComponent(ConsoleAppComponent, abc.ABC):

    def __init__(self, app: 'ConsoleApp'):
        super().__init__(app)
        self._subject = None
        self._exit_route: Optional[str] = None
        self._guard: Optional['BaseSaveCheckGuardComponent'] = None
        self._show_guard_condition: Callable[[], bool] = lambda: False

    def _configure(self, subject, guard_exit_route: Optional[str] = None,
                   guard: Optional['BaseSaveCheckGuardComponent'] = None) -> None:
        self._subject = subject
        if guard is not None and guard_exit_route is not None:
            guard.configure(subject=subject)
            self.app.guard_exit(guard_exit_route, guard_instance=guard)
