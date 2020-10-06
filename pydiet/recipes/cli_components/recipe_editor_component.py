from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydiet.recipes.recipe import Recipe

_main_view = '''Save | -save

Name | -name [name]

Edit Ingredients | -ingr ->
{ingredient_summary}

Edit Serve Times | -time ->
{serve_time_summary}

Edit Tags | -tags ->
{tag_summary}

Edit Instructions | -inst ->
{instruction_summary}
'''


class RecipeEditorComponent(EditorBaseComponent):
    def __init__(self, app):
        super().__init__(app)

    def configure(self, subject: 'Recipe'):
        exit_route = 'home.recipes'
        show_guard_condition = lambda: subject.name_is_defined and subject.has_unsaved_changes
        guard =
        super().configure(subject=subject, exit_route=exit_route, show_guard_condition=show_guard_condition,
                          guard=guard)
