import abc
from typing import Type, Callable, TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent, PrimaryArg, StandardPageComponent
from pydiet import persistence
from pydiet.cli_components import BaseEditorComponent

if TYPE_CHECKING:
    from pyconsoleapp import ConsoleApp
    from pyconsoleapp.builtin_components.base_search_component import BaseSearchComponent
    from pydiet.persistence.supports_persistence import SupportsPersistence

_main_view_template = '''
{u_type_name} Count: {saved_count}

Create a New {u_type_name} | -new
Edit an {u_type_name}      | -edit [{l_type_name} name]
Delete an {u_type_name}    | -del  [{l_type_name} name]
View {u_type_name}s        | -view
'''


class CRUDMenuComponent(ConsoleAppComponent, abc.ABC):
    def __init__(self, subject_type_name: str, subject_type: Type['SupportsPersistence'],
                 new_subject_factory: Callable[[], 'SupportsPersistence'],
                 subject_editor_component: Type['BaseEditorComponent'],
                 subject_search_component: Type['BaseSearchComponent'], subject_base_route: str, app: 'ConsoleApp'):
        super().__init__(app)

        self._subject_type_name = subject_type_name
        self._subject_type = subject_type
        self._new_subject_factory = new_subject_factory
        self._subject_editor_component = subject_editor_component
        self._subject_search_component = subject_search_component
        self._subject_base_route = subject_base_route

        self._subject_editor_route = self._subject_base_route + '.edit'
        self._subject_search_route = self._subject_base_route + '.search'
        self._subject_viewer_route = self._subject_base_route + '.view'

        self.configure_state('menu', self._print_main_view, responders=[
            self.configure_responder(self._on_create, args=[
                PrimaryArg('new', has_value=False, markers=['-new'])]),
            self.configure_responder(self._on_edit, args=[
                PrimaryArg('subject_name', has_value=True, markers=['-edit'])]),
            self.configure_responder(self._on_delete, args=[
                PrimaryArg('subject_name', has_value=True, markers=['-del'])]),
            self.configure_responder(self._on_view, args=[
                PrimaryArg('view', has_value=False, markers=['-view'])])
        ])

    def _print_main_view(self) -> str:
        saved_count = persistence.core.count_saved_instances(self._subject_type)
        return self.app.get_component(StandardPageComponent).print_view(
            page_title='{type_name} Menu'.format(type_name=self._subject_type_name.capitalize()),
            page_content=_main_view_template.format(
                saved_count=saved_count,
                u_type_name=self._subject_type_name.capitalize(),
                l_type_name=self._subject_type_name.lower()
            )
        )

    def _on_create(self):
        new_sub = self._new_subject_factory()
        ec = self.app.get_component(self._subject_editor_component)
        ec.configure(subject=new_sub)
        self.app.goto(self._subject_editor_route)

    def _on_search_and_action(self, on_result_selected: Callable, args):
        sc = self.app.get_component(self._subject_search_component)
        sc.configure(subject_name=self._subject_type_name.capitalize(),
                     on_result_selected=on_result_selected)
        results = sc.search_for(args['subject_name'])
        sc.load_results(results)
        sc.change_state('results')
        self.app.goto(self._subject_search_route)

    def _on_edit(self, args) -> None:
        def on_result_selected(subject_name: str):
            ec = self.app.get_component(self._subject_editor_component)
            selected_subject = persistence.core.load(self._subject_type, subject_name)
            ec.configure(subject=selected_subject)
            self.app.goto(self._subject_editor_route)

        self._on_search_and_action(on_result_selected, args)

    def _on_delete(self, args) -> None:
        def on_result_selected(subject_name: str):
            persistence.delete(self._subject_type, subject_name)
            self.app.goto(self._subject_base_route)

        self._on_search_and_action(on_result_selected, args)

    def _on_view(self) -> None:
        self.app.goto(self._subject_viewer_route)
