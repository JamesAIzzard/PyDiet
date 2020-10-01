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
        self._get_subject_name: Callable = lambda: None
        self._show_condition: Callable = lambda: False
        self._save_func: Optional[Callable] = None
        self._cancel_func: Optional[Callable] = None

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
            page_content=_view_template.format(subject_name=self._get_subject_name())
        )

    def _on_save_changes(self) -> None:
        self._save_func()

    def _on_cancel_changes(self) -> None:
        self._cancel_func()

    def configure(self, show_condition: Callable[[], bool], get_subject_name: Callable[[], str] = None,
                  on_save_changes: Callable = None,
                  on_cancel_changes: Callable = None) -> None:
        super().configure(show_condition)
        self._get_subject_name = get_subject_name
        self._save_func = on_save_changes
        self._cancel_func = on_cancel_changes
