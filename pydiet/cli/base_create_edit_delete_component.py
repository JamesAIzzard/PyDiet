import abc
from typing import Type, Callable, TYPE_CHECKING

from pyconsoleapp import Component, PrimaryArg, builtin_components
from pydiet import persistence, mandatory_attributes

if TYPE_CHECKING:
    from pydiet.persistence import SupportsPersistence
    from pydiet.cli import BaseEditorComponent, BaseSearchComponent


class BaseCreateEditDeleteComponent(Component, abc.ABC):
    """Abstract base component for a Create/Edit/Delete/View Menu."""

    _subject_type: Type['SupportsPersistence']
    _subject_type_name: str

    _template = u'''
{saved_names_summary}

{single_hr}
{u_type_name} Count: {saved_count}
-new  {spacer} \u2502 -> Create a new {l_type_name}
-edit [{l_type_name}] \u2502 -> Edit an {l_type_name}
-del  [{l_type_name}] \u2502 -> Delete an {l_type_name}
{single_hr}
'''

    def __init__(self, editor_component: 'BaseEditorComponent',
                 search_component: 'BaseSearchComponent', **kwds):
        super().__init__(**kwds)

        self.configure(responders=[
            self.configure_responder(self._on_create, args=[
                PrimaryArg(name='create', accepts_value=False, markers=['-new']),
            ]),
            self.configure_responder(self._on_edit, args=[
                PrimaryArg(name='subject_name', accepts_value=True, markers=['-edit'])
            ]),
            self.configure_responder(self._on_delete, args=[
                PrimaryArg(name='subject_name', accepts_value=True, markers=['-del'])
            ]),
        ])

        # type: builtin_components.StandardPageComponent
        self._page_component = self.use_component(builtin_components.StandardPageComponent(
            page_title='{} Menu'.format(self._subject_type.__class__.__name__.capitalize())
        ))
        self._editor_component: 'BaseEditorComponent' = editor_component
        self._search_component: 'BaseSearchComponent' = search_component

    @property
    def saved_names_summary(self) -> str:
        """Returns a newline separated list of all saved names.
        If the subject type supports mandatory attributes, a definition status is included."""
        # Flag if we need to get the status;
        get_status = False
        if issubclass(self._subject_type, mandatory_attributes.HasMandatoryAttributes):  # (*1)
            get_status = True
        # Compile the output;
        output = ''
        if get_status:
            _template = '{name}: {status}\n'
            for name in persistence.get_saved_names(self._subject_type):
                saved_item = persistence.load(self._subject_type, name=name)
                # noinspection PyUnresolvedReferences
                status = saved_item.definition_status_summary  # We know from (*1) above that we have mandatory attrs.
                output = output + _template.format(name=name, status=status)
        else:
            _template = '{name}\n'
            for name in persistence.get_saved_names(self._subject_type):
                output = output + _template.format(name=name)
        return output

    def printer(self, **kwds) -> str:
        return self._page_component.printer(page_content=self._template.format(
            saved_names_summary=self.saved_names_summary,
            saved_count=persistence.count_saved_instances(self._subject_type),
            single_hr=self.single_hr,
            l_type_name=self._subject_type_name.lower(),
            spacer=len(self._subject_type_name) + 2
        ))

    def _on_create(self):
        """Creates a new instance and passes it to the editor."""
        new_subject = self._subject_type()
        self._editor_component.configure(subject=new_subject)
        self.app.go_to(self._editor_component)

    def _on_search_and_action(self, search_name: str, on_result_selected: Callable[[str], None]):
        """Implements name selection and then calls a follow-up function."""
        self._search_component.configure(on_result_selected=on_result_selected)
        results = persistence.search_for_names(self._subject_type, search_name)
        self._search_component.load_results(results)
        self._search_component.current_state = 'results'

    def _on_edit(self, subject_name: str) -> None:
        """Implements selection/edit of a subject."""

        def on_result_selected():
            selected_subject = persistence.load(self._subject_type, name=subject_name)
            self._editor_component.configure(subject=selected_subject)
            self.app.go_to(self._editor_component)

        self._on_search_and_action(subject_name, on_result_selected)

    def _on_delete(self, subject_name: str) -> None:
        """Implements selection/deletion of a subject."""

        def on_result_selected():
            persistence.delete(self._subject_type, subject_name)
            self.app.info_message = '{} was deleted.'.format(subject_name)
            self.current_state = 'main'

        self._on_search_and_action(subject_name, on_result_selected)
