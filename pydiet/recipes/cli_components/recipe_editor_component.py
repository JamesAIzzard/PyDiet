from typing import Optional, TYPE_CHECKING

from pyconsoleapp import PrimaryArg, StandardPageComponent, ResponseValidationError
from pydiet import recipes, persistence
from pydiet.cli_components import BaseEditorComponent

if TYPE_CHECKING:
    from pydiet.recipes.recipe import Recipe

_main_view_template = '''Save | -save

Name | -name [name] -> {name}

Edit Ingredients | -ingr ->
{ingredient_composition_summary}

Edit Serve Times | -time ->
{serve_time_summary}

Edit Tags | -tags ->
{tag_summary}

Edit Instructions | -inst ->
{step_summary}
'''


class RecipeEditorComponent(BaseEditorComponent):
    def __init__(self, app):
        super().__init__(app)
        self._subject: Optional['Recipe'] = None

        self.configure_state('main', self._print_main_view, responders=[
            self.configure_responder(self._on_save, args=[
                PrimaryArg('save', has_value=False, markers=['-save'])]),
            self.configure_responder(self._on_edit_name, args=[
                PrimaryArg('name', has_value=True, markers=['-name'], validators=[self._validate_name])]),
            self.configure_responder(self._on_edit_ingredients, args=[
                PrimaryArg('edit_serve_times', has_value=False, markers=['-ingr'])]),
            self.configure_responder(self._on_edit_tags, args=[
                PrimaryArg('edit_tags', has_value=False, markers=['-tags'])]),
            self.configure_responder(self._on_edit_instructions, args=[
                PrimaryArg('edit_instructions', has_value=False, markers=['-inst'])
            ])
        ])

    def _on_edit_ingredients(self) -> None:
        ...

    def _on_edit_instructions(self) -> None:
        ...

    def _on_edit_name(self, args) -> None:
        self._subject.name = args['name']

    def _on_edit_tags(self) -> None:
        ...

    def _on_save(self) -> None:
        try:
            persistence.persistence_service.save(self._subject)
        except persistence.exceptions.UniqueFieldUndefinedError:
            self.app.error_message = 'The recipe name must be set before the recipe can be saved.'

    def _print_main_view(self) -> str:
        return self.app.get_component(StandardPageComponent).print_view(
            page_title='Recipe Editor',
            page_content=_main_view_template.format(
                name=self._subject.name,
                ingredient_composition_summary=self._subject.ingredient_composition_summary,
                serve_time_summary=self._subject.serve_times_summary,
                tag_summary=self._subject.tag_summary,
                step_summary=self._subject.step_summary
            )
        )

    def _validate_name(self, value) -> str:
        if not persistence.persistence_service.check_unique_val_avail(
                recipes.Recipe, self._subject.datafile_name, value):
            raise ResponseValidationError('There is already a recipe called {}'.format(value))
        return value


    def configure(self, subject: 'Recipe'):
        guard_exit_route = 'home.recipes.edit'
        guard = self.app.get_component(recipes.cli_components.RecipeSaveCheckGuardComponent)
        guard.configure(subject=subject)
        super()._configure(subject, guard_exit_route=guard_exit_route, guard=guard)
