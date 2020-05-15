from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent
from pinjector import inject

from pydiet.cli.recipes.exceptions import (
    UnnamedRecipeError
)

if TYPE_CHECKING:
    from pydiet.cli.recipes.recipe_edit_service import RecipeEditService
    from pydiet.recipes import recipe_service

_TEMPLATE = '''
Recipe Editor:

(s) -- Save Changes

(1) -- Edit Name: {name}

(2) -- Edit Serve Times:
{serve_times}
(3) -- Edit Categories:
{categories}
(4) -- Edit Ingredients:
{ingredients}
'''


class RecipeEditMenuComponent(ConsoleAppComponent):

    def __init__(self):
        super().__init__()
        self._res: 'RecipeEditService' = inject(
            'pydiet.cli.recipe_edit_service')
        self._rcs: 'recipe_service' = inject('pydiet.recipe_service')
        self.set_option_response('s', self.on_save)
        self.set_option_response('1', self.on_edit_name)

    def print(self):
        # Raise an exception if recipe has not been loaded;
        if not self._res.recipe:
            raise AttributeError
        # Build the template;
        output = _TEMPLATE.format(
            name=self._rcs.summarise_name(self._res.recipe),
            serve_times=self._rcs.summarise_serve_intervals(self._res.recipe),
            categories=self._rcs.summarise_categories(self._res.recipe),
            ingredients=self._rcs.summarise_ingredients(self._res.recipe)
        )
        output = self.app.fetch_component(
            'standard_page_component').print(output)
        # Return the view;
        return output

    def on_save(self) -> None:
        # Try and save the recipe;
        try:
            self._res.save_changes(redirect_to='home.recipes.edit')
        # Inform the user if it is unnamed;
        except UnnamedRecipeError:
            self.app.error_message = 'Cannot save an un-named recipe.'

    def on_edit_name(self)->None:
        self.app.goto('.edit_name')