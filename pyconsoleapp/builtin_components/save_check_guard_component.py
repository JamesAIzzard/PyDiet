from typing import Optional, Callable

from pyconsoleapp import ConsoleAppGuardComponent, PrimaryArg, builtin_components

_view_template = '''
Do you want to save changes to {subject_name}?

Yes, save changes  | -y
No, cancel changes | -n
'''


class SaveCheckGuardComponent(ConsoleAppGuardComponent):
    def __init__(self, app):
        super().__init__(app)
        self._subject_name: Optional[str] = None
        self._show_condition: Callable = lambda: False
        self._on_save_changes: Optional[Callable] = None
        self._on_cancel_changes: Optional[Callable] = None

        self.configure_state('main', self._print_main_view, responders=[
            self.configure_responder(self._on_save_changes, args=[
                PrimaryArg('yes', has_value=False, markers=['-y'])]),
            self.configure_responder(self._on_cancel_changes, args=[
                PrimaryArg('no', has_value=False, markers=['-n'])])
        ])



    def _on_load(self):
        if not self._show_condition():
            self.clear_self()

    def _print_main_view(self) -> str:
        return self.app.get_component(builtin_components.standard_page_component.StandardPageComponent).print_view(
            page_content=_view_template.format(subject_name=self._subject_name)
        )

    def configure(self, subject_name: str, show_only_if: Callable, on_save_changes: Callable, on_cancel_changes: Callable) -> None:
        self._subject_name = subject_name
        self._show_condition = show_only_if
        self._on_save_changes = on_save_changes
        self._on_cancel_changes = on_cancel_changes
