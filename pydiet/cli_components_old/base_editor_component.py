import abc
from typing import Callable, Optional, TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent
from pydiet import persistence

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
        self._revert_data: Optional[Callable] = None
        self._return_to_route: Optional[str] = None
        self._to_exit: Optional[Callable] = None

    @property
    def _subject_type(self) -> str:
        return self._subject.__class__.__name__

    def _on_ok_and_save(self) -> None:
        try:
            persistence.core.save(self._subject)
        except persistence.exceptions.UniqueFieldUndefinedError:
            self.app.error_message = 'The {subject_type} name must be set before the recipe can be saved.'.format(
                subject_type=self._subject_type
            )
        except persistence.exceptions.UniqueValueDuplicatedError:
            self.app.error_message = 'There is already an {subject_type} called {unique_val}.'.format(
                unique_val=self._subject.name,
                subject_type=self._subject_type
            )
        self.app.info_message = '{subject_type} saved.'.format(subject_type=self._subject_type.capitalize())
        self.app.goto(self._return_to_route)

    def _on_cancel(self) -> None:
        if self._revert_data is not None:
            self._revert_data()
        if self._return_to_route is not None:
            self.app.goto(self._return_to_route)
        else:
            self._to_exit()

    def _configure(self, subject, guard_exit_route: Optional[str] = None,
                   guard: Optional['BaseSaveCheckGuardComponent'] = None,
                   revert_data: Optional[Callable] = None,
                   return_to_route: Optional[str] = None,
                   to_exit: Optional[Callable] = None) -> None:

        self._subject = subject
        if revert_data is not None:
            self._revert_data = revert_data
        if return_to_route is not None:
            self._return_to_route = return_to_route
        if to_exit is not None:
            self._to_exit = to_exit
        if guard is not None and guard_exit_route is not None:
            guard.configure(subject=subject)
            self.app.guard_exit(guard_exit_route, guard_instance=guard)
