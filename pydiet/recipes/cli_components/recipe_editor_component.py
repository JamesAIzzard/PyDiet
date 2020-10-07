from typing import TYPE_CHECKING

from pydiet.cli_components import BaseEditorComponent

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


class RecipeEditorComponent(BaseEditorComponent):
    def __init__(self, app):
        super().__init__(app)

    def configure(self, subject: 'Recipe'):
        pass
