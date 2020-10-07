from typing import Optional, TYPE_CHECKING

from pyconsoleapp import builtin_components, ConsoleAppGuardComponent
from pydiet import persistence

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp
    from pydiet.persistence.supports_persistence import SupportsPersistence


class BaseSaveCheckGuardComponent(builtin_components.yes_no_dialog_component.YesNoDialogComponent,
                                  ConsoleAppGuardComponent):

    def __init__(self, message: str, app: 'ConsoleApp'):
        super().__init__(message=message, app=app)
        self._subject: Optional['SupportsPersistence'] = None

    def configure(self, subject: 'SupportsPersistence') -> None:
        super()._configure(show_condition=lambda: subject.unique_field_defined and subject.has_unsaved_changes)
        self._subject = subject

    def _on_yes(self) -> None:
        persistence.persistence_service.save(self._subject)
        self.clear_self()

    def _on_no(self) -> None:
        self.clear_self()
