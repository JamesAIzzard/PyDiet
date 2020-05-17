from typing import TYPE_CHECKING

from pyconsoleapp import ConsoleAppComponent
from pinjector import inject

from pydiet.recipes.exceptions import (
    RecipeNameUndefinedError
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
        self.set_option_response('2', self.on_edit_serve_times)

    def run(self):
        # If there is no recipe loaded;
        if not self._res.recipe:
            # Go back to the main recipe state;
            self.goto('home.recipes')

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

    @property
    def _check_name_defined(self) -> bool:
        if not self._res.recipe.name:
            self.app.error_message = 'Recipe name must be set first.'
            return False
        else:
            return True

    def on_save(self) -> None:
        # Try and save the recipe;
        try:
            self._res.save_changes()
        # Inform the user if it is unnamed;
        except RecipeNameUndefinedError:
            self.app.error_message = 'Cannot save an un-named recipe.'

    def on_edit_name(self)->None:
        self.app.goto('home.recipes.edit.name')

    def on_edit_serve_times(self)->None:
        if self._check_name_defined:
            self.app.goto('home.recipes.edit.serve_times')